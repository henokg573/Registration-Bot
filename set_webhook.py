import requests

API_KEY = '7759515826:AAEjjGhr8pM7WAJBWP8JG1F-wu85nJck338'
webhook_url = 'https://easygate-registration-bot-34qv.onrender.com/webhook'

response = requests.post(
    f'https://api.telegram.org/bot7759515826:AAEjjGhr8pM7WAJBWP8JG1F-wu85nJck338/setWebhook',
    data={'url': webhook_url}
)

if response.status_code == 200:
    print('Webhook has been set successfully!')
else:
    print(f'Failed to set webhook. Error: {response.text}')
