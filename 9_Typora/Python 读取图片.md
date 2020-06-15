# Python 读取图片

## 1. 通过 Image 库读取

```python
import Image

img = Image.open('D:/Typora/Lena.jpg').convert('RGB')
# 转换成numpy数组
# img = np.array(img)
```

<img src="E:\Typora\Lena.jpg" style="zoom: 33%;" />

------

## 2. 通过 opencv-python 库读取

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('D:/Typora/Lena.jpg')   # 读取矩阵值（行×列×RGB）
# opencv的颜色通道顺序为[B,G,R]，而matplotlib的颜色通道顺序为[R,G,B]。解决方案：把R和B的位置调换一下
img = img[:,:,(2,1,0)]
plt.imshow(img)            # 显示图片
```

