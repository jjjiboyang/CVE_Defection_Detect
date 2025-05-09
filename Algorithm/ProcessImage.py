import os
import queue
import traceback
from datetime import datetime
import cv2
import numpy as np
import CamGrab.datatype_pb2 as datatype_pb2
import ecal.core.core as ecal_core
import sys
import halcon as ha
import time

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Detect:
    def __init__(self, defect_types,log_queue):
        model1 = str(source_path(os.path.join("res", "model_water.hdl")))
        model2 = str(source_path(os.path.join("res", "model_black.hdl")))

        # 读取神经网络模型
        self.DLModelHandle_water = ha.read_dl_model(model1)
        self.DLModelHandle_black = ha.read_dl_model(model2)
        # 设置模型参数
        ha.set_dl_model_param(self.DLModelHandle_water, 'runtime', 'gpu')
        ha.set_dl_model_param(self.DLModelHandle_black, 'runtime', 'gpu')
        # 生成一个样本字典
        self.DLSample = ha.create_dict()
        self.DLSample_black = ha.create_dict()
        # 需要剔除的缺陷种类
        self.defect_type_1 = defect_types[0]
        self.defect_type_2 = defect_types[1]
        self.defect_type_3 = defect_types[2]
        self.defect_type_4 = defect_types[3]

        self.log_queue = log_queue

    def detect(self, Image, filename):
        try:
            FOLDER = f"./All_Images/{(datetime.now().strftime('%Y-%m-%d'))}"
            RectanglePoints = []
            ImageScaled = ha.scale_image(Image, 1.5, -50)
            ImageMedian = ha.median_image(ImageScaled, 'circle', 3, 'mirrored')
            # 计算偏差图
            ImageDeviation = ha.deviation_image(ImageMedian, 3, 21)
            # 进行阈值处理
            Region = ha.var_threshold(ImageDeviation, 30, 30, 0.2, 6, 'light')
            # 连通域分析
            ConnectedRegions = ha.connection(Region)
            # 填充连通域
            RegionFillUp = ha.fill_up(ConnectedRegions)

            Area, Row, Column = ha.area_center(RegionFillUp)
            Height, Width, Ratio = ha.height_width_ratio(RegionFillUp)
            gray_min, gray_max, Range = ha.min_max_gray(RegionFillUp, Image, 0)
            gray_mean, Deviation = ha.intensity(RegionFillUp, Image)

            # 定义规则类别
            # 长条划痕
            if self.defect_type_1 == 0:
                class1 = [0]
            else:
                aa = ha.tuple_greater_elem(Area, 400)
                bb = ha.tuple_greater_elem(Height, 600)
                cc = ha.tuple_greater_elem(2000, Height)
                dd = ha.tuple_greater_elem(10, Deviation)
                class1 = list(map(lambda x, y, z, w: x & y & z & w, aa, bb, cc, dd))

            # 水斑
            if self.defect_type_2 == 0:
                class2 = [0]
            else:
                a = ha.tuple_greater_elem(Area, 600)
                b = ha.tuple_greater_elem(5000, Area)
                c = ha.tuple_greater_elem(gray_max, 200)
                d = ha.tuple_greater_elem(gray_mean, 150)
                e = ha.tuple_greater_elem(100, Height)
                class2 = list(map(lambda x, y, z, w, t: x & y & z & w & t, a, b, c, d, e))

            # 糊料
            if self.defect_type_3 == 0:
                class3 = [0]
                class5 = [0]
            else:
                a = ha.tuple_greater_elem(Area, 120)
                b = ha.tuple_greater_elem(90, gray_min)
                c = ha.tuple_greater_elem(150, gray_mean)
                d = ha.tuple_greater_elem(2000, Height)
                class3 = list(map(lambda x, y, z, w: x & y & z & w, a, b, c, d))

                # 特大缺陷
                a = ha.tuple_greater_elem(Area, 5000)
                b = ha.tuple_greater_elem(2000, Height)
                c = ha.tuple_greater_elem(Width, 80)
                class5 = list(map(lambda x, y, z: x & y & z, a, b, c))

            # 连续晶圆和塑化不良
            if self.defect_type_4 == 0:
                class4 = [0]
            else:
                a = ha.tuple_greater_elem(Area, 300)
                b = ha.tuple_greater_elem(600, Area)
                c = ha.tuple_greater_elem(100, Height)
                class4 = list(map(lambda x, y, z: x & y & z, a, b, c))

            sum1 = ha.tuple_sum(class1)[0]
            sum2 = ha.tuple_sum(class2)[0]
            sum3 = ha.tuple_sum(class3)[0]
            sum4 = ha.tuple_sum(class4)[0]
            sum5 = ha.tuple_sum(class5)[0]

            # 提取每类索引
            class1_index = ha.tuple_find(class1, 1)
            class1_index = [x + 1 for x in class1_index]
            class2_index = ha.tuple_find(class2, 1)
            class2_index = [x + 1 for x in class2_index]
            class3_index = ha.tuple_find(class3, 1)
            class3_index = [x + 1 for x in class3_index]
            class4_index = ha.tuple_find(class4, 1)
            class4_index = [x + 1 for x in class4_index]
            class5_index = ha.tuple_find(class5, 1)
            class5_index = [x + 1 for x in class5_index]

            # 如果有特大缺陷
            if sum5 > 0:
                Region5 = ha.select_obj(RegionFillUp, class5_index)
                # 找到最小外接矩形
                Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(Region5)
                for K in range(1, sum5 + 1):
                    # 传入缺陷区域矩形参数
                    RectanglePoints.append([Row1[K - 1], Column1[K - 1], Row2[K - 1], Column2[K - 1]])
                return "3", RectanglePoints

            # 提取区域
            if sum1 > 0:
                Region1 = ha.select_obj(RegionFillUp, class1_index)
                # 找到最小外接矩形
                Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(Region1)
                # 创建矩形区域
                Rectangle = ha.gen_rectangle1(Row1, Column1, Row2, Column2)
                # 膨胀矩形区域
                RegionDilation = ha.dilation_rectangle1(Rectangle, 32, 32)
                # 重新计算最小外接矩形
                Row11, Column11, Row21, Column21 = ha.smallest_rectangle1(RegionDilation)
                # 裁剪图像
                ImageCrop = ha.crop_rectangle1(Image, Row11, Column11, Row21, Column21)

                # 判断有无水珠
                ImageConverted = ha.convert_image_type(ImageCrop, 'real')
                ImageZoom = ha.zoom_image_size(ImageConverted, 40, 100, 'constant')
                ImageScaled1 = ha.scale_image(ImageZoom, 1, -127)

                for K in range(1, sum1 + 1):
                    # 选择对象
                    ImageSingle = ha.select_obj(ImageScaled1, K)
                    ImageSave = ha.select_obj(ImageCrop, K)
                    ha.set_dict_object(ImageSingle, self.DLSample, 'image')
                    # 对处理后的样本字典送进模型进行推理，得到推理结果
                    DLResult = ha.apply_dl_model(self.DLModelHandle_water, [self.DLSample], [])
                    ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                    if not ImageClass[0]:
                        # 传入缺陷区域矩形参数
                        RectanglePoints.append([Row11[K - 1], Column11[K - 1], Row21[K - 1], Column21[K - 1]])
                        # 保存图像
                        os.makedirs(f"{FOLDER}/out_long", exist_ok=True)
                        output_path = f"{FOLDER}/out_long/{filename}_{K}.png"
                        ha.write_image(ImageSave, 'png', 0, output_path)
                        break
                    else:
                        # os.makedirs(f"{FOLDER}/out_water", exist_ok=True)
                        # output_path = f'{FOLDER}/out_water/{filename}_{K}.png'
                        # ha.write_image(ImageSave, 'png', 0, output_path)
                        sum1 -= 1

                if sum1 > 0:
                    return "1", RectanglePoints

            if sum2 > 0:
                Region2 = ha.select_obj(RegionFillUp, class2_index)
                # 找到最小外接矩形
                Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(Region2)
                # 创建矩形区域
                Rectangle = ha.gen_rectangle1(Row1, Column1, Row2, Column2)
                # 膨胀矩形区域
                RegionDilation = ha.dilation_rectangle1(Rectangle, 32, 32)
                # 重新计算最小外接矩形
                Row11, Column11, Row21, Column21 = ha.smallest_rectangle1(RegionDilation)
                # 裁剪图像
                ImageCrop = ha.crop_rectangle1(Image, Row11, Column11, Row21, Column21)

                # 判断有无水珠
                ImageConverted = ha.convert_image_type(ImageCrop, 'real')
                ImageZoom = ha.zoom_image_size(ImageConverted, 40, 100, 'constant')
                ImageScaled1 = ha.scale_image(ImageZoom, 1, -127)

                for K in range(1, sum2 + 1):
                    # 选择对象
                    ImageSingle = ha.select_obj(ImageScaled1, K)
                    ImageSave = ha.select_obj(ImageCrop, K)
                    ha.set_dict_object(ImageSingle, self.DLSample, 'image')
                    # 对处理后的样本字典送进模型进行推理，得到推理结果
                    DLResult = ha.apply_dl_model(self.DLModelHandle_water, [self.DLSample], [])
                    ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                    if not ImageClass[0]:
                        # 传入缺陷区域矩形参数
                        RectanglePoints.append([Row11[K - 1], Column11[K - 1], Row21[K - 1], Column21[K - 1]])
                        # 保存图像
                        os.makedirs(f"{FOLDER}/out_jingyuan", exist_ok=True)
                        output_path = f'{FOLDER}/out_jingyuan/{filename}_{K}.png'
                        ha.write_image(ImageSave, 'png', 0, output_path)
                        break
                    else:
                        # os.makedirs(f"{FOLDER}/out_water", exist_ok=True)
                        # output_path = f'{FOLDER}/out_water/{filename}_{K}.png'
                        # ha.write_image(ImageSave, 'png', 0, output_path)
                        sum2 -= 1

                if sum2 > 0:
                    return "2", RectanglePoints

            if sum3 > 0:
                Region3 = ha.select_obj(RegionFillUp, class3_index)
                # 找到最小外接矩形
                Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(Region3)
                # 创建矩形区域
                Rectangle = ha.gen_rectangle1(Row1, Column1, Row2, Column2)
                # 膨胀矩形区域
                RegionDilation = ha.dilation_rectangle1(Rectangle, 32, 32)
                # 重新计算最小外接矩形
                Row11, Column11, Row21, Column21 = ha.smallest_rectangle1(RegionDilation)
                # 裁剪图像
                ImageCrop = ha.crop_rectangle1(Image, Row11, Column11, Row21, Column21)

                # 判断有无水珠
                ImageConverted = ha.convert_image_type(ImageCrop, 'real')
                ImageZoom = ha.zoom_image_size(ImageConverted, 40, 100, 'constant')
                ImageScaled1 = ha.scale_image(ImageZoom, 1, -127)

                for K in range(1, sum3 + 1):
                    # 选择对象
                    ImageSingle = ha.select_obj(ImageScaled1, K)
                    ImageSave = ha.select_obj(ImageCrop, K)
                    ha.set_dict_object(ImageSingle, self.DLSample, 'image')
                    # 对处理后的样本字典送进模型进行推理，得到推理结果
                    DLResult = ha.apply_dl_model(self.DLModelHandle_water, [self.DLSample], [])
                    ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                    if not ImageClass[0]:
                        ha.set_dict_object(ImageSingle, self.DLSample_black, 'image')
                        DLResult_black = ha.apply_dl_model(self.DLModelHandle_black, [self.DLSample_black], [])
                        ImageClass_black = ha.get_dict_tuple(DLResult_black[0], 'classification_class_ids')
                        if not ImageClass_black[0]:
                            # 传入缺陷区域矩形参数
                            RectanglePoints.append([Row11[K - 1], Column11[K - 1], Row21[K - 1], Column21[K - 1]])
                            # 保存图像
                            os.makedirs(f"{FOLDER}/out_black", exist_ok=True)
                            output_path = f'{FOLDER}/out_black/{filename}_{K}.png'
                            ha.write_image(ImageSave, 'png', 0, output_path)
                            break
                        else:
                            # os.makedirs(f"{FOLDER}/out_noblack", exist_ok=True)
                            # output_path = f'{FOLDER}/out_noblack/{filename}_{K}.png'
                            # ha.write_image(ImageSave, 'png', 0, output_path)
                            sum3 -= 1
                    else:
                        # os.makedirs(f"{FOLDER}/out_water", exist_ok=True)
                        # output_path = f'{FOLDER}/out_water/{filename}_{K}.png'
                        # ha.write_image(ImageSave, 'png', 0, output_path)
                        sum3 -= 1

                if sum3 > 0:
                    return "3", RectanglePoints

            if sum4 >= 6:
                count = 0
                Region4 = ha.select_obj(RegionFillUp, class4_index)
                # 找到最小外接矩形
                Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(Region4)
                # 创建矩形区域
                Rectangle = ha.gen_rectangle1(Row1, Column1, Row2, Column2)
                # 膨胀矩形区域
                RegionDilation = ha.dilation_rectangle1(Rectangle, 32, 32)
                # 重新计算最小外接矩形
                Row11, Column11, Row21, Column21 = ha.smallest_rectangle1(RegionDilation)
                # 裁剪图像
                ImageCrop = ha.crop_rectangle1(Image, Row11, Column11, Row21, Column21)

                # 判断有无水珠
                ImageConverted = ha.convert_image_type(ImageCrop, 'real')
                ImageZoom = ha.zoom_image_size(ImageConverted, 40, 100, 'constant')
                ImageScaled1 = ha.scale_image(ImageZoom, 1, -127)

                for K in range(1, sum4 + 1):
                    # 选择对象
                    ImageSingle = ha.select_obj(ImageScaled1, K)
                    ImageSave = ha.select_obj(ImageCrop, K)
                    ha.set_dict_object(ImageSingle, self.DLSample, 'image')
                    # 对处理后的样本字典送进模型进行推理，得到推理结果
                    DLResult = ha.apply_dl_model(self.DLModelHandle_water, [self.DLSample], [])
                    ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                    if not ImageClass[0]:
                        # 传入缺陷区域矩形参数
                        RectanglePoints.append([Row11[K - 1], Column11[K - 1], Row21[K - 1], Column21[K - 1]])
                        # 保存图像
                        os.makedirs(f"{FOLDER}/out_continue", exist_ok=True)
                        output_path = f'{FOLDER}/out_continue/{filename}_{K}.png'
                        ha.write_image(ImageSave, 'png', 0, output_path)
                        count += 1
                        if count >= 6:
                            return "4", RectanglePoints
                    else:
                        # os.makedirs(f"{FOLDER}/out_water", exist_ok=True)
                        # output_path = f'{FOLDER}/out_water/{filename}_{K}.png'
                        # ha.write_image(ImageSave, 'png', 0, output_path)
                        sum4 -= 1

            return "0", RectanglePoints

        except Exception as e:
            error_message = str(e)
            tb = traceback.extract_tb(e.__traceback__)
            filename, line, func, text = tb[-1]
            detail_message = f"文件: {filename}, 行号: {line}, 函数: {func}, 代码: {text}, 错误信息: {error_message}"
            # 把错误信息+完整日志内容放进队列
            self.log_queue.put((error_message, detail_message))


class ProcessImage:
    def __init__(self, save_choice, image_encoder_queue, defect_types,log_queue):
        self.img_queue = queue.Queue()
        self.save_choice = save_choice
        self.image_encoder_queue = image_encoder_queue
        self.cam_num = 0
        self.Detect = Detect(defect_types,log_queue)
        self.log_queue = log_queue
        ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
        sub_1 = ecal_core.subscriber('defect_detection_topic_1')
        sub_2 = ecal_core.subscriber('defect_detection_topic_2')

        sub_1.set_callback(self.callback)
        sub_2.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        received_message = datatype_pb2.ImageParameters()
        received_message.ParseFromString(msg)
        self.img_queue.put([received_message, topic_name[-1:]])

    def detect_defects(self):
        try:
            ecal_core.initialize(sys.argv, "Processed Image Publisher")
            pub = ecal_core.publisher('ProcessedImage')
            last_cam1_encoder_value = 0
            last_cam2_encoder_value = 0
            while ecal_core.ok():
                # print("size:",self.img_queue.qsize())
                if not self.img_queue.empty():
                    start_t = time.time()
                    data = self.img_queue.get()
                    image_msg = data[0]
                    self.cam_num = data[1]
                    np_arr = np.frombuffer(image_msg.data, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
                    # 将 NumPy 数组转换为 Halcon 图像
                    halcon_image = ha.himage_from_numpy_array(img)
                    timestamp = image_msg.timestamp
                    image_filename = f"./All_Images/{datetime.now().strftime('%Y-%m-%d')}/defect_images/{self.cam_num}_{timestamp}.bmp"
                    image_msg.filename = image_filename
                    if last_cam1_encoder_value == 0:
                        last_cam1_encoder_value = image_msg.encoder_value
                        continue
                    if last_cam2_encoder_value == 0:
                        last_cam2_encoder_value = image_msg.encoder_value
                        continue
                    defect_type_num, Points = self.Detect.detect(halcon_image, image_msg.encoder_value)

                    if defect_type_num != "0":
                        # self.logger.info(f"Defect Type: {defect_type_num},Area:{Points}")
                        if self.cam_num == '1':
                            self.image_encoder_queue.put(last_cam1_encoder_value)
                        elif self.cam_num == '2':
                            self.image_encoder_queue.put(last_cam2_encoder_value)
                        self.image_encoder_queue.put(image_msg.encoder_value)

                        # **添加多个区域**
                        for point in Points:  # 假设 Points 里存的是 (row1, column1, row2, column2) 这样的缺陷区域
                            region = image_msg.regions.add()  # 添加一个 Region
                            region.row1 = point[0]
                            region.column1 = point[1]
                            region.row2 = point[2]
                            region.column2 = point[3]

                        image_msg.defect_type = defect_type_num
                        image_msg.is_blow = 1

                        serialized_message = image_msg.SerializeToString()
                        pub.send(serialized_message)

                    elif self.save_choice == 0:
                        image_msg.defect_type = "0"
                        serialized_message = image_msg.SerializeToString()
                        pub.send(serialized_message)

                    if self.cam_num == '1':
                        last_cam1_encoder_value = image_msg.encoder_value
                    elif self.cam_num == '2':
                        last_cam2_encoder_value = image_msg.encoder_value

                    end_t = time.time()
                    # print("total:", float(end_t - start_t) * 1000.0, "ms")

        except Exception as e:
            error_message = str(e)
            tb = traceback.extract_tb(e.__traceback__)
            filename, line, func, text = tb[-1]
            detail_message = f"文件: {filename}, 行号: {line}, 函数: {func}, 代码: {text}, 错误信息: {error_message}"
            # 把错误信息+完整日志内容放进队列
            self.log_queue.put((error_message, detail_message))


def run_ImageProcessing(save_choice, image_encoder_queue, defect_types,log_queue):
    process = ProcessImage(save_choice, image_encoder_queue, defect_types,log_queue)
    process.detect_defects()
