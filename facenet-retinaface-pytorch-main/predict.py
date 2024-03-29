#----------------------------------------------------#
#   对视频中的predict.py进行了修改，
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time

import cv2
import numpy as np

from retinaface import Retinaface

def facex(userid):
    retinaface = Retinaface()
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'video'表示视频检测，可调用摄像头或者视频进行检测，详情查看下方注释。
    #   'fps'表示测试fps，使用的图片是img里面的street.jpg，详情查看下方注释。
    #   'dir_predict'表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #----------------------------------------------------------------------------------------------------------#
    mode = "predict"
    #----------------------------------------------------------------------------------------------------------#
    #   video_path用于指定视频的路径，当video_path=0时表示检测摄像头
    #   想要检测视频，则设置如video_path = "xxx.mp4"即可，代表读取出根目录下的xxx.mp4文件。
    #   video_save_path表示视频保存的路径，当video_save_path=""时表示不保存
    #   想要保存视频，则设置如video_save_path = "yyy.mp4"即可，代表保存为根目录下的yyy.mp4文件。
    #   video_fps用于保存的视频的fps
    #   video_path、video_save_path和video_fps仅在mode='video'时有效
    #   保存视频时需要ctrl+c退出或者运行到最后一帧才会完成完整的保存步骤。
    #----------------------------------------------------------------------------------------------------------#
    video_path      = 0
    video_save_path = ""
    video_fps       = 25.0
    #-------------------------------------------------------------------------#
    #   test_interval用于指定测量fps的时候，图片检测的次数
    #   理论上test_interval越大，fps越准确。
    #-------------------------------------------------------------------------#
    test_interval   = 100
    #-------------------------------------------------------------------------#
    #   dir_origin_path指定了用于检测的图片的文件夹路径
    #   dir_save_path指定了检测完图片的保存路径
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_origin_path = "C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main/img/"
    dir_save_path   = "C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main/img_out/"

    if mode == "predict":
        '''
        predict.py有几个注意点
        1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用cv2.imread打开图片文件进行预测。
        2、如果想要保存，利用cv2.imwrite("img.jpg", r_image)即可保存。
        3、如果想要获得框的坐标，可以进入detect_image函数，读取(b[0], b[1]), (b[2], b[3])这四个值。
        4、如果想要截取下目标，可以利用获取到的(b[0], b[1]), (b[2], b[3])这四个值在原图上利用矩阵的方式进行截取。
        5、在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
        '''
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        flag = cap.isOpened()
        index = 1
        while (flag):
            ret, frame = cap.read()
            cv2.imshow("Capture_Paizhao", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('s'):  # 按下s键，进入下面的保存图片操作
                cv2.imwrite("C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main/img/" + str(index) + ".jpg", frame)
                print("save" + str(index) + ".jpg successfuly!")
                index += 1
                break
        cap.release() # 释放摄像头
        cv2.destroyAllWindows()# 释放并销毁窗口
        while True:

            image = cv2.imread('C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main/img/1.jpg')
            if image is None:
                # print('Open Error! Try again!')
                continue
            else:
                image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                r_image = retinaface.detect_image(image)
                # r_image = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
                # cv2.imshow("after",r_image)
                # cv2.waitKey(0)
                break
            cap.release() # 释放摄像头
            cv2.destroyAllWindows()# 释放并销毁窗口
    if userid==r_image[1]:
            return 1
    else:
            return 0
