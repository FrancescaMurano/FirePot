import os

class Path:

    DISPLAY_PATH =  '\r\ndebian@root: '
    
    def __init__(self) -> None:
            self.__start_full_path = os.path.join(os.getcwd(),"app","home")
            #self.__start_full_path = os.path.join(os.getcwd(),"telnet","app","home")

            print("SELF PATH ",self.__start_full_path)
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
        return self.__path_display


