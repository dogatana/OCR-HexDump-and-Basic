# 16進ダンプリスト、BASICプログラムの画像からテキストを生成

## 必要となるパッケージ

- easyocr

注）CUDA ライブラリをインストールすると速くなるらしい。
ただし easyocr の公式サイトに記載の方法で行なわないとCUDA が認識されない。

## scan_image.py

```
> python scan_image.py sample.png
sample.png: write sample.json
```

- 画像ファイルを指定して実行するとスキャン結果を json ファイルとして出力する
- 余計な文字が入らないようにするのが良い

![sample.png](sample.png)

## extract_text.py

```
> python extract_text.py sample.json
basic.json: write sample.txt
```

- json ファイルを指定して実行すると txt ファイルとして出力する
- en を指定しているのでカナは検出しない
- 記号類もうまくいかない場合がある

```
300 PRINT:PRINT:COLORS:PRINT"keyM    function}    ";:COLORZ:PRINT"UP":GOSUB450
310 PRINT"                 N7
320 PRINT"
330 PRINT"                 '8!'C7
340 PRINT"         LEFT  14 |    16 |MRIGHT"
350 PRINT"
360 PRINT:PRINT" 5000 PTS 7~ MAN EFV JIZZ0 ":GOSUB450"I
370 PRINT:PRINT:COLORS:PRINT"    HIt RETURN KEY  ;:GOSUB450
380 IF INPUTI(1) >CHRS(IS)THEN380
390 LOCATEO,0,O:DEFUSRI=RHD420:AAFUSRI(0)
```




