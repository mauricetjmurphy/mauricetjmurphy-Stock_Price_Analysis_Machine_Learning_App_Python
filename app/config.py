from dotenv import load_dotenv
import os

load_dotenv()

#Config object to store to staore all config settings for the app
class Config(object):

    # Set Flask config variables
    FLASK_ENV = 'development'
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Specifing the URI 
    MONGODB_SETTINGS = {
        "db": "Stock_Analyser"
        }
    MONGO_URI = os.getenv('MONGO_URI')