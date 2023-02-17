import os
from flask import Blueprint

routes = Blueprint("routes", __name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@routes.route("/")
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return os.getenv("STRING")
