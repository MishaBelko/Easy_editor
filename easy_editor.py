#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap

from PIL import Image 
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
Ib_image = QLabel('Картинка')
Btn_dir = QPushButton('Папка')
Iw_files = QListWidget()

btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Размытие')
btn_contour = QPushButton('Контур')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(Btn_dir)
col1.addWidget(Iw_files)
col2.addWidget(Ib_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_contour)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir =  ''

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modifled/'    

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveimage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        Ib_image.hide()
        pixmapimage = QPixmap(path)
        w, h = Ib_image.width(), Ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        Ib_image.setPixmap(pixmapimage)
        Ib_image.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_contour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.saveimage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

def showChosenImage():
    if Iw_files.currentRow() >= 0:
        filename = Iw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))
       

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extensions)
    Iw_files.clear()
    for filename in filenames:
        Iw_files.addItem(filename)

workimage = ImageProcessor()
Btn_dir.clicked.connect(showFilenamesList)
Iw_files.currentItemChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_blur.clicked.connect(workimage.do_blur)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_contour.clicked.connect(workimage.do_contour)
app.exec()