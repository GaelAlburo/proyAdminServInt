from flask import Flask
from flask_cors import CORS
from ftp_service.service import FTPService
from routes.routes import Routes


app = Flask(__name__) # Initialize Flask app
CORS(app) # Allow all domains to access the API

ftp_conn = FTPService() # Initialize FTP service

routes = Routes(ftp_conn) # Initialize routes with FTP service
app.register_blueprint(routes) # Register the routes blueprint


if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode