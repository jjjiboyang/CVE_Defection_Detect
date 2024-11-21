import time
import cProfile
import cv2
import halcon as ha


class Detect:
    def __init__(self):
        # 读取神经网络模型
        self.DLModelHandle = ha.read_dl_model('C:/Users/16146/Desktop/Deep Learning/model_Compact.hdl')
        # 设置模型参数
        ha.set_dl_model_param(self.DLModelHandle, 'runtime', 'cpu')

    def detect(self, Image, filename):

        ImageMedian = ha.median_image(Image, 'circle', 3, 'mirrored')
        # 计算偏差图
        ImageDeviation = ha.deviation_image(ImageMedian, 3, 41)
        # 进行阈值处理
        Region = ha.var_threshold(ImageDeviation, 30, 30, 0.2, 6, 'light')
        # 连通域分析
        ConnectedRegions = ha.connection(Region)
        # 选择形状
        SelectedRegions = ha.select_shape(ConnectedRegions, 'area', 'and', 600, 3000)
        MultiRegions = ha.select_shape(ConnectedRegions, 'area', 'and', 150, 400)
        # 计数
        Number1 = ha.count_obj(SelectedRegions)
        Number2 = ha.count_obj(MultiRegions)

        if 1 <= Number1 <= 8:
            # 找到最小外接矩形
            Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(SelectedRegions)
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
            ImageZoom = ha.zoom_image_size(ImageConverted, 40, 80, 'constant')
            # 生成一个样本字典
            DLSample = ha.create_dict()
            # 计算裁剪图像中的对象数
            Number1 = ha.count_obj(ImageCrop)

            for K in range(1, Number1 + 1):
                # 选择对象
                ImageSingle = ha.select_obj(ImageZoom, K)
                ImageSave = ha.select_obj(ImageCrop, K)
                ha.set_dict_object(ImageSingle, DLSample, 'image')
                # 对处理后的样本字典送进模型进行推理，得到推理结果
                DLResult = ha.apply_dl_model(self.DLModelHandle, [DLSample], [])
                ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                if not ImageClass[0]:
                    # 保存图像
                    output_path = f'out_ok/{filename}_{K}.png'
                    ha.write_image(ImageSave, 'png', 0, output_path)
                    pass
                else:
                    Number1 -= 1

        if 4 <= Number2 <= 20:
            # 找到最小外接矩形
            Row1, Column1, Row2, Column2 = ha.smallest_rectangle1(MultiRegions)
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
            ImageZoom = ha.zoom_image_size(ImageConverted, 40, 80, 'constant')
            # 生成一个样本字典
            DLSample = ha.create_dict()
            # 计算裁剪图像中的对象数
            Number2 = ha.count_obj(ImageCrop)

            for K in range(1, Number2 + 1):
                # 选择对象
                ImageSingle = ha.select_obj(ImageZoom, K)
                ImageSave = ha.select_obj(ImageCrop, K)
                ha.set_dict_object(ImageSingle, DLSample, 'image')
                # 对处理后的样本字典送进模型进行推理，得到推理结果
                DLResult = ha.apply_dl_model(self.DLModelHandle, [DLSample], [])
                ImageClass = ha.get_dict_tuple(DLResult[0], 'classification_class_ids')
                if not ImageClass[0]:
                    # 保存图像
                    output_path = f'out_ok/{filename}_{K}.png'
                    ha.write_image(ImageSave, 'png', 0, output_path)
                else:
                    Number2 -= 1

            if Number2<4:
                Number2=0

        return Number2+Number1


if __name__ == '__main__':
    d=Detect()
    Image=cv2.imread("C:/Users/16146/Desktop/test/Image_20241106134908954.bmp",cv2.IMREAD_GRAYSCALE)
    halcon_image = ha.himage_from_numpy_array(Image)

    s=time.time()
    d.detect(halcon_image, 'a')
    e=time.time()
    print((e-s)*1000,"ms")
