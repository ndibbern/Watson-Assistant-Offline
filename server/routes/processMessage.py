
import json
from flask import Flask
from flask import abort, session, request, redirect

app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')

from server.services import *

initServices(app) # Initialize Services

# The conversation instance from service_manager is already initialized
# with your supplied credentials
conversation = service_manager.get('watson-conversation')
# Each Conversation Service can have several workspaces associated with it.
# Find the workspace_id you want to connect this conversation instance with:
workspace_id = 'bdce14dd-65ce-4e50-91b9-dea4d7445393'

# Add new data to the collection
@app.route('/message', methods=['GET'])
def sendMessage():
	msg = request.args.get('msg')
	lat = request.args.get('lat')
	longi = request.args.get('longi')
	uuid = request.args.get('uuid')
	response = conversation.message(workspace_id=workspace_id, input={
		'text': msg
	})
	print(response)
	return response


def writeMessage():
   error = None
    
   return 


@app.route('/panic', methods=['POST'])
def login():
   error = None
   if request.method == 'POST':
       if valid_login(request.form['username'],
                      request.form['password']):
           return log_the_user_in(request.form['username'])
       else:
           error = 'Invalid username/password'
   # the code below is executed if the request method
   # was GET or the credentials were invalid
   return render_template('login.html', error=error)

