import os

class Path:

    _instance = None

    def __new__(cls) -> None:
        if not  cls._instance:
            cls._instance = super(Path,cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self,'initialized'):
            self.__start_full_path = os.path.join(os.getcwd(),"app","home")
            self.__current_path = self.__start_full_path
            self.initialized = True

    def get_start_full_path(self)-> str:
        return self.__start_full_path
    
    def get_current_path(self)-> str:
        return self.__current_path
    
    def set_current_path(self,path):
        self.__current_path = os.path.join(self.__start_full_path,path)
        
    def reset_path(self):
        self.__current_path = self.__start_full_path


