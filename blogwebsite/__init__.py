#holds organization of the application like connecting blueprints, and everything together, etc.
#blogwebsite/__init__.py

from flask import Flask

app=Flask(__name__)

#registering core blueprint
from blogwebsite.core.views import core
app.register_blueprint(core)





