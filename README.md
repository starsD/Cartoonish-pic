# Cartoonish-pic
使用openCV+pyqt5实现照片卡通化



#### 运行要求

1. python3
2. pyqt5
3. openCV-python
4. pywin32

#### 运行方法

```
python Cartoonish.py
```

#### 主程序

![](http://mystore0716.oss-cn-hangzhou.aliyuncs.com/pic/python_doc_pic/cartoonishUI.jpg)

打开图片后，拖动Slider调节参数。

#### 流程图

![](http://mystore0716.oss-cn-hangzhou.aliyuncs.com/pic/python_doc_pic/cartoonish-flow.jpg?raw=true)

#### 参数说明

- 下采样层数      决定细节丢失的程度
- 中值滤波大小   边缘检测前去掉噪声
- Blocksize         边缘检测轮廓的大小，值越大，轮廓越醋
- 滤波器选择       高斯双边滤波/均值偏移滤波

#### 样例

![](https://github.com/starsD/Cartoonish-pic/blob/master/examples/test_1.jpg?raw=true)

![](https://github.com/starsD/Cartoonish-pic/blob/master/examples/test_1_result.jpg?raw=true)

![](https://github.com/starsD/Cartoonish-pic/blob/master/examples/test_2.jpg?raw=true)

![](https://github.com/starsD/Cartoonish-pic/blob/master/examples/test_2_result.jpg?raw=true)

#### 其他

本工程的GUI通过*eric6+qtdesinger*生成 *CartooningGui.ui*文件，编译后成为*Ui_CartooningGui.py*。*Cartoonish.py*文件包含事件处理与照片卡通化的处理。可以通过*eric6+qtdesinger*对UI重制与修改。

![](http://mystore0716.oss-cn-hangzhou.aliyuncs.com/pic/python_doc_pic/cartoonish-qtdesigner.jpg?raw=true)

