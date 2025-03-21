from dotenv import dotenv_values
import os
settings = dotenv_values(".env")

class Config:
    
    def __init__(self, db_host="",db_database="", db_user="", db_password="") -> None:
        
        self.db_host=settings['DB_HOST']
        self.db_database=settings['DB_DATABASE']
        self.db_user=settings['DB_USER']
        self.db_password=settings['DB_PASSWORD']

        self.smtp_host=os.getenv('SMTP_HOST')
        self.smtp_port=os.getenv('SMTP_PORT')
        self.smtp_user=os.getenv('SMTP_USER')
        self.smtp_password=os.getenv('SMTP_PASSWORD')
        self.sender_mail=os.getenv('SENDER_MAIL')
        

    def getPathToPrit(self):
        return self.to_print
    
    def getPathPrinted(self):
        return self.printed
    
    def getPathTemplate(self):
        return self.template
    
config = Config( 
            settings['DB_HOST'],
            settings['DB_DATABASE'],
            settings['DB_USER'],
            settings['DB_PASSWORD'])

        