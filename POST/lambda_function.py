import boto3
import logging
import uuid
import json

from adt_parser import ADT_Messages

# Create logger, define formatter and the handler for the logger
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)

# Table name where to store the data
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('hl7_messages')
raw_table = dynamodb_client.Table('raw_hl7_messages')
RAW_PATH = "/message"

def lambda_handler(event, context):
    try:
        if event['rawPath'] == RAW_PATH:

            messageId = str(uuid.uuid4())
            message = event['body']
            LOG.info(f'processing the messageId: {messageId}')
            
            # Saving the raw message
            raw_data = {
                "messageId": messageId,
                "raw_message": message
            }
            raw_table.put_item(Item=raw_data)
            
            data = ADT_Messages.run(message)

            if data is not None:
                # The identifier attribute
                data['messageId'] = messageId
                # Saving the data to the DynamoDB
                table.put_item(Item=data)
                LOG.info(f'Message successfully stored DynamoDB with messageId: {messageId}')
                return {
                    "statusCode": 200,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({"messageId": messageId})
                }
            else:
                LOG.error(f'Error processing request')
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': 'Error: Data processing failed'
                }
        else:
            LOG.error('Invalid rawPath')
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': 'Invalid request path'
            }
    except KeyError as e:
        LOG.error(f'Missing key in event data: {e}')
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'Invalid event data format'
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