#holds organization of the application like connecting blueprints, and everything together, etc.
#blogwebsite/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app=Flask(__name__)

#setting up the database
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)
#setup context **IMPORTANT**
app.app_context().push()



#registering core blueprint
from blogwebsite.core.views import core
#registering error_pages blueprint
from blogwebsite.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(error_pages)






