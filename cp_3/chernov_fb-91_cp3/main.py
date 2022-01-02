from add_func import *
import re

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





def main():

    TEXT = alter_text()
    my_dict = bigram_freq(TEXT)
    
    sorted_dict = dict(sorted(my_dict.items(), key = lambda item: item[1], reverse = True))
    pop_bi_text = list(sorted_dict)[:5]
    print(pop_bi_text)



if __name__ == "__main__":
    main()


