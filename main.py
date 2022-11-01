import sys
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from fpdf import FPDF
from calculate import main_alg as calculate
from math import ceil, floor


class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('help.ui', self)
        self.setFixedSize(651, 631)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))


class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        uic.loadUi('UI.ui', self)
        self.button.clicked.connect(self.get_res)
        self.toPDF.clicked.connect(self.create_PDF)
        self.clear.clicked.connect(self.delete)
        self.help.clicked.connect(self.popup)
        self.txt.clicked.connect(self.get_data_from_txt)
        self.setFixedSize(816, 929)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setWindowTitle('Оптимальная раскройка')
        self.font = QFont("Consolas", 10, QFont.Bold)
        self.output.setFont(self.font)

    def get_data_from_txt(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Text Files(*.txt);")
        if filename:
            with open(filename) as f:
                data, cnt = f.readlines(), 1
                for i in data:
                    tmp = i.split()
                    if not tmp:
                        cnt = 11
                        continue
                    exec(f"self.line{cnt}.setText(tmp[0])\n"
                         f"self.n{cnt}.setValue(int(tmp[1]))")
                    cnt += 1

    def popup(self):
        self.w = MyPopup()
        self.w.show()


    def get_res(self):
        self.output.clear()
        self.collect_data()
        for i in self.data:
            res = calculate(len(self.pieces), i, self.pieces, int('0' + self.cutter_len.text()))
            self.draw(res, i)
            for j in res[1:]:
                self.pieces.remove(j)

    def draw(self, data, size):
        if data:
            tmp1, tmp2 = '', ''
            for i in data[1::]:
                s = floor((87 - len(str(data[0])) - 3) * (i / size))
                tmp1 += ' ' * floor((s + 1 - len(str(i))) / 2) + str(i) + ' ' * ceil((s + 1 - len(str(i))) / 2)
                tmp2 += '_' * s + '|'
            tmp1 += str(data[0]) + '*'
            tmp2 += '_' * (87 - len(tmp2))
            self.output.append(tmp1)
            self.output.append(tmp2)
            self.output.append('<' + '-' * 85 + '>')
            self.output.append(' ' * floor((87 - len(str(size))) / 2) + str(size) + ' ' * ceil((87 - len(str(size))) / 2))
            self.output.append("\n")
        else:
            self.output.append("_" * 87)
            self.output.append("<" + '-' * 85 + '>')
            self.output.append(' ' * floor((87 - len(str(size))) / 2) + str(size) + ' ' * ceil((87 - len(str(size))) / 2))

    def collect_data(self):
        self.data = []
        for i in range(1, 11):
            exec(f"self.data.extend([int('0' + self.line{i}.text())] * int('0' + self.n{i}.text()))")

        self.pieces = []
        for i in range(11, 21):
            exec(f"self.pieces.extend([int('0' + self.line{i}.text())] * int('0' + self.n{i}.text()))")

    def create_PDF(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку для сохранения чертежа в PDF", ".")
        if dirlist:
            pdf = FPDF()
            pdf.add_font("Consolas", style='B', fname='consolas.ttf', uni=True)
            pdf.set_font("Consolas", size=10, style='B')
            pdf.add_page()
            for i in self.output.toPlainText().split('\n'):
                pdf.cell(0, 10, i, align='L', ln=1)
            pdf.output(dirlist + '/' + self.file_name.text())

    def delete(self):
        for i in range(1, 21):
            exec(f"self.line{i}.setText('')")
            exec(f"self.n{i}.setValue(0)")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
