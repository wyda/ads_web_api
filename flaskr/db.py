import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

from flaskr.config import AppConfig

def init_db():
    db = get_db()
    config = AppConfig()
    config = config.load('flaskr\config.json')
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    cur = db.cursor()
    # Insert a row of data    
    cur.execute("INSERT INTO ads_config VALUES (?,?,?,?)", (1, config.ams_port, config.ams_address, config.log_level))
    cur.execute("INSERT INTO api_config VALUES (?, ?, ?)", (1, config.allow_var_req, 0))
    # Save (commit) the changes
    db.commit()

def reload_config():
    db = get_db()
    config = AppConfig()
    config = config.load('flaskr\config.json')
    
    cur = db.cursor()
    # Insert a row of data    
    cur.execute("UPDATE ads_config SET port=?, ams_address=?, log_level=? WHERE id=1", (config.ams_port, config.ams_address, config.log_level))
    cur.execute("UPDATE api_config SET allow_var_req=? WHERE id=1", (config.allow_var_req,))
    # Save (commit) the changes
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