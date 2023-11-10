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


# load config files
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

EVENT_FILE = app_config["datastore"]["filename"]

def populate_stats():
    """ Periodically update stats """
    num_rate_readings = 0
    num_saves_readings = 0
    highest_rated = 0

    log_file = log_config['handlers']['file']['filename']
    logger.info("====================> Periodic processing started...")
    current_timestamp = (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

    # read current json
    if(os.path.isfile(EVENT_FILE)):
        with open(EVENT_FILE, 'r') as f3:
            stats = json.load(f3)
    else:
        # If the file doesn’t yet exist, use default values for the stats??????
        stats = {'num_rate_readings': 0, 'highest_rated': 0, 'num_saves_readings': 0, 'most_active_user': 1, 'last_updated': '1800-01-01T23:59:59Z'}

    last_updated = stats["last_updated"]

    # -- RATE stats
    URLRATE = app_config["eventstore"]["rate"]
    result_raw = requests.get(URLRATE + "?start_timestamp=" + last_updated + "&end_timestamp=" + current_timestamp)
    rate_result=result_raw.json()

    # # -- SAVE stats
    URLSAVE = app_config["eventstore"]["save"]
    result_raw2 = requests.get(URLSAVE + "?start_timestamp=" + last_updated + "&end_timestamp=" + current_timestamp)
    save_result=result_raw2.json()

    # -- RATE stats
    if(len(rate_result) == 0):
        print("Nothing to log")
    else:
        ratings = [entry['rating'] for entry in rate_result]
        num_rate_readings=len(ratings)
        highest_rated=max(ratings)

    # -- SAVE stats
    if(len(save_result) == 0):
        print("Nothing to log")
        most_active_user = stats["most_active_user"]
    else:
        saves = [entry['id'] for entry in save_result]
        num_saves_readings=len(saves)
        counted = Counter([entry['user_id'] for entry in save_result])
        most_active_user = counted.most_common(1)[0][0]

    updated_num_rate_readings= num_rate_readings + stats["num_rate_readings"]
    updated_num_saves_readings= num_saves_readings + stats["num_saves_readings"]
    updated_highest_rated= max(highest_rated,stats["highest_rated"])
    updated_highest_rated = max(most_active_user,stats["most_active_user"])
    # note not sure what to do with most common user calc here...

    newstats = {
    "num_rate_readings": updated_num_rate_readings,
    "highest_rated": updated_highest_rated,
    "num_saves_readings": updated_num_saves_readings,
    "most_active_user": updated_highest_rated,
    "last_updated": current_timestamp
    }

    with open(EVENT_FILE, 'w') as file:
        json.dump(newstats, file, indent=2)
        # Note that values in the data.json file should correspond to the values in the JSON response from your GET /stats endpoint.
        # ^ ive been reading this over and over and still dont understand if im correct yall. its past 11

    logger.debug(newstats)
    logger.info("---------------------> Periodic processing complete...")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
        'interval',
        seconds=app_config['scheduler']['period_sec'])
    sched.start()
 
# Your functions here
def get_stats(): #/stats
    logger.info("===> Request for stats started...")
    if(os.path.isfile(EVENT_FILE)):
        with open(EVENT_FILE, 'r') as f4:
            statsread = json.load(f4)
    else:
        logger.error(f"Stats file {EVENT_FILE} cannot be found")
        return "Statistics do not exist", 404
    
    logger.debug(statsread)

    logger.info("===> Request for stats complete...")
    
    return statsread, 200

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)



