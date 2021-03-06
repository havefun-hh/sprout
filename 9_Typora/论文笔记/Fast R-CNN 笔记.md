# R-CNN 笔记

**摘要：**

​		这篇论文提出了一种基于卷积神经网络做目标检测的算法——Fast R-CNN，它是建立在之前R-CNN的基础上使用深度卷积神经网络进行高效的目标检测。Fast R-CNN做了几点创新来提高训练和测试阶段的速度，同时提高了检测的准确率。

* Fast R-CNN 使用的是 VGG16 网络，训练速度比 R-CNN 快了9倍，测试速度快了213倍，并且在 PASCAL VOC 2012上实现了更高的 mAP；
* 与 SSPnet 相比，Fast R-CNN 训练速度快了3倍，测试速度快了10倍，并且准确率更高。

### 1. 介绍

​		最近，深度卷积网络在图像分类（image classification）和物体检测（object detection）领域有了很明显的提高。相比于图像分类问题，物体检测是一个更具挑战性的任务，它需要使用更复杂的方法去解决。正是由于这种复杂性，当前很多训练模型的方法都是采用多阶段流水线的形式，不仅很慢而且很不优雅。

　　复杂性产生（Complexity arises）的原因是检测需要获得物体的精确位置，从而产生了**两个主要的挑战（Challenges）。首先，许多的物体候选区域（经常被称为“Proposals”）必须被处理。其次，这些所谓的候选区域仅仅能提供物体的一个粗略位置信息，因此必须对它进行细化（Refine）以实现更精确的定位。**解决这些问题往往需要在速度、精度、简易性上进行适当的妥协折中（Compromise）。

　　在这篇论文中，我们简化了(streamline)基于最先进（state-of-the-art）的卷积网络的物体检测的训练过程（R-CNN和SPP-Net）。**我们提出了一种单阶段（single-stage）的训练算法（algorithm），该算法将候选区域物体分类和它们的空间（spatial）位置细化合并在一起去学习训练（这里指的是图像分类和边界框回归）。**

　　由此产生的方法可以更快的训练一个非常深的卷积网络（VGG16，9倍于R-CNN，3倍于SPP-Net）。在测试时，检测网络处理一张图片仅仅需要0.3s（不包括候选区域的产生的时间），而且在PASCAL VOC 2012上的MAP为66%（R-CNN仅仅62%）。

#### 1.1. R-CNN 和 SPP-Net

　　基于区域的卷积网络方法（R-CNN）通过使用深度卷积网络完成了对物体候选区域的分类，并得到了很好的物体检测精度。然而，R-CNN有着明显地（notable）缺陷（drawbacks）：

　　**（1）训练是多阶段流水线（Pipeline）**：首先，R-CNN利用物体候选区域（Object Proposals）对卷积网络（ConvNet）模型进行调优（fine-tunes），损失函数是采用log损失，其实就是softmax函数。然后，让SVMs去适应了卷积特征（其实就是训练了SVM分类器）。这些SVMs通过fine-tuning取代了softmax分类器作为物体检测器。在第三个训练阶段，边界框（Bounding-box）回归器被训练学习。

　　**（2）训练在空间和时间上都很昂贵（expensive）**：对于SVM分类器和边界框回归器的训练来说，所输入的特征需要每一张图片的每一个候选区域中被提取（extract）并被写入磁盘（disk）。对于非常深的网络，比如VGG16，训练VOC2017的大约5000张图片的训练集需要花费2.5个GPU-Days，这些特征需要数百GB的存储空间（storage）。

　　**（3）物体检测速度很慢**：在测试时，特征从每一张测试图片的每一个物体候选区域被提取出来。对于VGG16网络来说，检测一张图片花费47s（在GPU上）。

　　R-CNN是很慢的原因是对于图片的每一个候选区域都执行一次前向传播计算（提取特征的卷积层），没有共享卷积计算（sharing computation）。**SPP-Net提出了共享计算去加速R-CNN算法。**SPP-Net方法对于一张完整的输入图片只计算一次卷积特征映射，然后从共享的特征映射提取每一个物体候选区域所对应的特征向量并做分类处理。对于每一个候选区域最大池化（max-pooling）它的特征映射提取它的特征向量，输出是固定的大小。汇聚多种不同大小的池化输出，然后在空间金字塔池化层连接它们。SPP-Net在测试上是R-CNN的10-100倍；在训练时由于加快了候选区域的特征提取，训练时间减少了3倍。（共享卷积计算）

　　SPP-Net也存在很明显地缺点。像R-CNN一样，训练是多阶段流水线，包含特征提取，利用log损失（softmax）fine-tuning网络，训练SVM分类器，最终拟合了边界框回归器。这些训练所需提取的特征需要存入磁盘。但是和R-CNN不同的是，在SPP-Net中的fine-tuning不同更新空间金字塔之前的池化层之前的卷积层。不足为奇，这种限制（固定卷积层）限制了非常深的网络（VGG16）的精度。

#### 1.2. 贡献（Contributions）

​		**我们提出了一种新的训练算法（algorithm），该算法在消除/修复（fix）R-CNN和SPPNet缺点（disadvantages）的同时，还提高了它们速度和精度。**我们把这种方法叫做Fast R-CNN，因为该方法在训练和测试的时候是比较快的。Fast R-CNN方法的优点如下：

　　**（1）比R-CNN和SPPNet更高的检测精度（mAP）**

　　**（2）训练是单阶段的，使用了多任务损失函数**

　　**（3）训练可以更新所有的网络层参数**

　　**（4）不需要磁盘去存储大量提取的特征 **

### 2. Fast R-CNN的架构和训练（Architecture and Training）

 　 图1展示了Fast R-CNN结构。FastR-CNN网络将整个图像和一组区域建议作为输入。网络首先使用几个卷积（conv）和最大池化层处理整个图像，以产生特征图。然后，对于每个区域建议，感兴趣区域（RoI）池化层从卷积得到的完整特征图中提取固定长度的特征向量。
每个特征向量被送到一系列全连接层，最终分支到两个子输出层：一个产生对K类对象的softmax概率估计加上一个“背景”类，另一个层对K类的每一个输出四个真实数字。这组数字表示了回归框的位置。

![Fast R-CNN架构](E:\Typora\Fast R-CNN架构.png)

​		图一. fast R-CNN架构。输入图像和多个感兴趣区域RoI被输入到完全卷积网络（这里指卷积网络的前面的所有卷积层）。每个感兴趣区域RoI被池化为固定尺寸的特征映射，然后通过全连接层映射到特征向量。网络中每个RoI有两个输出向量：softmax概率和每个类别的编辑框回归偏移量。**该架构使用多任务损失函数实现了端到端的训练。**

#### 2.1 、RoI 池化层
​       RoI池化层使用最大池化将任何有效的感兴趣区域内的特征转换为具有固定空间范围H×W（例如，7×7）的小特征图，其中H和W是独立于任何特定的RoI层的超参数。在本文中，RoI是一个转换特征图的矩形窗口。每个RoI由四维元组（r; c; h; w）定义，指定其左上角位置（r,c）及其高度和宽度（h,w）。

 		RoI max pooling通过将h,w的 RoI窗口划分为H*W子网格窗口工作，然后将每个子窗口中的值最大池化到相应的输出网格单元中。池化独立应用于每个特征图通道，如标准最大池化中所示。 RoI层只是SPPnets 中使用的空间金字塔池层的特例，在这里只有一个金字塔层。我们使用SPP中给出的池化子窗口方法来计算。

> **对上图网络结构的一些理解 ：**
>
> **输入的是一张完整的图像和图像上的多个感兴趣区域（RoIs）的坐标（选择性搜索）。首先使用深度卷积网络提取整张图片特征，然后通过输入的RoI坐标映射得到感兴趣区域的特征图，RoI max pooling将特征图池化得到固定大小（H×W）的新的小特征图，其中H W是超参数。然后通过FCs得到特征向量。该特征向量最终送到两个子网络，一个得到该RoI的概率，另一个得到RoI修正的回归框位置。**

### 2.2、从预训练的网络初始化
​		作者分别使用具有有5个最大池化层和5到13个不等的卷积层的三种网络进行预训练：CaffeNet，VGG_CNN_M_1024，VGG-16，使用这些网络初始化Fast R-CNN前，需要以下修改：

​		1. 用RoI pooling layer取代网络的最后一个池化层，该池化层通过将H和W设置为与网络的第一个全连接层相兼容来配置（例如，对于VGG16，H = W = 7）。

​		2. 网络的最后一个全连接层和softmax（经过1000类ImageNet分类训练）被前面描述的两个子层替换（全连接层和K+1 类的softmax和边界框回归）。

​		3. 输入两组数据到网络：一组图片和每一个图片的一组RoIs。

#### 2.3、用于目标检测的微调

​		为什么SPPnet不能更新金字塔池化之前的卷积池化的参数？论文中提到当每个训练样本（即RoI）来自不同的图像时，通过SPP层的反向传播非常低效。低效源于每个RoI可能具有非常大的感受野（接收区），通常包括整个输入图像。由于正向传播必须处理整个感受野，训练输入是非常大（通常是整个图像）。

​		我们提出了一种更加高效的训练方法，它可以在训练中共享特征。在Fast R-CNN训练中，一个minibatch的R个RoI来源于N张图片，即从每张图片中采样R/N个RoIs，而来自同一张图片的RoI在前向和反向传播中可以贡献计算和内存，通常N=2，R=128，这样的训练方案通常要比从128张不同图片中采样快64倍。

​		另外除了分层采样，Fast R-CNN将分类、回归放在一个网络中（loss合并），而不像原来那样单独训练分类器、回归模型。

**多任务损失。**

​		首先，每个RoI经过softmax计算最后输出离散的概率分布，共K个类别+1个背景。每个还输出了bbx回归偏移量。

​		每个训练的RoI的标签有真实的类别u和真实的边界框的位置v。我们使用多任务损失共同训练分类和bbx的回归。

​		其中类别损失用的是对数损失函数。第二个位置损失是对于u个真实类别来说的，背景的话u=0 即没有位置损失，其他情况只有当u大于等于1时，为1，其他情况为0.v是真实的边界框，为预测位置信息。损失函数用平滑的L1损失。

​		论文中说使用L1损失对离群点更加鲁棒，与R-CNN和SPP使用的L2相比，相对不敏感，不易出现梯度爆炸的情况。

**小批量采样。**

​		在微调阶段，每次SGD训练有N=2张图像组成。我们使用从每张采样64个RoI,共128个RoI的mini-batch。 比如，我们从候选框中获取25％的RoI，这些候选框与检测框真值的IoU至少为0.5。 这些RoI只包括用前景对象类标记的样本，即u≥1。 剩余的RoI从检测真值的最大IoU在区间[0.1,0.5)内的候选框中采样，这些是背景样本，并用u=0标记。在训练期间，图像以概率0.5水平翻转。不使用其他数据增强。

**通过RoI池化层的反向传播。**



**SGD超参数。**

​		用于Softmax分类和检测框回归的全连接层的权重分别使用具有方差0.01和0.001的零均值高斯分布初始化。偏置初始化为0。所有层的权重学习率为1倍的全局学习率，偏置为2倍的全局学习率，全局学习率为0.001。 当对VOC07或VOC12 trainval训练时，我们运行SGD进行30k次小批量迭代，然后将学习率降低到0.0001，再训练10k次迭代。当我们训练更大的数据集，我们运行SGD更多的迭代，如下文所述。 使用0.9的动量和0.0005的参数衰减（权重和偏置）。

#### 2.4 尺度不变性

​		我们探索了在物体检测中两种实现尺度不变的方法：（1）通过“强力”学习。（2）通过使用图像金字塔。这些策略遵循了文献[11]（SPPNet）中的两个方法。对于蛮力方法，在训练和测试期间以预定义的像素大小处理每个图像。网络必须从训练数据中学习尺度不变的物体检测。

　　相反，多尺度方法通过图像金字塔为网络提供近似的尺度不变性。在测试时，图像金字塔用于近似地缩放规范化每个建议区域。在多尺度训练期间，我们在每次采样图像时随机采样金字塔尺度[11]，作为数据增强的一种形式。由于GPU内存限制，我们仅针对较小的网络进行多尺度训练。

### 3、Fast R-CNN检测

​		一旦Fast R-CNN网络被微调完毕，检测相当于运行前向传播（假设候选框是预先计算的）。网络将图像（或图像金字塔，编码为图像列表）和待计算概率的R个候选框的列表作为输入。在测试的时候，R通常在2000左右，虽然我们将考虑将它变大（约45k）的情况。当使用图像金字塔时，每个RoI被缩放，使其最接近224*224像素。

#### 3.1 使用截断的SVD加快检测速度

​		对于整个图像分类，与conv层相比，计算全连接层所花费的时间较少。相反，检测时要处理的RoI的数量很大，并且将近一半的时间用于计算完全连接的层.



