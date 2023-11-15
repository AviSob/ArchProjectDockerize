import connexion
from connexion import NoContent
import json
import requests
import datetime
import yaml
import logging
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from flask_cors import CORS
import os

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


def get_movie_ratings(index): #/movies/movie_ratings?index=X
    """ Get movie rating in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"]) # kafka
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving movie rating at index %d" % index)
    list_of_msg = []
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            if(msg['type'] == 'rate'):
                list_of_msg.append(msg)
                print(msg)
            
        payload = list_of_msg[index]
        response = {
            "type": payload["type"],
            "datetime": payload["datetime"],
            "payload": json.loads(payload["payload"])
        }
        return response, 200
    except:
        logger.error("No more messages found")
        logger.error("Could not find BP at index %d" % index)
        return { "message": "Not Found"}, 404
    
def get_movie_saved(index): #/movies/movie_ratings?index=X
    """ Get movie saved in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"]) # kafka
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving movie rating at index %d" % index)
    list_of_msg = []
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            if(msg['type'] == 'save'):
                list_of_msg.append(msg)
                print(msg)
            
        payload = list_of_msg[index]
        response = {
            "type": payload["type"],
            "datetime": payload["datetime"],
            "payload": json.loads(payload["payload"])
        }
        return response, 200
    except:
        logger.error("No more messages found")
        logger.error("Could not find BP at index %d" % index)
        return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app, resources={r"/*": {"origins": "*"}})
# CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)
