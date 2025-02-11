import connexion
from connexion import NoContent
import json
import requests
import datetime
import yaml
import logging
import logging.config
from pykafka import KafkaClient

# load config files
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

# configs for kafka
kafka_server=app_config['events']['hostname']
kafka_port=app_config['events']['port']
kafka_topic=app_config['events']['topic']

# For logging
def log_data(event, choice):
    header = {"Content-Type":"application/json"}
    trace_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    event["trace_id"] = trace_id
    body = json.dumps(event)

    logger.debug(f'Received event {choice} request with a trace id of {trace_id}')

    # get kafka ready and sent message
    client = KafkaClient(hosts=f'{kafka_server}:{kafka_port}')
    topic = client.topics[str.encode(kafka_topic)]
    producer = topic.get_sync_producer()

    # build message
    msg = { "type": f"{choice}", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "payload": body }

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8')) 
    
    logger.debug(f'Returned event {choice} response id {trace_id} with status 201')
    
    return NoContent, 201
 
# Your functions here
def rate(body): #/movies/rate
    res=log_data(body, "rate")
    return NoContent, res[1]

def save_movie(body): #/movies/save
    res=log_data(body, "save")
    return NoContent, res[1]

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
