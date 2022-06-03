import os
import secrets
from flask import Flask, jsonify, request
from flask import g, current_app, session
from flaskr.db import get_db
from ads.ads_client import AdsClient


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
    def ads():             
        ads = AdsClient()    
        db = get_db()    
        api_config=db.execute(
            'SELECT * FROM api_config WHERE id = ?', (1,)
        ).fetchone()  
        if api_config['allow_var_req']:
            varnames = []                
            for arg in request.args:            
                varnames.append(arg)        
            return jsonify(ads.plc.read_list_by_name(varnames))                
        else:
            return 'direct var access not allowed'
    
    from . import db
    db.init_app(app)

    return app