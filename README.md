# dllshow
可视化wine及win7的dll及api之间的依赖、转发等关系。

|    文件夹     |    功能     |
| :--------: | :-------: |
|   DLLAPI   | dllapi调用图 |
| DLLForward |  dll转发图   |
|  DLLGRAPH  |  dll依赖图   |
|  DLLPOINT  |   dll点图   |

环境：

- python3.6
- flask
- pymysql

改进：

采用分布式架构，所有代码合并到**dllshow**工程下。以往代码仅供参考，不再使用。

主页如下所示：

![image](https://github.com/QianShengWu/DllShow/master/index.png?raw=true)