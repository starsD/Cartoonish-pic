# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMessageBox

from PyQt5.QtGui import QImage, QPixmap

from Ui_CartooningGui import Ui_MainWindow

import os
import cv2
import win32ui


class Cartoon(object):

    def __init__(self):
        self.parameters = {}
        self.raw_img = None
        self.out_img = None

    def set_parameter(self, ky):
        self.parameters.update(ky)
        pass

    def cartoonish(self):
        def bilateral_filter(img, filter):
            if filter == 0:
                # 高斯双边滤波
                dst = cv2.bilateralFilter(src=img, d=7, sigmaColor=100, sigmaSpace=15)
            elif filter == 1:
                # 均值漂移滤波
                dst = cv2.pyrMeanShiftFiltering(src=img, sp=15, sr=20)
            return dst

        def get_gray(img):
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return gray_img

        def median_fiflter(img, size=3):
            median_img = cv2.medianBlur(img, size)
            return median_img

        def get_edge(img, blocksize=9):
            edge_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize, C=2)
            edge_img = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2RGB)
            return edge_img

        def pyramid(img, level=2):
            temp = img.copy()
            pyramid_images = []
            for i in range(level):
                pyramid_img = cv2.pyrDown(temp)
                pyramid_images.append(pyramid_img)
                temp = pyramid_img.copy()
            return pyramid_images[-1]

        def pyrUp(img, level=2):

            temp = img.copy()
            for i in range(level):
                #
                # for k in range(1):
                #     temp = bilateral_filter(temp, self.parameters['bilateral_filter'])
                temp = cv2.pyrUp(temp)

            return temp
        if self.raw_img is None:
            return

        # 下采样
        pyramid_img = pyramid(self.raw_img, self.parameters['subsampled_level'])

        # 上采样
        pyrup_img = pyrUp(pyramid_img, self.parameters['subsampled_level'])

        # 双边滤波
        dst = bilateral_filter(pyrup_img, self.parameters['bilateral_filter'])

        # dst = pyrup_img
        # 灰度化
        gray_img = get_gray(dst)

        # 中值滤波
        median_img = median_fiflter(gray_img, self.parameters['median_fiflter'])

        # 边缘检测
        edge_img = get_edge(median_img, self.parameters['blocksize'])

        # 图像合并
        cartoon_img = cv2.bitwise_and(dst, edge_img)

        self.out_img = cartoon_img
        return cartoon_img

    def save(self, path):
        if self.out_img is not None:
            try:
                cv2.imwrite(path, self.out_img)
            except Exception as e:
                print(e)
                return False
            return True
        else:
            return False


class MainWindow(QMainWindow, Ui_MainWindow):

    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.cartoon = Cartoon()
        self.setupUi(self)

    def get_parameters(self):
        ky = dict()
        ky['subsampled_level'] = self.slider_subsampled_level.value()
        ky['blocksize'] = self.slider_blocksize.value()*2 + 1
        ky['median_fiflter'] = self.slider_median_fiflter.value()*2 + 1
        ky['bilateral_filter'] = self.slider_bilateral_filter.value()
        return ky

    def show_parameters(self, ky):
        try:
            self.subsampled_level_value.setText(str(ky['subsampled_level']))
            self.blocksize_value.setText(str(ky['blocksize']))
            self.median_fiflter_value.setText(str(ky['median_fiflter']))
            bilateral_filter_value = "高斯双边滤波" if ky['bilateral_filter'] == 0 else "均值漂移滤波"
            self.bilateral_filter_value.setText(bilateral_filter_value)
        except Exception as e:
            print(e)

    def set_parameters(self, ky):
        self.cartoon.set_parameter(ky)

    def save_img(self):
        dlg = win32ui.CreateFileDialog(0)
        dlg.SetOFNInitialDir(os.getcwd())
        dlg.DoModal()
        filename = dlg.GetPathName()

        if self.cartoon.save(filename):
            QMessageBox.information(self, "提示", "保存成功", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "错误", "保存失败，请检查路径中是否有中文", QMessageBox.Yes)

    def cvimg2pix(self, img):
        try:
            dst_img = img.copy()
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, dst_img)
            frame = QImage(dst_img, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
        except Exception as e:
            print("breakpoint cvimg2pix")
            print(e)
        return pix

    def graphic_show(self, pix):
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()  # 创建场景
        scene.addItem(item)
        self.graphicsView.setScene(scene)

    def cartoonish(self):
        cartoon_img = self.cartoon.cartoonish()
        if cartoon_img is None:
            QMessageBox.information(self, "提示", "请先打开图片", QMessageBox.Yes)
            return
        pix = self.cvimg2pix(cartoon_img)
        self.graphic_show(pix)

    @pyqtSlot()
    def on_button_open_image_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            dlg = win32ui.CreateFileDialog(1)
            dlg.SetOFNInitialDir(os.getcwd())
            dlg.DoModal()
            filename = dlg.GetPathName()

            img = cv2.imread(filename)
            if img is None:
                QMessageBox.information(self, "提示", "打开图片失败，请检查路径中是否有中文", QMessageBox.Yes)
                return
            self.cartoon.raw_img = img
            pix = self.cvimg2pix(img)
            item = QGraphicsPixmapItem(pix)                      # 创建像素图元
            scene = QGraphicsScene()                             # 创建场景
            scene.addItem(item)
            self.graphicsView.setScene(scene)
        except Exception as e:
            print(e)
        return

    @pyqtSlot()
    def on_button_save_image_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.save_img()
    
    @pyqtSlot(int)
    def on_slider_subsampled_level_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        ky = self.get_parameters()
        self.show_parameters(ky)
        self.set_parameters(ky)

    
    @pyqtSlot(int)
    def on_slider_blocksize_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        ky = self.get_parameters()
        self.show_parameters(ky)
        self.set_parameters(ky)

    
    @pyqtSlot(int)
    def on_slider_median_fiflter_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        ky = self.get_parameters()
        self.show_parameters(ky)
        self.set_parameters(ky)

    
    @pyqtSlot(int)
    def on_slider_bilateral_filter_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        ky = self.get_parameters()
        self.show_parameters(ky)
        self.set_parameters(ky)


    @pyqtSlot()
    def on_slider_subsampled_level_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        self.cartoonish()
    
    @pyqtSlot()
    def on_slider_blocksize_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        self.cartoonish()
    
    @pyqtSlot()
    def on_slider_median_fiflter_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        self.cartoonish()

    
    @pyqtSlot()
    def on_slider_bilateral_filter_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        self.cartoonish()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
