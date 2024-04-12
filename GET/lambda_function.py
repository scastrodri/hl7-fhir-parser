import logging
import boto3
import json

from fhir_parser import FHIR_message

# Create logger, define formatter and the handler for the logger
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)

# Table name where to the data is stored
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('hl7_messages')
RAW_PATH = "/messageId"

def lambda_handler(event, context):
    """
    Retrieves, invokes the parser fhir parser data and return the message in FHIR format for the given messageId.
    """
    try:
        if event['rawPath'] != RAW_PATH:
            LOG.error('Invalid rawPath')
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': 'Invalid request path'
            }
            
        messageId = event['queryStringParameters']['messageId']
        LOG.info(f'Retrieving data for messageId: {messageId}')
        
        try:
            # Retrieve data from the DynamoDB table
            table_item = table.get_item(Key={'messageId': messageId})
            table_item = table_item.get('Item', {})
            LOG.info(f'Data retrieved for the messageId: {messageId}')
        
        except boto3.exceptions.DynamoDBError as e:
            LOG.error(f'Error accessing DynamoDB: {e}')
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': 'Invalid request messageId'
            }
        
        fhir_object = FHIR_message.run(table_item)
        LOG.info(f'The fhir_object is: {fhir_object}')
        
        if fhir_object is not None:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(fhir_object)
            }
        else:
            LOG.error(f'item not parsed')
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': 'Error: Data processing failed'
            }
    except Exception as e:
        LOG.error(f'Error processing request: {e}')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'Error: Internal server error'
        }