import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

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

db_conn = mysql.connector.connect(**config)

db_cursor = db_conn.cursor()
db_cursor.execute('''
                  DROP TABLE saved_movies, movie_ratings
                  ''')

db_conn.commit()
db_conn.close()