# Dijkstra 算法

## 1. 单源最短路径

### 1.1 Dijkstra 算法

**思路：**

​		给定一张图，一步一步地求出到各个节点的最短路径，过程中都是基于已经求出的最短路径基础上，求得更远顶点的最短路径。

**算法：**

* 找出距离最近的节点；
* 对于该节点的邻居，检查是否有前往他们的更短路劲，如果有，就更新其新距离；
* 重复这个过程，直到对图中的每个节点都这样做了；
* 可以获得从起始节点到任一节点的最短路径。

**适用范围：有向无环图，且不能处理负权边。**

**时间复杂度**：$O(n^2)$

```python
def dijkstra(graph, vs):
    """
    graph -- 图的邻接矩阵
       vs -- 起始顶点
    """
    
    """
     prev -- 前驱顶点数组。用于存储最短路径下标的数据，prev值为前驱节点下标。
     dist -- 最短路径长度数组。比如dist[i]是"顶点vs"到"顶点i"的最短路径的长度。
     flag -- 记录"顶点vs"到"顶点i"的最短路径是否已成功获取。flag[i]=1表示已获取；flag[i]=0表示未获取。
    """
    
    # 初始化
    flag = [0 for i in range(len(graph[0]))]
    prev = [0 for i in range(len(graph[0]))]
    dist = graph[vs]
    # 对"顶点vs"自身进行初始化（顶点到自身的距离为0，所以不用再修改dist[vx]）
    flag[vs] = 1
    # 遍历图n-1次；每次找出一个顶点的最短路径。
    for i in range(1, len(graph)):  # 已经初始化了第一个点
        Min = float('inf')  # 当前所知距vs顶点最近的距离
        for j in range(len(graph)):
            if flag[j] == 0 and dist[j] < Min:  # 遍历一遍，找到最小的距离
                Min = dist[j]
                k = j  # 记录距离最小的节点为k
        flag[k] = 1
        # 修正当前最短路径和前驱顶点
        # 即，当已经获取"顶点k的最短路径"之后，更新"未获取最短路径的顶点的最短路径和前驱顶点"。
        for j in range(len(graph)):
            new_dist = Min + graph[k][j]
            if flag[j] == 0 and (new_dist < dist[j]):
                dist[j] = new_dist  # 更新当前路径长度
                prev[j] = k   # 更新当前路径
    return dist, prev
```

```python
if __name__ == '__main__':
    Inf = float('inf')
    graph = [[0, 1, 12, Inf, Inf, Inf],
            [Inf, 0, 9, 3, Inf, Inf],
            [Inf, Inf, 0, Inf, 5, Inf],
            [Inf, Inf, 4, 0, 13, 15],
            [Inf, Inf, Inf, Inf, 0, 4],
            [Inf, Inf, Inf, Inf, Inf, 0]]
    dist, prev = dijkstra(graph, 0)
    print(dist, prev)  # 结果为[0, 1, 8, 4, 13, 17] [0, 0, 3, 1, 2, 4]
    # 输出逆序的路径
    print(len(prev) - 1, end=' ')
    print(prev[-1], end=' ')
    p = prev[-1]
    for i in range(len(prev)):
        if p != 0:
            print(prev[p], end=' ')
            p = prev[p]
    # 结果为5 4 2 3 1 0 
```

### 1.2 堆优化的 Dijkstra 算法

​		在寻找未得到最优值的点中最小的值时，采用堆优化，弹出最小值复杂度为O(1)，更新最短距离时压入时间复杂度为O(logn)。

**优化前后时间复杂度对比**：

* **优化前时间复杂度**：$O(V^2+E)$

​		对于每个顶点 $V$ 首先外层循环扫描一遍，在寻找当前最小距离时，内层循环又扫描一遍，所以需 $O(V^2)$ 的时间；对于每条边 $E$ ，在更新其最短距离时，还需 $O(E)$ 的时间。所以总时间为 $O(V^2+E)$。**对于稀疏图效果好，即 $E$ 与 $V^2$ 是一个数量级时**。

*  **优化后时间复杂度**：$O(Vlog(V)+Elog(V))$

​		对于每个顶点 $V$ 首先外层循环扫描一遍，在寻找当前最小距离时，直接 `pop` 出最小堆的跟节点，只需 $O(1)$ 的时间，但是后续再向堆中 `push` 节点时还需 $O(logV)$ 的时间，所以合起来是 $O(VlogV)$ ；对于每条边，更新其最短距离时也需向堆中 `push` 节点，故需 $O(ElogV)$ 的时间。所以总时间为 $O(Vlog(V)+Elog(V))$。**对于稠密图效果好，即 $E$ 与 $V$ 是一个数量级时**。

```python
import heapq

def dijkstra(graph, vs):
    """
    graph -- 图的邻接矩阵
       vs -- 起始顶点
    """
    
    """
     prev -- 前驱顶点数组。用于存储最短路径下标的数据，prev值为前驱节点下标。
     dist -- 最短路径长度数组。比如dist[i]是"顶点vs"到"顶点i"的最短路径的长度。
     flag -- 记录"顶点vs"到"顶点i"的最短路径是否已成功获取。flag[i]=1表示已获取；flag[i]=0表示未获取。
    """
    
    # 初始化
    flag = [0 for i in range(len(graph[0]))]
    prev = [0 for i in range(len(graph[0]))]
    dist = graph[vs]
    # 对"顶点vs"自身进行初始化（顶点到自身的距离为0，所以不用再修改dist[vx]）
    flag[vs] = 1
    # 建立一个小顶堆heap--O(logn)
    heap = []
    for i in range(len(dist)):
        heapq.heappush(heap, [dist[i], i])
    # 循环终止条件为堆中无元素时
    while len(heap) > 0:
        Min, k = heapq.heappop(heap)
        if flag[k] == 1:   # 如果当前节点k已找到了最短路径，跳出循环继续下一次
            continue
        flag[k] = 1
        for j in range(len(graph)):  #此处为了加快速度可以选择只遍历与当前k直接相连的点，需传入邻接表（链式前向星结构）而不是邻接矩阵
            new_dist = Min + graph[k][j]
            if flag[j] == 0 and (new_dist < dist[j]):
                dist[j] = new_dist  # 更新当前路径长度
                prev[j] = k   # 更新当前路径
                heapq.heappush(heap, [new_dist, j])  # 更新堆中元素
    return dist, prev
```

前向星结构如下：

```python
G = {1:{1:0,    2:1,    3:12},
     2:{2:0,    3:9,    4:3},
     3:{3:0,    5:5},
     4:{3:4,    4:0,    5:13,   6:15},
     5:{5:0,    6:4},
     6:{6:0}}
```

### 1.3 前向星与链式前向星

​		前向星**（以储存边的方式来存储图）**是一种特殊的边集数组，我们把边集数组中的每一条边按照起点从小到大排序，如果起点相同就按照终点从小到大排序，并记录下以某个点为起点的所有边在数组中的起始位置和存储长度,那么前向星就构造好了。

​		利用**前向星**，我们可以**在 $O(1)$ 的时间内找到以 $i$ 为起点的第一条边**，**以 $O(len(i))$ 的时间找到以 $i$ 为起点的所有边**。

​		但是利用前向星会有排序操作,如果用快排时间至少为$O(nlog(n))$，如果用链式前向星，就可以避免排序。

## 2. 多源最短路径

### 2.1Dijkstra 算法

​		只需对每个节点都进行一次 Dijkstra 算法。(对于稀疏图效果好)

**时间复杂度**：$V \times O(V^2+E)=O(V^3+V \times E)$

### 2.2 Floyd 算法

​		与 Dijkstra 算法思路类似，也是逐个点寻找最短路径。

**思路**：

​		当从节点 $i$ 到节点 $j$ 时，对于每个中转节点  $k$ ，如果经过这个新节点的路径比原来短，就将从 $i$ 到 $j$ 的最短路径更新为新的值，同时记录新的路径。

**时间复杂度**：$O(V^3)$

```python
def floyd(graph):
    """
    dist -- 邻接矩阵
    path -- 到各个节点的最短路径
    """
    n = len(graph)  # 节点个数
    dist = graph
    # 初始化path
    path = [[i for i in range(len(graph))] for j in range(len(graph[0]))]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if (dist[i][k] + dist[k][j]) < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = path[i][k]
    return dist, path
```

```python
if __name__ == '__main__':
    Inf = float('inf')
    graph = [[0, 1, 12, Inf, Inf, Inf],
            [Inf, 0, 9, 3, Inf, Inf],
            [Inf, Inf, 0, Inf, 5, Inf],
            [Inf, Inf, 4, 0, 13, 15],
            [Inf, Inf, Inf, Inf, 0, 4],
            [Inf, Inf, Inf, Inf, Inf, 0]]
    dist, path = floyd(graph)
    print(dist[0])  # 结果为[0, 1, 8, 4, 13, 17]
    # 输出路径
    n = len(path) - 1
    p = 0
    print(p, end=' ')
    for i in range(n):
        if path[p][n] != n:
            print(path[p][n], end=' ')
            p = path[p][n]
    print(n)   
    # 结果为0 1 3 2 4 5
```

