import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    print ("Importing boto3 class for transfer service")
    client = boto3.client('transfer')

    # Get Transfer server id and server state
    transferserverid = event["transferserverid"]
    instanceState = event["instanceState"]

    print ("Transfer Server ID :" + transferserverid)
    
    # Get Transfer Server Status
    status = describe_server(transferserverid, client, instanceState)
    print ("Transfer Server Current State : " + status['Server']['State'])

    # Start Transfer Server
    if instanceState == "on":
        # Start Transfer Server
        start_server(transferserverid, client, instanceState)
        # Get Transfer Server Status
        start_status = describe_server(transferserverid, client, instanceState)
        print ("Transfer Server state after startup : " + start_status['Server']['State'])
    
    # Stop Transfer Server
    if instanceState == "off":
        # Stop Transfer Server
        stop_server(transferserverid, client, instanceState)
        # Get Transfer Server Status
        stop_status = describe_server(transferserverid, client, instanceState)
        print ("Transfer Server state after startup : " + stop_status['Server']['State'])
    
    # End
    return "Script execution completed. See Cloudwatch logs for complete output"


def describe_server(serverid, serverclient, serverstate):
    print ('Trying to describe Transfer Server :' + serverid)
    try:
        response = serverclient.describe_server(
            ServerId=serverid
        )
        return response
    except ClientError as e:
        print(e)

def stop_server(serverid, serverclient, serverstate):
    print ('Trying to stop Transfer Server :' + serverid)
    try:
        response = serverclient.stop_server(
            ServerId=serverid
        )
        return response
    except ClientError as e:
        print(e)

def start_server(serverid, serverclient, serverstate):
    print ('Trying to start Transfer Server :' + serverid)
    try:
        response = serverclient.start_server(
            ServerId=serverid
        )
        return response
    except ClientError as e:
        print(e)