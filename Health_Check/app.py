import connexion
from connexion import NoContent
import json
import requests
import datetime
import yaml
import logging
import logging.config
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os.path
from collections import Counter
from flask_cors import CORS, cross_origin
import os
from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from health import Health
import sqlite3

DB_ENGINE = create_engine("sqlite:///health.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

# load config files
with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

# get VARS
URL_receiver = app_config["domain"] + app_config["urls"]["receiver"]
URL_storage = app_config["domain"] + app_config["urls"]["storage"]
URL_processing = app_config["domain"] + app_config["urls"]["processing"]
URL_audit = app_config["domain"] + app_config["urls"]["audit"]
URL_list = [URL_receiver , URL_storage, URL_processing, URL_audit]

# ---- functions
def check_health():
    logger.info("====> Periodic health scan started...")
    session = DB_SESSION()
    
    # scan health for each url endpoint 
    for url in URL_list:
        try:
            result_raw = requests.get(url, timeout=5)
           
            if(result_raw.status_code == 200):
                status = "Running"
            else:
                status = "Down"
        except:
            status = "Down"

        service = url.split("/")[-2]
        current_timestamp = (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        
        # commit to sqlite
        new = Health(service,
                    status,
                    current_timestamp)

        session.add(new)
    
    session.commit()
    session.close()      
    logger.info("----> Periodic health scan scomplete...")
    
def get_health_stats(): # /status
    result = {}
    
    conn = sqlite3.connect("health.sqlite")
    cur = conn.cursor()
    for url in URL_list:
        cur.execute(f"SELECT * FROM health where service='{url.split('/')[-2]}' ORDER BY time_stamp DESC LIMIT 1 ")
        rows = cur.fetchall()
        for row in rows:
            # print(row)
            result[row[1]] = row[2]
            result['last_updated'] = row[3]
    conn.close()
    
    return result
        
def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(check_health,
        'interval',
        seconds=app_config['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("openapi.yaml", base_path="/healthcheck", strict_validation=True, validate_responses=True) #------ BRING BACK
# app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) #------ BRING BACK
# app.add_api("openapi.yaml", base_path="/healthcheck") #------ BRING BACK

if __name__ == "__main__":
    init_scheduler() #------ BRING BACK
    # app.run(port=8120, use_reloader=False)
    app.run(port=8120)
