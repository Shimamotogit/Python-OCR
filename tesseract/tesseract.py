from PIL import ImageGrab
import numpy as np
import pyperclip
import time
import sys

def command_line_argument():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", choices=['eng+jpn','jpn+eng', 'eng', 'jpn'], default="eng+jpn", type=str, 
                        help="英語だけを抽出したい場合は 'eng' 日本語を中心に抽出したい場合は 'jpn' 日本語かつ英語も抽出したい場合は 'jpn+eng 'デフォルトは'eng+jpn'")

    parser.add_argument("-p", "--path_to_tesseract", default="C:/Program Files/Tesseract-OCR/tesseract.exe", type=str, 
                        help="tesseract.exeまでのファイルパスを入力してください。デフォルトは'C:/Program Files/Tesseract-OCR/tesseract.exe'")

    parser.add_argument("-s", "--standby_time", default=0.5, type=float, 
                        help="クリップボード参照の待機秒数、値が小さくなるとOCR結果の出力までが早くなりますが、CPU使用率が多くなる可能性があります。デフォルトは'0.5'")

    parser.add_argument("--paragraph_threshold_value", default=0.9, type=float, 
                    help="改行の閾値設定、OCRの結果が崩れる場合に調整してください。デフォルトは'0.9'")

    parser.add_argument("-e", "--exit_detection_sound", default=False, action="store_true", 
                        help="OCRの結果をクリップボードにコピーした時に音を流すかどうか。デフォルトは'False'")

    parser.add_argument("-r", "--result_print", default=False, action="store_true", 
                        help="OCRの結果をコマンドプロンプトに出力するかどうか。デフォルトは'False'")

    args = parser.parse_args()
    return args

def preprocessing(path):
    import pyocr

    pyocr.tesseract.TESSERACT_CMD = path
    tools = pyocr.get_available_tools()
    try:
        tool = tools[0]
    except IndexError:
        print("\ntesseract.exeまでのパスが正しくありません。できる限り絶対パスを使用してください。")
        sys.exit()

    builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)

    return tool, builder

def main():

    args = command_line_argument()
    tool, builder = preprocessing(args.path_to_tesseract)

    print("\n起動中...\n")

    X = 0
    Y = 1

    while True:
        time.sleep(args.standby_time)
        try:#稀にエラーが出ることがある　繰り返すとエラーは出ない
            new_image = ImageGrab.grabclipboard()
        except:
            continue

        if new_image == None:
            continue

        #OCR処理の実行
        result = tool.image_to_string (
            new_image,
            lang = args.language,
            builder = builder
        )

        #利用する辞書、リスト、変数の初期化
        result_dict = {'up_left': [],
                       'down_left': [],
                       'down_right':[], 
                       "text":[]
                       }

        create_text_composition = []
        jpn_language_list = []
        output_text = []
        front_space = ""
        end_space = ""
        space_flag = 0
        jpn_flag = 0

        # インデントの基準値を取得。可読性向上のため、リストではなく辞書に挿入
        det_position = tuple(result[0].position)
        result_dict["up_left"].append(det_position[0])
        result_dict["down_right"].append(det_position[1])

        #OCR結果を展開
        for detection_list in result:
            det_text = detection_list.content
            det_position = tuple(detection_list.position)
            result_dict["down_left"].append((det_position[0][0], det_position[1][1]))
            result_dict["text"].append(det_text)

        # 改行、インデントの基準値を計算
        paragraph_threshold = (result_dict["down_left"][0][Y] - result_dict["up_left"][0][Y]) * args.paragraph_threshold_value
        space = (result_dict["down_right"][0][X] - result_dict["down_left"][0][X]) / len(result_dict["text"][0])
        standard_space_value = result_dict["down_left"][0][X]

        # 改行、インデントを適切に挿入する
        for index in range(len(result_dict["text"])-1):
            diff = result_dict["down_left"][index+1][Y] - result_dict["down_left"][index][Y]
            space_flag, end_space = (1, "\n") if diff > paragraph_threshold else (0, " ")
            create_text_composition.append(front_space + result_dict["text"][index] + end_space)
            front_space = " " * int(np.round((result_dict["down_left"][index+1][X] - standard_space_value) / space, decimals=0)) if space_flag == 1 else ""

        create_text_composition.append(front_space + result_dict["text"][-1])

        # テキストを一次元にする
        join_text = "".join(create_text_composition)

        # 日本語が入っている場合、分かち書きの不要な空白を削除
        for i in range(len(join_text) - 1):

            if join_text[i].isascii() == False or join_text[i+1].isascii() == False:
                jpn_language_list.append(join_text[i])
                jpn_flag = 1
                continue

            else :
                if jpn_flag == 0:
                    output_text.append(join_text[i])

                else:
                    output_text.append(("".join(jpn_language_list) + join_text[i]).replace(" ", ""))
                    jpn_language_list = []
                    jpn_flag = 0
                    
        if not jpn_language_list == []:
            output_text.append("".join(jpn_language_list).replace(" ", ""))
            
        output_text.append(join_text[-1])

        # テキストを一次元にする
        output_text = "".join(output_text)

        # クリップボードにOCR結果をコピーする
        pyperclip.copy(output_text)

        # result_printがTrueの場合にOCR結果を表示する
        if args.result_print:
            print(output_text)
            print("\n============================\n")

        # exit_detection_soundがTrueの場合に処理終了を通知する
        if args.exit_detection_sound:
            import winsound
            winsound.PlaySound("./", winsound.SND_FILENAME)

if __name__ == '__main__':
    main()


