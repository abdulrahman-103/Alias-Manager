#Copyright (C) 2026 Abdulrahman
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPalette
from PySide6.QtCore import QTimer, Qt
import sys
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance()
        resolution = self.app.primaryScreen().availableSize()
        self.resize(resolution.width()/1.5, resolution.height()/1.5)
        self.setWindowTitle("Alias Manager")
        self.file_path = None
        self.file_name = None
        self.format_filter = None
        self.last_directory = None
        #con_path = str(Path(__file__).resolve().parent / "images" / "icon.png")
        #self.setWindowIcon(QIcon(icon_path))
        self.showMaximized()
        home = Path.home()
        self.bashrc = home / ".bashrc"

    def read_bashrc(self):
        if not self.bashrc.exists():
            QMessageBox.critical(self, "Error", "~/.bashrc not found")
            return False

        list = QListWidget()
        with open(self.bashrc, "r") as file:
            row = -1
            for index, line in enumerate(file):
                if line.startswith("alias"):
                    row += 1
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    
                    line_edit = QLineEdit(line[5:].strip("\n"))
                    line_edit.setReadOnly(True)

                    layout.addWidget(line_edit)
                    layout.addStretch()
                    edit = QPushButton("Edit")
                    delete = QPushButton("Delete")
                    layout.addWidget(edit)
                    layout.addWidget(delete)
                    item_widget = QListWidgetItem(list)
                    item_widget.setSizeHint(widget.sizeHint() * 0.75)
                    list.setItemWidget(item_widget, widget)
                    edit.clicked.connect(lambda checked=False, le=line_edit, l=layout, i=index: self.edit_mode(le, l, i))
                    delete.clicked.connect(lambda checked=False, l=list, r=row, i=index: self.delete(l, r, i))
        new = QPushButton("New")
        central_widget = QWidget()
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.addWidget(new)
        central_widget_layout.addWidget(list)
        new.clicked.connect(lambda checked=False, l=list, r=row, i=index: self.new(l))
        self.setCentralWidget(central_widget)
        return True

    def edit_mode(self, line_edit, layout, index):
        if not line_edit.isReadOnly():
            return
        line_edit.setReadOnly(False)
        line_edit.setFocus()
        accept = QPushButton("Accept")
        layout.addWidget(accept)
        accept.clicked.connect(lambda checked=False, a=accept, le=line_edit, i=index: self.accept(a, le, i))

    def accept(self, button, line_edit, index):
        button.deleteLater()
        line_edit.setReadOnly(True)
        with open(self.bashrc, "r") as file:
            lines = file.readlines()
        lines[index] = "alias " + line_edit.text() + "\n"
        with open(self.bashrc, "w") as file:
            file.writelines(lines)
    
    def delete(self, list, row, index):
        list.takeItem(row)
        with open(self.bashrc, "r") as file:
            lines = file.readlines()
        lines[index]  = ""
        with open(self.bashrc, "w") as file:
            file.writelines(lines)
        self.read_bashrc()

    def new(self, list):
        with open(self.bashrc, "a+") as f:
            file = f.read()
            if not file.endswith("\n"):
                f.write("\n")
            f.write("alias ")

        self.read_bashrc()




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    if not window.read_bashrc():
        sys.exit(0)
    app.exec()

if __name__ == "__main__":
    main()