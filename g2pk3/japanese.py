import re
from unidecode import unidecode
import pyopenjtalk
from .korean import join_jamos, split_syllables


# Regular expression matching Japanese without punctuation marks:
_japanese_characters = re.compile(
    r'[A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# Regular expression matching non-Japanese characters or punctuation marks:
_japanese_marks = re.compile(
    r'[^A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# List of (symbol, Japanese) pairs for marks:
_symbols_to_japanese = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('％', 'パーセント')
]]



def symbols_to_japanese(text):
    for regex, replacement in _symbols_to_japanese:
        text = re.sub(regex, replacement, text)
    return text


def japanese_to_romaji_with_accent(text):
    '''Reference https://r9y9.github.io/ttslearn/latest/notebooks/ch10_Recipe-Tacotron.html'''
    text = symbols_to_japanese(text)
    sentences = re.split(_japanese_marks, text)
    marks = re.findall(_japanese_marks, text)
    text = ''
    for i, sentence in enumerate(sentences):
        if re.match(_japanese_characters, sentence):
            if text != '':
                text += ' '
            labels = pyopenjtalk.extract_fullcontext(sentence)
            for n, label in enumerate(labels):
                phoneme = re.search(r'\-([^\+]*)\+', label).group(1)
                if phoneme not in ['sil', 'pau']:
                    text += phoneme.replace('ch', 'ʧ').replace('sh',
                                                               'ʃ').replace('cl', 'Q')
                else:
                    continue
                # n_moras = int(re.search(r'/F:(\d+)_', label).group(1))
                a1 = int(re.search(r"/A:(\-?[0-9]+)\+", label).group(1))
                a2 = int(re.search(r"\+(\d+)\+", label).group(1))
                a3 = int(re.search(r"\+(\d+)/", label).group(1))
                if re.search(r'\-([^\+]*)\+', labels[n + 1]).group(1) in ['sil', 'pau']:
                    a2_next = -1
                else:
                    a2_next = int(
                        re.search(r"\+(\d+)\+", labels[n + 1]).group(1))
                # Accent phrase boundary
                if a3 == 1 and a2_next == 1:
                    text += ' '
                # Falling
                elif a1 == 0 and a2_next == a2 + 1:
                    text += '↓'
                # Rising
                elif a2 == 1 and a2_next == 2:
                    text += '↑'
        if i < len(marks):
            text += unidecode(marks[i]).replace(' ', '')
    return text




repl_lst = {
    '.': '. ',
    '↓': '',
    '↑': '',
    'a': 'a ',
    'i': 'i ',
    'u': 'u ',
    'e': 'e ',
    'o': 'o ',
    'Q': '|Q',
    'N': '|N',
    'U': 'u ',
    'I': 'i ',
    'A': 'a ',
    'E': 'e ',
    'O': 'o ',
}

repl_lst2 = {
    'ts': 'ㅊ',
    'ʧu': '츠',
    'tsu': '츠',
    'zu': '즈',
    'su': '스',

    'wa': '*ㅘ',
    'wo': '오',

    'g': 'ㄱ',
    'n': 'ㄴ',
    'd': 'ㄷ',
    'r': 'ㄹ',
    'm': 'ㅁ',
    'b': 'ㅂ',
    'v': 'ㅂ',
    'ʃ': 'ㅅ',
    's': 'ㅅ',
    'j': 'ㅈ',
    'ʧ': 'ㅊ',
    'k': 'ㅋ',
    't': 'ㅌ',
    'p': 'ㅍ',
    'h': 'ㅎ',
    'f': 'ㅎ',

    'a': '*ㅏ',
    'i': '*ㅣ',
    'u': '*ㅜ',
    'e': '*ㅔ',
    'o': '*ㅗ',

    'y*ㅏ':'*ㅑ',
    'y*ㅜ':'*ㅠ',
    'y*ㅔ':'*ㅖ',
    'y*ㅗ':'*ㅛ',
}

repl_lst3 = {
    '|Qㄱ': 'ㄱㄱ',
    '|Qㅅ': 'ㅅㅅ',
    '|Qㄷ': 'ㄷㄷ',
    '|Qㅊ': 'ㄷㅊ',
    '|Qㅍ': 'ㅂㅍ',

    '|Nㅁ': 'ㅁㅁ',
    '|Nㅂ': 'ㅁㅂ',
    '|Nㅍ': 'ㅁㅍ',

    '|Nㅅ': 'ㄴㅅ',
    '|Nㅈ': 'ㄴㅈ',
    '|Nㅌ': 'ㄴㅌ',
    '|Nㅊ': 'ㄴㅊ',
    '|Nㄷ': 'ㄴㄷ',
    '|Nㄴ': 'ㄴㄴ',
    '|Nㄹ': 'ㄴㄹ',

    '|Nㅋ': 'ㅇㅋ',
    '|Nㄱ': 'ㅇㄱ',
    '|Nㅇ': 'ㅇㅇ',
    '|Nㅎ': 'ㅇㅎ',
    
    '|Q': 'ㅅ',
    '|N': 'ㄴ',
}


def convert_jpn(string):
    jpn_words = set(re.findall("[ぁ-んァ-ン一-龯']+", string))
    for jpn_word in jpn_words:
        word = japanese_to_romaji_with_accent(jpn_word).strip().replace('^', '').replace(' ', '^ ')
        for k, v in repl_lst.items():
            word = word.replace(k, v)
        for k, v in repl_lst2.items():
            word = word.replace(k, v)
        word = ' '.join([i.replace('*', 'ㅇ') if i.startswith('*') else i.replace('*', '') for i in word.strip().split(' ')])
        for k, v in repl_lst3.items():
            word = word.replace(k, v)
        word = join_jamos(word.replace('  ', ' ')).replace(' ', '').replace('^', ' ')
        string = join_jamos(split_syllables(string.replace(jpn_word, word))).replace('ㄴ', 'ㅇㅡㅇ').replace('ㅇㅇ', 'ㅇ').replace('ㅅ', '')

    return string