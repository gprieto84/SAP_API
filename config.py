import os
import connexion
import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from configparser import ConfigParser
from pyrfc import Connection
import pyodbc

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Getting SAP config parameters
config = ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'config', 'sapnwrfc.cfg')))
params_connection = config._sections['connection']

# Stablishing the SAP connection
sap_conn = Connection(**params_connection)

# Build the MSSQL ULR for SqlAlchemy
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=Cobartram016\TRABDSP10;DATABASE=BDVIAJE2;UID=tra-sap;PWD=12345.TS;')
mssql_url = "mssql+pyodbc:///?odbc_connect=%s" % params

engine = create_engine(mssql_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = mssql_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)