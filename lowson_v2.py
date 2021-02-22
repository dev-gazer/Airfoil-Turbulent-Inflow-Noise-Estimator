import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QTextEdit, QPushButton, QAction
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
from functions import LowsonRDT


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('RDT-Modified-Lowson Method')
        # creating Lowson widget and setting it as central
        self.lowson = Lowson(parent=self)
        self.setCentralWidget(self.lowson)
        # filling up a menu bar
        bar = self.menuBar()
        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        #export_action = QAction('Export as .png', self) #Soon
        close_action = QAction('Close', self)
        #file_menu.addAction(export_action) #Soon
        file_menu.addAction(close_action)
        # Edit menu
        about_menu = bar.addMenu('About')
        # adding actions to edit menu
        about_action = QAction('About RDT Modified Lowson method', self)
        creator_action = QAction('About the creator', self)
        about_menu.addAction(about_action)
        about_menu.addAction(creator_action)

        # use `connect` method to bind signals to desired behavior
        close_action.triggered.connect(self.close)


class Lowson(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('RDT-Modified-Lowson Method')
        self.window_width, self.window_height = 600, 400
        self.setMinimumSize(self.window_width ,self.window_height)

        layout = QHBoxLayout()
        sublayout = QGridLayout()
        self.setLayout(layout)

        #Labels and Inputs
        self.chordLabel = QLabel(self)
        self.chordLabel.setText('Chord [m]:')
        self.chord = QLineEdit(self)
        self.chord.setText("0.15") 
        self.chord.setValidator(QDoubleValidator(0.99,99.99,2))
        self.chord.textChanged.connect(self.update_chart) # TO DO
        self.chord.move(80, 20)
        self.chord.resize(200, 32)
        self.chordLabel.move(20, 20)
        sublayout.addWidget(self.chordLabel,0,0)
        sublayout.addWidget(self.chord,0,1)
        self.spanLabel = QLabel(self)
        self.spanLabel.setText('Span [m]:')
        self.span = QLineEdit(self)
        self.span.setText("0.495") 
        self.span.setValidator(QDoubleValidator(0.99,99.99,2))
        self.span.textChanged.connect(self.update_chart) # TO DO
        self.span.move(80, 20)
        self.span.resize(200, 32)
        self.spanLabel.move(20, 20)
        sublayout.addWidget(self.spanLabel,1,0)
        sublayout.addWidget(self.span,1,1)
        self.velocityLabel = QLabel(self)
        self.velocityLabel.setText('Velocity [m/s]:')
        self.velocity = QLineEdit(self)
        self.velocity.setText("30")
        self.velocity.setValidator(QDoubleValidator(0.99,99.99,2))
        self.velocity.textChanged.connect(self.update_chart) # TO DO
        self.velocity.move(80, 20)
        self.velocity.resize(200, 32)
        self.velocityLabel.move(20, 20)
        sublayout.addWidget(self.velocityLabel,2,0)
        sublayout.addWidget(self.velocity,2,1)
        self.intensityLabel = QLabel(self)
        self.intensityLabel.setText('Intensity:')
        self.intensity = QLineEdit(self)
        self.intensity.setText("0.04") 
        self.intensity.setValidator(QDoubleValidator(0.99,99.99,2))
        self.intensity.textChanged.connect(self.update_chart) # TO DO
        self.intensity.move(80, 20)
        self.intensity.resize(200, 32)
        self.intensityLabel.move(20, 20)
        sublayout.addWidget(self.intensityLabel,3,0)
        sublayout.addWidget(self.intensity,3,1)
        self.lengthscaleLabel = QLabel(self)
        self.lengthscaleLabel.setText('Length Scale [m]:')
        self.lengthscale = QLineEdit(self)
        self.lengthscale.setText("0.0065") 
        self.lengthscale.setValidator(QDoubleValidator(0.99,99.99,2))
        self.lengthscale.textChanged.connect(self.update_chart) # TO DO
        self.lengthscale.move(80, 20)
        self.lengthscale.resize(200, 32)
        self.lengthscaleLabel.move(20, 20)
        sublayout.addWidget(self.lengthscaleLabel,4,0)
        sublayout.addWidget(self.lengthscale,4,1)
        self.distanceLabel = QLabel(self)
        self.distanceLabel.setText('Distance [m]:')
        self.distance = QLineEdit(self)
        self.distance.setText("1.22")
        self.distance.setValidator(QDoubleValidator(0.99,99.99,2))
        self.distance.textChanged.connect(self.update_chart) # TO DO
        self.distance.move(80, 20)
        self.distance.resize(200, 32)
        self.distanceLabel.move(20, 20)
        sublayout.addWidget(self.distanceLabel,5,0)
        sublayout.addWidget(self.distance,5,1)
        self.aoaLabel = QLabel(self)
        self.aoaLabel.setText('aoa [°]:')
        self.aoa = QLineEdit(self)
        self.aoa.setText("0") 
        self.aoa.setValidator(QDoubleValidator(0.99,99.99,2))
        self.aoa.textChanged.connect(self.update_chart) # TO DO
        self.aoa.move(80, 20)
        self.aoa.resize(200, 32)
        self.aoaLabel.move(20, 20)
        sublayout.addWidget(self.aoaLabel,6,0)
        sublayout.addWidget(self.aoa,6,1)
        self.phiLabel = QLabel(self)
        self.phiLabel.setText('phi [°]:')
        self.phi = QLineEdit(self)
        self.phi.setText("90") 
        self.phi.setValidator(QDoubleValidator(0.99,99.99,2))
        self.phi.textChanged.connect(self.update_chart) # TO DO
        self.phi.move(80, 20)
        self.phi.resize(200, 32)
        self.phiLabel.move(20, 20)
        sublayout.addWidget(self.phiLabel,7,0)
        sublayout.addWidget(self.phi,7,1)
        self.thetaLabel = QLabel(self)
        self.thetaLabel.setText('theta [°]:')
        self.theta = QLineEdit(self)
        self.theta.setText("90") 
        self.theta.setValidator(QDoubleValidator(0.99,99.99,2))
        self.theta.textChanged.connect(self.update_chart) # TO DO
        self.theta.move(80, 20)
        self.theta.resize(200, 32)
        self.thetaLabel.move(20, 20)
        sublayout.addWidget(self.thetaLabel,8,0)
        sublayout.addWidget(self.theta,8,1)
        
        layout.addLayout(sublayout)
        
        self.canvas = FigureCanvas(plt.Figure(figsize=(50,6)))
        layout.addWidget(self.canvas)

        self.insert_ax()

    def insert_ax(self):
        self.ax = self.canvas.figure.subplots()
        #self.ax.set_ylim([0,100])
        self.ax.set_xlim([10,10000])
        self.ax.set_xscale('log')
        self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('SPL [dB]')
        self.ax.grid(linestyle='--', which='both', axis='both', linewidth=0.5)
        self.plot = None

    def update_chart(self):
        chord = self.chord.text()
        span = self.span.text()
        velocity = self.velocity.text()
        intensity = self.intensity.text()
        lengthscale = self.lengthscale.text()
        distance = self.distance.text()
        aoa = self.aoa.text()
        phi = self.phi.text()
        theta = self.theta.text()
        try:
            chord = float(chord)
        except ValueError:
            chord = 0
        try:
            span = float(span)
        except ValueError:
            span = 0
        try:
            velocity = float(velocity)
        except ValueError:
            velocity = 0
        try:
            lengthscale = float(lengthscale)
        except ValueError:
            lengthscale = 0
        try:
            distance = float(distance)
        except ValueError:
            distance = 0
        try:
            aoa = float(aoa)
        except ValueError:
            aoa = 0
        try:
            phi = float(phi)
        except ValueError:
            phi = 0
        try:
            theta = float(theta)
        except ValueError:
            theta = 0
        try:
            intensity = float(intensity)
        except ValueError:
            intensity = 0
        

        frequency = np.array([10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])

        if self.plot:
            l = self.plot.pop(0)
            l.remove()
            del l
        self.plot = self.ax.plot(frequency, LowsonRDT(frequency, chord, span, aoa, velocity, intensity, lengthscale, distance, phi, theta), color='g')
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    QWidget {
        font-size: 15px
    }'''
    )
    # creating main window
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing window...')