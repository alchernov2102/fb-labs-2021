import re
import math
import csv

russian_dict = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

#фильтруем исходный текст
def alter_text(no_spaces):
#открываем файл с исходным текстом для чтения
    with open('mytext.txt','r', encoding='utf-8') as myfile:
        original_text = myfile.read()

#переводим весь текст в lowercase, заменяем нужные символы, форматируем текст в одну строку
    altered_text = original_text.lower().replace('\n', ' ').replace('ъ', 'ь').replace('ё', 'е')
#убираем спец символы 
    altered_text = re.sub('[^А-Яа-я\s]', '', altered_text)
#заменяем все пропуски одинарным пробелом
    combined_whitespace = re.compile(r'\s+')
    altered_text = combined_whitespace.sub(" ", altered_text).strip()
    
    if no_spaces:
      altered_text = altered_text.replace(' ', '')
    
#записываем отфильтрованный текст в новый файл
    new_file = open('altered_text.txt', 'w')
    n = new_file.write(altered_text)
    new_file.close()

#считаем частоту каждой буквы в тексте
def calculate_letter_frequency():
    print("Started calculating letters....")

    new_file = open('altered_text.txt', 'r')
    our_text = new_file.read()
    
    #количество каждой буквы в тексте
    frequency_by_letter = {}
    for n in our_text:
        keys = frequency_by_letter.keys()
        if n in keys:
            frequency_by_letter[n]+=1
        else:
            frequency_by_letter[n] = 1

    #считаем частоту для каждой буквы
    for i in frequency_by_letter:
        frequency_by_letter[i] = frequency_by_letter[i] / len(our_text)



    print("Frequency by each letter in text: ", frequency_by_letter)

    #пишем частоту каждой буквы в csv файл
    with open('letter_freq.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in frequency_by_letter.items():
            writer.writerow([key, value])



    return(frequency_by_letter.values())
   
#считаем частоту биграм
def bigram_freq(step):
    new_file = open('altered_text.txt', 'r')
    our_text = new_file.read()

    
    #считаем количество биграм с шагом 2
    if step:
        list_of_bigrams = [our_text[i:i+2] for i in range(0, len(our_text), 2)]
    #считаем количество биграм с шагом 1
    else:
        list_of_bigrams = [our_text[i:i+2] for i in range(len(our_text)-1)]

    bigram_frequency = {}

    for bi in list_of_bigrams:
        if bi not in bigram_frequency:
            bigram_frequency[bi] = list_of_bigrams.count(bi)/ len(list_of_bigrams)
   
    
    #print("AMOUNT OF BIGRAMS: ", len(list_of_bigrams))
    #print (bigram_frequency)

    #записываем матрицу в csv файл
    with open('bi_freq.csv', 'w') as csv_file:
        for char1 in russian_dict:
            for char2 in russian_dict:
                bigram = char1 + char2
                if bigram in bigram_frequency:
                    csv_file.write(str(bigram_frequency[bigram]))
                    csv_file.write(',')
                else:
                    csv_file.write(',')
            csv_file.write('\n')
    return (bigram_frequency.values())

#считаем энтропию
def calculate_entropy(entry_frequency, n):
    h = 0
    for keys in entry_frequency:
        if keys != 0:
            h += keys/n * math.log2(1 / keys)
    red = 1 - h/5
    print('H = ', h)
    print ('R =', red)



def main():

    print("Started....")
    alter_text(1)
    letters_frqs = calculate_letter_frequency()
    calculate_entropy(letters_frqs, 1)
    bigram_frqs = bigram_freq(1)
    calculate_entropy(bigram_frqs, 2)
    
    
    #bigram_freq()
    

if __name__ == "__main__":
    main()
