# Python 原图转灰度图

## 1. Image 库

```python
import Image

img = Image.open('D:/Typora/Lena.jpg').convert('L')
```



## 2. opencv-python 库

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('D:/Typora/Lena.jpg')   # 读取矩阵值（长×款×RGB）

# 图像灰度化算法：Gray = 0.299R+0.587G+0.114*B
r, g, b = [img[:, :, i] for i in range(3)]
img_gray = 0.299 * r + 0.587 * g + 0.114 * b
plt.imshow(img_gray, cmap="gray")
```

