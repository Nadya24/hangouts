import json
import re
from pprint import pprint
import operator

with open('Hangouts.json') as data_file:
    data = json.load(data_file)

messages = {}
dict_gaia_id = {}
all_words = {}
counts = {}

for elem in data['conversation_state']:
    partners = elem['conversation_state']['conversation']['participant_data']
    print(partners)
    for element in partners:
        if 'fallback_name' in element:
            dict_gaia_id[element['fallback_name']] = element['id']['gaia_id']
            messages[element['fallback_name']] = []
            counts[element['fallback_name']] = {}
            all_words[element['fallback_name']] = []

# Sprint(dict_gaia_id)
conv = data['conversation_state']
for con in conv:
    events = con['conversation_state']['event']
    for el in events:
        gaia_id = el['sender_id']['gaia_id']
        if 'chat_message' in el:
            if 'segment' in el['chat_message']['message_content']:
                segments = el['chat_message']['message_content']['segment']
                for seg in segments:
                    if seg['type'] == 'TEXT':
                        for name,el_gaia_id in dict_gaia_id.items():
                            if gaia_id == el_gaia_id:
                                if 'text' in seg:
                                    messages[name].append(seg['text'])
                    else:
                        continue
            else:
                continue

def getWords(text):
    return re.compile('\w+').findall(text)

for key in messages:
    for mes in messages[key]:
        all_words[key].extend(getWords(mes))

for key in all_words:
    for word in all_words[key]:
        if word in counts[key]:
            counts[key][word] += 1
        else:
            counts[key][word] = 1
    sorted_x = sorted(counts[key].items(), key=operator.itemgetter(1))
    print('-------------')
    print(key+':')
    print(sorted_x[-10:])
