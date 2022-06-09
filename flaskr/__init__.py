import os
import secrets
from flask import Flask, jsonify, request, abort
#from flask import g, current_app, session
from flaskr.db import get_db
from ads.ads_client import AdsClient
from .config import AppConfig
from .api import create_var_list, create_response, omit_apiinfo_var_name
from markupsafe import escape

ALLOW_VAR_REQ='allow_var_req'
OMIT_VAR_NAMES='omit_var_names'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)                 
    app.config.from_mapping(
        SESSION_TYPE = 'filesystem',
        SECRET_KEY= secrets.token_urlsafe(32),        
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),    
    )

    #Session(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    

    @app.route('/readvar/', methods=['GET'])
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
            return jsonify(ads.plc.read_list_by_name(varnames))                
        abort(403)

    @app.route('/api/<call>')
    def api(call):                
        config = AppConfig()                
        api_config = config.load_api(r'flaskr\api.json')        
        
        if varnames := create_var_list(call, api_config, request):
            ads = AdsClient()                                    
            results = ads.plc.read_list_by_name(varnames)            
            return jsonify(create_response(results, call, api_config))        
        abort(404)
    
    @app.route('/apiinfo')
    def apiinfo():        
        config = AppConfig()                        
        api_info = config.load_api(r'flaskr\api.json')              
        db = get_db()   
        api_config=db.execute(
            'SELECT * FROM api_config WHERE id = ?', (1,)
        ).fetchone() 
        if api_config[OMIT_VAR_NAMES]:
            return omit_apiinfo_var_name(api_info) 
        return jsonify(api_info)
    
    from . import db
    db.init_app(app)

    return app