from ibmcloudenv import IBMCloudEnv
from watson_developer_cloud import AssistantV1

if IBMCloudEnv.getString('watson_conversation_apikey'):
    iam_url = 'https://iam.stage1.bluemix.net/identity/token' if 'staging' in IBMCloudEnv.getString('watson_conversation_iam_serviceid_crn') else 'https://iam.bluemix.net/identity/token'
    conversation = AssistantV1(
        url=IBMCloudEnv.getString('watson_conversation_url'),
        iam_api_key=IBMCloudEnv.getString('watson_conversation_apikey'),
        version='2018-02-16',
        iam_url=iam_url)
else:
    conversation = AssistantV1(
        username=IBMCloudEnv.getString('watson_conversation_username'),
        password=IBMCloudEnv.getString('watson_conversation_password'),
        version='2018-02-16')

def getService(app):
    return'watson-conversation', conversation

