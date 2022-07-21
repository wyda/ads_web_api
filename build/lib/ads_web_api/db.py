import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

from ads_web_api.app_config import AppConfig

CONFIG_FILE_PATH=r'config.json'

def init_db():
    db = get_db()
    config = AppConfig().load(CONFIG_FILE_PATH)    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    cur = db.cursor()     
    if type(config) == dict: #ToDo Why is the config not allways form type AppConfig after laoding with jsonpickle?
        cur.execute("INSERT INTO ads_config VALUES (?,?,?,?)", (1, config['ams_port'], config['ams_address'], config['log_level']))
        cur.execute("INSERT INTO api_config VALUES (?, ?, ?, ?)", (1, config['allow_var_req'], config['omit_var_names'], 0))    
    else:
        cur.execute("INSERT INTO ads_config VALUES (?,?,?,?)", (1, config.ams_port, config.ams_address, config.log_level))   
        cur.execute("INSERT INTO api_config VALUES (?, ?, ?, ?)", (1, config.allow_var_req, config.omit_var_name, 0))    
    db.commit()

def reload_config():
    db = get_db()
    config = AppConfig().load(CONFIG_FILE_PATH)    
    cur = db.cursor()    
    if type(config) == dict: #ToDo Why is the config not allways form type AppConfig after laoding with jsonpickle?
        cur.execute("UPDATE ads_config SET port=?, ams_address=?, log_level=? WHERE id=1", (config['ams_port'], config['ams_address'], config['log_level']))
        cur.execute("UPDATE api_config SET allow_var_req=?, omit_var_names=? WHERE id=1", (config['allow_var_req'], config['omit_var_names']))    
    else:
        cur.execute("UPDATE ads_config SET port=?, ams_address=?, log_level=? WHERE id=1", (config.ams_port, config.ams_address, config.log_level))
        cur.execute("UPDATE api_config SET allow_var_req=?, omit_var_names=? WHERE id=1", (config.allow_var_req, config.omit_var_name))    
    db.commit()
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('reload-config')
@with_appcontext
def reload_config_command():
    """Load config.json to database"""
    reload_config()
    click.echo('Load config.json to db')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(reload_config_command)

def get_db():
    if 'db' not in g:                
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()