import requests
#xis996HlgMjutU9KCf50F2D4154140BfA642C6464aC6480b
model = 'gpt-3.5-turbo'
#model = 'chatty-gpt-4'
url = 'https://api.chatanywhere.cn/v1'

#https://neuroapi.host/v1
api_key = 'sk-lVyIGFN0e4Il91M6VmIVEZbxEpuKoMMfUfRzT8IiKn8XzpMH'
#api_key = 'sk-lVyIGFN0e4Il91M6VmIVEZbxEpuKoMMfUfRzT8IiKn8XzpMH'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}
messages = []

payload = {
        'model': model,
        'messages': messages,
    }

def prompt(msg):
    messages.append({'role': 'user', 'content': msg})
    response = requests.post(url+'/chat/completions', json=payload, headers=headers)
    answer = ''
    if response.status_code == 200:
        data = response.json()
        answer = data['choices'][0]['message']['content']
        messages.clear()
        return answer
    else: return "произошла ошибка "+str(response.status_code)