from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet('font-size:20px;')
        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle('About Me')
       
        self.my_name=QLabel('Idan Naor',self)
        self.my_name.setGeometry(150,20,300,30)

        self.my_email=QLabel('Email: idan.naor@s.afeka.ac.il',self)
        self.my_email.setGeometry(70,60,300,30)

        self.my_linkedin=QLabel('<a href="https://www.linkedin.com/in/IDAN_NAOR">My linkedin</a>', self)
        self.my_linkedin.setGeometry(150,100,300,30)
        self.my_linkedin.setOpenExternalLinks(True)

        self.my_github = QLabel('<a href="https://github.com/idann98/HW__4">My GitHub</a>', self)
        self.my_github.setGeometry(150,130,300,30)
        self.my_github.setOpenExternalLinks(True)

        image=QPixmap('123.jpg')
        self.my_picture=QLabel(self)
        self.my_picture.setGeometry(50, 170, 300, 300)
        self.my_picture.setStyleSheet('border: 4px solid #2c3e50; border-radius: 10px; background-color: white;')
        image=QPixmap('123.jpg').scaled(300,300)
        self.my_picture.setPixmap(image)

if __name__ == '__main__':
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()