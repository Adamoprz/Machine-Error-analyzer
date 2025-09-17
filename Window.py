import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox, QLabel, QFileDialog, QAbstractItemView, QListWidget, QListView, QTableWidgetSelectionRange, QStyleOptionViewItem
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import numpy as np

matplotlib.rcParams['figure.figsize'] = [15, 15] # for square canvas
matplotlib.rcParams['figure.subplot.left'] = 0
matplotlib.rcParams['figure.subplot.bottom'] = 0
matplotlib.rcParams['figure.subplot.right'] = 1
matplotlib.rcParams['figure.subplot.top'] = 1


class ChartWindow(QWidget):

    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Calibration Data Tool")
        self.df = df
        self.df_init = df
        layout = QVBoxLayout()
        self.values_important = [20, 220, 420, 620, 820, 1020, 1220, 1420, 1620, 1820, 2020]

        # Chart setup
        self.canvas = FigureCanvas(Figure())
        layout.addWidget(self.canvas)
        self.my_list_view = QListWidget()
        self.my_list_view.setSortingEnabled(True)
        #self.my_list_view.setAcceptDrops(True)

        self.my_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection.MultiSelection)

        self.my_list_view.setFixedSize(800, 120)

        self.model = QStandardItemModel()

        # Create label and combo box
        self.label = QLabel("Choose the operator")
        self.label.setFixedSize(800, 20)
        self.combo = QComboBox()
        self.combo.setFixedSize(800, 20)
        self.combo.addItems(["ALL" + " [" + str(len(self.df_init)) + "]"])
        self.combo.setCurrentIndex(0)
        for el in self.df['Operator'].unique():
            number = len(self.df[self.df['Operator'].str.contains(el, case=False, na=False)])
            el_temp = el + " [" + str(number) +"]"
            self.combo.addItems([el_temp])

        self.label2 = QLabel("Choose the date")
        self.label2.setFixedSize(800, 20)

        for el in sorted(self.df['Date'].unique()):
            el_str = el.strftime('%Y-%m-%d')
            self.my_list_view.addItems([el_str])
            self.model.appendRow(QStandardItem(str(el_str)))
        self.my_list_view.selectAll()

        #Create Button Widgets
        self.button_save = QPushButton("Save the Chart")
        self.button_select = QPushButton("Select ALL Dates")
        self.button_unselect = QPushButton("Unselect Dates")
        self.update_ = QPushButton("Update")


        # Add Button widgets to layout
        layout.addWidget(self.button_save)
        layout.addWidget(self.button_select)
        layout.addWidget(self.button_unselect)
        #layout.addWidget(self.update_)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.label2)
        layout.addWidget(self.my_list_view)

        #Create connection for actions
        self.combo.currentIndexChanged.connect(self.update_label)
        self.combo.currentIndexChanged.connect(self.update_available_dates)
        self.my_list_view.itemSelectionChanged.connect(self.update_all)
        self.update_.clicked.connect(self.update_all)
        self.button_unselect.clicked.connect(self.unselect_dates)
        self.button_select.clicked.connect(self.select_dates)
        self.button_save.clicked.connect(self.save_plots)

        #Create Layouts
        self.setLayout(layout)
        self.plot_chart()
        self.showMaximized()

        #self.tests()
        #print("1_Init")

    def update_label(self):
        self.reduce_df()
        self.update_all()
        #self.tests()
        #print("2_Update label")

    def reduce_df(self):
        self.df = self.df_init
        last_space_index = self.combo.currentText().rfind(" ")
        red_op = self.combo.currentText()[:last_space_index]
        # Slice up to the last space
        if red_op == "ALL":
            self.df = self.df_init
        else:
            self.df = self.df[self.df['Operator'].str.contains(red_op, case=False, na=False)]
        #self.tests()
        #print("3_Reduce_df")

    def update_all(self):
        #print([el.text() for el in self.my_list_view.selectedItems()])
        self.reduce_df()
        self.plot_chart()
        #self.tests()
        #print("4_update_all")

    def update_available_dates(self):
        self.my_list_view.clear()
        for el in sorted(self.df['Date'].unique()):
            el_str = el.strftime('%Y-%m-%d')
            self.my_list_view.addItems([el_str])
            self.model.appendRow(QStandardItem(str(el_str)))


        self.update_label()
        #self.tests()
        #print("5_Update_available_dates")


    def unselect_dates(self):
        self.my_list_view.selectAll()
        self.my_list_view.clearSelection()
        self.update_all()
        #self.plot_chart()
        #self.tests()
        #print("5_Unselect_dates")


    def select_dates(self):
        self.my_list_view.selectAll()
        self.update_all()
        #self.tests()
        #print("6_Select_Dates")


    def save_plots(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz wykres",
            "wykres.png",  # domyślna nazwa
            "PNG Files (*.png);;All Files (*)"
        )

        if file_path:
            self.sciezka = file_path
            self.canvas.figure.savefig(self.sciezka, dpi=600)
        #self.tests()
        #print("7_Save_Plots")

    def tests(self):
        print([el for el in self.my_list_view.selectionModel().selectedRows()])

    def plot_chart(self):
        self.fig = self.canvas.figure
        self.fig.clear()
        ax1 = {}
        #print([el.text() for el in self.my_list_view.selectedItems()])

        for a in range(1, 5, 1):
            ax1[a] = self.fig.add_subplot(2, 2, a,  frameon=True, adjustable='datalim')
            x_values = np.array(self.values_important)
            df_reduced = self.df[self.df['Type'].str.contains(str(a-1), case=False, na=False)]

            df_reduced = df_reduced[df_reduced['Date'].astype('str').isin([el.text() for el in self.my_list_view.selectedItems()])]

            for _, row in df_reduced.iterrows():
                label = row["File_name"]
                #label = row["Date"].strftime('%Y-%m-%d')
                y_values = row[x_values].values
                ax1[a].plot(x_values, y_values, label = label)
                ax1[a].set_title(f'Stp_Diag ( {a - 1} ) ')

            # Line 1
            y1 = 1.7/1000 + x_values/500000.0
            ax1[a].plot(x_values, y1, label='MAX', color="red")

            # Line 2
            y2 = -1.7/1000 - x_values/500000.0
            ax1[a].plot(x_values, y2, label='MIN', color="red")

            # Line 3
            y3 = (1.7/1000 + x_values/500000.0) * 0.8
            ax1[a].plot(x_values, y3, label='MAX_80%', color="orange")

            # Line 4
            y4 = (-1.7/1000 - x_values/500000.0) * 0.8
            ax1[a].plot(x_values, y4, label='MIN_80%', color="orange")

            # Line 5
            y5 = 0.0 * x_values
            ax1[a].plot(x_values, y5, label='Nominal', color="black")

            ax1[a].set_xlabel("x")
            ax1[a].set_ylabel("y")
            ax1[a].grid(True)
            ax1[a].legend().columnspacing = 0.4

            #ax1[a].legend(loc="lower left", ncols=3, markerscale=0.5).get_frame().set_alpha(0.5)
            ax1[a].legend(fontsize=5, handletextpad=1, loc="lower left", markerscale=1, ncols=4)

        self.fig.tight_layout()
        self.canvas.draw()
        #self.tests()
        #print("8_Print_Plots")


