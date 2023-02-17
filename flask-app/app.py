# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
from flask import Flask
import routes

# Flask constructor takes the name of
# current module (__name__) as argument.
def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes.routes)
    return app

# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
