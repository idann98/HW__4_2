import sys
from pathlib import Path
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QFileDialog,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.figure import Figure

from About import AboutWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Graph Viewer")
        self.setGeometry(100, 100, 900, 650)
        self.setMinimumSize(700, 500)

        self.load_button = QPushButton("Select CSV File", self)
        self.load_button.setObjectName("loadButton")
        self.load_button.setGeometry(20, 20, 180, 40)
        self.load_button.clicked.connect(self.load_file)

        self.about_button = QPushButton("About", self)
        self.about_button.setObjectName("aboutButton")
        self.about_button.setGeometry(700, 20, 180, 40)
        self.about_button.clicked.connect(self.open_about)

        self.figure = Figure(figsize=(7.5, 4.5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 110, 860, 430)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setGeometry(20, 70, 860, 36)

        self.about_window = None
        self.csv_path = ""
        self.temps = []
        self.revenues = []

        self.load_style()
        self.plot_graph()

    def load_style(self):
        style_path = Path(__file__).resolve().with_name("style.qss")
        if style_path.exists():
            self.setStyleSheet(style_path.read_text(encoding="utf-8"))

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if file_path != "":
            self.csv_path = file_path
            self.temps = []
            self.revenues = []

            with open(self.csv_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines[1:]:
                line = line.strip()
                if line != "":
                    parts = line.split(",")
                    temp = float(parts[0].strip())
                    rev = float(parts[1].strip())

                    self.temps.append(temp)
                    self.revenues.append(rev)

            self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        axes = self.figure.add_subplot(111)

        if len(self.temps) > 0 and len(self.revenues) > 0:
            axes.scatter(self.temps, self.revenues, s=1)
            axes.set_xlabel("Temperature")
            axes.set_ylabel("Revenue")
            axes.set_title("Ice Cream Revenue vs Temperature")
            axes.spines["top"].set_visible(False)
            axes.spines["right"].set_visible(False)

            m, b = np.polyfit(self.temps, self.revenues, 1)
            x_line = np.linspace(min(self.temps), max(self.temps), 100)
            y_line = m * x_line + b

            axes.plot(x_line, y_line, color="red", linewidth=2)

            sign = "+" if b >= 0 else "-"
            eq_text = f"y = {m:.2f}x {sign} {abs(b):.2f}"
            axes.text(
                0.05,
                0.9,
                eq_text,
                transform=axes.transAxes,
                fontsize=11,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )
        else:
            axes.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16], marker="o")
            axes.set_title("Temporary Plot")
            axes.set_xlabel("X")
            axes.set_ylabel("Y")
            axes.spines["top"].set_visible(False)
            axes.spines["right"].set_visible(False)

        self.figure.tight_layout()
        self.canvas.draw()

    def open_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        margin = 20
        toolbar_height = 36
        toolbar_top = 70
        canvas_top = toolbar_top + toolbar_height + 4
        canvas_width = max(0, self.width() - 2 * margin)
        canvas_height = max(0, self.height() - canvas_top - 20)

        self.load_button.setGeometry(margin, 20, 180, 40)
        self.about_button.setGeometry(
            max(margin, self.width() - margin - 180),
            20,
            180,
            40,
        )
        self.toolbar.setGeometry(margin, toolbar_top, canvas_width, toolbar_height)
        self.canvas.setGeometry(
            margin,
            canvas_top,
            canvas_width,
            canvas_height,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())