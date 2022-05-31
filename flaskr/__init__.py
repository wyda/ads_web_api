import os

from flask import Flask
from flask import g, current_app
from . import ads_client

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # a simple page that says hello
    @app.route('/ads')
    def ads():
        if 'ads' not in g:
            print("NO g.ads")      
            g.ads = ads_client.AdsClient()
            g.ads.start()   
            return(str(type(g.ads)))      
        return("ads")

    from . import ads_client
    ads_client.init_ads(app)
   
    return app