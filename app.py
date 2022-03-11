import sys
from typing import Set
import aiohttp
from time import sleep
import asyncio
import discord
import mainbot
import config
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFrame,
    QFontComboBox,
    QLabel,
    QListWidget,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)



# def clickable(widget):
#     class Filter(QObject):

#         clicked = pyqtSignal()

#         def eventFilter(self, obj, event):

#             if obj == widget:
#                 if event.type() == QEvent.MouseButtonRelease:
#                     if obj.rect().contains(event.pos()):
#                         self.clicked.emit()
#                         # can opt for emit(obj) to get an object
#                         return True
#             return False

#     filter = Filter(widget)
#     widget.installEventFilter(filter)
#     return filter.clicked

'''
Pass a mutable object (list or dictionary) to the threads constructor
along with an index or identifier. The thread can then store it's results
in its proper location.

'''


#approx 400x480 would be a good size for entire window
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long running task"""
        # for i in range(5):
        #     sleep(1)
        #     self.progress.emit(i + 1)
        
        print('start_bot running')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #print('before emit')
        self.progress.emit('run in progress')
        #print('after emit')
        client = mainbot.MainBot()
        #client.loop.create_task()
        
        client.run(config.api_token)
        print('start_bot end')
        self.finished.emit()



class SetListMessage(QObject):
    startedBotSuccess = pyqtSignal()



# Subclass QMainWindow to customize application's main window
class MainWindow(QMainWindow):
    asyncFuncSignal = pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()
        # self.setStyleSheet("myLabel { background-color: #7EA7B7 }")
        #self.setStyleSheet("myLabel { background-color: #5B808F; border-style:solid; border-width:1px}")
        
        self.setStyleSheet("MainWindow { background-color: #BBCFDE; border-style:outset; border-width:4px; border-color: grey;}")
        self.setStyleSheet("myLabel { background-color: #798777; border-style:outset; border-width:4px; border-color: grey;} MainWindow { background-color: #A2B29F; border-style:outset; border-width:4px; border-color: grey;} QListWidget { background: #F8EDE3; }"
        
        
        )
        
    # def expandThumbnail(self):
    #     self.expandThumbnail()
        

    def initUI(self):
        self.setWindowTitle("Discord Bot")
        # connect button box layout
        connectVBox = QVBoxLayout()
        # title box with image layout
        titleHBox = QHBoxLayout()
        

        # Main title widget and styling
        widgetMainTitle = QLabel("BenderBot")
        font = widgetMainTitle.font()
        font.setPointSize(15)
        widgetMainTitle.setFont(font)
        widgetMainTitle.setAlignment(Qt.AlignVCenter)
        titleHBox.addWidget(widgetMainTitle)
        

        # Thumbnail image
        class myLabel(QLabel):
            def __init__(self):
                super().__init__()
                self.setThumbnail(QLabel)
                self.ToggleSize = False
                # self.setFixedWidth(100)
                self.setFixedHeight(130)
                self.setFixedWidth(130)
                self.rotationCopy = []
                
                # self.setFixedHeight()
                # TODO: could implement flag here for click status
                
                # mousePressEvent = self.expandThumbnail(QLabel)
                
                # self.setThumbnail(QLabel)
            # def expandThumbnail(self):
            #     if self.toggleSize:
            #         self.resize(100, 100)
            #         self.ToggleSize = False
            #     else:
            #         self.resize(120, 120)
            #         # self.scaledToWidth(64)
            #         # self.scaledToHeight(64)
            #         self.ToggleSize = True

            def setThumbnail(self, QLabel):
                self.setPixmap(QPixmap('./img/bender-head-50.png'))
                
                # self.toggleActive = False

            def bender_was_left_clicked(self, ToggleSize):
                # self.setStyleSheet("myLabel { background-color: #5B808F; border-style:solid; border-width:3px}")
                # self.setStyleSheet("myLabel { background-color: #5B808F; border-style:inset; border-width:5px; border-color: grey;}")
                self.setStyleSheet("myLabel { background-color: #6C7A6A; border-style:inset; border-width:5px; border-color: grey;}")
                self.setFrameStyle(QFrame.WinPanel | QFrame.Sunken)
                # MainWindow.addItemToList(self.MainOutputList)
                # on the window, add an item to the window list
                rotationList = [
                    './img/bender-head-50.png',
                    './img/bender-head-50-right.png',
                    './img/bender-head-50-flip.png',
                    './img/bender-head-50-left.png',
                    
                ]
                #rotationCopy = rotationList[:]
                if len(self.rotationCopy) > 0:
                    tmpThumb = self.rotationCopy.pop()
                else:
                    self.rotationCopy = rotationList[:]
                    tmpThumb = self.rotationCopy.pop()
                    # tmpThumb = rotationList[3]

                
                self.setPixmap(QPixmap(tmpThumb))

                self.adjustSize()

            def bender_was_right_clicked(self, ToggleSize):
                print("right clicked")

            def bender_was_left_released(self, ToggleSize):
                self.setFrameStyle(QFrame.WinPanel | QFrame.Raised)
                self.setStyleSheet("myLabel { background-color: #798777; border-style:outset; border-width:4px; border-color: grey;}")
                # self.setStyleSheet("myLabel { background-color: #5B808F; border-left: 4px solid black; border-bottom: 4px solid black; }")

                # TODO: Implement right click event
            def mousePressEvent(self, e):
                if e.button() == Qt.LeftButton:
                    self.bender_was_left_clicked(self.ToggleSize)
                    #window.addItemToList(QListWidget)
                    print("mousePressEvent LEFT")
                elif e.button() == Qt.MiddleButton:
                    print("mousePressEvent MIDDLE")
                elif e.button() == Qt.RightButton:
                    print("mousePressEvent RIGHT")

            def mouseReleaseEvent(self, e):
                if e.button() == Qt.LeftButton:
                    self.bender_was_left_released(self.ToggleSize)
                    self.s = SetListMessage()
                    
                    print("mouseReleaseEvent LEFT")
                elif e.button() == Qt.MiddleButton:
                    print("mouseReleaseEvent MIDDLE")
                elif e.button() == Qt.RightButton:
                    print("mouseReleaseEvent RIGHT")
             
                

                
        # benderThumbnail
        # benderThumbnail.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        
        
        thumbnail = myLabel()
        thumbnail.setAlignment(Qt.AlignCenter)
        # thumbnail.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        thumbnail.setFrameStyle(QFrame.WinPanel | QFrame.Raised)

        # clickable(thumbnail).connect(thumbnail.expandThumbnail)
        # thumbnail.mousePressEvent()

        #thumbnail.mouseReleaseEvent = self.expandThumbnail

        titleHBox.addWidget(thumbnail)
        class InfoPanel(QListWidget):
            def __init__(self, QListWidget):
                super().__init__()
                self.initUI()

            def initUI(self):
                self.mainOutputBox = SetListMessage()
                self.mainOutputBox.startedBotSuccess.connect(self.addItemToList)
            def addItemToList(self):
                self.addItem("We have logged in as Bender!")


               

        # Main output display
        self.mainOutputList = InfoPanel(QListWidget)
        self.mainOutputList.resize(200, 120)

        def addItemToList(self):
            self.mainOutputList.addItem("We have logged in as Bender!")
        
        # make a class that inherits from QListWidget
        

        # give this wiget an add 

        # Connect button
        self.connectBtn = QPushButton("Start Me Up!")
        self.connectBtn.setCheckable(True)
        #task1 = asyncio.create_task(connect_to_server)
        self.connectBtn.clicked.connect(self.the_button_was_clicked)
        
        #connectBtn.clicked.connect(clicked)
        connectVBox.addWidget(self.connectBtn)

        self.exitBtn = QPushButton("Exit")
        self.exitBtn.clicked.connect(self.exit_button_event)
        
        connectVBox.addWidget(self.exitBtn)
        # Main window layout is a vertical box with components nested
        mainWindowLayout = QVBoxLayout()

        mainWindowLayout.addLayout(titleHBox)

        mainWindowLayout.addWidget(self.mainOutputList)

        mainWindowLayout.addLayout(connectVBox)
        widget = QWidget()
        widget.setLayout(mainWindowLayout)
        

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
    
    def setThumbNail(self):
        benderThumbnail = QLabel()
        benderThumbnail.setPixmap(QPixmap('./img/bender-head-50.png'))
        benderThumbnail
        # benderThumbnail.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        benderThumbnail.setFrameStyle(QFrame.WinPanel | QFrame.Raised)

        benderThumbnail.setAlignment(Qt.AlignCenter)

    def setMainInfo(self, Qlabel):
        self.add


    def exit_button_event(self):
        print('Exiting...')
        sys.exit(0)
    
    def the_button_was_clicked(self):
        self.mainOutputList.addItem("Connecting...")
        self.s = SetListMessage()
        
        
        try:
            
            #print("Attempting to contact server...")

            self.connectBtn.setEnabled(False)
            self.asyncFuncSignal.connect(self.runLongTask, Qt.QueuedConnection)
            self.asyncFuncSignal.emit() # check this emit
            # self.mainOutputList.addItem("We have logged in as Bender!")
            self.s.startedBotSuccess.emit()
            #self.mainOutputList.addItem("Connected.")
            
        except Exception as e:
            print("There was an error while trying to connect")
            print(e)
            sys.exit(1)
        #print('The button was clicked!')



    def runLongTask(self):
        # Create a qthread object
        self.thread = QThread()
        # Create a worker object - this will be where the bot loop runs
        self.worker = Worker()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.reportProgress)
        # Start the thread
        self.thread.start()

# @pyqtSlot(str)
# def on_my_signal_str(self, value):
#     assert isinstance(value, str)



def window():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    '''Uncomment this block to have window be frameless'''
    #window.setWindowFlags(Qt.FramelessWindowHint)
    
    window.show()
    sys.exit(app.exec_())

window()


'''
TODO

    - Remove API KEY and implement references to config file -- must be done before pushing to github
    - Add menu bar to top of main window
    - add dark mode
    - have a disconnect button? apply some way to stop bot from running
'''

