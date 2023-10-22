import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from movie_rating import MovieRating
from saved_movies import SavedMovies
import datetime
import pymysql
import yaml
import logging
import logging.config
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


# load config files
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

# prepare config vars
user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

# db engine
DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
print(DB_ENGINE)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# =============== GET
def get_rated_movies(timestamp):
    """ Gets movies rated after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(MovieRating).filter(MovieRating.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()
    logger.info(f"Query for movies rated after {timestamp} returns {len(results_list)} results")

    return results_list, 200


def get_saved_movies(timestamp):
    """ Gets movies saved after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(SavedMovies).filter(SavedMovies.date_created >= timestamp_datetime)
    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()
    logger.info(f"Query for movies saved after {timestamp} returns {len(results_list)} results")

    return results_list, 200

# =============== KAFKA
def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)
    print(consumer)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]
        body = json.loads(payload)
        # print(">>>>>>>>>>>>>>>")
        # print(body)
        # print(">>>>>>>>>>>>>>>")

        if msg["type"] == "rate":
            logger.info(f'Connecting to DB. Hostname: {hostname}, Port: {port}')
            session = DB_SESSION()

            mr = MovieRating(body['movie_id'],
                             body['trace_id'],
                             body['movie_name'],
                             body['rating'],
                             body['review'])
            
            session.add(mr)
            session.commit()
            session.close()
            logger.debug(f'Stored event rate request with a trace id of {body["trace_id"]}')

        elif msg["type"] == "save":
            logger.info(f'Connecting to DB. Hostname: {hostname}, Port: {port}')
            session = DB_SESSION()

            rs = SavedMovies(body['movie_id'],
                             body['trace_id'],
                             body['notes'],
                             datetime.datetime.strptime(
                                 body['save_date'], "%Y-%m-%d"),
                             body['user_id'],
                             body['season'])

            session.add(rs)

            session.commit()
            session.close()
            logger.debug(f'Stored event save request with a trace id of {body["trace_id"]}')

        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
