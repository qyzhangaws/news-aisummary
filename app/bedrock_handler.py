from urllib import response
import boto3

class BedrockHandler:
    def __init__(self, region, model):
        self.region = region
        self.model = model 
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=region)

    def invoke_bedrock_runtime(self, system_prompt, user_prompt):
        """
        Invokes the Bedrock Claude Sonnet 3.0 API to generate a summary for the given input content using AWS Bedrock.
        
        Args:
            input_content (str): The content for which a summary is required.
            
        Returns:
            str: The summary generated by the Bedrock Claude Sonnet 3.0 API.
        """
        
        response = self.bedrock_client.converse(
            modelId=self.model,
            messages=[
                {
                    "role": 'user',
                    'content': [
                        {
                            "text": user_prompt
                        }
                    ]
                }
            ],
            system = [
                {
                    'text': system_prompt
                }
            ],
            inferenceConfig={
                "temperature": 0.4,
                "topP": 0.8
            },
        )
        
        try:
            summary_content = ""
            resp_message_content = response["output"]["message"]["content"]
            for item in resp_message_content:
                summary_content+=item["text"] 
            return summary_content
        except Exception as e:
            print(f"Error: {e}")
            return None