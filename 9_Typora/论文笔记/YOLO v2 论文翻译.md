# YOLO v2 论文翻译

### 摘要

​		我们推出的YOLO9000是一款先进的实时目标检测系统，可检测9000多种目标类别。首先，我们提出对YOLO检测方法的各种改进，这些改进有独创的，也有的是来源于以前的研究。改进后的模型YOLOv2在PASCAL VOC和COCO等标准检测任务中处于技术领先地位。通过使用一种新颖的多尺度训练方法，同样的YOLOv2模型可以以不同的尺寸运行，在速度和准确性之间提供了一个简单的折衷。在67 FPS时，YOLOv2在VOC 2007上获得了76.8 mAP。在40 FPS时，YOLOv2获得了78.6 mAP，超越了采用ResNet和SSD的Faster R-CNN等先进的方法，同时运行速度仍然更快。最后我们提出一种联合训练目标检测和分类的方法。使用这种方法，我们在COCO检测数据集和ImageNet分类数据集上同时训练YOLO9000。**我们的联合训练使YOLO9000能够预测未标注检测数据的目标类别的检测结果**。我们在ImageNet检测任务上验证了我们的方法。 YOLO9000在ImageNet检测验证集上获得19.7 mAP，尽管200个类中只有44个具有检测数据。在COCO上没有的156种类上，YOLO9000获得16.0 mAP。但YOLO可以检测超过200个种类;它预测超过9000个不同的目标类别的检测结果，而且它仍然是实时运行的。

![YOLO v2 图1](E:\Typora\论文笔记\YOLO v2 图1.png)

图1：YOLO9000可以实时预测的目标的种类很丰富。

### 1. 引言

​		通用的目标检测应该快速，准确，并且能够识别各种各样的目标。自从引入神经网络，检测框架变得越来越快速和准确。但是，大多数检测方法仅限于检测一小部分目标。

​		与分类和标记等其他任务的数据集相比，目前目标检测数据集是有限的。最常见的检测数据集包含成千上万到数十万张具有成百上千个标签的图像[3],[10],[2]。而分类数据集有数以百万计的图像，数十或数百万个类别[20],[2]。

​		我们希望检测的类别能够扩展到目标分类的级别。但是，标注检测图像要比标注分类或贴标签要昂贵得多（标签通常是用户免费提供。因此，我们不太可能在近期内看到与分类数据集相同规模的检测数据集。

​		我们提出了一种新方法——**通过利用我们已有的大量分类数据来扩大当前检测系统的范围**。 **我们的方法使用目标分类的分层视图，使得我们可以将不同的数据集组合在一起**。

​		我们还提出了一种联合训练算法，它允许我们在检测和分类数据上训练目标检测器。 我们的方法利用标记检测图像来学习精确定位目标，同时使用分类图像来增加词汇量和鲁棒性。

​		我们使用这种方法训练YOLO9000——一种可以检测超过9000种不同的目标类别的实时目标检测器。 **首先，我们改进YOLO基础检测系统，生成最先进的实时检测器YOLOv2**。 **然后，采用我们的数据集组合方法和联合训练算法，使用来自ImageNet的9000多个类以及COCO的检测数据来训练模型**。

​		我们所有代码和预训练模型都可在线获得：[http://pjreddie.com/yolo9000/](https://link.zhihu.com/?target=http%3A//pjreddie.com/yolo9000/)。

### 2. 更好

​		与最先进的检测系统相比，YOLO存在各种缺点。 YOLO与Fast R-CNN的误差比较分析表明，YOLO产生了大量的定位错误。此外，与生成候选区域方法相比，YOLO召回率相对较低。 因此，我们主要关注改善召回率和定位，同时保持分类准确性。

​		计算机视觉通常趋向于更大更深的网络[6] [18] [17]。 更好的性能通常取决于训练更大的网络或将多个模型组合在一起。 但是，对于YOLOv2，我们需要一个更精确的检测器，而且保持很快的速度。 **我们不是要扩大网络，而是简化网络，然后让表征更易于学习**。 我们将以往工作中的各种创意与我们自己新颖的方法结合起来，以提高YOLO的表现。 表2列出了结果的总结。

![YOLO v2 表2](E:\Typora\论文笔记\YOLO v2 表2.png)

表2：从YOLO到YOLOv2的路径。大多数列出的设计决策都会导致MAP显着增加。有两个例外情况是：切换到带有锚框的全卷积网络和使用新网络。切换到锚框方法增加召回率，而不改变mAP，而使用新网络削减33％的计算。

​		**批量标准化。**批量标准化（batch normalization）可以显着改善收敛性，而且不再需要其他形式的正则化[7]。 通过在YOLO中的所有卷积层上添加批量标准化，可以在mAP中获得了2％以上的改进。 批量标准化也有助于规范模型。 **通过批量标准化，可以从模型中删除dropout而不会发生过拟合**。

​		**高分辨率分类器。**所有的最先进的检测方法都使用在ImageNet上预先训练好的分类器[16]。 从AlexNet开始，大多数分类器用小于256×256的图像作为输入[8]。 最初的YOLO以224×224的图像训练分类器网络，并将分辨率提高到448以进行检测训练。 这意味着网络必须切换到目标检测的学习，同时能调整到新的输入分辨率。

​		对于YOLOv2，我们首先以448×448的全分辨率在ImageNet上进行10个迭代周期的微调。这给予网络一些时间，以调整其滤波器来更好地处理更高分辨率的输入。然后，我们再对该检测网络进行微调。 这个高分辨率的分类网络使mAP增加了近4％。

​		**与锚框卷积。** YOLO直接使用卷积特征提取器顶部的全连接层来预测边界框的坐标。 Fast R-CNN不是直接预测坐标，而是使用手工选取的先验来预测边界框[15]。 Faster R-CNN中的候选区域生成网络（RPN）仅使用卷积层来预测锚框的偏移和置信度。由于预测层是卷积的，所以RPN可以在特征图中的每个位置预测这些偏移。使用预测偏移代替坐标，可以简化问题并使网络更易于学习。

​		我们从YOLO中移除全连接层，并使用锚框来预测边界框。 首先我们消除一个池化层，以使网络卷积层的输出具有更高的分辨率。 我们还缩小网络，使其在分辨率为416X416的输入图像上运行，而不是448×448。我们这样做是因为我们想要在特征图中有奇数个位置，只有一个中心单元。目标，尤其是大的目标，往往占据图像的中心，所以最好在正中心拥有单独一个位置来预测这些目标，而不是在中心附近的四个位置。 YOLO的卷积层将图像下采样32倍，所以通过使用416的输入图像，我们得到13×13的输出特征图。

​		引入锚框后，我们将类预测机制与空间位置分开处理，单独预测每个锚框的类及其目标。 遵循原来的YOLO的做法，目标预测依然预测了真实标签框（ground truth box）和候选框的IOU，而类别预测也是预测了当有目标存在时，该类别的条件概率。

​		使用锚框，精确度会小幅下降。因为原始的YOLO仅为每个图片预测98个框，但使用锚框后，我们的模型预测的框数超过一千个。 如果没有锚框，我们的中等模型将获得69.5 的mAP，召回率为81％。 使用锚框，我们的模型获得了69.2 的mAP，召回率为88％。尽管mAP减少，但召回率的增加意味着我们的模型有更大的改进空间。

​		**维度聚类。**当把锚框与YOLO一起使用时，我们会遇到两个问题。 首先是框的尺寸是手工挑选的。虽然网络可以通过学习适当地调整方框，但是如果我们从一开始就为网络选择更好的先验，就可以让网络更容易学习到更好的检测结果。

​		我们不用手工选择先验，而是在训练集的边界框上运行k-means，自动找到良好的先验。 如果我们使用具有欧几里得距离的标准k-means，那么较大的框比较小的框产生更多的误差。 然而，我们真正想要的是独立于框的大小的，能获得良好的IOU分数的先验。 因此对于距离度量我们使用：
$$
d(box,centroid)=1-IOU(box,centroid)
$$
​		我们用不同的k值运行k-means，并绘制最接近质心的平均IOU（见图2）。为了在模型复杂度和高召回率之间的良好折衷，我们选择k = 5。聚类的质心与手工选取的锚框显着不同，它有更少的短且宽的框，而且有更多既长又窄的框。

![YOLO v2 图2](E:\Typora\论文笔记\YOLO v2 图2.png)

图2：VOC和COCO上的聚类框尺寸。我们在边界框的维上运行k-means聚类，以获得我们模型的良好先验。左图显示了我们通过k的各种选择获得的平均IOU。我们发现k = 5为召回与模型的复杂性提供了良好的折衷。右图显示了VOC和COCO的相对质心。这两种方案都喜欢更薄，更高的框，而COCO的尺寸的多变性比VOC更大。

​		表1中，我们将聚类策略的先验中心数和手工选取的锚框数在最接近的平均IOU上进行比较。仅5个先验中心的平均IOU为61.0，其性能类似于9个锚框的60.9。 使用9个质心会得到更高的平均IOU。这表明使用k-means生成边界框可以更好地表示模型并使其更容易学习。

![YOLO v2 表1](E:\Typora\论文笔记\YOLO v2 表1.png)

表1：VOC 2007最接近先验的框的平均IOU。VOC 2007上的目标的平均IOU与其最接近的，未经修改的使用不同生成方法的目标之间的平均IOU。聚类结果比使用手工选取的先验结果要好得多。

​		**直接位置预测**。当在YOLO中使用锚框时，我们会遇到第二个问题：模型不稳定，尤其是在早期迭代的过程中。 大多数不稳定来自于预测框的（x，y）位置。 在候选区域网络中，网络预测的 $t_x$ 和 $t_y$，中心坐标（x，y）计算如下：
$$
x=(t_x*w_a)-x_a\\
y=(t_y*h_a)-y_a\\
$$
​		例如，预测 $t_x= 1$ 会使该框向右移动锚框的宽度，而预测 $t_x= -1$会将其向左移动相同的量。

​		这个公式是不受约束的，所以任何锚框都可以在图像中的任何一点结束，而不管这个框是在哪个位置预测的。随机初始化模型需要很长时间才能稳定以预测合理的偏移。

​		我们没有预测偏移，而是遵循YOLO的方法，预测相对于网格单元位置的位置坐标。这使得真实值的界限在0到1之间。我们使用逻辑激活来限制网络的预测落在这个范围内。

​		网络为特征图的输出的每个单元预测5个边界框。网络预测每个边界框的5个坐标 $t_x, t_y, t_w, t_h, t_o$ 。如果单元格从图像的左上角偏移了 $(c_x,c_y)$ ,并且之前的边界框具有宽度和高度，则预测对应于：
$$
b_x=\sigma(t_x)+c_x\\
b_y=\sigma(t_y)+c_y\\
b_w=p_we^{t_w}\\
b_h=p_he^{t_h}\\
Pr(object)*IOU(b,object)=\sigma(t_o)
$$
​		由于我们限制位置预测，因此参数化更容易学习，从而使网络更加稳定。 使用维度聚类并直接预测边界框中心位置，可以使YOLO比锚框的版本提高近5％。

![YOLO v2 图3](E:\Typora\论文笔记\YOLO v2 图3.png)

图3：具有维度先验和位置预测的边界框。我们预测框的宽度和高度作为聚类质心的偏移量。我们使用sigmoid函数预测相对于滤波器应用位置的框的中心坐标。

​		**细粒度功能。**修改后的YOLO在13×13特征图上预测检测结果。 虽然这对于大型物体是足够的，但使用更细粒度特征对定位较小物体有好处。Faster R-CNN和SSD都在网络中的各种特征图上运行网络，以获得多个分辨率。 我们采取不同的方法，只需添加一个直通层，以26×26的分辨率从较早的层中提取特征。

​		直通层将高分辨率特征与低分辨率特征连接起来，将相邻特征叠加到不同的通道中，而不是空间位置上，类似于ResNet中的恒等映射。将26×26×512的特征图变为13×13×2048的特征图，然后就可以与原来的特征连接。我们的检测器运行在这张扩展的特征图的顶部，以便它可以访问细粒度的功能。这使性能提高了1％。

​		**多尺度训练。**原来的YOLO使用448×448的输入分辨率。通过添加锚框，我们将分辨率更改为416×416。但是，由于我们的模型仅使用卷积层和池化层，因此可以实时调整大小。我们希望YOLOv2能够在不同尺寸的图像上运行，因此我们可以将多尺度训练应到模型中。

​		我们不需要修改输入图像大小，而是每隔几次迭代就改变一次网络。每10个批次我们的网络会随机选择一个新的图像尺寸大小。由于我们的模型缩减了32倍，所以我们从32的倍数中抽取：{320,352，…，608}。因此，最小的选项是320×320，最大的是608×608。我们调整网络的尺寸并继续训练。

​		这个策略迫使网络学习如何在各种输入维度上做好预测。这意味着相同的网络可以预测不同分辨率下的检测结果。网络在较小的尺寸下运行速度更快，因此YOLOv2在速度和准确性之间提供了一个简单的折衷。

​		在低分辨率下，YOLOv2作为一种便宜但相当准确的检测器工作。 在288×288情况下，它的运行速度超过90 FPS，而mAp几乎与Fast R-CNN一样好。这使其成为小型GPU，高帧率视频或多视频流的理想选择。

​		在高分辨率下，YOLOv2是一款先进的检测器，在VOC2007上获得了78.6的mAP，同时仍以高于实时速度运行。请参阅表3，了解YOLOv2与其他框架在VOC 2007上的比较

![YOLO v2 表3](E:\Typora\论文笔记\YOLO v2 表3.png)

表3：PASCAL VOC 2007的检测框架。YOLOv2比以前的检测方法更快，更准确。它也可以以不同的分辨率运行，以便在速度和准确性之间轻松折衷。每个YOLOv2项实际上都是具有相同权重的相同训练模型，只是以不同的大小进行评估。所有的时间的测试都运行在Geforce GTX Titan X（原始的，而不是Pascal模型）

​		**进一步的实验。** 我们在VOC 2012上训练YOLOv2进行检测。表4显示了YOLOv2与其他最先进的检测系统的性能比较。 YOLOv2运行速度远高于对手，且精度达到73.4 mAP。 我们还在COCO上训练，并与表5中的其他方法进行比较。使用VOC度量（IOU = 0.5），YOLOv2获得44.0 mAP，与SSD和Faster R-CNN相当。

![YOLO v2 表4](E:\Typora\论文笔记\YOLO v2 表4.png)

表4：PASCAL VOC2012测试检测结果。YOLOv2与采用ResNet和SSD512的Faster R-CNN等先进检测器性能相当，速度提高2至10倍。

![YOLO v2 表5](E:\Typora\论文笔记\YOLO v2 表5.png)

表5：COCO test-dev集上的结果，来源于论文【11】

### 3. 更快

​		我们希望检测结果准确，但我们也希望检测速度更快。 大多数用于检测的应用程序（如机器人或自动驾驶汽车）都依赖于低延迟预测。 为了最大限度地提高性能，我们从头开始设计YOLOv2。



