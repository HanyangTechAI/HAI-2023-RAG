import requests
import json

url = "https://api.llm.girinman.kr/generate_stream"


def createTokens(input):
    data = {"inputs": input, } # "parameters": {"max_new_tokens": 20}
    response = requests.post(url=url, json=data)

    event = {}
    list = []
    for token in response.text.splitlines():
            if(token):
                # Data line.
                key, value = token.split(':', 1)
                print()
                if key == 'data':
                    value = json.loads(value)['token'].get('text')
                    if(value != '</s>'):
                        list.append(value)

    return list




# tokens = createTokens("My name is Olivier and I")
# for token in tokens:
#     print(token)


# res = requests.post(url=url, json=data)
# tokens = res.text.splitlines()

# for token in tokens:
#     if token == '':
#         continue

#     tmp = token[5:]

#     obj = json.loads(tmp)
#     print(obj['token']['text'])
