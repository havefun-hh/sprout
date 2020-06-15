# torch.transforms

```python
import torchvision.transforms as transforms
```

### 1 裁剪

#### 1.1 中心裁剪：CenterCrop

```python
transforms.CenterCrop(64)(img)  #从中心裁剪一个64×64的图像
transforms.CenterCrop((64, 128))(img)  #从中心裁剪一个64×128的图像
```

#### 1.2 随机裁剪：RandomCrop

```python
transforms.RandomCrop(64)(img)
```

#### 1.3 FiveCrop

```python
pics = transforms.FiveCrop(64)(img)  #从上、下、左、右、中心各裁一个64×64的图像
pics[0], pics[4]
```

### 2 旋转

#### 2.1 随机旋转某一角度：RandomRotation

```python
transforms.RandomRotation(30)(img)  #在（-30,30）之间选择一个角度进行旋转
transforms.RandomRotation((60,90))(img) #在60-90之间选择一个角度进行旋转
```

#### 2.2 依概率随机水平旋转： RandomHorizontalFlip

```python
transforms.RandomHorizontalFlip(p=1.0)(img)  #p默认为0.5，这里设成1，那么就肯定会水平翻转
```

#### 2.2依概率随机垂直翻转： RandomVerticalFlip

```python
transforms.RandomVerticalFlip(p=1)(img)
```

###  3 重置大小：Resize

```python
transforms.Resize((64, 128))(img)
```

### 4 随机改变亮度、对比度、饱和度、色调：ColorJitter

```python
transforms.ColorJitter(brightness=0, contrast=0, saturation=0, hue=0)
```

### 5 数据标准化：Normalize

```python
norm_data = transforms.Normalize(mean=(0.2,0.2,0.2), std=(0.9,0.9,0.9))(data)
```

### 6 将数据转化成图像：ToPILImage

```python
transforms.ToPILImage(mode='RGB')(norm_data)
```

### 7 图像转换成 tensor：ToTensor

```python
data = transforms.ToTensor()(img)
data.size() #3表示有3个通道，805表示长有805个pixel，1440表示宽有1440个pixel
torch.Size([3, 805, 1440])
```

### 8 连续操作：Compose

```python
trans = transforms.Compose([
    transforms.Resize((64, 128)),
    transforms.ColorJitter(0.3, 0.3, 0.2),
    transforms.RandomRotation(5),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
trans(img)
```

### 9 转换成灰度图：Grayscale

```python
transforms.Grayscale(num_output_channels=1)  # num_output_channels (int) – (1 or 3) number of channels desired for output image
```

### 10 填充：Pad

使用指定的 pad 值对指定的 PIL 图像四处填充

```
transforms.Pad(padding, fill=0, padding_mode='constant')
```

