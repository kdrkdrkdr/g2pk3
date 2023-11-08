# g2pk3
G2PK's upgrade version


## Updated content
* 제20조항 오류 문제 해결
* 일본어 발음 전사 추가

## Requirements
* python >= 3.6
* jamo
* g2p_en
* pyopenjtalk

## Installation
```
pip install g2pk3
```

## How To Use
g2pk3 uses same syntaxes as g2pk.
```python
>>> from g2pk3 import G2p
>>> g2p = G2p()
>>> g2p("こんにちは. hello. 반갑습니다.")
콘니치와. 헐로. 반갑씀니다.
```

## Reference
[g2pk](https://github.com/Kyubyong/g2pK)
[g2pk2](https://github.com/tenebo/g2pk2)