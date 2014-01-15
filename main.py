#!/usr/bin/python3

import sys
from PyQt4 import QtGui,QtCore
import re
from html.parser import HTMLParser
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Rsvp(QtGui.QWidget):
    
    def __init__(self):
        super(Rsvp, self).__init__()
        self.news=[]
        self.article=[]
        self.allNews()
        self.initUI()
        self.prev=0
        self.play=0
        self.buf=[0,""]
        self.time=2000
        self.word=3          

    def initUI(self):           
        self.lbl = QtGui.QLabel(self)
        self.lbl.move(50, 40)
        self.lbl.setText('Press Space to start!')
        self.lbl.setStyleSheet('background-color:  #f9f4ef; color:  #140e0a; font-size: 18pt;')
        self.lbl.adjustSize()       

        self.lbl2 = QtGui.QLabel(self)
        self.lbl2.move(50, 120)
        self.lbl2.setText('Replay speed : '+ str(60000*3/2000)+' w/s')
        self.lbl2.setStyleSheet('background-color:  #f9f4ef; color:  #140e0a; font-size: 16pt;')
        self.lbl2.adjustSize()

        self.lbl3 = QtGui.QLabel(self)
        self.lbl3.move(50, 160)
        self.lbl3.setText('Quantity of words : '+ str(3))
        self.lbl3.setStyleSheet('background-color:  #f9f4ef; color:  #140e0a; font-size: 16pt;')
        self.lbl3.adjustSize()

        self.but1 = QtGui.QPushButton('-', self)
        self.but1.move(310, 160)
        self.but1.clicked[bool].connect(self.setWordsL)
        self.but1.setStyleSheet('background-color: #f4e9e0')
        self.but1.setFocusPolicy(QtCore.Qt.NoFocus)

        self.but2 = QtGui.QPushButton('+', self)
        self.but2.move(400, 160)
        self.but2.clicked[bool].connect(self.setWordsB)
        self.but2.setStyleSheet('background-color: #f4e9e0')
        self.but2.setFocusPolicy(QtCore.Qt.NoFocus)

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(50, 220, 400, 30)

        self.setGeometry(300, 300, 750, 300)
        self.setWindowTitle('RSVP')
        self.setStyleSheet("QWidget {background-color: #dfbda2 }")
        
        self.show()
        self.setAutoFillBackground(True)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.setText()

        elif key == QtCore.Qt.Key_Left:
            self.setFrameP()
            
        elif key == QtCore.Qt.Key_Right:
            self.setFrameN()
            
        elif key == QtCore.Qt.Key_Down:
            self.setSpeedM()
            
        elif key == QtCore.Qt.Key_Up:
            self.setSpeedF()
        else:
            event.ignore()

    def allNews(self):
        url='http://w-o-s.ru/news/'    
        data = urlopen(url).read().decode('utf8')
        html_doc = urlopen(url).read().decode('utf8') 
        soup = BeautifulSoup(html_doc)
        mt=soup.findAll('div', 'list')
        r = re.compile(r'(/news/\d+)')
        news= re.findall(r, str(mt[-1]))
        for i in news:
            i='http://w-o-s.ru'+i
            if i not in self.news:
                self.news.append(i)  
   
    def readArticle(self,n):
        url=self.news[n]    
        html_doc = urlopen(url).read().decode('utf8') 
        soup = BeautifulSoup(html_doc)
        content=soup.findAll('div', 'content')
        tag = re.compile( '(<.*?>)')
        text=""
        for i in content:
            buf= tag.sub(' ', str(i.find('p')))
            if buf!="None":
                text+=buf
        return (text)

    def setWordsL(self):
        if (self.play==0):
            if(self.word>3): 
                self.word-=1
                self.lbl3.setText('Quantity of words : '+ str(self.word))
                self.lbl3.adjustSize()
        
    def setWordsB(self):
        if (self.play==0):
            if(self.word<5): 
                self.word+=1
                self.lbl3.setText('Quantity of words : '+ str(self.word))
                self.lbl3.adjustSize()

    def setSpeedM(self):
        self.time+=200
        self.lbl2.setText('Replay speed : '+str(int(60000*self.word/self.time))+' w/m')
        self.lbl2.adjustSize()

    def setSpeedF(self):
        if(self.time>200):
            self.time-=200
            self.lbl2.setText('Replay speed : '+str(int(60000*self.word/self.time))+' w/m')
            self.lbl2.adjustSize()

    def setFrameP(self):
        if (self.play==1):
            self.prev=2

    def setFrameN(self):
        if (self.play==1):
            self.prev=-1

    def goRsvp(self,j,data):
        if (self.play==1):
            if(j<len(self.article)):
                self.step = int(100*(j+1)/len(self.article))
                self.pbar.setValue(self.step)
                if(self.prev==0):  
                    self.lbl.setText(self.article[j])
                    self.lbl.adjustSize()
                    j+=1
                    self.buf[0]=j
                    if(j==len(self.article)):
                        self.buf[1]=self.article[j-1]   
                    else:
                        self.buf[1]=self.article[j]   
                    QtCore.QTimer.singleShot(self.time, lambda: self.goRsvp(j,self.buf[1]))
                elif(self.prev>0):
                    self.lbl.setText(data)
                    self.lbl.adjustSize()
                    self.buf[0]=j-1
                    self.buf[1]=self.article[j]  
                    QtCore.QTimer.singleShot(self.time, lambda: self.goRsvp(j-1,self.article[j]))
                    self.prev-=1
                elif(self.prev<0):
                    self.buf[0]=j+1
                    self.buf[1]=self.article[j]  
                    QtCore.QTimer.singleShot(self.time, lambda: self.goRsvp(j+1,self.article[j]))
                    self.prev+=1

    def setText123(self):
        if(self.play==0):
            self.play=1
            self.but1.setEnabled(False)
            self.but2.setEnabled(False)
            for i in range(len(self.news)):
                text=self.readArticle(i)
                array=text.split()
                t="" 
                for j in array:
                    t+=j+" "
                    if(len(t)>20): 
                        self.article.append(t)
                        t=""
                self.article.append(t)
            self.goRsvp(0,"")
        elif(self.play==2): 
            self.play=1
            self.goRsvp(self.buf[0],self.buf[1])
        else:
             self.play=2

    def setText(self):
        if(self.play==0):
            self.play=1
            self.but1.setEnabled(False)
            self.but2.setEnabled(False)
            for i in range(len(self.news)):
                text=self.readArticle(i)
                array=text.split()
                t="" 
                k=1
                for j in range(len(array)):
                    t+=array[j]+" "
                    if(len(array[j])>3):
                        k+=1
                    if (k % ( self.word+1))==0: 
                        self.article.append(t)
                        t=""
                        k=1
                self.article.append(t)
            self.goRsvp(0,"")
        elif(self.play==2): 
            self.play=1
            self.goRsvp(self.buf[0],self.buf[1])
        else:
             self.play=2
   
app = QtGui.QApplication(sys.argv)
ex = Rsvp()
sys.exit(app.exec_())
