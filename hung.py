import json
import re
from pprint import pprint
import operator

with open('Hangouts.json') as data_file:
    data = json.load(data_file)

# R: захардконены имена, они должны доставаться из самого файла.
#    См. participant_data и fallback_name
messages = {
    'nadya': [],
    'alexandr': []

    }

# R: [0] - почти наверняка ошибка, т.к. если это массив,
#    то следует смотреть все элементы, а не только первый.
events = data['conversation_state'][0]['conversation_state']['event']
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
            if el['chat_message']['message_content']['segment'][0]['type'] == 'TEXT':
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
                if gaia_id=='116003021892114994463':
                    messages['alexandr'].append(el['chat_message']['message_content']['segment'][0]['text'])

                #Nadya
                if gaia_id=='112073426858751033150':
                    messages['nadya'].append(el['chat_message']['message_content']['segment'][0]['text'])
            else:
                continue
        else:
            continue

# R: выделять работу в функции - хорошо
# R: в питоне используется так называемый snake_case,
#    т.е. функции называются через подчёркивание маленькими буквами: get_words()
def getWords(text):
    return re.compile('\w+').findall(text)  # R: отбивай функции пустыми строками
all_words = []
for mes in messages['alexandr']:
    all_words.extend(getWords(mes))
print(all_words)
counts = {}  # R: вот этот подсчёт хороший кусок кода для вынесения в отдельную функцию
for word in all_words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
sorted_x = sorted(counts.items(), key=operator.itemgetter(1))
print(sorted_x[-10:])  # R: можно было отсортировать в обратном порядке и вывести первые 10


# R: задача рефакторинга 1: применить все замечания, кроме автоматического узнавания
#    кто есть какой gaia_id. Достать сообщения всех в виде словаря {gaia_id: messages}.
#    Хардкодинг gaia_id -> имя вынести в костанту вверху файла.
