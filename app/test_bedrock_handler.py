from calendar import c
import unittest
from unittest.mock import patch, MagicMock
import boto3
from bedrock_handler import BedrockHandler

class TestBedrockHandler(unittest.TestCase):
    def setUp(self):
        self.region = 'us-west-2'
        self.model = 'anthropic.claude-3-sonnet-20240229-v1:0'
        self.handler = BedrockHandler(self.region, self.model)

    @patch('boto3.client')
    def test_invoke_bedrock_runtime(self, mock_client):
        # Arrange
        system_prompt = '''
You are an AI assistant with rich crypto knowledge. You are trained to summarize news in a few sentences or concise paragraphs.
Guidelines:
1. The summary must be based on the input content.
2. The summary should include all the important information from the input content.
3. The summary should be concise, informative, and easy to understand.
4. The summary must be not more than 200 words.
5. The summary must not include any preamble or title.
'''
        user_prompt = "Your task is to provide summary for input content. The input content is within <content></content> tags.\n\n<content>{content}</content>"
        input_content = '''
Hashnote, a digital asset manager, has announced a partnership with crypto custody firm Anchorage Digital to offer secure investment returns for institutional clients. This collaboration integrates Anchorage’s custody services with Hashnote’s derivative strategies.

Hashnote and Anchorage Join Forces to Reduce Counterparty Risk for Institutional Investors Investing in Crypto
On Monday, Hashnote stated that the “collaboration integrates Anchorage Digital’s secure custody services with Hashnote’s advanced derivative strategies, providing a secure environment for yield generation.” According to the firm, by keeping assets in Anchorage’s secure custody and utilizing Hashnote’s strategic expertise, the collaboration aims to reduce counterparty risk in order to provide “peace of mind” to institutional investors.

Hashnote, a regulated asset management platform, specializes in providing institutional-grade digital asset investment solutions. It offers a range of investment options, including cash management through interest-bearing products, crypto yield and hedging strategies, and long token funds. The platform is registered with the U.S. Commodity Futures Trading Commission (CFTC) and the Cayman Islands Monetary Authority (CIMA).

Anchorage Digital, the federally chartered cryptocurrency bank in the United States, provides integrated digital asset financial services and infrastructure solutions specifically designed for institutions. Anchorage’s services include the custody of digital assets, staking, governance participation, 24/7 trading, and lending. The company employs biometric authentication, behavioral analytics, and hardware security modules to safeguard digital assets.


“This partnership solves a significant problem for institutions seeking to generate yields on their crypto assets without compromising security,” Hashnote wrote on the social media platform X. The onchain digital asset manager backed by Cumberland and DRW recently formed a partnership with Paxos in late March. At that time, Hashnote announced that this initiative aimed to meet the demands of market makers, traders, and institutions by incorporating Paypal USD (PYUSD) into Hashnote’s yield-bearing USYC.

Nathan McCauley, the CEO and co-founder of Anchorage, explained that institutions are looking for multiple methods to engage with the crypto economy. “Institutions seek a variety of ways to participate in digital assets,” McCauley said on Monday. “The driving, integral aspect to their participation is safety and security, a hallmark of Anchorage Digital. That’s why we’re pleased to partner with Hashnote in the launch of its crypto derivatives program.”
'''
        expected_summary = "Summary of the long text."

        mock_response = {
            "output": {
                "content": [
                    {"text": expected_summary}
                ]
            }
        }
        mock_client.return_value.converse.return_value = mock_response
        user_prompt_final = user_prompt.format(content=input_content)
        # print(user_prompt_final)
        # Act
        summary = self.handler.invoke_bedrock_runtime(system_prompt, user_prompt_final)
        print(summary)

        # Assert
        # self.assertEqual(summary, expected_summary)
        # mock_client.return_value.converse.assert_called_once()

if __name__ == '__main__':
    unittest.main()
