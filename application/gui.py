import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyApp(QMainWindow):

    # window setup
    def __init__(self):
        super().__init__()
        # params
        self.x_coord = 0
        self.y_coord = 0
        self.width = 1280
        self.height = 720
        self.setWindowTitle("WTASS v1.0")
        self.setGeometry(self.x_coord, self.y_coord, self.width, self.height)

        # table layout setup
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
    
class TabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # create tab objects
        self.tabs = QTabWidget()    # tab container widget
        self.t1 = QWidget()
        self.t2 = QWidget()
        self.t3 = QWidget()

        # global font size
        self.font_size = 20

        #########################################
        # Create Tab Layouts
        #########################################
        
        # add tabs to parent tab widget
        self.tabs.addTab(self.t1, "Home")
        self.tabs.addTab(self.t2, "Settings")
        self.tabs.addTab(self.t3, "About")

        # tab 1
        self.t1.layout = QVBoxLayout(self) 

        self.h_box_layout = QHBoxLayout()
        self.h_box_layout.setSpacing(5)


        self.gen_btn = QPushButton("Generate")

        self.comb_box = QComboBox()
        self.comb_box.addItem("Fines")
        self.comb_box.addItem("Warnings/Errors")
        self.comb_box.addItem("Both")

        # add widget to h box sub-layout
        self.h_box_layout.addWidget(self.comb_box, 1)
        self.h_box_layout.addWidget(self.gen_btn, 1)

        # add horiztonal box layout to tab parent layout
        self.t1.layout.addItem(self.h_box_layout)


        # text browser
        self.text_box = QTextBrowser()
        self.text_box.setMaximumHeight(80)
        self.text_box.setAcceptRichText(False)
        self.text_box.setOpenExternalLinks(True)    # later used to open the output in file explorer
        self.t1.layout.addWidget(self.text_box)

        # tab 2
        self.t2.layout = QVBoxLayout(self) 
        self.l2 = QLabel()
        self.l2.setText("Tab2 Label") 
        self.t2.layout.addWidget(self.l2) 

        # tab 2
        self.t3.layout = QVBoxLayout(self) 
        self.l3 = QLabel()
        self.l3.setText("Tab3 Label") 
        self.t3.layout.addWidget(self.l3)

        # apply the changes to respective QVBox layout tabs
        self.t1.setLayout(self.t1.layout)
        self.t2.setLayout(self.t2.layout)
        self.t3.setLayout(self.t3.layout)  

        # Add tabs to layout widget (which gets added to the myApp window clas) 
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # create an object of class myApp
    appWindow = MyApp()
    # show the window
    MyApp.show(appWindow)
    sys.exit(app.exec_()) 