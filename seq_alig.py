# Sequence Alignment of strings
# código adaptado de https://github.com/projeto-de-algoritmos/Lista5-Gabriela-e-Geovana/blob/master/lista5.ipynb
# autoras: github.com/GeovanaRamos e github.com/gabiMSilva

from math import sqrt
KEY_DIST = 1.0
KEY_START = [0.0, 0.5, 1.0, 1.5]

gap = 2

keyboard = [
    '1234567890',
    'qwertyuiop',
    'asdfghjklç',
    'zxcvbnm'
]

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

coords = {}
num_lines = len(keyboard)

# calculating position of the keys
for line in range(num_lines):
    line_size = len(keyboard[line])
    for column in range(line_size):
        coords[keyboard[line][column]] = Coord(
            KEY_START[line]+column*KEY_DIST , line*KEY_DIST)
        # print(keyboard[line][column]+' ',end=',')
    # print('\n========')

def key_key(l,c):
    return "{}-{}".format(c,l)

all_keys = ''
num_of_keys = 0
for i in keyboard:
    all_keys += i

num_of_keys = len(all_keys)

#print(num_of_keys)
distances = {}

# calculating distances between keys
for l in all_keys:
    for c in all_keys:
        key_1 = coords[l]
        key_2 = coords[c]
        dist = sqrt((key_2.x-key_1.x)**2 + (key_2.y-key_1.y)**2 )
        distances[key_key(l,c)] = dist
        distances[key_key(c,l)] = dist

# print(distances["d-d"])

# return euclidian distance between letters on keyboard
def getMismatch(letterA, letterB):
    if letterA == letterB:
        return 0.0
    else:
        return distances[key_key(letterA,letterB)]

def editDistance(str1, str2, m, n): 
    table = [[0 for j in range(n+1)] for i in range(m+1)] 
    
    for i in range(m+1):
        table[i][0] = gap*i

    for j in range(n+1):
        table[0][j] = gap*j

    for i in range(1,m+1): 
        for j in range(1,n+1): 
  
            table[i][j] = min(
                                gap + table[i][j-1],         
                                gap + table[i-1][j],            
                                getMismatch(str1[i-1], str2[j-1]) + table[i-1][j-1]   
                             )
    return table[m][n]


## scripts for tests

# words = [
#     'maça',
#     'banana',
#     'uva',
#     'pera',
#     'melao',
#     'manga',
#     'melancia',
#     'caju',
#     'cereja',
#     'coco',
#     'goiaba',
#     'jaca',
#     'limao',
#     'mamao',
#     'maracuja',
#     'tangerina',
#     'pessego'
# ]

def get_correct(word, words):
    if len(words) < 1:
        print("lista de palavras vazia")
        return ''
    len_word = len(word)
    min_dist = editDistance( words[0], word, len(words[0]), len_word )
    aux = min_dist
    correct = ''
    for i in words:
        aux = editDistance( i, word, len(i), len_word )
        # print(i,aux)
        if(aux < min_dist):
            min_dist = aux
            correct = i
    return correct

# word = ''
# continuar = True
# print(words)
# while continuar:
#     word = input("palavra: ")#.replace('\n','')
#     correct = get_correct(word, words)
#     if word == 'exit':
#         continuar = False
#     else:
#         print("correto",correct)
#         print('=======')