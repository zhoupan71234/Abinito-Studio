import sys
from PyQt5.QtWidgets import QApplication, QDialog
import numpy as np
import UI_lattice


class My_window(QDialog):
    def __init__(self):
        super(My_window, self).__init__()
        self.ui = UI_lattice.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_row)  # Add button is clicked
        self.ui.pushButton_4.clicked.connect(self.romove_row)  # Remove button is clicked
        self.ui.pushButton_3.clicked.connect(self.clear_contents)  # Clear button is clicked
        self.ui.pushButton_2.clicked.connect(self.get_parameters)  # Enter button is clicked

    # Insert to the last row
    def add_row(self):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())

    # Remove selected row
    def romove_row(self):
        self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())

    # Clear all data, not including header
    def clear_contents(self):
        self.ui.tableWidget.clearContents()

    # Get all parameters on the panel
    def get_parameters(self):
        # Space group
        self.space_group = self.ui.lineEdit.text()
        # Lattice input mode
        if self.ui.radioButton.isChecked() == True:
            self.lattice_model = 'lattice_coordinate'
        else:
            self.lattice_model = 'lattice_matrix'
        # Lattice length and angle
        self.length_a = self.ui.lineEdit_2.text()
        self.length_b = self.ui.lineEdit_3.text()
        self.length_c = self.ui.lineEdit_4.text()
        self.angle_alpha = self.ui.lineEdit_8.text()
        self.angle_beta = self.ui.lineEdit_9.text()
        self.angle_gamma = self.ui.lineEdit_10.text()
        # Lattice matrix
        self.lattice_matrix = np.array([[int(self.ui.lineEdit_11.text()),
                                         int(self.ui.lineEdit_12.text()),
                                         int(self.ui.lineEdit_13.text())],
                                        [int(self.ui.lineEdit_14.text()),
                                         int(self.ui.lineEdit_15.text()),
                                         int(self.ui.lineEdit_16.text())],
                                        [int(self.ui.lineEdit_17.text()),
                                         int(self.ui.lineEdit_18.text()),
                                         int(self.ui.lineEdit_19.text())]])
        # Coordinate input mode
        if self.ui.radioButton_4.isChecked() == True:
            self.coordinate_model = 'Fractional'
        else:
            self.coordinate_model = 'Cartesian'
        # Read tableWidget data
        num_row = self.ui.tableWidget.rowCount()
        num_col = self.ui.tableWidget.columnCount()
        self.table_item = []
        try:
            for i in range(num_row):
                row_text = f"{i + 1} row："
                row_list = []
                for j in range(num_col):
                    row_item = self.ui.tableWidget.item(i, j)
                    row_text = row_text + row_item.text()
                    row_list.append(row_item.text())
                self.table_item.append(row_list)
        except:
            print('Input information is available')
            self.table_item = []
        # Printing parameters
        self.show_parameters()

    def show_parameters(self):
        print(f'空间群：{self.space_group}')
        print(f'晶格输入模式选择：{self.lattice_model}')
        print(f'长度{self.length_a}、{self.length_b}、{self.length_c}，'
              f'角度{self.angle_alpha}、{self.angle_beta}、{self.angle_gamma}')
        print(f'矩阵：\n{self.lattice_matrix}')
        print(f'坐标输入模式选择：{self.coordinate_model}')
        print(f'表格信息{self.table_item}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = My_window()
    my_app.show()
    sys.exit(app.exec_())
