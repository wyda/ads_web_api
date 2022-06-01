import sys
import os
from ads import ads_config

def get_root_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)        
    elif __file__:        
        return os.path.dirname(os.path.realpath(__file__))

def load_config():
    return ads_config.AppConfig(get_root_dir()).load_config()