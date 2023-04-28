# -*- coding: utf-8 -*- 

import mediapipe as mp
from scipy.spatial import distance
import numpy as np  # 数据处理的库numpy
import cv2  # 图像处理的库OpenCv
import wx  # 构造显示界面的GUI
import wx.xrc
import wx.adv
import numpy as np  # 数据处理的库 numpy
import time
import math
import os

###########################################################################
## Class Fatigue_detecting
###########################################################################

COVER = 'D:/workspace/000GraduationDesign/fatigue_detecting-master/images/camera.png'


class Fatigue_detecting(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(873, 535),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_animCtrl1 = wx.adv.AnimationCtrl(self, wx.ID_ANY, wx.adv.NullAnimation, wx.DefaultPosition,
                                                wx.DefaultSize, wx.adv.AC_DEFAULT_STYLE)
        bSizer3.Add(self.m_animCtrl1, 1, wx.ALL | wx.EXPAND, 5)
        bSizer2.Add(bSizer3, 9, wx.EXPAND, 5)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)
        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"参数设置"), wx.VERTICAL)
        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"视频源"), wx.VERTICAL)
        gSizer1 = wx.GridSizer(0, 2, 0, 8)
        m_choice1Choices = [u"摄像头ID_0", u"摄像头ID_1", u"摄像头ID_2"]
        self.m_choice1 = wx.Choice(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(90, 25),
                                   m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        gSizer1.Add(self.m_choice1, 0, wx.ALL, 5)
        self.camera_button1 = wx.Button(sbSizer2.GetStaticBox(), wx.ID_ANY, u"开始检测", wx.DefaultPosition,
                                        wx.Size(90, 25), 0)
        gSizer1.Add(self.camera_button1, 0, wx.ALL, 5)
        self.vedio_button2 = wx.Button(sbSizer2.GetStaticBox(), wx.ID_ANY, u"打开视频文件", wx.DefaultPosition,
                                       wx.Size(90, 25), 0)
        gSizer1.Add(self.vedio_button2, 0, wx.ALL, 5)

        self.off_button3 = wx.Button(sbSizer2.GetStaticBox(), wx.ID_ANY, u"暂停", wx.DefaultPosition, wx.Size(90, 25), 0)
        gSizer1.Add(self.off_button3, 0, wx.ALL, 5)
        sbSizer2.Add(gSizer1, 1, wx.EXPAND, 5)
        sbSizer1.Add(sbSizer2, 2, wx.EXPAND, 5)
        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"疲劳检测"), wx.VERTICAL)
        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.yawn_checkBox1 = wx.CheckBox(sbSizer3.GetStaticBox(), wx.ID_ANY, u"打哈欠检测", wx.Point(-1, -1),
                                          wx.Size(-1, 15), 0)
        self.yawn_checkBox1.SetValue(True)
        bSizer5.Add(self.yawn_checkBox1, 0, wx.ALL, 5)
        self.blink_checkBox2 = wx.CheckBox(sbSizer3.GetStaticBox(), wx.ID_ANY, u"闭眼检测", wx.Point(-1, -1),
                                           wx.Size(-1, 15), 0)
        self.blink_checkBox2.SetValue(True)
        bSizer5.Add(self.blink_checkBox2, 0, wx.ALL, 5)
        sbSizer3.Add(bSizer5, 1, wx.EXPAND, 5)
        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.nod_checkBox7 = wx.CheckBox(sbSizer3.GetStaticBox(), wx.ID_ANY, u"点头检测", wx.Point(-1, -1), wx.Size(-1, 15),
                                         0)
        self.nod_checkBox7.SetValue(True)
        bSizer6.Add(self.nod_checkBox7, 0, wx.ALL, 5)
        self.m_staticText1 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"疲劳时间(秒):", wx.DefaultPosition,
                                           wx.Size(-1, 15), 0)
        self.m_staticText1.Wrap(-1)
        bSizer6.Add(self.m_staticText1, 0, wx.ALL, 5)
        m_listBox2Choices = [u"3", u"4", u"5", u"6", u"7", u"8"]
        self.m_listBox2 = wx.ListBox(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(50, 24),
                                     m_listBox2Choices, 0)
        bSizer6.Add(self.m_listBox2, 0, 0, 5)
        sbSizer3.Add(bSizer6, 1, wx.EXPAND, 5)
        sbSizer1.Add(sbSizer3, 2, 0, 5)
        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"脱岗检测"), wx.VERTICAL)
        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_checkBox4 = wx.CheckBox(sbSizer4.GetStaticBox(), wx.ID_ANY, u"脱岗检测", wx.DefaultPosition, wx.Size(-1, 15),
                                       0)
        self.m_checkBox4.SetValue(True)
        bSizer8.Add(self.m_checkBox4, 0, wx.ALL, 5)
        self.m_staticText2 = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"脱岗时间(秒):", wx.DefaultPosition,
                                           wx.Size(-1, 15), 0)
        self.m_staticText2.Wrap(-1)
        bSizer8.Add(self.m_staticText2, 0, wx.ALL, 5)
        m_listBox21Choices = [u"5", u"10", u"15", u"20", u"25", u"30"]
        self.m_listBox21 = wx.ListBox(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(50, 24),
                                      m_listBox21Choices, 0)
        bSizer8.Add(self.m_listBox21, 0, 0, 5)
        sbSizer4.Add(bSizer8, 1, 0, 5)
        sbSizer1.Add(sbSizer4, 1, 0, 5)
        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"分析区域"), wx.VERTICAL)
        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText3 = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"检测区域：   ", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        bSizer9.Add(self.m_staticText3, 0, wx.ALL, 5)
        m_choice2Choices = [u"全视频检测", u"部分区域选取"]
        self.m_choice2 = wx.Choice(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   m_choice2Choices, 0)
        self.m_choice2.SetSelection(0)
        bSizer9.Add(self.m_choice2, 0, wx.ALL, 5)
        sbSizer5.Add(bSizer9, 1, wx.EXPAND, 5)
        sbSizer1.Add(sbSizer5, 1, 0, 5)
        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"状态输出"), wx.VERTICAL)
        self.m_textCtrl3 = wx.TextCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, wx.TE_MULTILINE | wx.TE_READONLY)
        sbSizer6.Add(self.m_textCtrl3, 1, wx.ALL | wx.EXPAND, 5)
        sbSizer1.Add(sbSizer6, 5, wx.EXPAND, 5)
        bSizer4.Add(sbSizer1, 1, wx.EXPAND, 5)
        bSizer2.Add(bSizer4, 3, wx.EXPAND, 5)
        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        self.m_choice1.Bind(wx.EVT_CHOICE, self.cameraid_choice)  # 绑定事件
        self.camera_button1.Bind(wx.EVT_BUTTON, self.camera_on)  # 开
        self.vedio_button2.Bind(wx.EVT_BUTTON, self.vedio_on)
        self.off_button3.Bind(wx.EVT_BUTTON, self.off)  # 关

        self.m_listBox2.Bind(wx.EVT_LISTBOX, self.AR_CONSEC_FRAMES)  # 闪烁阈值设置
        self.m_listBox21.Bind(wx.EVT_LISTBOX, self.OUT_AR_CONSEC_FRAMES)  # 脱岗时间设置

        # 封面图片
        self.image_cover = wx.Image(COVER, wx.BITMAP_TYPE_ANY)
        # 显示图片在m_animCtrl1上
        self.bmp = wx.StaticBitmap(self.m_animCtrl1, -1, wx.Bitmap(self.image_cover))

        # 设置窗口标题的图标
        self.icon = wx.Icon('../images/123.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        # 系统事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        print("wxpython界面初始化加载完成！")

        """参数"""
        # 默认为摄像头0
        self.VIDEO_STREAM = 0
        self.CAMERA_STYLE = False  # False未打开摄像头，True摄像头已打开
        # 闪烁阈值（秒）
        self.AR_CONSEC_FRAMES_check = 3
        self.OUT_AR_CONSEC_FRAMES_check = 60
        # 眼睛长宽比
        self.EYE_AR_THRESH = 0.31
        self.EYE_AR_CONSEC_FRAMES = self.AR_CONSEC_FRAMES_check
        # 打哈欠长宽比
        self.MAR_THRESH = 1.0
        self.MOUTH_AR_CONSEC_FRAMES = self.AR_CONSEC_FRAMES_check * 2
        # 瞌睡点头
        self.HAR_THRESH = 90
        self.NOD_AR_CONSEC_FRAMES = self.AR_CONSEC_FRAMES_check * 3

        """计数"""
        # 初始化帧计数器和眨眼总数
        self.COUNTER = 0
        self.TOTAL = 0
        # 初始化帧计数器和打哈欠总数
        self.mCOUNTER = 0
        self.mTOTAL = 0
        # 初始化帧计数器和点头总数
        self.hCOUNTER = 0
        self.hTOTAL = 0
        # 离职时间长度
        self.oCOUNTER = 0

    def __del__(self):
        pass

    def get_euler_angles(self, rotation_matrix):
        sy = np.sqrt(rotation_matrix[0][0] * rotation_matrix[0][0] + rotation_matrix[1][0] * rotation_matrix[1][0])
        singular = sy < 1e-6
        if not singular:
            x = np.arctan2(rotation_matrix[2][1], rotation_matrix[2][2])
            y = np.arctan2(-rotation_matrix[2][0], sy)
            z = np.arctan2(rotation_matrix[1][0], rotation_matrix[0][0])
        else:
            x = np.arctan2(-rotation_matrix[1][2], rotation_matrix[1][1])
            y = np.arctan2(-rotation_matrix[2][0], sy)
            z = 0
        return x * 180 / np.pi, y * 180 / np.pi, z * 180 / np.pi

    def _learning_face2(self, event):
        # 建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
        self.cap = cv2.VideoCapture(self.VIDEO_STREAM)

        if self.cap.isOpened() == True:  # 返回true/false 检查初始化是否成功
            self.CAMERA_STYLE = True
            self.m_textCtrl3.AppendText(u"打开摄像头成功!!!\n")
        else:
            self.m_textCtrl3.AppendText(u"摄像头打开失败!!!\n")
            # 显示封面图
            self.bmp.SetBitmap(wx.Bitmap(self.image_cover))

        mp_drawing = mp.solutions.drawing_utils
        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                min_detection_confidence=0.5) as face_mesh:
            # 成功打开视频，循环读取视频流
            while (self.cap.isOpened()):
                flag, im_rd = self.cap.read()
                if not flag:
                    pass
                # 取灰度
                img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
                # 图片设置为不可写，提升效率
                im_rd.flags.writeable = False
                results = face_mesh.process(im_rd)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            image=im_rd,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1,
                                                                         circle_radius=1),
                            connection_drawing_spec=mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1))
                        """点头"""
                        if self.nod_checkBox7.GetValue():
                            obj_points = np.array([
                                [0.0, 0.0, 0.0],
                                [0.0, -330.0, -65.0],
                                [-225.0, 170.0, -135.0],
                                [225.0, 170.0, -135.0],
                                [-150.0, -150.0, -125.0],
                                [150.0, -150.0, -125.0]
                            ], dtype=np.float32)
                            landmarks = results.multi_face_landmarks[0]
                            image_height, image_width, _ = im_rd.shape
                            landmark_points = []
                            landmark_indices = [1, 152, 33, 263, 61, 291]
                            for i, landmark in enumerate(landmarks.landmark):
                                if i in landmark_indices:
                                    landmark_x = min(max(0, int(landmark.x * image_width)), image_width - 1)
                                    landmark_y = min(max(0, int(landmark.y * image_height)), image_height - 1)
                                    landmark_points.append([landmark_x, landmark_y])
                            landmark_points = np.array(landmark_points, dtype=np.float32)
                            camera_matrix = np.array(
                                [[image_width, 0, image_width / 2], [0, image_width, image_height / 2], [0, 0, 1]],
                                dtype="double")
                            dist_coeffs = np.zeros((4, 1), dtype="double")
                            _, rotation_vector, _ = cv2.solvePnP(
                                obj_points,
                                landmark_points,
                                camera_matrix,
                                dist_coeffs
                            )
                            rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
                            pitch, yaw, roll = self.get_euler_angles(rotation_matrix)
                            if pitch > self.HAR_THRESH or pitch < -self.HAR_THRESH + 10:  # 点头阈值90
                                self.hCOUNTER += 1
                            else:
                                # 如果连续3次都小于阈值，则表示瞌睡点头一次
                                if self.hCOUNTER >= self.NOD_AR_CONSEC_FRAMES:  # 阈值：3
                                    self.hTOTAL += 1
                                    self.m_textCtrl3.AppendText(
                                        time.strftime('%Y-%m-%d %H:%M ', time.localtime()) + u"瞌睡点头\n")
                                # 重置点头帧计数器
                                self.hCOUNTER = 0
                            cv2.putText(im_rd, "pitch:" + "{:.2f}".format(pitch), (10, 90),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), thickness=2)  # GREEN
                            cv2.putText(im_rd, "yaw:" + "{:.2f}".format(yaw), (150, 90),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), thickness=2)  # BLUE
                            cv2.putText(im_rd, "roll:" + "{:.2f}".format(roll), (300, 90),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), thickness=2)  # RED
                            cv2.putText(im_rd, "Nod:{}".format(self.hTOTAL), (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                        (255, 255, 0), 2)
                        """眨眼、打哈欠"""
                        if self.blink_checkBox2.GetValue() and self.yawn_checkBox1.GetValue():
                            left_eye = [face_landmarks.landmark[159].x, face_landmarks.landmark[159].y,
                                        face_landmarks.landmark[145].x, face_landmarks.landmark[145].y,
                                        face_landmarks.landmark[33].x, face_landmarks.landmark[33].y,
                                        face_landmarks.landmark[133].x, face_landmarks.landmark[133].y]
                            right_eye = [face_landmarks.landmark[386].x, face_landmarks.landmark[386].y,
                                         face_landmarks.landmark[374].x, face_landmarks.landmark[374].y,
                                         face_landmarks.landmark[362].x, face_landmarks.landmark[362].y,
                                         face_landmarks.landmark[263].x, face_landmarks.landmark[263].y]
                            mouth = [face_landmarks.landmark[0].x, face_landmarks.landmark[0].y,
                                     face_landmarks.landmark[17].x, face_landmarks.landmark[17].y,
                                     face_landmarks.landmark[61].x, face_landmarks.landmark[61].y,
                                     face_landmarks.landmark[291].x, face_landmarks.landmark[291].y]

                            ear = (distance.euclidean((left_eye[0], left_eye[1]),
                                                      (left_eye[2], left_eye[3])) + distance.euclidean(
                                (right_eye[0], right_eye[1]), (right_eye[2], right_eye[3]))) / (
                                          distance.euclidean((left_eye[4], left_eye[5]),
                                                             (left_eye[6], left_eye[7])) + distance.euclidean(
                                      (right_eye[4], right_eye[5]), (right_eye[6], right_eye[7])))
                            mar = (distance.euclidean((mouth[0], mouth[1]), (mouth[2], mouth[3])) / distance.euclidean(
                                (mouth[4], mouth[5]), (mouth[6], mouth[7])))

                            if mar > self.MAR_THRESH:  # 张嘴阈值1.0
                                self.mCOUNTER += 1
                            else:
                                # 如果连续3次都大于阈值，则表示打了一次哈欠
                                if self.mCOUNTER >= self.MOUTH_AR_CONSEC_FRAMES:  # 阈值：3
                                    self.mTOTAL += 1
                                    # 显示
                                    cv2.putText(im_rd, "Yawning!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                                                2)
                                    self.m_textCtrl3.AppendText(
                                        time.strftime('%Y-%m-%d %H:%M ', time.localtime()) + u"打哈欠\n")
                                # 重置嘴帧计数器
                                self.mCOUNTER = 0
                            if ear < self.EYE_AR_THRESH:  # 眼睛长宽比：0.24
                                self.COUNTER += 1
                            else:
                                # 如果连续3次都小于阈值，则表示进行了一次眨眼活动
                                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:  # 阈值：3
                                    self.TOTAL += 1
                                    self.m_textCtrl3.AppendText(
                                        time.strftime('%Y-%m-%d %H:%M ', time.localtime()) + u"眨眼\n")
                                # 重置眼帧计数器
                                self.COUNTER = 0

                            cv2.putText(im_rd, "COUNTER: {}".format(self.mCOUNTER), (150, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (0, 0, 255), 2)
                            cv2.putText(im_rd, "MAR: {:.2f}".format(mar), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                        (0, 0, 255), 2)
                            cv2.putText(im_rd, "Yawning: {}".format(self.mTOTAL), (450, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (255, 255, 0), 2)
                            cv2.putText(im_rd, "COUNTER: {}".format(self.COUNTER), (150, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (0, 0, 255), 2)
                            cv2.putText(im_rd, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                        (0, 0, 255), 2)
                            cv2.putText(im_rd, "Blinks: {}".format(self.TOTAL), (450, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (255, 255, 0), 2)

                else:
                    # 没有检测到人脸
                    self.oCOUNTER += 1
                    cv2.putText(im_rd, "No Face", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                    if self.oCOUNTER >= self.OUT_AR_CONSEC_FRAMES_check:
                        self.m_textCtrl3.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime()) + u"员工脱岗!!!\n")
                        self.oCOUNTER = 0

                # 确定疲劳提示:眨眼60次，打哈欠30次，瞌睡点头15次
                if self.TOTAL >= 60 or self.mTOTAL >= 30 or self.hTOTAL >= 15:
                    cv2.putText(im_rd, "SLEEP!!!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                    # self.m_textCtrl3.AppendText(u"疲劳")

                # opencv中imread的图片内部是BGR排序，wxPython的StaticBitmap需要的图片是RGB排序，不转换会出现颜色变换
                height, width = im_rd.shape[:2]
                image1 = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB)
                pic = wx.Bitmap.FromBuffer(width, height, image1)
                # 显示图片在panel上：
                self.bmp.SetBitmap(pic)

                # 释放摄像头
            self.cap.release()

    def camera_on(self, event):
        """使用多线程，子线程运行后台的程序，主线程更新前台的UI，这样不会互相影响"""
        import _thread
        # 创建子线程，按钮调用这个方法，
        _thread.start_new_thread(self._learning_face2, (event,))

    def cameraid_choice(self, event):
        # 摄像头编号
        cameraid = int(event.GetString()[-1])  # 截取最后一个字符
        if cameraid == 0:
            self.m_textCtrl3.AppendText(u"准备打开本地摄像头!!!\n")
        if cameraid == 1 or cameraid == 2:
            self.m_textCtrl3.AppendText(u"准备打开外置摄像头!!!\n")
        self.VIDEO_STREAM = cameraid

    def vedio_on(self, event):
        if self.CAMERA_STYLE == True:  # 释放摄像头资源
            # 弹出关闭摄像头提示窗口
            dlg = wx.MessageDialog(None, u'确定要关闭摄像头？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
            if (dlg.ShowModal() == wx.ID_YES):
                self.cap.release()  # 释放摄像头
                self.bmp.SetBitmap(wx.Bitmap(self.image_cover))  # 封面
                dlg.Destroy()  # 取消弹窗
        # 选择文件夹对话框窗口
        dialog = wx.FileDialog(self, u"选择视频检测", os.getcwd(), '', wildcard="(*.mp4)|*.mp4",
                               style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            # 如果确定了选择的文件夹，将文件夹路径写到m_textCtrl3控件
            self.m_textCtrl3.SetValue(u"文件路径:" + dialog.GetPath() + "\n")
            self.VIDEO_STREAM = str(dialog.GetPath())  # 更新全局变量路径
            dialog.Destroy
            """使用多线程，子线程运行后台的程序，主线程更新前台的UI，这样不会互相影响"""
            import _thread
            # 创建子线程，按钮调用这个方法，
            _thread.start_new_thread(self._learning_face2, (event,))

    def AR_CONSEC_FRAMES(self, event):
        self.m_textCtrl3.AppendText(u"设置疲劳间隔为:\t" + event.GetString() + "秒\n")
        self.AR_CONSEC_FRAMES_check = int(event.GetString())

    def OUT_AR_CONSEC_FRAMES(self, event):
        self.m_textCtrl3.AppendText(u"设置脱岗间隔为:\t" + event.GetString() + "秒\n")
        self.OUT_AR_CONSEC_FRAMES_check = int(event.GetString())

    def off(self, event):
        """关闭摄像头，显示封面页"""
        self.cap.release()
        self.bmp.SetBitmap(wx.Bitmap(self.image_cover))

    def OnClose(self, evt):
        """关闭窗口事件函数"""
        dlg = wx.MessageDialog(None, u'确定要关闭本窗口？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            self.Destroy()
        print("检测结束，成功退出程序!!!")


class main_app(wx.App):
    """
     在OnInit() 里边申请Frame类，这样能保证一定是在app后调用，
     这个函数是app执行完自己的__init__函数后就会执行
    """

    # OnInit 方法在主事件循环开始前被wxPython系统调用，是wxpython独有的
    def OnInit(self):
        self.frame = Fatigue_detecting(parent=None, title="Fatigue Demo")
        self.frame.Show(True)
        return True


if __name__ == "__main__":
    app = main_app()
    app.MainLoop()
