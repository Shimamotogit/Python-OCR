# Python_OCR

## 目次

- [概要](#summary)

    - [他のアプリに対する優位性](#他のアプリに対する優位性)
    - [PaddleOCR_v4とTesseractの比較](#comparison)
    - [PaddleOCR_v4について](#PaddleOCR_v4_in_summary)
    - [Tesseractについて](#Tesseract_in_summary)

- [PaddleOCR_v4を使ったOCRの実装](#PaddleOCR_v4)
- [Tesseractを使ったOCRの実装](#Tesseract)
- [使い方](#how_to_use)

##### Tesseract OCR プログラムをexe化しました。
#### ***[ここからexeファイルをインストールできます。](https://tk-2025.oops.jp/app/ocr/OCR%E3%82%A2%E3%83%97%E3%83%AA.zip)***

<a id="summary"></a>

## 概要

<a id="comparison"></a>

Windowsのスクリーンショット機能とOCR機能を統合したプログラムです。<br>

<a id="他のアプリに対する優位性"></a>

似たものに Power Toys の Text Extractor がありますが、
今回作成したプログラムが Text Extractor より優位な点は以下の3つです。

- ***他のアプリに対する優位性***

    - ***認識精度と実行速度***

        - Tesseractでは [ベストモデル](https://github.com/tesseract-ocr/tessdata_best) を使うことによって英語、日本語の両方で Text Extractor よりも高い精度でOCR処理をすることができます。

        - 入力する画像の大きさによって処理時間は増減しますが、基本的に意識して処理を待つことなくペースト処理まで完了することができます。

        - ※PaddleOCR_v4の場合、OCR精度高いとされますが、Tesseractに比べて処理時間が長い傾向にあります。

    - ***改行とインデント***

        - Text Extractor では適切に改行とインデントを挟むことができませんでしたが、これらの問題を解消しました。

    - ***ショートカットキーの統合***

        - Text Extractor ではショートカットキーが既存のものと重複してしまうと、動作しなくなる欠点がありましたが、`windows + shift + s` のショートカットと統合することで新しくショートカットキーを覚える必要がなくなりました。

#### [使い方](#how_to_use)

- PaddleOCR_v4とTesseractの比較

    - CPUで処理を行う場合、Tesseract のほうが高速に動作します。
    - 厳密な検証はしていませんが、精度は PaddleOCR_v4 のほうが高いように感じます。

<a id="PaddleOCR_v4_in_summary"></a>

- PaddleOCR_v4について

    - [PaddleOCR_v4](https://github.com/PaddlePaddle/PaddleOCR)は2023年8月7日に中国のBaiduによって公開されたオープンソースのOCRエンジンです。
    - [PaddlePaddle](https://github.com/PaddlePaddle/Paddle)というディープラーニングフレームワーク利用して作られています。

<a id="Tesseract_in_summary"></a>

- Tesseractについて

    - [Tesseract_OCR](https://github.com/tesseract-ocr/tesseract)は現在Googleによって管理されているオープンソースのOCRエンジンです。
    - [ベストモデル](https://github.com/tesseract-ocr/tessdata_best)を入手することで精度が向上する可能性があります。
    - Tesseractは転移学習することができるため、使用用途が決まっている場合はカスタマイズすることで精度を向上させることができます。

## 使用例

- ビデオ通話、会議中に表示されたスライドの内容を瞬時に抽出する
- 写真や動画の中のテキストを抽出する
- OCR処理されていないPDFファイルの内容を抽出する
- テキストコピーを禁止しているサイトでテキストをコピーする
- etc...

**Windowsのスクリーンショット機能 `windows + shift + s` と連携しているため、ストレスなく使うことができます。**

#### [使い方](#how_to_use)

<a id="PaddleOCR_v4"></a>

## PaddleOCR_v4 の環境構築

現在、作成中です。
***


<a id="Tesseract"></a>

## Tesseract の環境構築

- **注意事項**

    - Windows10,11 でのみ動作確認済みです。
    - 事前にTesseractをインストールしている必要があります。

1, このリポジトリをクローンします。

```bash 
git clone https://github.com/Shimamotogit/Python-OCR.git
```

2, Anaconda Prompt で仮想環境を作成する。

```bash
conda create -n tesseract_ocr python=3.7.16
```

3, ライブラリをインストールします。
```bash 
pip install -r ./tesseract/requirements.txt
```

4, 実行方法は以下の通りです。

```bash 
python ./tesseract/tesseract.py
```

#### [使い方](#how_to_use)

初期値以外のパラメータを設定する場合は以下を参考にしてください。

```bash 
python ./tesseract/tesseract.py --language eng+jpn --path_to_tesseract "C:/Program Files/Tesseract-OCR/tesseract.exe" --standby_time 0.5 --paragraph_threshold_value 0.9 --exit_detection_sound --result_print
```

### 引数説明

引数名|初期値|type|説明
|:---:|:---:|:---:|:---:|
|--language|eng+jpn|str|OCRで優先する言語を設定します。<br>eng+jpn or jpn+eng or eng or jpn
|--path_to_tesseract|C:/Program Files/Tesseract-OCR/tesseract.exe|str|インストールしているtesseract.exeまでのパスを入力
|--standby_time|0.5|float|クリップボード参照の待機秒数、値が小さくなるとOCR結果の出力までが早くなりますが、CPU使用率が多くなる可能性があります。
|--paragraph_threshold_value|0.9|float|改行の閾値設定、OCRの結果が崩れる場合に調整してください。
|--exit_detection_sound|False|bool|OCR結果をクリップボードにコピーした際に音を鳴らす。
|--result_print|False|bool|OCRの結果をCUIに出力する。

<a id="how_to_use"></a>

## 使い方

1, [Tesseractの環境構築](#Tesseract)

2, プログラム起動後に `windows + shift + s` でスクリーンショットモードに入ります。

3, 数秒後 `ctrl + v` でOCR結果をペーストすることができます。

- Snipping Toolの設定

    - Snipping Toolの設定で `スクリーンショットを自動的に保存する` の項目がオンになっている場合、意図しない写真が大量に保存されることがあります。<br>
    本プログラムを利用する際はこの設定を `オフ` にすることをおすすめします。

<!-- 

```
--language
    OCRで優先する言語を設定します。eng+jpn or jpn+eng or eng or jpn 
    初期値 : eng+jpn

--path_to_tesseract　
    インストールしているtesseract.exeまでのパスを設定します。
    初期値 : C:/Program Files/Tesseract-OCR/tesseract.exe

--standby_time
    クリップボード参照の待機秒数、値が小さくなるとOCR結果の出力までが早くなりますが、CPU使用率が多くなる可能性があります。
    初期値 : 1.0

--paragraph_threshold_value
    改行の閾値設定、OCRの結果が崩れる場合に調整してください。
    初期値 : 0.9

--exit_detection_sound
    OCR結果をクリップボードにコピーした際に音を鳴らす。
    初期値 : False

--result_print
    OCRの結果をCUIに出力する。
    初期値 : False
``` -->