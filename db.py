import mysql.connector
import config as setting
import traceback
from sqlalchemy import create_engine


class DB:
    def __init__(self):
        self.server = setting.config.db_host
        self.db = setting.config.db_database
        self.user = setting.config.db_user
        self.password  = setting.config.db_password
        try:

            conn_str = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.server}/{self.db}' #f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
            engine = create_engine(conn_str)	
            print ('CONECTADO')
            self.engine = engine
        
        except Exception as e:
            print(traceback.format_exc())
            print(e)
    
    
    