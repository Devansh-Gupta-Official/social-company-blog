#holds organization of the application like connecting blueprints, and everything together, etc.
#blogwebsite/__init__.py

from flask import Flask

app=Flask(__name__)

#registering core blueprint
from blogwebsite.core.views import core
#registering error_pages blueprint
from blogwebsite.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(error_pages)





