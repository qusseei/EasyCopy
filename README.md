## EasyCopy是什么?
一个简单好用的拷贝维修机日志的工具
## EasyCopy如何使用呢?
* 将文件`easycopy.exe`、`easycopy.json`放到任意相同目录下
* 打开`easycopy.json`，设置`starttime`和`endtime`，日期格式遵循：`XXXX-XX-XX`，例如 `2021-03-01`
* `remote`：此值为`0`时，拷贝本地计算机维修机和日志数据；此值为`1`时，开启FTP远程下载功能；此值为`2`时，开启FTP远程下载功能和本地数据;
* IP列表：`remote为1或2时`，此项设置才有作用。命名可以为`ip0、ip1、ip2、ip3`等等，依照地铁项目IP分配表依次添加各站维修机IP
* 双击或右键打开软件easycopy.exe运行，等待软件自动执行完毕，任意键退出或关闭控制台，生成数据在同目录下以此时日期命名的文件夹。
* EasyCopy[下载链接](https://github.com/qusseei/EasyCopy/releases/tag/V1.2)
## easycopy.json示例如下
```javascript
{
  "starttime": "2021-03-25",
  "endtime": "2021-05-26",
  "remote": "0",
  "ip0": "193.1.1.9",
  "ip1": "192.168.56.1",
  "ip2": "2.16.24.28"
}
```
## 问题反馈
* 邮箱:10070794@sdic.com.cn