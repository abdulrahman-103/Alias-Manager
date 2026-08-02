#Copyright (C) 2026 Abdulrahman
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QStatusBar, QMessageBox, QWidget, QHBoxLayout
from PySide6.QtGui import QAction, QIcon, QShortcut, QPalette
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