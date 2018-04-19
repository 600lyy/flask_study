from peewee import PostgresqlDatabase
import logging


DB_NAME = 'postgres'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = '127.0.0.1'

DB = PostgresqlDatabase(
    DB_NAME, user=USERNAME, password=PASSWORD, host=HOST, 
    autocommit=True, autorollback=True
)

SETTINGS = {
    'DB' : DB,
    'LOGGING_LEVEL' : logging.INFO,
    'DEBUG' : True,
}