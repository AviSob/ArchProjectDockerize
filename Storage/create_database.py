import mysql.connector
import yaml
import logging
import logging.config

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

# prepare config vars
user=app_config['datastore']['user']
password=app_config['datastore']['password']
hostname=app_config['datastore']['hostname']
port=app_config['datastore']['port']
db=app_config['datastore']['db']

config = {
    'user': user,
    'password': password,
    'host': hostname,
    'port': port,
    'database': db
}

logger.setLevel(logging.INFO)
logger.info(f'Connecting to DB. Hostname: {hostname}, Port: {port}')

db_conn = mysql.connector.connect(**config)

db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE DATABASE IF NOT EXISTS movies; 
          ''')

db_cursor.execute('''
          CREATE TABLE IF NOT EXISTS movies.movie_ratings
          (id INT NOT NULL AUTO_INCREMENT,
           trace_id VARCHAR(20) NOT NULL,
           movie_id VARCHAR(250) NOT NULL,
           movie_name VARCHAR(250) NOT NULL,
           rating INTEGER NOT NULL,
           review VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT id PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE IF NOT EXISTS movies.saved_movies
          (id INT NOT NULL AUTO_INCREMENT,
           trace_id VARCHAR(20) NOT NULL,
           movie_id VARCHAR(150) NOT NULL,
           notes VARCHAR(150) NOT NULL,
           save_date TEXT NOT NULL,
           user_id INTEGER NOT NULL,
           season INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT id PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()