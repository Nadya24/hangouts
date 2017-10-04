import json
import re
from pprint import pprint
import operator

with open('Hangouts.json') as data_file:
    data = json.load(data_file)

messages = {
    'nadya': [],
    'alexandr': []

    }

events = data['conversation_state'][0]['conversation_state']['event']
#print(events)
for el in events:
    gaia_id = el['sender_id']['gaia_id']
   # print(gaia_id)
#print(data['conversation_state']['conversation_state']['event'][0]['chat_message']['message_content']['segment'][0]['type'])
#print(data['conversation_state']['conversation_state']['event'][0]['chat_message']['message_content']['segment'][0]['text'])
    if 'chat_message' in el:
        if 'segment' in el['chat_message']['message_content']:
            if el['chat_message']['message_content']['segment'][0]['type'] == 'TEXT':
                #Alex
                if gaia_id=='116003021892114994463':
                    messages['alexandr'].append(el['chat_message']['message_content']['segment'][0]['text'])

                #Nadya
                if gaia_id=='112073426858751033150':
                    messages['nadya'].append(el['chat_message']['message_content']['segment'][0]['text'])
            else:
                continue
        else:
            continue

def getWords(text):
    return re.compile('\w+').findall(text)
all_words = []
for mes in messages['alexandr']:
    all_words.extend(getWords(mes))
print(all_words)
counts = {}
for word in all_words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
sorted_x = sorted(counts.items(), key=operator.itemgetter(1))
print(sorted_x[-10:])

