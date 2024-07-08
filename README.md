# news-aisummary

### process flow

Event Bridge --> Lambda(crawl webnews) |--> bedrock(summary)
                                       |
                                       |--> DynamoDB

### Prepration
1. Enable Bedrock Claude 
2. deploy on account
3. edit conf.yaml for configuration;

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "news-aisummary"
```

## Run with container image

docker run -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 --entrypoint  /aws-lambda/aws-lambda-rie news-aisummary:latest  /usr/bin/python -m awslambdaric app.handler

### Lambda Setup

#### Lambda preparation

```
sam init --runtime python3.12 --name {name}
```

#### Lambda local invoking testing

```
docker build -t news-aisummary .
docker run -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 --entrypoint /aws-lambda/aws-lambda-rie news-aisummary:latest  /usr/bin/python -m awslambdaric app.handler 
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

```

#### Lambda build && execution 

```
pip3 install -r requirements.txt 
sam build --use-container
sam deploy --guided
```


#### DynamoDB query

aws dynamodb query --table-name crypto_article_summaries --index-name website-date-index --key-condition-expression "website = :website AND publish_date BETWEEN :start_date AND :end_date" --expression-attribute-values '{":website": {"S":"https://news.bitcoin.com"}, ":start_date": {"S":"2024-07-08"}, ":end_date":{"S":"2024-07-08"}}'
