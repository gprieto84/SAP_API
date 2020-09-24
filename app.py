from flask import Flask
import config

import connexion

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    return "SAP API testing v001"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', port=5000, debug=True)