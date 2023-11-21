# g2pk3
G2PK's upgrade version


## Updated content
* 제20조항 오류 문제 해결
* 일본어 발음 전사 추가

## Installation
```
pip install git+https://github.com/kdrkdrkdr/pyopenjtalk
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
[Kyubyong/g2pk](https://github.com/Kyubyong/g2pK)<br>
[tenebo/g2pk2](https://github.com/tenebo/g2pk2)