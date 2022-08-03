import os
import secrets
import logging
from flask import Flask, jsonify, request, abort
#from flask import g, current_app, session
from ads_web_api.db import get_db
from .ads_client import AdsClient
from .app_config import AppConfig
from .api import create_var_list, create_response, omit_apiinfo_var_name
from markupsafe import escape

ALLOW_VAR_REQ='allow_var_req'
OMIT_VAR_NAMES='omit_var_names'
API_FILE_PATH=r'api.json'

logging.basicConfig(filename='app.log', encoding='utf-8', 
                    level=10, 
                    format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')         

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)                 
    app.config.from_mapping(
        SESSION_TYPE = 'filesystem',
        SECRET_KEY= secrets.token_urlsafe(32),        
        DATABASE=os.path.join(app.instance_path, 'ads_web_api.sqlite'),    
    )        

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:        
        os.makedirs(app.instance_path)
    except OSError as e:
        logging.info('Folder for app instance already exists')        
        logging.info(app.instance_path)   

    @app.route('/api/readvar')
    def readvar():             
        ads = AdsClient()    
        db = get_db()    
        api_config=db.execute(
            'SELECT * FROM api_config WHERE id = ?', (1,)
        ).fetchone()  
        if api_config[ALLOW_VAR_REQ]:
            varnames = []
            for arg in request.args:            
                varnames.append(escape(arg)) 
            try:
                return jsonify(ads.plc.read_list_by_name(varnames))                
            except Exception as e:
                abort(502, description=e)
        abort(403, description='Direct var access not allowed!')

    @app.route('/api/<call>')
    def api(call):                
        config = AppConfig()         
        try:       
            api_config = config.load_api(API_FILE_PATH)        
        except Exception as e:
            logging.error("No valid API description!")
            abort(404, description='No API description available!')

        if varnames := create_var_list(call, api_config, request):
            ads = AdsClient()                                    
            try:
                results = ads.plc.read_list_by_name(varnames)            
                return jsonify(create_response(results, call, api_config))        
            except Exception as e:                            
                abort(502, description=e)
        abort(404, description='api call "{}" not available!'.format(call))
    
    @app.route('/api/apiinfo')
    def apiinfo():                
        try:
            api_info = AppConfig().load_api(API_FILE_PATH)                      
        except Exception as e:
            logging.error("No valid API description!")
            abort(404, description='No API description available!')

        db = get_db()   
        api_config=db.execute(
            'SELECT * FROM api_config WHERE id = ?', (1,)
        ).fetchone() 
        if api_config[OMIT_VAR_NAMES]:
            return omit_apiinfo_var_name(api_info) 
        return jsonify(api_info)
    
    from . import db
    db.init_app(app)

    @app.errorhandler(403)
    def resource_not_found(e):
        return jsonify(error=str(e)), 403

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(502)
    def resource_not_found(e):
        return jsonify(error=str(e)), 502  

    return app