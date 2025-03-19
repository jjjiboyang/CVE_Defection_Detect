import sys
import cv2
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
import numpy as np
from CamGrab import datatype_pb2
from CamGrab.CameraParams_header import *
from CamGrab.MvCameraControl_class import *
from CamGrab.PixelType_header import *
from CamGrab.MvCameraControl_class import MvCamera


class Camera:
    def __init__(self,log_queue):
        self.device_list = None
        self.cam = None
        self.encoder_value = [0]
        self.log_queue = log_queue

        ecal_core.initialize(sys.argv, "Encoder Value Subscriber")
        sub = StringSubscriber("encoder_topic")
        sub.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        self.encoder_value[0] = int(msg)

    def OpenDevice(self):
        # ch:初始化SDK | en: initialize SDK
        MvCamera.MV_CC_Initialize()
        self.device_list = MV_CC_DEVICE_INFO_LIST()
        t_layer_type = (MV_GIGE_DEVICE | MV_USB_DEVICE | MV_GENTL_CAMERALINK_DEVICE
                        | MV_GENTL_CXP_DEVICE | MV_GENTL_XOF_DEVICE)

        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(t_layer_type, self.device_list)
        if ret != 0:
            print("error: enum devices fail! ret[0x%x]" % ret)

        # ch:创建相机实例 | en:Creat Camera Object
        self.cam = MvCamera()
        # ch:选择设备并创建句柄 | en:Select device and create handle
        current_device_info_1 = cast(self.device_list.pDeviceInfo[1], POINTER(MV_CC_DEVICE_INFO)).contents

        ret = self.cam.MV_CC_CreateHandle(current_device_info_1)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)

        # ch:打开设备 | en:Open device
        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            self.log_queue.put(("error: open device fail! ret[0x%x]" % ret,"error: open device fail! ret[0x%x]" % ret))
            print("open device fail! ret[0x%x]" % ret)
        else:
            self.log_queue.put(("open device successfully 2", "open device successfully 2"))
            print("open device successfully 2")

        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE self.camera)
        if current_device_info_1.nTLayerType == MV_GIGE_DEVICE or current_device_info_1.nTLayerType == MV_GENTL_GIGE_DEVICE:
            nPacketSize = self.cam.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = self.cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

        b_enable = c_bool(False)
        ret = self.cam.MV_CC_GetBoolValue("AcquisitionLineRateEnable", b_enable)
        if ret != 0:
            print("error: get AcquisitionLineRateEnable fail! ret[0x%x]" % ret)

    def StartGrab(self):
        # ch:开始取流 | en:Start grab image
        ret = self.cam.MV_CC_StartGrabbing()

        ecal_core.initialize(sys.argv, "Grab Image Publisher")
        pub = ecal_core.publisher(f'defect_detection_topic_2')

        out_frame_info = MV_FRAME_OUT()
        memset(byref(out_frame_info), 0, sizeof(out_frame_info))

        while True:
            ret = self.cam.MV_CC_GetImageBuffer(out_frame_info, 1000)

            if out_frame_info.pBufAddr is not None and 0 == ret:
                # 第一时间获取编码器的值
                encoder_value = self.encoder_value[0]
                # 获取图像的宽度和高度
                width = out_frame_info.stFrameInfo.nWidth
                height = out_frame_info.stFrameInfo.nHeight

                # 假设图像是 8-bit 灰度图或 24-bit RGB 图像（具体根据相机配置调整）
                if out_frame_info.stFrameInfo.enPixelType == PixelType_Gvsp_Mono8:
                    img_np = np.ctypeslib.as_array(out_frame_info.pBufAddr, shape=(height, width))
                    # 编码为字节流
                    is_success, buffer = cv2.imencode('.bmp', img_np)
                    image_msg = datatype_pb2.ImageParameters()
                    image_msg.data = buffer.tobytes()
                    image_msg.width = width
                    image_msg.height = height
                    image_msg.encoder_value = encoder_value
                    image_msg.timestamp = out_frame_info.stFrameInfo.nHostTimeStamp
                    serialized_message = image_msg.SerializeToString()
                    pub.send(serialized_message)
                else:
                    print("Unsupported pixel format")
                    continue
                ret = self.cam.MV_CC_FreeImageBuffer(out_frame_info)
            else:
                pass


def camera_grab_2(log_queue):
    cam = Camera(log_queue)
    cam.OpenDevice()
    cam.StartGrab()


if __name__ == "__main__":
    camera_grab_2()
