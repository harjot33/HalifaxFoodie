import json
import boto3

client = boto3.client('dynamodb')
result = {}
intent = ""
orderNumber = ""

def lambda_handler(event, context):
    print((event))
    intent = event['currentIntent']['name']
    print('the intent is : ', intent)
    if intent == 'TrackOrder':
        orderNumber = event['currentIntent']['slots']['OrderID']
        print('Order Number is : ', orderNumber)
        orderStatusEnquiry(orderNumber)
        return result


# Method to Fetch the order status from DynamoDB by giving the Order ID as paramater
def orderStatusEnquiry(orderNumber):
    response = client.get_item(
        TableName='Orders',
        Key={
            'OrderID': {
                'S': orderNumber,
            }
        })
    print('response is: ', response)
    # Declaring a key to verify the response
    key = 'Item'
    # Storing the boolean value wether key present or not
    value = key in response.keys()
    if value:
        OrderStatus = response['Item']['OrderStatus']['S']
        message = 'Hello Mansi, Your order is in ', OrderStatus, ' status'
        msg = ''.join(message)
        print(msg)
        global result
        # Result to lex bot
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                },
            }
        }
        return result
    else:
        message = "Sorry! I can't find your details in our records. Please contact our support center."
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                },
            }
        }
        return result