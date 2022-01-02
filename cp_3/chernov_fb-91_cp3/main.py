from add_func import *
import re

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

mod = len(rus_alphabet)

pop_bi_rus = ["ст", "но", "то", "на", "ен"]
pop_bi_text = ['фт', 'йо', 'дт', 'шж', 'ют']

#форматуємо текст
def alter_text():

    with open('21.txt', 'r+', encoding='UTF-8') as file:
        raw_text = file.read()


        altered_text = altered_text = raw_text.lower().replace('\n', ' ').replace('ъ', 'ь').replace('ё', 'е').replace(' ', '')
        altered_text = re.sub('[^А-Яа-я\s]', '', altered_text)
        
        combined_whitespace = re.compile(r'\s+')
        altered_text = combined_whitespace.sub(" ", altered_text).strip()

    new_file = open('altered_text.txt', 'w')
    n = new_file.write(altered_text)
    new_file.close()

    return altered_text

#рахуємо частоту біграм у тексті
def bigram_freq(altered_text):

     list_of_bigrams = [altered_text[i:i+2] for i in range(0, len(altered_text), 2)]

     bigram_frequency = {}

     for bi in list_of_bigrams:
        if bi not in bigram_frequency:
            bigram_frequency[bi] = list_of_bigrams.count(bi)/ len(list_of_bigrams)
     
     return bigram_frequency


#переводимо біграму у число
def bi_convert(bi):

    converted = (rus_alphabet.index(bi[0]) * mod + rus_alphabet.index(bi[1])) % pow(mod, 2)

    return converted


#пари біграм
def bi_group(altered_text):

    bi1 = []
    bi2 = []

    for el1 in pop_bi_rus:
        for el2 in pop_bi_text:
            bi1.append((el1,el2))

    for el1 in bi1:
        for el2 in bi1:
            if el1 != el2 or (el1, el2) not in bi2:
                bi2.append((el1, el2))

    return bi2

#знайдемо ключі
def calculate_keys(bi_group):


    x1 = bi_convert(bi_group[0][0])
    x2 = bi_convert(bi_group[0][1])
    y1 = bi_convert(bi_group[1][0])
    y2 = bi_convert(bi_group[1][1])

    print(x1, x2, y1, y2)

    possible_keys = []

    value_a = linear_comparsion(x1-x2, y1 - y2, pow(mod, 2))

    print(value_a)

    for element in value_a:
            value_b = (calculate_GCD(y1 - element * x1, pow(mod, 2))[1]) % pow(mod, 2)
            possible_keys.append((element, value_b))
    return possible_keys

    
        

#пари ключів
def keys_group(bi2):

    my_keys = []

    for element in bi2:
        key = calculate_keys(element)
        if len(key) != 0:
            for i in len(key):
                my_keys.append(key[i])

    return my_keys


#перевірка тексту
def text_check(all_txt):

    final_txt = []

    for txt in all_txt:
        if not any(txt.find("оо"), txt.find("аь"), txt.find("оь"), txt.find("юь"), txt.find("эь")):
            final_txt.append(txt)

#дешифровка
def txt_decrypt(altered_text, keys):
    key_a = int(keys[0])
    key_b = int (keys[1])

    decrypted = []

    for i in range(0, len(altered_text), 2):
        temp = (reverse_element(key_a, pow(mod, 2)) * (bi_convert(altered_text[i:i+2]) - key_b)) % pow(mod, 2)
        decrypted.append(rus_alphabet[temp // mod] + rus_alphabet[temp % mod])

    return ''.join()


def main():

    my_text = alter_text()
    my_dict = bigram_freq(my_text)
    
    sorted_dict = dict(sorted(my_dict.items(), key = lambda item: item[1], reverse = True))
    pop_bi_text = list(sorted_dict)[:5]
    print(pop_bi_text)

    grp = bi_group(my_text)
    keys = keys_group(grp)
    print(keys)
   

if __name__ == "__main__":
    main()


