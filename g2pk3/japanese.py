from g2pk3.korean import join_jamos, split_syllables
import re
import pyopenjtalk
import jaconv

patt_repl = [
    ('ア',    'A'),
    ('イ',    'I'),
    ('ウ',    'U'),
    ('エ',    'E'),
    ('オ',    'O'),

    ('カ',       'ka'),
    ('キ',       'ki'),
    ('ク',       'ku'),
    ('ケ',       'ke'),
    ('コ',       'ko'),

    ('ガ',       'ga'),
    ('ギ',       'gi'),
    ('グ',       'gu'),
    ('ゲ',       'ge'),
    ('ゴ',       'go'),

    ('サ',       'sa'),
    ('シ',       'si'),
    ('ス',       'ㅅㅡ'),
    ('セ',       'se'),
    ('ソ',       'so'),

    ('ザ',       'za'),
    ('ジ',       'zi'),
    ('ズ',       'ㅈㅡ'),
    ('ゼ',       'ze'),
    ('ゾ',       'zo'),

    ('タ',       'ta'),
    ('チ',       'ci'),
    ('ツ',       'cu'),
    ('テ',       'te'),
    ('ト',       'to'),

    ('ダ',       'da'),
    ('ヂ',       'zi'),
    ('ヅ',       'zu'),
    ('デ',       'de'),
    ('ド',       'do'),

    ('ナ',       'na'),
    ('ニ',       'ni'),
    ('ヌ',       'nu'),
    ('ネ',       'ne'),
    ('ノ',       'no'),

    ('ハ',       'ha'),
    ('ヒ',       'hi'),
    ('フ',       'hu'),
    ('ヘ',       'he'),
    ('ホ',       'ho'),

    ('バ',       'ba'),
    ('ビ',       'bi'),
    ('ブ',       'bu'),
    ('ベ',       'be'),
    ('ボ',       'bo'),

    ('パ',       'pa'),
    ('ピ',       'pi'),
    ('プ',       'pu'),
    ('ペ',       'pe'),
    ('ポ',       'po'),

    ('マ',       'ma'),
    ('ミ',       'mi'),
    ('ム',       'mu'),
    ('メ',       'me'),
    ('モ',       'mo'),

    ('ヤ',       'ya'),
    ('ユ',       'yu'),
    ('ヨ',       'yo'),
    ('ャ',       'ja'),
    ('ュ',       'ju'),
    ('ョ',       'jo'),

    ('ラ',       'ra'),
    ('リ',       'ri'),
    ('ル',       'ru'),
    ('レ',       're'),
    ('ロ',       'ro'),
    ('ワ',       'wa'),
    ('ヲ',       'o'),

    ('ン',       'N'),
    ('ッ',       'Q'),

    

    (r'([td])eィ',       r'\1i'),
    (r'([td])oゥ',       r'\1u'),
    (r'([td])ej',       r'\1y'),
    (r'([aiueoAIUEO])(ー)', r'\1\1'),
    (r'([aiueoAIUEO])Q([gsd])', r'\1\2\2'),
    (r'([aiueoAIUEO])Q([c])', r'\1ㄷ\2'),
    (r'([aiueoAIUEO])Q([p])', r'\1ㅂ\2'),
    (r'([aiueoAIUEO])Q([^gsdcp]|$)', r'\1ㅅ\2'),
    (r'(Q+)', '읏 '),
    (r'([aiueoAIUEO])N([mbp])', r'\1ㅁ\]2'),
    (r'([aiueoAIUEO])N([kghaiueoy])', r'\1ㅇ\2'),
    (r'([aiueoAIUEO])N([sztcdnr]|$)', r'\1ㄴ\2'),
    (r'(N+)', lambda match: '으'*(len(match.group())-1) + '응'),

    ('A', 'ㅇㅏ'),
    ('I', 'ㅇㅣ'),
    ('U', 'ㅇㅜ'),
    ('E', 'ㅇㅔ'),
    ('O', 'ㅇㅗ'),
    ('wa',        '와'),
    ('k',         'ㅋ'),
    ('g',         'ㄱ'),
    ('s',         'ㅅ'),
    ('z',         'ㅈ'),
    ('t',         'ㅌ'),
    ('c',         'ㅊ'),
    ('d',         'ㄷ'),
    ('n',         'ㄴ'),
    ('h',         'ㅎ'),
    ('b',         'ㅂ'),
    ('p',         'ㅍ'),
    ('m',         'ㅁ'),
    ('r',         'ㄹ'),
    ('ya',        'ㅑ'),
    ('yu',        'ㅠ'),
    ('yo',        'ㅛ'),
    ('ija',       'ㅑ'),
    ('iju',       'ㅠ'),
    ('ijo',       'ㅛ'),
    ('a',         'ㅏ'),
    ('i',         'ㅣ'),
    ('u',         'ㅜ'),
    ('e',         'ㅔ'),
    ('o',         'ㅗ'),
    ('・',          ' '),
]

def convert_jpn(string):
    jpn_words = set(re.findall("[ぁ-んァ-ン一-龯']+", string))
    for jpn_word in jpn_words:
        word = pyopenjtalk.g2p(jpn_word, kana=True)
        for pattern, repl in patt_repl:
            word = re.sub(pattern, repl, word)
        string = string.replace(jpn_word, word)
    return string