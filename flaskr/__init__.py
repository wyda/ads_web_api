import os
import secrets
from flask import Flask, jsonify, request
from flask import g, current_app, session
#from flask_session import Session
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

    @app.route('/read_var/', methods=['GET'])
    def ads():        
        ads = AdsClient()         
        varnames = []                
        for arg in request.args:            
            varnames.append(arg)        
        return jsonify({"results": ads.plc.read_list_by_name(varnames)})                

    return app