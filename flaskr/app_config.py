from pathlib import Path
import jsonpickle
import logging

class AppConfig():
    def __init__(self, app_path):                
        self.__file_name = '\\param.json'
        self.ads_port = 851
        self.ams_address = ""    
        self.app_path = app_path
        self.log_level = logging.NOTSET                  

    def load_config(self):
        print(self.app_path + self.__file_name)
        try:                        
            with open(Path(self.app_path + self.__file_name)) as paramFile:                                                                                           
                return jsonpickle.decode(paramFile.read())
        except Exception as e:            
            logging.error ('No valid param file available! Creating empty parameter file...', e)

            with open(Path(self.app_path + self.__file_name), 'w') as paramFile:   
                paramFile.write(jsonpickle.encode(self))
            logging.debug('...new parameter file created')

    def save_config(self):    
        with open(Path(self.app_path + self.__file_name), 'w') as paramFile:   
            paramFile.write(jsonpickle.encode(self))        
