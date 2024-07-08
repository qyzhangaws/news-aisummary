import boto3
from datetime import datetime

class DynamoDBManager:
    def __init__(self, region, table_name):
        self.dynamodb_client = boto3.client('dynamodb', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table_name = table_name

    def create_table(self, ):
        try:
            table = self.dynamodb_client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'link',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'publish_date',
                        'KeyType': "RANGE" # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'link',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'publish_date',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'website',
                        'AttributeType': 'S'
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'website-date-index',
                        'KeySchema': [
                            {
                                'AttributeName': 'website',
                                'KeyType': 'HASH'
                            },
                            {
                                'AttributeName': 'publish_date',
                                'KeyType': 'RANGE'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        }
                    }
                ],
                BillingMode='PAY_PER_REQUEST',
            )

            self.dynamodb_client.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f"Table '{self.table_name}' created successfully.")
            return table
        except Exception as e:
            print(f"Error creating table: {e}")
            return None
        
    def is_table_exists(self,):
        try:
            self.dynamodb_client.describe_table(TableName=self.table_name)
            return True
        except:
            return False

    def put_item(self, link, title, content, author, publish_date, website):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(
                Item={
                    'link': link,
                    'title': title,
                    'content': content,
                    'author': author,
                    'publish_date': publish_date,
                    'website': website
                }
            )
            print(f"Item added successfully: {link}")
        except Exception as e:
            print(f"Error adding item: {e}")
    
    def delete_item(self, link):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.delete_item(
                Key={
                    'link': link
                }
            )
            print(f"Item deleted successfully: {link}")
        except Exception as e:
            print(f"Error deleting item: {e}")

    def query_items_between_dates(self, website, start_date, end_date):
        try:
            table = self.dynamodb.Table(self.table_name)
            start_date_str = start_date.isoformat()
            end_date_str = end_date.isoformat()
            print(start_date_str, end_date_str)

            key_condition_expression = 'website = :website AND publish_date BETWEEN :start_date AND :end_date'
            expression_attribute_values = {
                ':website': website,
                ':start_date': start_date_str,
                ':end_date': end_date_str
            }
            response = table.query(
                IndexName='website-date-index',
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ScanIndexForward=True
            )

            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.query(
                    IndexName='date-index',
                    KeyConditionExpression=key_condition_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                    ExclusiveStartKey=response['LastEvaluatedKey'],
                    ScanIndexForward=True
                )
                items.extend(response['Items'])

            return items

        except Exception as e:
            print(f"Error querying items between dates: {e}")
            return []



if __name__ == "__main__":
    # Example usage
    dynamodb_manager = DynamoDBManager('us-west-2', 'test-website') # 'crypto_article_summaries')
    if not dynamodb_manager.is_table_exists():
        dynamodb_manager.create_table()

    dynamodb_manager.put_item(
        link='https://example.com/article2',
        title='Article 2',
        content='This is the content of article 2.',
        author='John Doe',
        publish_date='2024-07-02',
        website='example.com'
    )

    # Query items between dates
    start_date = datetime.fromisoformat('2024-07-01').date()
    end_date = datetime.fromisoformat('2024-07-03').date()
    items = dynamodb_manager.query_items_between_dates("example.com", start_date, end_date)
    print(len(items))
    print(items)
