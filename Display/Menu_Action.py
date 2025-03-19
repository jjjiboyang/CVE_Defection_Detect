from CamGrab.Camera1 import camera_grab_1
from CamGrab.Camera2 import camera_grab_2
from multiprocessing import Process

class MenuAction:
    def __init__(self,ui,log_queue):
        self.ui=ui
        self.log_queue=log_queue
        self.camera_grab_1 = Process(target=camera_grab_1,args=(self.log_queue,))
        self.camera_grab_2 = Process(target=camera_grab_2,args=(self.log_queue,))
        self.ui.menu_2.setStyleSheet("Margin:10px")
        self.ui.actionOpen_Camera.triggered.connect(self.open_camera)
        self.ui.actionClose_Camera.triggered.connect(self.close_camera)
        self.ui.actionOpen_Camera.trigger()

    def open_camera(self):
        self.ui.actionOpen_Camera.setEnabled(False)
        self.ui.actionClose_Camera.setEnabled(True)
        if self.camera_grab_1 is None or not self.camera_grab_1.is_alive():
            self.camera_grab_1 = Process(target=camera_grab_1, args=(self.log_queue,))
        if self.camera_grab_2 is None or not self.camera_grab_2.is_alive():
            self.camera_grab_2 = Process(target=camera_grab_2,args=(self.log_queue,))
        # 启动采集图像的进程
        try:
            self.camera_grab_1.start()
            self.camera_grab_2.start()
        except Exception as e:
            self.log_queue.put(str(e))

    def close_camera(self):
        self.ui.actionOpen_Camera.setEnabled(True)
        self.ui.actionClose_Camera.setEnabled(False)
        # 关闭采集图像的进程
        self.camera_grab_1.terminate()
        self.camera_grab_2.terminate()
