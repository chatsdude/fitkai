from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

def create_app():
    '''DB_USERNAME = chaiasht
      DB_PASSWORD = cva12345678
      HOST = chaiasht.mysql.pythonanywhere-services.com
      DB_PORT = 3306
      DB_NAME = fitki
    username = os.environ.get('DB_USERNAME')
    password = quote_plus(os.environ.get('DB_PASSWORD'))
    host = os.environ.get('HOST')
    port = os.environ.get('DB_PORT')
    dbname = os.environ.get('DB_NAME')'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://chaiasht:cva123456@chaiasht.mysql.pythonanywhere-services.com/chaiasht$fitki'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "jasjkjajkjabjbsjxjaxkjsxkjbjkxbjkx"

    return app

app = create_app()
db = SQLAlchemy(app)

import routes

if __name__=='__main__':
    app.run()