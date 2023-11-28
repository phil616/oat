"""
    filename: image_tools/match.py
    ~~~~~~~~~~~~~~~~~~~~
    OpenCV process module. Image processing functions.

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""
import typing
import cv2
import numpy as np
import PIL
import PIL.Image


class CV:
    @classmethod
    def cv2pil(cls, image: np.ndarray, /):
        """
        Convert an OpenCV image to a PIL image.

        :param image: OpenCV image.
        :return: PIL image.
        """
        return PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    @classmethod
    def quick_match_exist(cls,
                          src,
                          template, threshold=0.95):
        _, max_val, _, _ = cv2.minMaxLoc(
            cv2.matchTemplate(
                src,
                template,
                cv2.TM_CCOEFF_NORMED)
        )
        return max_val >= threshold

    @classmethod
    def quick_match_position(cls,
                             src,
                             template, threshold=0.90):
        """
        find the template in the src image and return the central position of the template

        """
        res = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
        # basic match
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > threshold:
            center_x = max_loc[0] + template.shape[1] / 2
            center_y = max_loc[1] + template.shape[0] / 2
            return center_x, center_y
        else:
            raise Exception("No match found")

    @classmethod
    def find_image_matches(cls,
                           src,
                           template,
                           min_threshold=0.9,
                           matches_count=5,
                           ) -> typing.List[typing.Tuple[typing.Tuple[int, int], float]]:
        """
        Find the matches of a template image in a source image., return the center of the matches and the match value.

        Args:
            src: The source image path.
            template: The template image path.
            min_threshold: The minimum threshold of the match value.
            matches_count: The number of the matches.

        Returns:
            A list of tuples, each tuple contains the center of the match and the match value.
            ex: [((x1, y1), match_value1), ((x2, y2), match_value2), ...]
        """
        # if the src and template are not existed, raise error
        assert src is not None
        assert template is not None
        # load the src and template image
        img = cv2.imread(src, 0)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]

        # use template matching method
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # sort the res
        sorted_indices = np.dstack(np.unravel_index(np.argsort(res.ravel()), res.shape))[0][::-1]

        # prepare a list to save the non-overlapping match
        non_overlapping = []
        distance_threshold = (w ** 2 + h ** 2) ** 0.5
        # calculate the distance threshold by the diagonal of the template

        for pt in sorted_indices:
            overlap = False
            for non_overlap in non_overlapping:
                dist = ((non_overlap[0][0] - pt[0]) ** 2 + (non_overlap[0][1] - pt[1]) ** 2) ** 0.5
                if dist < distance_threshold:
                    overlap = True
                    break
            if not overlap:
                # calculate the center of the match
                center = (pt[1] + w // 2, pt[0] + h // 2)
                match_value = res[pt[0], pt[1]]
                if match_value < min_threshold:  # if the match value is lower than the threshold, stop the loop
                    break
                non_overlapping.append((center, match_value))
            if len(non_overlapping) == matches_count:  # get the first n non-overlapping matches
                break

        return non_overlapping

    @classmethod
    def find_scale_and_position(cls, source_img, template_img, scale_range=(0.5, 2.0), scale_step=0.1):
        """
        Find the best scale and position of the template image in the source image.
        Args:
            source_img: The source image path.
            template_img: The template image path.
            scale_range: The scale range to check.
            scale_step: The scale step to check.
        Returns:
            A tuple, contains the best scale, the best location and the best match value.
            best_scale: The best scale.
            best_loc: The best location.
            best_match_val: The best match value.
        """
        source_img = cv2.imread(source_img)
        template_img = cv2.imread(template_img)
        template_height, template_width = template_img.shape[:2]
        best_scale = None
        best_loc = None
        best_match_val = -1

        # get all scales to check
        for scale in np.arange(scale_range[0], scale_range[1], scale_step):
            # use the current scale to resize the source image
            scaled_img = cv2.resize(source_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            # check if the scaled image is smaller than the template
            if template_height > scaled_img.shape[0] or template_width > scaled_img.shape[1]:
                continue
            # use the resized image to do template matching
            res = cv2.matchTemplate(scaled_img, template_img, cv2.TM_CCOEFF_NORMED)
            # find the best match location
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # if the current match value is better than the current best match value
            if max_val > best_match_val:
                best_scale = scale
                best_loc = max_loc
                best_match_val = max_val

        return best_scale, best_loc, best_match_val
