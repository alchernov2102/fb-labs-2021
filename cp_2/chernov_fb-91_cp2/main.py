import re
import csv

my_keys = ['яд', 'дух', 'фура', 'кошка', 'фольга', 
'абитуриент', 'магистратура', 'абстрактность', 'аккумулировать' 'актуализировать', 
'воспламеняемость','благотворительный','высококачественный','конкурентоспособный', 'дисциплинированность']

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

ru_alphabet = 'aбвгдежзийклмнопрстуфхцчшщъыьэюя'



def alter_text():

    with open('encrypt_text.txt','r+', encoding='UTF-8') as myfile:
        raw_text = myfile.read()
    
    #переводим весь текст в lowercase, заменяем нужные символы, форматируем текст в одну строку
        altered_text = raw_text.lower().replace('\n', ' ').replace('ъ', 'ь').replace('ё', 'е').replace(' ', '')
    #убираем спец символы 
        altered_text = re.sub('[^А-Яа-я\s]', '', altered_text)
    #заменяем все пропуски одинарным пробелом
        combined_whitespace = re.compile(r'\s+')
        altered_text = combined_whitespace.sub(" ", altered_text).strip()

    

    new_file = open('altered_text.txt', 'w')
    n = new_file.write(altered_text)
    new_file.close()

    return altered_text

#визначаємо індекс відповідності тексту за формулою
def corr_index(source):

    letter_counter = 0
    for letter in rus_alphabet:
        letter_counter += source.count(letter) * (source.count(letter) - 1)
    crs_index = letter_counter / (len(source) * (len(source) - 1))
    return crs_index


#шифруємо текст
def encode_text(text, key):

    position = 0
    encoded_text = ''
    for i in text:
        encoded_text += rus_alphabet[(rus_alphabet.index(i) + rus_alphabet.index(key[position%len(key)])) % 32]
        position += 1

    
    print("ІНДЕКС ВІДПОВІДНОСТІ ШИФРТЕКСТУ: ", corr_index(encoded_text), '\n')
    

    return encoded_text

#дешифруємо текст
def decode_text(encoded_text, key):

    position = 0
    decoded_text = ''
    for i in encoded_text:
        decoded_text += rus_alphabet[(rus_alphabet.index(i) + 32 - rus_alphabet.index(key[position%len(key)])) % 32]
        position += 1
    
    return decoded_text

#розділяємо текст на блоки 
def text_to_blocks(text, length):

    cipher_blocks = []

    for i in range(0, length):
        cipher_blocks.append(text[i::length])

    return cipher_blocks

#знаходимо довжину ключа шифртексту
def key_length(text):

    dict = {}
    for k_len in range (1, 31):

        index_of_coin = 0
        created_blocks = text_to_blocks(text, k_len)

        for each_block in created_blocks:
            index_of_coin += corr_index(each_block)
        index_of_coin = index_of_coin / k_len
        dict[k_len] = index_of_coin

   
    with open('key_length.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in dict.items():
            writer.writerow([key, value])

    return dict

#визначаємо літеру із найбільшою частотою у блоці
def max_freq_in_block(source):

    freq_dict = {}
    for letter in source:
        if letter in freq_dict:
            freq_dict[letter]+=1
        else:
            freq_dict[letter] = 1

    get_max_value = max(freq_dict, key=freq_dict.get)

    #print("FREQ DICT: ", freq_dict)

    return get_max_value


#отримуємо ключ
def get_secret_key(text, key_L):
#буква із найбільшою частотою у російській мові
    max_freq_letter = 'о' 
    my_keys = []
    separate_blocks = text_to_blocks(text, key_L)
    for each_block in separate_blocks:
        block_max_frequency = max_freq_in_block(each_block)
        key = (rus_alphabet.index(block_max_frequency) - rus_alphabet.index(max_freq_letter)) % len(rus_alphabet)
        my_keys.append(rus_alphabet[key])
    secret_key = ''.join(my_keys)

    return secret_key



def main():

    
    '''
    text = alter_text()
    key = 'дисциплинированность'
    print("KEY: ", key, len(key))
    encoded_message = encode_text(text,key)
    decoded_message = decode_text(encoded_message, key)
    print ("ENCODED:", encoded_message)
    #print ("DECODED: ", decoded_message)
    
    #keyL = key_length(encoded_message)
    #print("LENGTH: ", key)
    

    #key_len = max(keyL, key=keyL.get) #наибольшее значение из словаря
    #print("KEY LEN: ", key_len)
'''

    with open('decrypt_text.txt','r+', encoding='UTF-8') as myfile:
       coded_message = myfile.read()
    
    keys_length_dict = key_length(coded_message)
    print(keys_length_dict, '\n')
    key_L = max(keys_length_dict, key=keys_length_dict.get)
    print ("LENGTH: ", key_L, "\n")
    secret_key = get_secret_key(coded_message, key_L)
    print ("KEY: ", secret_key, "\n")


    decoded_msg = decode_text(coded_message, "вшекспирбуря")
    print ("DECODED: ", decoded_msg)



if __name__ == "__main__":
    main()