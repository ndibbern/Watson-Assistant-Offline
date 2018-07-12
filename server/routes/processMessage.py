import json
import datetime
from server import app
from flask import Flask
from flask import abort, session, request, redirect
from server.services import *
from bson.json_util import dumps

initServices(app) # Initialize Services

# The conversation instance from service_manager is already initialized
# with your supplied credentials
conversation = service_manager.get('watson-conversation')
# Each Conversation Service can have several workspaces associated with it.
# Find the workspace_id you want to connect this conversation instance with:
workspace_id = '6ee41931-3476-487d-a9e9-857dbc718cb8'

client = service_manager.get('mongodb')
db = client.loc_database
collection = db.loc_collection

# Add new data to the collection
@app.route('/message')
def sendMessage():
  msg = request.args.get('msg')
  lat = request.args.get('lat')
  longi = request.args.get('long')
  uuid = request.args.get('uuid')
  response = conversation.message(workspace_id=workspace_id, input={
	 'text': msg
  })
  json_str = json.dumps(response)
  resp = json.loads(json_str)
  response = resp['output']['text'][0]
  return uuid + "|" + response


@app.route('/panic', methods=['POST'])
def panic():
  lat = request.args.get('lat')
  longi = request.args.get('long')
  uuid = request.args.get('uuid')
  ts = datetime.datetime.now()

  data = {
    "latitude": lat,
    "longitude": longi,
    "timestamp": ts,
    "uuid": uuid
  }

  entry = collection.find_one({'uuid': uuid})
  if entry:
    collection.find_one_and_update({'uuid': uuid}, {'$set': {'latitude': lat, "longitude": longi, "timestamp": ts}})
  else:
    collection.insert_one(data)

  return data


@app.route('/locations')
def getLocs():
  return dumps(collection.find({}, {'_id': 0}))

@app.route('/update')
def updateAssistant():
  response = assistant.update_dialog_node(
    workspace_id = '9978a49e-ea89-4493-b33d-82298d3db20d',
    dialog_node = 'greeting',
    new_dialog_node = 'greeting',
    new_output = {
        'text': 'Hello! What can I do for you?'
    }
  )
  
