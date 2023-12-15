# coding: utf-8
from PIL import ImageGrab
import pyperclip
import time
from paddleocr import PaddleOCR
import numpy as np
import cv2
import winsound

def image_resizer(image:np.array, width_size:int=None, hight_size:int=None):
    """
    画像を指定した値にリサイズします。width_size と hight は片方だけ入力してください。
    
    ----------
    Args:
        image: np.ndarray
            numpy 配列の画像
            
        width_size int: 
            出力する画像の幅、高さは自動的に等倍されます
            
        hight_size int: 
        出力する画像の高さ、幅は自動的に等倍されます
        
    ----------
    Returns:
        np.ndarray: リサイズした画像 
    """
    import cv2
    import numpy as np
    image = image.copy()
    x, y = image.shape[:2]
    
    if width_size != None and hight_size == None:
        diff = width_size-y
        x += (x * np.round(diff/y, 3))
        y = width_size
        
    elif  hight_size != None and width_size == None:
        diff = hight_size-x
        y += (y * np.round(diff/x, 3))
        x = hight_size
        
    return cv2.resize(image, dsize=(int(y), int(x)))
    
def launch_program():
    return PaddleOCR(
        use_gpu=False,
        lang = "en",
        rec_bath_num=1,
        cpu_threads=14,
        ocr_version='PP-OCRv4',
        det_limit_side_len=1000
        )

def predict():
    ocr = launch_program()
    X = 0
    Y = 1
    while True:
        time.sleep(1)
        try:
            new_image = ImageGrab.grabclipboard()
        except:
            print("画像の読み込みに失敗")#稀にエラーが出ることがある　繰り返すとエラーは出ない
            continue
        if new_image == None:
            continue
        start = time.time()
        
        print("shape_print")
        print(np.array(new_image).shape)

        ocr_image = image_resizer(np.array(new_image.convert("RGB"), dtype=np.uint8), 1000)
        # ret, dst = cv2.threshold(new_image, 0, 255, cv2.THRESH_OTSU)
        print("this image shape")
        print(ocr_image.shape)
        y, x = ocr_image.shape[:2]
        padding_size = x - y
        if padding_size > 5:
            padding = int(padding_size / 6)
            ocr_image = cv2.copyMakeBorder(ocr_image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, (0,0,0))

        # cv2.imshow("ew", ocr_image)
        # cv2.waitKey(0)

        result = ocr.ocr(img=ocr_image, det=True, rec=True, cls=False)

        space_flag = 0
        new_text = []
        front_space = ""
        end_space = ""
        res_dct = {'up_left':[],'down_left':[],'down_right':[], "text":[]}

        if result == [[]]:
            print("テキストが検出できませんでした。")
            continue

        for detection_list in result[0]:
            up_left = tuple([int(i) for i in detection_list[0][0]]) #左上
            # up_right = tuple([int(i) for i in detection_list[0][1]]) #右上
            down_right = tuple([int(i) for i in detection_list[0][2]]) #右下
            down_left = tuple([int(i) for i in detection_list[0][3]]) #左下

            res_dct["up_left"].append(up_left)
            res_dct["down_left"].append(down_left)
            res_dct["down_right"].append(down_right)
            res_dct["text"].append(detection_list[-1][0].replace("\n", ""))

        new_line_threshold = (res_dct["down_left"][0][Y] - res_dct["up_left"][0][Y])

        space = (res_dct["down_right"][0][X] - res_dct["down_left"][0][X]) / len(res_dct["text"][0])

        space_reference = res_dct["down_left"][0][X]
        for index in range(len(res_dct["text"])-1):

            diff = res_dct["down_left"][index+1][Y] - res_dct["down_left"][index][Y]
            # diffがマイナスになるとき（後ろの文字のほうが座標が高くなる時に文字が入れ替わる）　改行しないかつ値がマイナスの時の分岐を入れないといけない

            space_flag, end_space = (1, "\n") if diff > new_line_threshold / 2 else (0, " ")
            new_text.append(front_space + res_dct["text"][index] + end_space)

            front_space = " " * int(np.round((res_dct["down_left"][index+1][X] - space_reference) / space, decimals=0)) if space_flag == 1 else "" #"" or " "
            print(int(np.round((diff - new_line_threshold) / new_line_threshold, decimals=0)))
            new_text.append("\n" * int(np.round((diff - new_line_threshold*2) / new_line_threshold, decimals=0)))

        new_text.append(front_space + res_dct["text"][-1])

        pyperclip.copy("".join(new_text))
        winsound.PlaySound("./", winsound.SND_FILENAME)
        end = time.time()
        print("==============")
        print(f"pred_time : {int(end-start)} / s")
        print(res_dct)

if __name__ == '__main__':
    predict()

