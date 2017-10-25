import json
import re
from pprint import pprint
import operator

with open('Hangouts.json') as data_file:
    data = json.load(data_file)

# R: захардконены имена, они должны доставаться из самого файла.
#    См. participant_data и fallback_name
messages = {}
dict_gaia_id = {}
all_words = {}
counts = {}

# R: [0] - почти наверняка ошибка, т.к. если это массив,
#    то следует смотреть все элементы, а не только первый.
for elem in data['conversation_state']:
    partners = elem['conversation_state']['conversation']['participant_data']
    print(partners)
    for element in partners:
        if 'fallback_name' in element:
            dict_gaia_id[element['fallback_name']] = element['id']['gaia_id']
            messages[element['fallback_name']] = []
            counts[element['fallback_name']] = {}
            all_words[element['fallback_name']] = []
        # if element['fallback_name'] == 'demetranadya93@gmail.com':
        #     gaia_my_id = element['id']['gaia_id']

# Sprint(dict_gaia_id)
conv = data['conversation_state']
for con in conv:
    events = con['conversation_state']['event']
    #print(events)
    for el in events:
        gaia_id = el['sender_id']['gaia_id']
        # R: отладочные принты следует убирать перед выпуском кода
       # print(gaia_id)
    #print(data['conversation_state']['conversation_state']['event'][0]['chat_message']['message_content']['segment'][0]['type'])
    #print(data['conversation_state']['conversation_state']['event'][0]['chat_message']['message_content']['segment'][0]['text'])
        # R: лучше использовать быстрый выход, а затем защищённый код,
        #    так мы избегаем увеличения степени вложенности и висящих continue:
        #
        #       if 'chat_message' not in el:
        #           continue
        #
        if 'chat_message' in el:
            if 'segment' in el['chat_message']['message_content']:
                # R: супердлинные выборки затрудняют написание и чтение кода,
                #    используй переменные:
                #
                #        message_content = el['chat_message']['message_content']
                #        if 'segment' in message_content:
                #           segment = message_content['segment']
                #           if segment[0]['type'] == 'TEXT':
                #               ...
                #               messages.append(segment['text'])
                # R: [0] - ошибка, мы игнорируем кучу сообщений
                segments = el['chat_message']['message_content']['segment']
                for seg in segments:
                    if seg['type'] == 'TEXT':
                        # R: захардкоженные gaia_id - это очень плохо,
                        #    не будет работать на других файлах, с другими авторами сообщений.
                        #    Нужно собирать все сообщения вне зависимости от того, какой gaia_id,
                        #    просто группировать по нему.
                        #
                        #    Разруливать кому какой gaia_id принадлежит можно сразу или потом,
                        #    по participant_data и fallback_name.
                        #
                        #    То, что ты два раза написала одну строку тебя должно было насторожить.
                        #Alex
                        for name,el_gaia_id in dict_gaia_id.items():
                            if gaia_id == el_gaia_id:
                                if 'text' in seg:
                                    messages[name].append(seg['text'])
                    else:
                        continue
            else:
                continue

# R: выделять работу в функции - хорошо
# R: в питоне используется так называемый snake_case,
#    т.е. функции называются через подчёркивание маленькими буквами: get_words()
def getWords(text):
    return re.compile('\w+').findall(text)  # R: отбивай функции пустыми строками

for key in messages:
    for mes in messages[key]:
        all_words[key].extend(getWords(mes))
    #print(all_words)
  # R: вот этот подсчёт хороший кусок кода для вынесения в отдельную функцию
for key in all_words:
    for word in all_words[key]:
        if word in counts[key]:
            counts[key][word] += 1
        else:
            counts[key][word] = 1
    sorted_x = sorted(counts[key].items(), key=operator.itemgetter(1))
    print('-------------')
    print(key+':')
    print(sorted_x[-10:])  # R: можно было отсортировать в обратном порядке и вывести первые 10


# R: задача рефакторинга 1: применить все замечания, кроме автоматического узнавания
#    кто есть какой gaia_id. Достать сообщения всех в виде словаря {gaia_id: messages}.
#    Хардкодинг gaia_id -> имя вынести в костанту вверху файла.
