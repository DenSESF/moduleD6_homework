import os
import json

if __name__ == '__main__':
    keyword_dict = {}
    word = ''
    while word != '.':
        word = input('Ведите нецензурное слово или . для завершения: ')
        if len(word) > 2:
            word_key = word.replace(word[0:-1], '*' * len(word[0:-1]))
            if word_key in keyword_dict:
                keyword_dict[word_key].append(word)
            else:
                keyword_dict[word_key] = [word]

    if not os.path.isfile('censuredlist.json'):
        with open('censuredlist.json', 'w') as file_censor:
            json.dump(keyword_dict, file_censor, sort_keys=True, indent=2)
        with open('censuredlist.json', 'r') as file_censor:
            load_kw_dict = json.load(file_censor)
        print(load_kw_dict.keys(), load_kw_dict.values(), sep='\n')
