import unittest
from image_tools import match
import os
class TestDevice(unittest.TestCase):
    def test_matchs(self):
        assets_p = os.path.join(os.path.dirname(__file__),'.',"images")
        source = os.path.join(assets_p,"test_full_screen.png")
        python = os.path.join(assets_p,"python_icon.png")
        assert source is not None
        assert python is not None
        at_least = 2  # at least 2 matches
        for res in match.CV.find_image_matches(source,python):
            self.assertGreaterEqual(res[1],0.9)
            at_least -= 1

    def test_scale_matchs(self):
        """
        Test the matching degree of the image in various scaling factors.
        """
        MAX_SCALE = 2.0 
        MIN_SCALE = 0.5 
        STEP = 0.1   
        THRESHOLD = 0.9 

        assets_p = os.path.join(os.path.dirname(__file__),'.',"images")
        source = os.path.join(assets_p,"full_size.png")
        scaled = os.path.join(assets_p,"scaled.png")

        assert source is not None
        assert scaled is not None
        r = match.CV.find_scale_and_position(source,scaled,(MIN_SCALE,MAX_SCALE),STEP)
        # r structure: (scale, location, match_value)
        self.assertGreaterEqual(r[0],MIN_SCALE)
        self.assertLessEqual(r[0],MAX_SCALE)
        self.assertGreaterEqual(r[2],THRESHOLD)

        
