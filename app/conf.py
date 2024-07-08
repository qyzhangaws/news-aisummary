import yaml

class ConfParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()
        self.bedrock_config = None
        self.dynamodb_config = None
        self.websites_config = None

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
        return config_data

    def parse_config(self):
        self.get_bedrock_config()
        self.get_dynamodb_config()
        self.get_websites_config()
        parsed_config = {
            'bedrock': self.bedrock_config,
            'websites': self.websites_config
        }
        return parsed_config

    # parse bedrock config
    def get_bedrock_config(self):
        if self.bedrock_config is not None:
            return self.bedrock_config

        bedrock_config_data = self.config_data.get('conf', {}).get('bedrock', {})    
        parsed_config = {
            'region': bedrock_config_data.get('region'),
            'model': bedrock_config_data.get('model'),
            'system_prompt': bedrock_config_data.get('system_prompt'),
            'user_prompt': bedrock_config_data.get('user_prompt'),
            'stop_sequences': bedrock_config_data.get('stop_sequences', []),
            'max_tokens': bedrock_config_data.get('max_tokens'),
            'temperature': bedrock_config_data.get('temperature'),
            'top_p': bedrock_config_data.get('top_p')
        }
        self.bedrock_config = parsed_config
        return parsed_config

    # parse dynamodb config
    def get_dynamodb_config(self):
        if self.dynamodb_config is not None:
            return self.dynamodb_config

        dynamodb_config_data = self.config_data.get('conf', {}).get('dynamodb', {})
        parsed_config = {
            'table': dynamodb_config_data.get('table'),
            'region': dynamodb_config_data.get('region'),
        }
        self.dynamodb_config = parsed_config
        return self.dynamodb_config

    # parse websites config
    def get_websites_config(self):
        if self.websites_config is not None:
            return self.websites_config
    
        websites_config_data = self.config_data.get('conf', {}).get('websites', [])
        websites_config = []
        for item in websites_config_data:
            websites_config.append(self._parse_website_config(item))

        self.websites_config = websites_config 
        return self.websites_config

    # internal parse website config   
    def _parse_website_config(self, website_config):
        categories_data = website_config.get('categories', [])
        categories_config = []
        for cate in categories_data:
            categories_config.append(self._parse_website_category(cate))
        return {
            'base_url': website_config.get('base_url', ''),
            'scrape_class': website_config.get('scrape_class', ''),
            'categories': categories_config
        }

    # internal parse website categories config
    def _parse_website_category(self, website_category):
        return {
            'name': website_category.get('name', ''),
            'sublink': website_category.get('sublink', ''),
        }

