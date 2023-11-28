"""
    filename: io_tools/systeminfo.py
    ~~~~~~~~~~~~~~~~~~~~
    System information module. Get system information. Windows only.

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

import dataclasses
import typing
import psutil
import ctypes
import pywinauto

@dataclasses.dataclass
class WindowsProcess:
    """WindowsProcess class provides a data structure for Windows processes"""
    process_name: str  # Process name
    has_children: bool  # Does the process have children?
    pid: int  # Process ID
    status: str  # Process status
    executable: str  # Executable Path


class WindowsProcessOperate:

    @classmethod
    def _is_system_process(cls, process: WindowsProcess) -> bool:
        """
        Determine if a process is a system process.
        Args:
            process: A WindowsProcess object.
        Returns:
            bool: True if it is a system process, otherwise False.
        """
        return process.pid == 0 or process.process_name == "System Idle Process"

    @classmethod
    def is_runas_administrator(cls) -> bool:
        """
        Check if the current process is running as administrator.
        Returns:
            bool: True if it is running as administrator, otherwise False.
        """
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

    @classmethod
    def get_all_processes(cls) -> typing.List[WindowsProcess]:
        """
        Get all system processes.
        Returns:
            typing.List[WindowsProcess]: A list of WindowsProcess objects.
        """
        pids = psutil.pids()
        process_list = []
        for pid in pids:
            if pid == 0:  # System Idle Process
                continue
            process = psutil.Process(pid)
            process_list.append(
                WindowsProcess(process.name(), process.children(), process.pid, process.status(), process.exe()))
        return process_list

    @classmethod
    def kill_process_by_pid(cls, pid: int) -> None:
        """
        Kill a process by its pid. need administrator privileges.
        Args:
            pid: The pid of the process.
        """
        if not cls.isRunAsAdministrator():
            raise PermissionError("Need administrator privileges.")
        psutil.Process(pid).kill()
    @classmethod
    def start_executable(cls, path: str) -> None:
        """
        Start a executable file as administrator.
        Args:
            path: The path of the executable file.
        """
        if not cls.isRunAsAdministrator():
            raise PermissionError("Need administrator privileges.")
        psutil.Popen(path)

    @classmethod
    def load_process_to_front(cls,program_name: str) -> None:
        """
        load a background program to front.
        """
        for process in cls.get_all_processes():
            if process.process_name==program_name:
                app = pywinauto.Application().connect(process=process.pid)
                app.window().set_focus()
                return
            
    @classmethod
    def load_process_from_executable(cls,executable_path: str) -> None:
        """
        start a program from executable path.
        """
        pywinauto.Application().start(executable_path)
        return
    