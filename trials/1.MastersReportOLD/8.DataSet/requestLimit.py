import requests

headers = {
    'Authorization': 'token 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',
}

response = requests.get('https://api.github.com/rate_limit', headers=headers)

print(response.text)