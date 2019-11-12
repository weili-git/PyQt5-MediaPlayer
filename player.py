from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore
import sys

class QtPlayer(QMainWindow):
    pRate = 1.0
    def __init__(self):
        super().__init__()
        # 设置窗口
        self.setGeometry(300, 300, 800, 600 + 96)
        self.setWindowTitle('Player')
        self.setFixedSize(800, 600+96)

        # 设置滑动条
        self.slider = QSlider(QtCore.Qt.Horizontal,self)
        self.slider.setGeometry(10, 640, 800-20, 20)
        self.slider.setRange(0, 100)
        self.slider.sliderPressed.connect(self.SlideChanged)
        self.slider.valueChanged.connect(self.setClock) # 设置时间条
        self.slider.show()
        
        # 设置按钮
        self.btn = QPushButton('暂停', self)
        self.btn.clicked.connect(self.handleButton)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(700/2, 600+60)

        self.btn1 = QPushButton('播放', self)
        self.btn1.clicked.connect(self.handleButton1)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(700/2, 600+60)
        self.btn1.hide()
        
        self.forward = QPushButton('快进', self)
        self.forward.clicked.connect(self.handleForward)
        self.forward.resize(self.btn.sizeHint())
        self.forward.move(700/2+70, 600+60)

        self.back = QPushButton('快退', self)
        self.back.clicked.connect(self.handleBack)
        self.back.resize(self.btn.sizeHint())
        self.back.move(700/2-70, 600+60)   
        
        # 设置菜单
        self.createMenu()
        
        # 多媒体播放器
        self.vw = QVideoWidget(self)
        self.vw.setGeometry(QtCore.QRect(0, 30, 800, 600))
        self.vw.show()

        # 视频读入
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.vw) # 视频播放输出的widget，就是上面定义的
        self.player.positionChanged.connect(self.PlaySlide)
        self.player.durationChanged.connect(self.MediaTime)

        # 音量条（音量初始化需要player定义好了才能设置）
        self.createVol()

        # 时间条    （播放时间/视频时长）
        self.clock = QLabel(self)
        self.clock.setText("00:00/00:00")
        self.clock.setGeometry(550, 660, 80, 30)
        
        # 进入主循环
        self.show()

    def createVol(self): # 音量调节
        self.volLabel = QLabel(self)
        self.volLabel.setText("音量")
        self.volLabel.setGeometry(100, 660, 30, 30)

        self.volSlider = QSlider(QtCore.Qt.Horizontal,self)
        self.volSlider.setGeometry(130, 660, 80, 30)
        self.volSlider.setRange(0, 100)
        self.volSlider.valueChanged.connect(self.volChanged)
        self.volSlider.setValue(80) # 默认80%的音量
        self.volSlider.show()

    def setClock(self):
        tmp1 = self.player.position()
        tmp2 = self.player.duration()
        self.clock.setText("%d:%d/%d:%d" % (tmp1/1000/60, tmp1/1000%60,tmp2/1000/60, tmp2/1000%60))

    def volChanged(self): # 音量调节
        self.player.setVolume(self.volSlider.value())

    def SlideChanged(self): # 滚动条手动改变
        self.player.setPosition(self.slider.value()*1000)

    def PlaySlide(self, val): # 设置滚动条值
        self.slider.setValue(int(val/1000))

    def MediaTime(self, time): # 设置滚动条范围
        self.slider.setValue(0)
        self.time = self.player.duration()/1000
        self.slider.setRange(0, int(self.time))
        
    def handleButton1(self): # 播放
        self.player.play()
        self.btn1.hide()
        self.btn.show()
    
    def handleButton(self): # 暂停
        self.player.pause()
        self.btn.hide()
        self.btn1.show()

    def handleBack(self): # 慢放
        if self.pRate>0.5:
            self.pRate = self.pRate - 0.5
            self.player.setPlaybackRate(self.pRate)
        
    def handleForward(self): # 快放
        if self.pRate<1.5:
            self.pRate = self.pRate + 0.5
            self.player.setPlaybackRate(self.pRate)
        
    def createMenu(self): #创建菜单
        self.fileMenu()

    def fileMenu(self):
        menu = self.menuBar().addMenu('文件(&F)')

        openfile = menu.addAction('打开(&O)', self.openfile_triggered)
        quitfile = menu.addAction('退出(&Q)', self.quitfile_triggered)

        openfile.setShortcut("Ctrl+O")
        quitfile.setShortcut("Ctrl+Q")
        

    def openfile_triggered(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        self.player.play()
        """
        filename, fileType = QFileDialog.getOpenFileName(self, "打开文件", './', "Video Files(*.mp4)")
        if len(fileType) != 0:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))  # 选取视频文件
            self.player.play() # 播放视频
        """
        

    def quitfile_triggered(self):
        self.close()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtPlayer()
    sys.exit(app.exec_())
