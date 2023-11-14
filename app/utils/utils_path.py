import os
import pathlib

class Path:

    _instance = None
    DISPLAY_PATH =  '\r\ndebian@root: '

    def __new__(cls) -> None:
        if not  cls._instance:
            cls._instance = super(Path,cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self,'initialized'):
            self.__start_full_path = os.path.join(os.getcwd(),"app","home")
            self.__current_path = self.__start_full_path
            self.initialized = True
            self.__path_display = self.DISPLAY_PATH

    def get_start_full_path(self)-> str:
        return self.__start_full_path
    
    def get_current_path(self)-> str:
        return self.__current_path
    
    def set_current_path(self,path):
        self.__current_path = os.path.join(self.__start_full_path,path)
        self.__path_display = os.path.join(self.__path_display.replace(" ",""), os.path.basename(path))+"$ "
        
    def reset_path(self):
        self.__current_path = self.__start_full_path
        self.__path_display = self.DISPLAY_PATH

    def get_cli_display_path(self):
        print("path display ", self.__path_display)
        return self.__path_display

