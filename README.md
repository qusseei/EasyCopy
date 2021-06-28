# EasyCopy V1.2 20210628
1、拷贝easycopy.exe、easycopy.json、readme.txt到U盘任一纯英文目录下（比如F:\），首先依照以下几点配置easycopy.json，右键记事本打开。
2、starttime：需要拷贝的起始日期（包含此日期）、格式必须为：xxxx-xx-xx，例如：2021-03-05
3、endtime：需要拷贝的终止日期（包含此日期）、格式必须为：xxxx-xx-xx，例如：2021-04-05
4、remote：此值为0时，拷贝本地计算机维修机和日志数据；此值为1时，开启FTP远程下载功能（通常地铁才使用，大铁不需要）；不能为其他数值
5、IP列表：remote为1时，此项设置才有作用。命名可以为ip0、ip1、ip2、ip3等等，依照地铁项目IP分配表依次添加各站维修机IP
6、注意格式，英文双引号，英文冒号，每行后有英文逗号，最后一行没有英文逗号。
7、双击或右键打开软件easycopy.exe运行（不能使用管理员运行），等待软件自动执行完毕，任意键退出或关闭控制台，生成数据在同目录下以此时日期命名的文件夹。
8、演示如下
{
  "starttime": "2021-03-25",
  "endtime": "2021-05-26",
  "remote": "0",
  "ip0": "193.1.1.9",
  "ip1": "192.168.56.1",
  "ip2": "2.16.24.28"
}