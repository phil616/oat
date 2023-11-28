"""
    filename: io_tools/device.py
    ~~~~~~~~~~~~~~~~~~~~
    System Input and Output API, provide the basic input and output functions.

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""
import os
import ctypes
import dataclasses
import subprocess
import collections
import time
import typing
import datetime
import uuid
import queue
import mss
import mss.screenshot
import mss.tools
import pyautogui
import pynput

# local module
# no local module

SAVE_DEBUG_SCREENSHOT = False

@dataclasses.dataclass
class ScreenInfo:
    capture_picture: mss.screenshot.ScreenShot = None
    capture_screen_pictrue_path: typing.Optional[os.PathLike] = None
    capture_time: datetime.datetime = datetime.datetime.now()
    capture_screen_number: int = 0
    capture_size: typing.Tuple[int, int] = (0, 0)
    screen_top: int = 0
    screen_left: int = 0
    screen_width: int = 0
    screen_height: int = 0


class DeviceOperate:
    """
    DeviceOperate is a class that provides basic input and output functions.

    1. Keyboard operate
    2. Mouse operate
    3. Screen capture
    
    Attributes:
        None

    Methods:
        get_quick_screenshot: Get a quick screenshot.
        get_screen_device_numbers: Get the number of screens.
        get_all_screen_info: Get all screen information.
        get_combined_screen_info: Get the combined screen information.
        get_screen_info_by_number: Get the screen information by number.
        get_mouse_position: Get the current mouse position.
        set_mouse_position: Set the current mouse position.
        mouse_click: Perform a mouse click operation.
        keyboard_press: Perform a keyboard press operation.
        keyboard_write: Perform a keyboard write operation.
        keyboard_hotkey: Perform a keyboard hotkey operation.
        keyboard_key_down: Perform a keyboard key down operation.
        keyboard_key_up: Perform a keyboard key up operation.
        keyboard_is_pressed: Check if the key is pressed.
    
    Examples:
        >>> from io_tools import DeviceOperate
        >>> device = DeviceOperate()
        >>> device.get_quick_screenshot()
        <PIL.Image.Image image mode=RGB size=1920x1080 at 0x1E9F4E3B0D0>
        >>> device.get_screen_device_numbers()
        1
        >>> device.get_all_screen_info()
        [ScreenInfo(capture_picture=<ScreenShot left=0 top=0 width=1920 height=1080 pixel_format='rgb24' filename=None>, capture_screen_pictrue_path=None, capture_time=datetime.datetime(2021, 7, 25, 20, 0, 43, 448000), capture_screen_number=0, capture_size=(1920, 1080), screen_top=0, screen_left=0, screen_width=1920, screen_height=1080)]
        >>> device.get_combined_screen_info()
        ScreenInfo(capture_picture=<ScreenShot left=0 top=0 width=1920 height=1080 pixel_format='rgb24' filename=None>, capture_screen_pictrue_path=None, capture_time=datetime.datetime(2021, 7, 25, 20, 0, 43, 448000), capture_screen_number=0, capture_size=(1920, 1080), screen_top=0, screen_left=0, screen_width=1920, screen_height=1080)
        >>> device.get_screen_info_by_number(0)
        ScreenInfo(capture_picture=<ScreenShot left=0 top=0 width=1920 height=1080 pixel_format='rgb24' filename=None>, capture_screen_pictrue_path=None, capture_time=datetime.datetime(2021, 7, 25, 20, 0, 43, 448000), capture_screen_number=0, capture_size=(1920, 1080), screen_top=0, screen_left=0, screen_width=1920, screen_height=1080)
        >>> device.get_mouse_position()
        (0, 0)
        >>> device.set_mouse_position(100,100)
        >>> device.mouse_click(100,100)
        >>> device.keyboard_press("a")
        >>> device.keyboard_write("hello world")
        >>> device.keyboard_hotkey("ctrl","c")
    Raises:
        ValueError: If the number of screen is less than the input number.

    """
    @classmethod
    def get_quick_screenshot(cls):
        """
        Get a quick screenshot.
        Returns:
            screenshot: The screenshot.
        """
        return pyautogui.screenshot()
    @classmethod
    def get_screen_device_numbers(cls) -> int:
        """
        Get the number of screens.
        `The number of display monitors on a desktop. For more information, see the Remarks section in this topic.`
        more for https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
        Returns:
            device_numbers: The number of screens.
        """
        user32 = ctypes.windll.user32
        screens = user32.GetSystemMetrics(
            80)  # 80 refers to the SM_CMONITORS, the number of display monitors on a desktop.
        return screens

    @classmethod
    def get_all_screen_info(cls) -> typing.List[ScreenInfo]:
        """
        Get all screen information.

        Returns:
            screen_info_list: A list of screen information.
        """
        screen_capture_save_path = os.path.join(__file__, "..", "debug")
        if not os.path.exists(screen_capture_save_path):
            os.mkdir(screen_capture_save_path)
        screen_info_list = []
        number = 0
        with mss.mss() as sct:
            for monitor in sct.monitors:
                monitor_obj = ScreenInfo(
                    capture_picture=None,
                    capture_screen_pictrue_path=None,
                    capture_time=datetime.datetime.now(),
                    capture_screen_number=number,
                    capture_size=(monitor["width"], monitor["height"]),
                    screen_top=monitor["top"],
                    screen_left=monitor["left"],
                    screen_width=monitor["width"],
                    screen_height=monitor["height"],
                )
                monitor_obj.capture_picture = sct.grab(monitor)
                monitor_obj.capture_screen_pictrue_path = os.path.join(screen_capture_save_path, f"{uuid.uuid4()}.png")
                if SAVE_DEBUG_SCREENSHOT:
                    # save to folder ScreenShot to png
                    monitor_obj.capture_picture # type: mss.screenshot.ScreenShot
                    mss.tools.to_png(monitor_obj.capture_picture.rgb, 
                                     monitor_obj.capture_picture.size,
                                     # level=6,  # default is 6 # no need to compress
                                     output=monitor_obj.capture_screen_pictrue_path)
                screen_info_list.append(monitor_obj)
                number += 1
        return screen_info_list
    @classmethod
    def screenshot_to_png(cls, screenshot:mss.screenshot.ScreenShot,
                          save_path:os.PathLike):
        """
        Save screenshot to png file.
        Args:
            screenshot: The screenshot to save.
            save_path: The path to save.
        """
        mss.tools.to_png(screenshot.rgb,
                            screenshot.size,
                            # level=6,  # default is 6 # no need to compress
                            output=save_path)

    @classmethod
    def get_combined_screen_info(cls) -> ScreenInfo:
        return cls.get_all_screen_info()[0]

    @classmethod
    def get_screen_info_by_number(cls, number: int) -> ScreenInfo:
        if number > cls.get_screen_device_numbers():
            raise ValueError(f"the number of screen is {cls.get_screen_device_numbers()}, but you input {number}")
        return cls.get_all_screen_info()[number]

    @classmethod
    def get_mouse_position(cls) -> typing.Tuple[int, int]:
        """
        Get the current mouse position.
        Returns:
            mouse_position: The current mouse position.
        """
        return pyautogui.position()

    @classmethod
    def set_mouse_position(cls, x: int, y: int) -> None:
        """
        Set the current mouse position.
        Args:
            x: The x coordinate of the mouse position.
            y: The y coordinate of the mouse position.
        """
        pyautogui.moveTo(x, y)
    @classmethod
    def simulate_click(cls,
                            x: int,
                            y: int,
                            duration: float = 0.1,
                            ):
        """
        a simple click but with duration
        Args:
            x: The x coordinate of the mouse position.
            y: The y coordinate of the mouse position.
            duration: The duration of the mouse down. Default is 0.1.
        """
        pyautogui.mouseDown(x,y)
        time.sleep(duration)
        pyautogui.mouseUp(x,y)
    @classmethod
    def mouse_click(cls,
                    x: int,
                    y: int,
                    button: str = typing.Literal["left", "middle", "right"],
                    # arg button can be "primary" or "secondary", they defines in pyautogui.__init__
                    clicks: int = 1,
                    interval: float = 0.0,
                    duration: float = 0.0) -> None:
        """
        Perform a mouse click operation.
        Args:
            x: The x coordinate of the mouse position.
            y: The y coordinate of the mouse position.
            button: The mouse button to click. Default is left.
            clicks: The number of clicks. Default is 1.
            interval: The interval between clicks. Default is 0.0.
            duration: The duration of the mouse down. Default is 0.0.
        """
        pyautogui.click(x, y, button=button, clicks=clicks, interval=interval, duration=duration)

    @classmethod
    def keyboard_press(cls,
                       key: str,
                       interval: float = 0.0,
                       duration: float = 0.0) -> None:
        """
        Perform a keyboard press operation.
        Args:
            key: The key to press down.
            interval: The interval between key down and key up. Default is 0.0.
            duration: The duration of the key down. Default is 0.0.
        """
        pyautogui.press(key, interval=interval, duration=duration)

    @classmethod
    def keyboard_write(cls,
                       message: str,
                       interval: float = 0.0,
                       duration: float = 0.0) -> None:
        """
        Perform a keyboard write operation.
        Args:
            message: The message to write.
            interval: The interval between key down and key up. Default is 0.0.
            duration: The duration of the key down. Default is 0.0.
        """
        pyautogui.write(message, interval=interval, duration=duration)

    @classmethod
    def keyboard_hotkey(cls,
                        *args,
                        interval: float = 0.0,
                        duration: float = 0.0) -> None:
        """
        Perform a keyboard hotkey operation.
        Args:
            *args: The hotkey to press down.
            interval: The interval between key down and key up. Default is 0.0.
            duration: The duration of the key down. Default is 0.0.
        """
        pyautogui.hotkey(*args, interval=interval, duration=duration)

    @classmethod
    def keyboard_key_down(cls,
                          key: str,
                          interval: float = 0.0,
                          duration: float = 0.0) -> None:
        """
        Perform a keyboard key down operation.
        Args:
            key: The key to press down.
            interval: The interval between key down and key up. Default is 0.0.
            duration: The duration of the key down. Default is 0.0.
        """
        pyautogui.keyDown(key, interval=interval, duration=duration)

    @classmethod
    def keyboard_key_up(cls,
                        key: str,
                        interval: float = 0.0,
                        duration: float = 0.0) -> None:
        """
        Perform a keyboard key up operation.
        Args:
            key: The key to press down.
            interval: The interval between key down and key up. Default is 0.0.
            duration: The duration of the key down. Default is 0.0.
        """
        pyautogui.keyUp(key, interval=interval, duration=duration)

    @classmethod
    def keyboard_is_pressed(cls,
                            key: str) -> bool:
        """
        Check if the key is pressed.
        Args:
            key: The key to check.
        Returns:
            is_pressed: True if the key is pressed, otherwise False.
        """
        return pyautogui.isPressed(key)


class InputListener:
    """
    InputListener is a class that provides basic input listener functions.

    provides two listening modes, one is callback mode and the other is queue mode, the default is callback mode.
    You can give the global instance of this class a callback function through a class method, 
    and the callback function will be triggered when keyboard or mouse events occur.

    In queue mode, you can get the keyboard or mouse event through the get_mouse_events and get_keyboard_events methods.
    The act of calling these methods is actually to act as a consumer to obtain the elements in the queue.
    However, the queue mode only provides a basic message structure and is not as flexible as the callback mode. It can be used in simple scenarios.

    Methods:
        get_recent_mouse_events: Get recent mouse events.
        get_recent_keyboard_events: Get recent keyboard events.
        get_all_mouse_events: Get mouse events from queue.
        get_all_keyboard_events: Get keyboard events from queue.
        get_keyboard_event: Get keyboard events from queue.
        get_mouse_event: Get mouse events from queue.
        set_keyboard_pressed_callback: Set the callback function for keyboard pressed event.
        set_keyboard_released_callback: Set the callback function for keyboard released event.
        set_mouse_pressed_callback: Set the callback function for mouse pressed event.
        set_mouse_moved_callback: Set the callback function for mouse moved event.
        set_mouse_scrolled_callback: Set the callback function for mouse scrolled event.
        start: Start the listener.
        stop: Stop the listener.
    
    Examples:
        >>> from io_tools import InputListener
        >>> listener = InputListener()
        >>> listener.set_keyboard_pressed_callback(lambda key:print(key))
        >>> listener.set_mouse_pressed_callback(lambda x,y,button,pressed:print(x,y,button,pressed))
        >>> listener.start()
        >>> listener.stop()
    """
    _instance = None
    _keyboard_listener = None
    _mouse_listener = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InputListener, cls).__new__(cls)
        return cls._instance

    def __init__(self, callback_mode: bool = False) -> None:
        """
        Constructor of InputListener class.

        Args:
            callback_mode: The listening mode, True is callback mode, False is queue mode.

        """
        self.callback_mode = callback_mode
        if not callback_mode:  # in queue mode
            # init queue
            self.mouse_event_queue = queue.Queue()
            self.keyboard_event_queue = queue.Queue()

            # init recent event deque
            self._recent_mouse_event_deque = collections.deque(maxlen=10)
            self._recent_keyboard_event_deque = collections.deque(maxlen=10)
            # init listener
            self._keyboard_listener = pynput.keyboard.Listener(on_press=self._q_on_keyboard_press)
            self._mouse_listener = pynput.mouse.Listener(on_click=self._q_on_mouse_click)
            # start listener
            self._keyboard_listener.start()
            self._mouse_listener.start()

        else:  # in callback mode
            self.callbacks: typing.Dict[
                str, typing.Callable] = {}  # keys: keyboard_pressed, keyboard_released, mouse_pressed, mouse_moved, mouse_scrolled
            # waiting for callback function to be set, and user have to start listener manually

    def _q_on_keyboard_press(self, key):
        self.keyboard_event_queue.put(key)
        self._recent_keyboard_event_deque.append(key)

    def _q_on_mouse_click(self, x, y, button, pressed):
        self.mouse_event_queue.put((x, y, button, pressed))
        self._recent_mouse_event_deque.append((x, y, button, pressed))
    
    def get_recent_mouse_events(self) -> typing.List[typing.Tuple[int, int, str, bool]]:
        """
        Get recent mouse events.
        Returns:
            events: A list of mouse events.
        """
        return list(self._recent_mouse_event_deque)
    
    def get_recent_keyboard_events(self) -> typing.List[pynput.keyboard.Key]:
        """
        Get recent keyboard events.
        Returns:
            events: A list of keyboard events.
        """
        return list(self._recent_keyboard_event_deque)

    def get_all_mouse_events(self) -> typing.List[typing.Tuple[int, int, str, bool]]:
        """
        Get mouse events from queue.
        Returns:
            events: A list of mouse events.
        """
        events = []
        while not self.mouse_event_queue.empty():
            events.append(self.mouse_event_queue.get())
        return events

    def get_all_keyboard_events(self) -> typing.List[pynput.keyboard.Key]:
        """
        Get keyboard events from queue.
        Returns:
            events: A list of keyboard events.
        """
        events = []
        while not self.keyboard_event_queue.empty():
            events.append(self.keyboard_event_queue.get())
        return events

    def get_keyboard_event(self) -> typing.Generator[pynput.keyboard.Key, None, None]:
        """
        Get keyboard events from queue.
        Returns:
            event: A keyboard event.
        """
        while True:
            yield self.keyboard_event_queue.get()

    def get_mouse_event(self) -> typing.Generator[typing.Tuple[int, int, str, bool], None, None]:
        """
        Get mouse events from queue.
        Returns:
            event: A mouse event.
        """
        while True:
            yield self.mouse_event_queue.get()

    def set_keyboard_pressed_callback(self, callback: typing.Callable) -> None:
        """
        Set the callback function for keyboard pressed event.
        Args:
            callback: The callback function.
        """
        self.callbacks["keyboard_pressed"] = callback

    def set_keyboard_released_callback(self, callback: typing.Callable) -> None:
        """
        Set the callback function for keyboard released event.
        Args:
            callback: The callback function.
        """
        self.callbacks["keyboard_released"] = callback

    def set_mouse_pressed_callback(self, callback: typing.Callable) -> None:
        """
        Set the callback function for mouse pressed event.
        Args:
            callback: The callback function.
        """
        self.callbacks["mouse_pressed"] = callback

    def set_mouse_moved_callback(self, callback: typing.Callable) -> None:
        """
        Set the callback function for mouse moved event.
        Args:
            callback: The callback function.
        """
        self.callbacks["mouse_moved"] = callback

    def set_mouse_scrolled_callback(self, callback: typing.Callable) -> None:
        """
        Set the callback function for mouse scrolled event.
        Args:
            callback: The callback function.
        """
        self.callbacks["mouse_scrolled"] = callback

    def start(self) -> None:
        """
        Start the listener.
        """
        # register callbacks

        if not self.callback_mode:  # not in callback mode, don't need to start listener manually
            return
        else:
            # register six callback functions
            _kbd_pd = self.callbacks.get("keyboard_pressed", None)
            _kbd_rl = self.callbacks.get("keyboard_released", None)
            _ms_pd = self.callbacks.get("mouse_pressed", None)
            _ms_mv = self.callbacks.get("mouse_moved", None)
            _ms_sc = self.callbacks.get("mouse_scrolled", None)

            # init listener
            self._keyboard_listener = pynput.keyboard.Listener(on_press=_kbd_pd, on_release=_kbd_rl)
            self._mouse_listener = pynput.mouse.Listener(on_click=_ms_pd, on_move=_ms_mv, on_scroll=_ms_sc)
            # start listener
            self._keyboard_listener.start()
            self._mouse_listener.start()

    def stop(self) -> None:
        """
        Stop the listener.
        """

        self._keyboard_listener.stop()
        self._mouse_listener.stop()


# static methods:
"""
these methods are used to provide basic input and output functions.
"""
def click_position(x:int,y:int):
    """
    Click the position of the screen.
    Args:
        x: The x coordinate of the mouse position.
        y: The y coordinate of the mouse position.
    """
    pyautogui.click(x=x,y=y)

def io_input_text(text:str):
    """
    Input text.
    Args:
        text: The text to input.
    """
    pyautogui.write(text)

def io_press_key(options:list):
    """
    Press key.
    Args:
        options: The key to press.
    """
    if len(options) == 1:
        pyautogui.press(options[0])
    if len(options) > 1:
        pyautogui.hotkey(*options)


def run_shell(cmd_text:str):
    """
    Run shell command.
    Args:
        cmd_text: The command to run.
    """
    result = subprocess.run(cmd_text, shell=True, capture_output=True, text=True)
    return result
