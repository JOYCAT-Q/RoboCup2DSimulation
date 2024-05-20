# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import sys


# ==============================
# @author: Joycat
# @time: 2024/5/3
# ==============================
class Simulation2DEnvironment:
    def __init__(self):
        self.sysVersion = str()
        self.sysSources = str()
        self.supportedSysVersion = ("20.04", "22.04")  # 本脚本所支持的系统版本,后期可增加更新其他系统版本
        self.serverPath = ("./Server17", "./Server18")  # 不同版本Server等软件包所在文件夹
        self.SystemSourcesFolder = "./SystemSources"  # Ubuntu系统镜像源所在文件夹
        self.netWorkDriversFolder = "./NetWorkDrivers"  # 部分网卡驱动所在文件夹
        self.debFolder = "./deb"  # QQ等deb软件包所在文件夹
        self.isInstalledToolsAndDependencies = False  # 判断当前对象是否已安装前置依赖
        self.errorMessages = list()
        self.correctMessages = list()
        self.neededDict = {"bison": 0, "fedit2": 0, "librcsc": 0, "rcsslogplayer": 0, "rcssmonitor": 0, "rcssserver": 0,
                           "soccerwindow2": 0}
        if not self.checkSystemVersion():
            sys.exit(0)
        self.getSystemSource()
        self.APPCOUNTS = 7  # 一共有7个软件包
        self.installedServerVersion = None  # 保存用户选择的Server版本信息

    @staticmethod
    def checkNetworkStatus():
        response = os.system("ping -c 1 www.baidu.com")
        if response == 0:
            print("\n网络连接正常\n")
            # self.correctMessages.append("\n网络连接正常\n")
            return True
        else:
            print("\n网络连接异常,请检查网络是否连接\n")
            # self.errorMessages.append("\n网络连接异常,请检查网络是否连接\n")
            return False

    def checkSystemVersion(self):
        try:
            cmd = "cat /etc/lsb-release | grep DISTRIB_RELEASE | awk -F '=' '{print $2}'"
            self.sysVersion = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        except Exception as e:
            print(e)
            print("\nCould not find release information\n")
            # self.errorMessages.append(str(e))
            # self.errorMessages.append("\nCould not find release information\n")
            return False
        if self.sysVersion in self.supportedSysVersion:
            print("\n系统版本为: ", self.sysVersion)
            # self.correctMessages.append("\n系统版本为: " + self.sysVersion)
            return True
        else:
            print("\n暂未对该版本系统进行支持\n")
            # self.errorMessages.append("\n暂未对该版本系统进行支持\n")
            return False

    def getSystemSource(self):
        if self.sysVersion == self.supportedSysVersion[0]:
            self.sysSources = "sources_U20.04.list"
            return True
        elif self.sysVersion == self.supportedSysVersion[1]:
            self.sysSources = "sources_U22.04.list"
            return True
        else:
            print("\nUnknown version\n")
            # self.errorMessages.append("\nUnknown version\n")
            return False

    @staticmethod
    def runCommands(commands, cwd=os.getcwd()):
        outputs = []
        for cmd in commands:
            # 启动命令并获取输出和错误  
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            stdout, stderr = proc.communicate()  # 等待进程完成并获取输出和错误  
            # 如果需要文本，则解码  
            if stdout:
                # stdout = stdout.decode()    
                print(stdout.decode())
            if stderr:
                # stderr = stderr.decode()    
                print(stderr.decode())
            # outputs.append((stdout, stderr))  # 将输出和错误添加到列表中    
        # 返回所有命令的输出和错误    
        return outputs

    def showRunCommandOutputs(self, outputs):
        # 终端打印移入runCommands(self, commands, cwd=os.getcwd())中
        # 有需要可自行移至此函数下打印
        pass
        # for output in outputs:
        #     if output[0]:
        #         print(output[0])
        #     if output[1]:
        #         print(output[1])

    def changeSysSource(self):
        cmds = list()
        if not os.path.exists("/etc/apt/sources.backup.list"):
            cmds.append("sudo cp /etc/apt/sources.list /etc/apt/sources.backup.list")
        else:
            print("\nsources.backup.list already exists\n")
            # self.correctMessages.append("\nsources.backup.list already exists\n")
            return True
        cmds.append("sudo rm -f /etc/apt/sources.list")
        cmds.append(f"sudo cp {self.SystemSourcesFolder}/{self.sysSources} /etc/apt/sources.list")
        cmds.append("sudo chmod 777 /etc/apt/sources.list")
        cmds.append("sudo apt-get update")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)
        print("\nChanged the source successfully \n")
        # self.correctMessages.append("\nChanged the source successfully \n")
        return True

    def resetSysSource(self):
        cmds = list()
        os.system("clear")
        print("当前是重置系统镜像源===========")
        input("\nPress <Enter> to continue")

        if not os.path.exists("/etc/apt/sources.backup.list"):
            answer = input("\n不存在系统源备份文件,是否现在进行备份?(Y/n): ")
            if answer.lower() == "y":
                cmds.append("sudo cp /etc/apt/sources.list /etc/apt/sources.backup.list")
            else:
                return False
        cmds.append("sudo rm -f /etc/apt/sources.list")
        cmds.append("sudo cp /etc/apt/sources.backup.list /etc/apt/sources.list")
        cmds.append("sudo apt-get update")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)
        print("\nSource has been reseted\n")
        # self.correctMessages.append("\nSource has been reseted\n")
        return True

    def installToolsAndDependencies(self):
        self.changeSysSource()
        preDependences = (
            "-f", "build-essential", "libboost-all-dev", "autoconf", "automake", "libtool", "flex", "bison",
            "libfontconfig1-dev", "libaudio-dev", "libxt-dev", "libglib2.0-dev", "libxi-dev", "libxrender-dev",
            "libfreetype6-dev", "libpng-dev")
        tools = (
            "rar", "unrar", "p7zip", "zlib*", "vim", "qtcreator", "python-setuptools", "python3-pip", "zip", "unzip",
            "git",
            "wget", "qtbase5-dev", "qt5-qmake", "ssh")
        cmds = list()
        for preDependence in preDependences:
            cmds.append(f"sudo apt-get -y install {preDependence}")
        for tool in tools:
            cmds.append(f"sudo apt-get -y install {tool}")

        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)
        if self.sysVersion == self.supportedSysVersion[0]:  # 20.04下可以正常在线安装QT4,其他则取消安装
            self.installQT4Online()

        print("\nTools and dependencies have been installed\n")
        # self.correctMessages.append("\nTools and dependencies have been installed\n")
        self.deleteAndCleanLock()
        self.isInstalledToolsAndDependencies = True
        return True

    def installQT4Online(self):
        cmds = list()
        qt4s = ("libqt4-dev", "qt4-dev-tools", "qt4-doc", "qt4-designer", "qt4-qtconfig", "libqt4-opengl-dev",
                "libqt4-sql-mysql", "libqt4-sql-odbc", "libqt4-sql-psql", "libqt4-sql-sqlite")

        cmds.append("sudo add-apt-repository ppa:rock-core/qt4")
        for qt4 in qt4s:
            cmds.append(f"sudo apt-get -y install {qt4}")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)

        print("\nQT4 has been installed\n")
        # self.correctMessages.append("\nQT4 has been installed\n")
        return True

    def deleteAndCleanLock(self):
        cmds = list()
        cmds.append("sudo rm -f /var/lib/dpkg/lock")
        cmds.append("sudo rm -f /var/lib/dpkg/lock-frontend")
        cmds.append("sudo rm -f /var/cache/apt/archives/lock")
        cmds.append("sudo dpkg --configure -a")
        cmds.append("sudo apt-get autoclean")
        cmds.append("sudo apt-get clean")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)

        print("\nLock has been deleted\n")
        # self.correctMessages.append("\nLock has been deleted\n")
        return True

    @staticmethod
    def findAndRemoveFolder(targetFolder):
        if os.path.exists(targetFolder):
            shutil.rmtree(targetFolder)
            print(f"\nAlready Delete {targetFolder}\n")
            # self.correctMessages.append(f"\nAlready Delete {targetFolder}\n")
            return True
        else:
            print(f"\n{targetFolder} does not exist\n")
            # self.correctMessages.append(f"\n{targetFolder} does not exist\n")
            return False

    def installBison(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                # 旧版本包bison-2.7.1由于库更新导致编译错误，换用新版包
                self.findAndRemoveFolder(f"{self.serverPath[0]}/bison-3.8.2")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/bison-3.8.2.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/bison-3.8.2"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/bison-3.8.2")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/bison-3.8.2.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/bison-3.8.2"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./configure")
            cmds2.append("sudo ldconfig")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过bison安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过bison安装--------------------------------------------\n")
            return False

    def installLibrcsc(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/librcsc")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/librcsc.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/librcsc"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/librcsc-rc2023")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/librcsc-rc2023.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/librcsc-rc2023"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./bootstrap")
            cmds2.append("./configure --disable-unit-test")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过librcsc安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过librcsc安装--------------------------------------------\n")
            return False

    def installRcssserver(self, serverVersion, isInstall=True):
        if isInstall:
            os.system("rm -rf ~/.rcssserver/")
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/rcssserver-17.0.0")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/rcssserver-17.0.0.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/rcssserver-17.0.0"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/rcssserver-18.1.3")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/rcssserver-18.1.3.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/rcssserver-18.1.3"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./bootstrap")
            cmds2.append("./bootstrap")
            cmds2.append("./configure")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            cmds2.append("sudo ldconfig")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过rcssserver安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过rcssserver安装--------------------------------------------\n")
            return False

    def installRcssmonitor(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/rcssmonitor-17.0.0")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/rcssmonitor-17.0.0.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/rcssmonitor-17.0.0"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/rcssmonitor-18.0.0")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/rcssmonitor-18.0.0.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/rcssmonitor-18.0.0"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./bootstrap")
            cmds2.append("./bootstrap")
            cmds2.append("./configure")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            cmds2.append("sudo ldconfig")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过rcssmonitor安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过rcssmonitor安装--------------------------------------------\n")
            return False

    def installRcsslogplayer(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/rcsslogplayer-15.2.0")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/rcsslogplayer-15.2.0.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/rcsslogplayer-15.2.0"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/rcsslogplayer-15.2.1")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/rcsslogplayer-15.2.1.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/rcsslogplayer-15.2.1"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./configure")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            cmds2.append("sudo ldconfig")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过rcsslogplayer安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过rcsslogplayer安装--------------------------------------------\n")
            return False

    def installFedit2(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/fedit2")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/fedit2.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/fedit2"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/fedit2-support-v18")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/fedit2-support-v18.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/fedit2-support-v18"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./bootstrap")
            cmds2.append("./configure")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过fedit2安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过fedit2安装--------------------------------------------\n")
            return False

    def installSoccerwindow2(self, serverVersion, isInstall=True):
        if isInstall:
            cmds1 = list()
            if serverVersion == "17":
                self.findAndRemoveFolder(f"{self.serverPath[0]}/soccerwindow2")
                cmds1.append(f"tar -zxvf {self.serverPath[0]}/soccerwindow2.tar.gz -C {self.serverPath[0]}")
                cwd = f"{self.serverPath[0]}/soccerwindow2"
            elif serverVersion == "18":
                self.findAndRemoveFolder(f"{self.serverPath[1]}/soccerwindow2-rc2023")
                cmds1.append(f"tar -zxvf {self.serverPath[1]}/soccerwindow2-rc2023.tar.gz -C {self.serverPath[1]}")
                cwd = f"{self.serverPath[1]}/soccerwindow2-rc2023"
            else:
                return False
            outputs = self.runCommands(cmds1)
            self.showRunCommandOutputs(outputs)
            cmds2 = list()
            cmds2.append("./bootstrap")
            cmds2.append("./configure")
            cmds2.append("make -j$(nproc)")
            cmds2.append("sudo make install")
            cmds2.append("sudo ldconfig")
            outputs = self.runCommands(cmds2, cwd)
            self.showRunCommandOutputs(outputs)
            return True
        else:
            print("\n跳过soccerwindow2安装--------------------------------------------\n")
            # self.correctMessages.append("\n跳过soccerwindow2安装--------------------------------------------\n")
            return False

    def installDeb(self):
        cmds = list()
        os.system("clear")
        print("当前是安装软件包QQ,VScode===========")
        print("QQ: 强大的聊天软件,不必多说")
        print("VScode: 强大且好用，适合新手的代码编辑器, 或者使用QT进行编写代码")
        input("\nPress <Enter> to continue")
        if not os.path.exists(f"{self.debFolder}/linuxqq_3.2.5-21357_amd64.deb"):
            # cmds.append(f"rm -f {self.debFolder}/linuxqq_3.2.5-21357_amd64.deb")
            cmds.append(
                f"wget -P {self.debFolder} https://dldir1.qq.com/qqfile/qq/QQNT/7c0c5cc3/linuxqq_3.2.5-21357_amd64.deb")
        cmds.append(f"sudo dpkg -i {self.debFolder}/linuxqq_3.2.5-21357_amd64.deb")
        cmds.append(f"sudo dpkg -i {self.debFolder}/code_1.82.0-1694039253_amd64.deb")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)
        return True

    def checkInstall(self):
        os.system("clear")
        print("当前是测试已安装文件===========")
        input("\nPress <Enter> to continue")

        if self.sysVersion == self.supportedSysVersion[1]:
            cmds = ["soccerwindow2", "fedit2"]
        elif self.sysVersion == self.supportedSysVersion[0]:
            cmds = ["soccerwindow2", "fedit2", "rcssmonitor", "rcsslogplayer"]
        else:
            return False
        try:
            print("\n将弹出的测试窗口自行关闭后测试自动结束.........")
            print(
                "=============\n\trcssserver命令由于无法自行关闭,请自行测试(右键新开终端输入命令即可)\t\n=============")
            outputs = self.runCommands(cmds)
            self.showRunCommandOutputs(outputs)
        except Exception:
            pass

    def changePip3Source(self):
        cmds = list()
        os.system("clear")
        print("当前是更改pip3镜像源===========")
        input("\nPress <Enter> to continue")

        cmds.append("pip3 -V")
        cmds.append("pip3 config --global set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)

    def makeClean(self, foldersPath):
        if os.path.exists(foldersPath):
            cmds = list()
            cmds.append("make uninstall")
            cmds.append("make clean")
            outputs = self.runCommands(cmds, foldersPath)
            self.showRunCommandOutputs(outputs)
            print(f"\n{foldersPath} has been removed ")
            self.findAndRemoveFolder(foldersPath)
            return True
        else:
            print(f"\n{foldersPath} does not exist ")
            return False

    def getNeededDict(self, operation):
        os.system("clear")
        print(f"请选择需要{operation}的软件===========")
        print("bison", "fedit2", "librcsc", "rcsslogplayer", "rcssmonitor", "rcssserver", "soccerwindow2")
        print(f"\n输入顺序与上述顺序一一对应, 模式 a 即代表全部{operation}, 模式 b 即代表选择特定{operation}")
        print("\n模式 a 下输入格式: a (仅一个a即可)")
        print(
            f"\n模式 b 下输入格式: b0000000(即为全部不{operation}) b1111111(即为全部{operation})"
            f"\n[({operation}操作 即为1, 无操作则为0)请自行选择所需进行{operation}]")
        print("\n输入格式错误会进行重新输入")
        print(
            "\n安装旧的librcsc包(Server17目录下的库)后,单独安装新的其他软件包时(如Server18目录下的SoccerWindow2),需要将librcsc安装新版")
        print(f"\nUbuntu {self.supportedSysVersion[1]} 下取消 rcsslogplayer rcssmonitor 的安装(有需要自行摸索安装)")
        choice = input("\n输入你的选择: ")
        choiceList = list(choice)
        i = 1
        try:
            while len(choiceList) <= self.APPCOUNTS:
                choiceList.append(0)
            if choiceList[0].lower() == "a":
                for key in self.neededDict.keys():
                    self.neededDict[key] = 1
            elif choiceList[0].lower() == "b":
                for key in self.neededDict.keys():
                    if int(choiceList[i]):
                        self.neededDict[key] = 1
                    i = i + 1
            else:
                return False
        except Exception:
            return False
        return True

    def uninstall(self):
        while not self.getNeededDict("卸载"):
            self.getNeededDict("卸载")
        print(f"请确认你的卸载选择: {self.neededDict}")
        answer = input("\nPress <Enter> to continue, or 'q' to reinput: ")
        if answer.lower() == 'q':
            return self.uninstall()

        foldersServer17 = ["bison-3.8.2", "fedit2", "librcsc", "rcsslogplayer-15.2.0", "rcssmonitor-17.0.0",
                           "rcssserver-17.0.0", "soccerwindow2"]
        cwd1 = f"{self.serverPath[0]}/"
        foldersServer18 = ["bison-3.8.2", "fedit2-support-v18", "librcsc-rc2023", "rcsslogplayer-15.2.1",
                           "rcssmonitor-18.0.0", "rcssserver-18.1.3", "soccerwindow2-rc2023"]
        cwd2 = f"{self.serverPath[1]}/"
        pathListServer17 = list()
        pathListServer18 = list()
        for path in foldersServer17:
            pathListServer17.append(cwd1 + path)
        for path in foldersServer18:
            pathListServer18.append(cwd2 + path)
        tmp = 0
        for key in self.neededDict.keys():
            if self.neededDict[key]:
                self.makeClean(pathListServer17[tmp])
                self.makeClean(pathListServer18[tmp])
            tmp = tmp + 1

    def installApplication(self, serverVersion):
        while not self.getNeededDict("安装"):
            self.getNeededDict("安装")
        print(f"请确认你的安装选择: {self.neededDict}")
        print("\nThe system  version is : Ubuntu", self.sysVersion)
        print("\nThe system source version is : ", self.sysSources)
        answer = input("\nPress <Enter> to continue, or 'q' to reinput: ")
        if answer.lower() == 'q':
            return self.installApplication(serverVersion=self.installedServerVersion)

        self.installBison(serverVersion, isInstall=bool(self.neededDict["bison"]))
        self.installLibrcsc(serverVersion, isInstall=bool(self.neededDict["librcsc"]))
        self.installFedit2(serverVersion, isInstall=bool(self.neededDict["fedit2"]))
        if self.sysVersion == self.supportedSysVersion[0]:  # 20.04下可以正常在线安装Qt4,根据用户选择进行安装
            pass
        else:
            # 22.04以外下无法在线安装Qt4, 因此需要相关环境的软件也取消安装
            self.neededDict["rcsslogplayer"] = 0
            self.neededDict["rcssmonitor"] = 0
        self.installRcsslogplayer(serverVersion, isInstall=bool(self.neededDict["rcsslogplayer"]))
        self.installRcssmonitor(serverVersion,
                                isInstall=bool(self.neededDict["rcssmonitor"]))  # 此软件不需要QT4环境,但一般用不到,所以在20.04以外也取消安装
        self.installRcssserver(serverVersion, isInstall=bool(self.neededDict["rcssserver"]))
        self.installSoccerwindow2(serverVersion, isInstall=bool(self.neededDict["soccerwindow2"]))

    def releaseLocked(self):
        os.system("clear")
        print("当前是释放锁资源,遭遇锁资源被占用无法释放时使用===========")
        input("\nPress <Enter> to continue")
        self.deleteAndCleanLock()

    def syncTime(self):
        os.system("clear")
        cmds = list()
        print("当前是实机安装ubuntu后进行同步时间操作,虚拟机无需操作,即使操作也不会产生影响===========")
        input("\nPress <Enter> to continue")

        cmds.append("sudo apt-get -y install ntpdate")
        cmds.append("sudo ntpdate time.windows.com")
        cmds.append("sudo hwclock --localtime --systohc")
        outputs = self.runCommands(cmds)
        self.showRunCommandOutputs(outputs)

        print("------> 网络时间同步完成!!!")

    @staticmethod
    def netWorkDriversMenu():
        os.system("clear")
        print("\t\t================= NetWorkDrivers Menu==============================")
        print("\t\t------>1. \tRtl8852 Series")
        print("\t\t------>2. \tIntel AX210/AX211 160MHz")
        print("\t\t------> \t Intel AX201 160MHz")
        print("\t\t------> \t Intel AX200 160MHz")
        print("\t\t------> \t Intel Wireless-AC 9560/9462/9461")
        print("\t\t------> \t Intel Wireless-AC 9260")
        print("\t\t------> \t Intel Dual Band Wireless-AC 3168")
        print("\t\t------> \t Intel Dual Band Wireless-AC 8265")
        print("\t\t------> \t Intel Dual Band Wireless-AC 8260")
        print("\t\t------>\t\t Intel Dual Band Wireless-AC 3165/7265 Series")
        print("\t\t------>\t\t Intel Dual Band Wireless-AC 3160")
        print("\t\t------>\t\t Intel Dual Band Wireless-AC 7260 Series")
        print("\t\t------> 3. Extra Opeartion")
        print("\t\t------> 4. 重置网卡驱动文件夹(即恢复到最开始状态)")
        print("\t\t------> 0. Exit")
        print("\t\t------> 操作完自己手动重启电脑进行验证")
        print("\t\t------> Intel 系列网卡放在一起, 只要型号满足,选择 2 即可")
        print("\t\t------> 当网卡驱动安装好重启后仍未有WIFI, 但蓝牙正常时, 输入 3 额外操作进行尝试")
        print("\t\t------> 不要修改默认内核版本,若已经修改,自行在开机界面选择高级模式下切换默认内核进入系统")
        print("\t\t------> 不清楚自己网卡型号的,请切换到 Windows 下打开设备管理器中网络适配器下进行查看")
        print("\n")

    def installNetWorkDrivers(self):
        self.netWorkDriversMenu()
        while True:
            choice = input("\n输入你的选择(0-4): ")
            choice = list(choice)[0]
            if not os.path.exists("/lib/firmwarebak"):
                os.system("sudo cp -r /lib/firmware /lib/firmwarebak")
            if choice == "1":
                self.findAndRemoveFolder(f"{self.netWorkDriversFolder}/rtl8852be-main/")
                os.system(f"tar -zxvf {self.netWorkDriversFolder}/rtl8852be-main.tgz -C {self.netWorkDriversFolder}/")
                cmds = list()
                cmds.append("make -j$(nproc)")
                cmds.append("sudo make install")
                cmds.append("sudo modprobe 8852be")
                outputs = self.runCommands(cmds, f"{self.netWorkDriversFolder}/rtl8852be-main/")
                self.showRunCommandOutputs(outputs)
                break
            elif choice == "2":
                self.findAndRemoveFolder(f"{self.netWorkDriversFolder}/NetDriversALL/")
                self.findAndRemoveFolder(f"{self.netWorkDriversFolder}/backport-iwlwifi/")
                cmds = list()
                cmds2 = list()
                cmds.append("unzip ./backport-iwlwifi.zip")
                cmds.append("unzip ./NetDriversALL.zip")

                cmds2.append("sudo make defconfig-iwlwifi-public")
                cmds2.append("sudo make -j$(nproc)")
                cmds2.append("sudo make install")

                cmds.append(f"sudo cp -r ./NetDriversALL/* /lib/firmware/")

                outputs = self.runCommands(cmds, f"{self.netWorkDriversFolder}/")
                self.showRunCommandOutputs(outputs)
                outputs = self.runCommands(cmds2, cwd=f"{self.netWorkDriversFolder}/backport-iwlwifi/")
                self.showRunCommandOutputs(outputs)

                break
            elif choice == "3":
                if os.path.exists("/lib/firmware/iwlwifi-ty-a0-gf-a0.pnvm"):
                    os.system(
                        "sudo mv /lib/firmware/iwlwifi-ty-a0-gf-a0.pnvm /lib/firmware/iwlwifi-ty-a0-gf-a0.pnvm.bak")
                else:
                    print("\nyou already have done it. ")
                break
            elif choice == "4":
                if os.path.exists("/lib/firmwarebak"):
                    cmds = list()
                    cmds.append("sudo rm -rf /lib/firmware")
                    cmds.append("sudo cp -r /lib/firmwarebak /lib/firmware")
                    outputs = self.runCommands(cmds)
                    self.showRunCommandOutputs(outputs)
                    print("\nNetDriver firmware resets Successfully...")
                    break
            elif choice == "0":
                break
            else:
                print("invalid choice, input again\n")

    @staticmethod
    def mainMenuShow():
        print("\n")
        print("\t\t====================MENU===================")
        print("\t\t===  1.安装前置依赖和工具            \t===")
        print("\t\t===  2.自定义选择安装软件包(Server17)\t===")
        print("\t\t===  3.自定义选择安装软件包(Server18)\t===")
        print("\t\t===  4.自定义选择卸载已安装软件包     \t===")
        print("\t\t===  5.测试软件包安装结果            \t===")
        print("\t\t===  6.安装QQ VSCode              \t===")
        print("\t\t===  7.更换pip3默认下载源(清华源)    \t===")
        print("\t\t===  8.重置Ubuntu系统源            \t===")
        print("\t\t===  9.更换Ubuntu系统源(清华源)     \t===")
        print("\t\t===  10.释放锁资源占用              \t===")
        print("\t\t===  11.同步BIOS网络时间            \t===")
        print("\t\t===  0.退出                        \t===")
        print("\t\t===  PS:每一个功能需要运行结束后才会有反馈")
        print("\t\t===  所以可能无法及时给出终端反馈")
        print("\t\t===  因此请不要手动取消进程的执行")
        print("\t\t===  ./NetworkDrivers/目录下存放着一些")
        print("\t\t===  网卡驱动文件,Ubuntu无线网卡驱动")
        print("\t\t===  无法正常加载时可自行摸索安装")
        print("\t\t===========================================")
        print("\n")

    def runMain(self):
        if not self.checkNetworkStatus():
            sys.exit(1)

        if os.system('''python3 -V''') != 0:
            print("Please install python3 by yourself with install_py3.sh !!!")
            sys.exit(1)

        while True:
            self.mainMenuShow()
            choice = input("Input your choice(0-12): ")
            if choice == "1":
                self.installToolsAndDependencies()
            elif choice == "2":
                if not self.isInstalledToolsAndDependencies:
                    answer = input(
                        "Please install Tools and Dependencies first, do you want to install it now?"
                        "\nIf you have already installed pre-dependencies and tools, please enter n (Y/n): ")
                    if answer.lower() == "y":
                        self.installToolsAndDependencies()
                    elif answer.lower() == "n":
                        pass
                    else:
                        continue
                self.installApplication(serverVersion="17")
                self.installedServerVersion = "17"
            elif choice == "3":
                if not self.isInstalledToolsAndDependencies:
                    answer = input(
                        "Please install Tools and Dependencies first, do you want to install it now?"
                        "\nIf you have already installed pre-dependencies and tools, please enter n (Y/n): ")
                    if answer.lower() == "y":
                        self.installToolsAndDependencies()
                    elif answer.lower() == "n":
                        pass
                    else:
                        continue
                self.installApplication(serverVersion="18")
                self.installedServerVersion = "18"
            elif choice == "4":
                self.uninstall()
            elif choice == "5":
                self.checkInstall()
            elif choice == "6":
                self.installDeb()
            elif choice == "7":
                self.changePip3Source()
            elif choice == "8":
                self.resetSysSource()
            elif choice == "9":
                self.changeSysSource()
            elif choice == "10":
                self.releaseLocked()
            elif choice == "11":
                self.syncTime()
            # elif choice == "12":
            #     self.installNetWorkDrivers()
            elif choice == "0":
                print("\nThanks for using")
                break
            else:
                print("invalid choice, input again\n")


if __name__ == "__main__":
    try:
        S2DE = Simulation2DEnvironment()
        S2DE.runMain()
    except Exception as e:
        print(e)
