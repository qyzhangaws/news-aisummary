from operator import is_
import os 

import conf
import scrape
import utils
import bedrock_handler
import datastore

def handler(event, context):
    # load config
    main_dir = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(main_dir, "conf.yaml")
    if not os.path.exists(conf_file):
        print("conf file not found: %s" % conf_file)
        exit(1)

    conf_parser = conf.ConfParser(conf_file)
    conf_parser.parse_config()
    bedrock_conf = conf_parser.get_bedrock_config()
    dynamodb_conf = conf_parser.get_dynamodb_config()
    websites_conf = conf_parser.get_websites_config()

    print(bedrock_conf)
    print(dynamodb_conf)
    print(websites_conf)   

    bedrock_handler_obj = bedrock_handler.BedrockHandler(
        region = bedrock_conf["region"],
        model = bedrock_conf["model"]
    )

    # ensure dynamodb table exists
    dynamodb_handler = datastore.DynamoDBManager(
        region = dynamodb_conf["region"],
        table_name = dynamodb_conf["table"]
    )
    if not dynamodb_handler.is_table_exists():
        dynamodb_handler.create_table()

    for website_item in websites_conf:
        scrape_obj =  utils.create_obj_from_class_name(
           website_item["scrape_class"], 
           "scrape", 
           website_item["base_url"]
        )  
        for cate in website_item["categories"]:
            cate_article_links = scrape_obj.extract_links(cate["name"], cate["sublink"])
            print(cate_article_links)
            
            for cate_link in cate_article_links:
                raw_article_obj = scrape_obj.scrape_article(cate_link)

                # to invoke bedrock handler to summary document
                content_summary = bedrock_handler_obj.invoke_bedrock_runtime(
                    system_prompt = bedrock_conf["system_prompt"],
                    user_prompt = bedrock_conf["user_prompt"].format(content=raw_article_obj["content"])
                )

                # store into dynamodb
                dynamodb_handler.put_item(
                    link = cate_link["link"],
                    title = raw_article_obj["title"],
                    content = content_summary,
                    author = raw_article_obj['author'],
                    publish_date = raw_article_obj["date"],
                    website = website_item["base_url"] 
                )
        utils.cleanup_tmp_space()

if __name__ == "__main__":
    handler(None, None)