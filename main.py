from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from prediction_function import prediction


class drawingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PenBuddy")
        self.setMinimumSize(800,600)
        self.setMaximumSize(800,600)
        self.setStyleSheet( "background-image: url(../doc/DocsUI/FilesUI/PenBuddyDrawingPageBackground.png)" )

        self.previousPoint = None

        Hlayout = QHBoxLayout()
        Hlayout.setContentsMargins(60,30,0,0)
        Vlayout = QVBoxLayout()
        Vlayout.setContentsMargins(0,0,0,0)

        self.label = QLabel()
        self.canvas = QPixmap(QSize(300, 300))
        self.canvas.fill(QColor("white"))
        self.pen = QPen()
        self.pen.setColor(QColor("black"))
        self.pen.setWidth(20)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.brush = QBrush()
        self.brush.setColor(QColor("black"))
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)

        self.label.setPixmap(self.canvas)

        Hlayout.addWidget(self.label)

        button1 = QPushButton(text="Predict")
        button2 = QPushButton(text="Clear")
        self.predictiontxt = QLabel(self)
        self.predictiontxt.setText("Predicted value:  ")

        button1.setStyleSheet(
            '''
            QPushButton {
            background-color: "#2f2f2f";
            border-radius: 5px;
            color: "white";}
            QPushButton:pressed {
            background-color: "#606368";
            }
            '''
        )
        
        button2.setStyleSheet(
            '''
            QPushButton {
            background-color: "#2f2f2f";
            border-radius: 5px;
            color: "white";}
            QPushButton:pressed {
            background-color: "#606368";
            }
            '''
        )

        self.predictiontxt.setStyleSheet(
        '''
        QLabel {
        color: white;
        font-family: Verdana;
        font-size: 24px;
        text-align: right;
        }
        '''
        )

        button1.setMinimumSize(250,50)
        button1.setMaximumSize(250,50)
        button2.setMinimumSize(250,50)
        button2.setMaximumSize(250,50)
        button1.setFont(QFont("Verdana",15))
        button2.setFont(QFont("Verdana",15))
        button1.setCursor(QCursor(QCursor(QCursor(Qt.CursorShape.PointingHandCursor))))
        button2.setCursor(QCursor(QCursor(QCursor(Qt.CursorShape.PointingHandCursor))))

        button1.clicked.connect(self.handle_predict)
        button2.clicked.connect(self.clear)

        Vlayout.addSpacerItem(QSpacerItem(110, 310, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        Vlayout.addWidget(button1)
        Vlayout.addWidget(button2)
        Vlayout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        Vlayout.addWidget(self.predictiontxt)
        Vlayout.addSpacerItem(QSpacerItem(110, 170, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        Hlayout.addLayout(Vlayout)
        Hlayout.addSpacerItem(QSpacerItem(90, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        backgroundWidget = QWidget()
        self.setCentralWidget(backgroundWidget)
        backgroundWidget.setStyleSheet("background:none")
        backgroundWidget.setLayout(Hlayout)
        
    def clear(self):
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)
        self.predictiontxt.setText("Predicted value:  ")  # Reset the prediction text when the canvas is cleared

    def handle_predict(self):
        self.save()
        self.predictiontxt.setText("Predicted value:  " + self.prediction)  # Set the prediction text

    def save(self):
        filePath = "../doc/temp/temp_image.png"
        if filePath:
            self.canvas.save(filePath)
        self.prediction = prediction()

    def mouseMoveEvent(self, event):
        globalPos = QCursor.pos()
        localPos = self.label.mapFromGlobal(globalPos) + QPoint(0,-135)
        
        painter = QPainter(self.canvas)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        if self.previousPoint:
            painter.drawLine(self.previousPoint, localPos)
        else:
            painter.drawPoint(localPos)
        painter.end()

        self.label.setPixmap(self.canvas)
        self.previousPoint = localPos

    def mouseReleaseEvent(self, event):
        self.previousPoint = None

class welcomeScreen(QMainWindow):
    # definisco la schermata principale, all'avvio del programma l'utente visualizzerà questa.
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PenBuddy")
        self.setMinimumSize(800,600)
        self.setMaximumSize(800,600)
        self.setStyleSheet( "background-image: url(../doc/DocsUI/FilesUI/PenBuddyHomePageBackground.png)" )

        layout = QVBoxLayout()
        layout.setContentsMargins(275,350,275,80)
        

        button1 = QPushButton(text="Start Drawing")
        button2 = QPushButton(text="Quit PenBuddy")
        button1.setStyleSheet(
            '''
            QPushButton {
            background-color: "#2f2f2f";
            border-radius: 5px;
            color: "white";}
            QPushButton:pressed {
            background-color: "#606368";
            }
            '''
        )
        
        button2.setStyleSheet(
            '''
            QPushButton {
            background-color: "#2f2f2f";
            border-radius: 5px;
            color: "white";}
            QPushButton:pressed {
            background-color: "#606368";
            }
            '''
        )

        button1.setMinimumSize(250,50)
        button1.setMaximumSize(250,50)
        button2.setMinimumSize(250,50)
        button2.setMaximumSize(250,50)
        button1.setFont(QFont("Verdana",15))
        button2.setFont(QFont("Verdana",15))
        button1.setCursor(QCursor(QCursor(QCursor(Qt.CursorShape.PointingHandCursor))))
        button2.setCursor(QCursor(QCursor(QCursor(Qt.CursorShape.PointingHandCursor))))

        layout.addWidget(button1)
        layout.addWidget(button2)

        backgroundWidget = QWidget()
        self.setCentralWidget(backgroundWidget)
        backgroundWidget.setStyleSheet("background:none")

        backgroundWidget.setLayout(layout)

        button1.clicked.connect(self.startDrawingTab)
        self.drawingWindow = None

    def startDrawingTab(self):
        self.drawingWindow = drawingWindow()
        self.drawingWindow.show()



def main():
    app = QApplication(sys.argv)

    window = welcomeScreen()
    window.show()
     
    app.exec()

if __name__ == '__main__':
    main()