import data
import numpy as np
import re

mydict = {}
data = data.MinimizedData("tr_boun-ud-train.conllu", True, mydict)

sentences = [
    "Gelecek ay A.B.D. 'ye gideceklermiş",
    "Abd başkanı bu konuda konuştu.",
    "Bu yıl en çok tercih edilen firma Getir oldu.",
    "Sana su getirdim.",
    "Sarı-Kırmızılı takım yenilgiye uğradı.",
    "AR-GE faaliyetleri yürütülüyor.",
    "Bu şehirde Hırıstiyan-Alevi milletler iç içe yaşıyor.",
    "Kanarya sırasıyla Kayseri, Bursa, G.Saray, Ankara, Beşiktaş, Antalya ve Trabzon 'a konuk olacak.",
    "GS taraftarlarının tezahüratları duyuluyor.",
    "Bu akşam G.S. maçı saat 20:45 'te yayınlanacak.",
    "Toplantı saat 10.30 'da gerçekleşti.",
    "21/11/2021 tarihinde mezun oldum.",
    "Başbakan 21.11.2021 'de konuşma yapacak."
]

def convert_lowercase(sentence):
    return (sentence.lower())

def split_sentence(sentence):
    split_by_whitespace = sentence.split()
    return split_by_whitespace

def normalize(word_list):
    for i in range(len(word_list)):
        if word_list[i] == "A.B.D":
            word_list[i] = "ABD"
        if  word_list[i] == "G.Saray" or word_list[i] == "G.S.":
            word_list[i] = "GS"
        if  word_list[i] == "AR-GE":
            word_list[i] = "ARGE"
        if re.search(r'\d{2}:\d{2}', word_list[i]):
            ind = word_list[i].index(":")
            print(ind)
            str_first = word_list[i][:ind]
            print(str_first)
            str_after= word_list[i][ind+1:]
            print(str_after)
            word_list[i]= str_first + "." + str_after
        if re.search(r'[A-z]*-[A-z]*', word_list[i]):
            ind = word_list[i].index("-")
            str_first = word_list[i][:ind]
            print(str_first)
            str_after = word_list[i][ind + 1:]
            print(str_after)
            word_list[i] = str_first + " " + str_after
        if re.search(r'\d*\/\d*\/\d*', word_list[i]):
            indexes = [index for index, v in enumerate(word_list[i]) if v == '/']
            for x in indexes:
                print(x)
                word_list[i] = word_list[i][:x] + "." + word_list[i][x+1:]
    return word_list
print(normalize(split_sentence(sentences[6])))
print(normalize(split_sentence(sentences[5])))
print(normalize(split_sentence(sentences[-2])))