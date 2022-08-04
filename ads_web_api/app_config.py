import logging
import os
import jsonpickle
import click
from flask import current_app
from flask.cli import with_appcontext

CONFIG_FILE_PATH=r'config.json'
API_FILE_PATH=r'api.json'
class AppConfig():
    def __init__(self):        
        self.ams_port = 851
        self.ams_address = ""
        self.log_level = 0
        self.allow_var_req = False   
        self.omit_var_name = True        

    def create_config(self, file_path):
        logger = logging.getLogger('AppConfig')

        with open(file_path, 'w') as f: 
            f.write(jsonpickle.encode(self))
            logger.info('...new parameter file created')                                

    def load(self, file_path):
        logger = logging.getLogger('AppConfig')

        try:                        
            with current_app.open_resource(file_path, 'r') as f:                              
                return jsonpickle.decode(f.read())                           
        except FileNotFoundError:            
            logger.warning('No valid param file available! Creating empty parameter file...')            
            logger.info('return empty parameter file!')    
            self.create_config(file_path)
            return self.load(file_path)

    def create_api(self, file_path):
        logger = logging.getLogger('AppConfig')

        with open(file_path, 'w') as f:                                           
            logger.info('...new empty api file created')

    def load_api(self, file_path):
        logger = logging.getLogger('AppConfig')        
        try:                        
            logger.info(file_path)
            with current_app.open_resource(file_path, 'r') as f:                                
                return jsonpickle.decode(f.read())                           
        except FileNotFoundError:            
            logger.error('No valid api file available!')
            with current_app.open_resource(file_path, 'w') as f:                                
                logger.info('...new empty api file created')
            logger.info('return empty api file (api.json)! Add API description to this file!')
            raise Exception("No valid api description found!")

def create_config():
    config = AppConfig()
    path = os.path.join(current_app.instance_path, CONFIG_FILE_PATH)
    config.create_config(path)

def create_api():
    config = AppConfig()
    path = os.path.join(current_app.instance_path, API_FILE_PATH)
    config.create_api(path)
      
@click.command('create_config')
@with_appcontext
def create_config_command():
    """create a config file with default values."""
    create_config()
    click.echo('created new config file')

@click.command('create_api')
@with_appcontext
def create_api_command():
    """create a config file with default values."""
    create_api()
    click.echo('created new config file')

def init_app(app):    
    app.cli.add_command(create_config_command)
    app.cli.add_command(create_api_command)
