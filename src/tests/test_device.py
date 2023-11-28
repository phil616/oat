import unittest
import time
import threading
from io_tools.device import DeviceOperate,ScreenInfo,InputListener
class TestDevice(unittest.TestCase):
    FISRT_SCREEN_SIZE = (2560, 1080)  # replace with your monitor size
    SECOND_SCREEN_SIZE = (900, 1600)  # replace with your monitor size
    SCREEN_NUMBER = 2  # replace with your monitor device numbers
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
    
    def setUp(self):
        print("setUp")
    
    def tearDown(self):
        print("tearDown")

    def test_screen_count(self):
        print("test_screeninfo")
        DEVICE_NUMBERS = 2  # replace with your monitor device numbers
        self.assertEqual(DEVICE_NUMBERS,DeviceOperate.get_screen_device_numbers())

    def test_screen_info(self):
        print("test_screeninfo")
        my_screen_size = self.FISRT_SCREEN_SIZE  # replace with your monitor size
        infos:list[ScreenInfo] = DeviceOperate.get_all_screen_info()
        screen_size = infos[1].capture_picture.size
        self.assertEqual(my_screen_size, infos[1].capture_size)
        self.assertEqual(screen_size, my_screen_size)

    def test_combined_screen(self):
        print("test_combined_screen")
        if DeviceOperate.get_screen_device_numbers() < 2:
            return
        # no suitable test method for now
    
    def test_mouse_position(self):
        print("test_mouse_position")
        mouse_pos = DeviceOperate.get_mouse_position()
        # test mouse position in first screen's range
        self.assertTrue(mouse_pos.x < self.FISRT_SCREEN_SIZE[0])
        self.assertTrue(mouse_pos.y < self.FISRT_SCREEN_SIZE[1])
        # hardly test mouse position in second screen's range
        # because due to the relative position of the two screens, 
        # windows has a certain offset when calculating the mouse position
    def test_set_mouse_position(self):
        print("test_set_mouse_position")
        print("PLEASE WATCHING YOUR MOUSE POSITION")
        cur_mouse_pos = DeviceOperate.get_mouse_position()
        new_mouse_pos = (cur_mouse_pos.x + 100, cur_mouse_pos.y + 100)
        DeviceOperate.set_mouse_position(*new_mouse_pos)
        print("set mouse position to {}".format(new_mouse_pos))
    def test_mouse_click(self):
        # TODO: test mouse click
        pass

class TestInputListener(unittest.TestCase):
    def test_input_listener(self):
        WAITING_SECONDS = 1
        input_listener = InputListener(callback_mode=False)

        def mouse_event_print(input_listener):
            for e in input_listener.get_mouse_event():
                print(e)

        def keyboard_event_print(input_listener):
            for e in input_listener.get_keyboard_event():
                print(e)
        
        mouse_thread = threading.Thread(target=mouse_event_print,args=(input_listener,),daemon=True)
        keyboard_thread = threading.Thread(target=keyboard_event_print,args=(input_listener,),daemon=True)
        mouse_thread.start()
        keyboard_thread.start()
        while True:
            time.sleep(1)
            if WAITING_SECONDS == 0:
                input_listener.stop()
                break
            WAITING_SECONDS -= 1
        print("test_input_listener end")
    