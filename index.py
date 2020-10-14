from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType
import sys, os
import sqlite3


def resource_path(relative_path):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


form_class,_ = loadUiType(resource_path("data/main.ui"))


x = 0
idx = 0


class Main(QMainWindow, form_class):
	def __init__(self, parent=None):
		super(Main, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.Handel_Buttons()
		self.Open_Details()
		self.QDark_Theme()


	def Handel_Buttons(self):
		self.btn_refresh.clicked.connect(self.Get_data)
		self.btn_search.clicked.connect(self.search)
		self.btn_check.clicked.connect(self.level)
		self.btn_update.clicked.connect(self.update)
		self.btn_delete.clicked.connect(self.delete)
		self.btn_add.clicked.connect(self.add)
		self.btn_next.clicked.connect(self.next)
		self.btn_previous.clicked.connect(self.previous)
		self.btn_last.clicked.connect(self.last)
		self.btn_first.clicked.connect(self.first)
		self.btn_details.clicked.connect(self.Open_Details)
		self.btn_statistics.clicked.connect(self.Open_Statistics)
		self.btn_edit.clicked.connect(self.Open_Edit)
		self.btn_settings.clicked.connect(self.Open_Settings)
		self.btn_apply.clicked.connect(self.Change_Theme)


	def Change_Theme(self):
		combotext = str(self.cmb_box_themes.currentText())
		if not "-- Themes --" == combotext:
			if "dark orange".lower() in combotext.lower():
				self.Dark_Orange_Theme()
			elif "dark blue".lower() in combotext.lower():
				self.Dark_Blue_Theme()
			elif "q dark".lower() in combotext.lower():
				self.QDark_Theme()
			elif "dark gray".lower() in combotext.lower():
				self.Dark_Gray_Theme()
			else:
				pass
		else:
			print("themess")


	def Open_Details(self):
		self.tabWidget.setCurrentIndex(0)

	def Open_Statistics(self):
		self.tabWidget.setCurrentIndex(1)

	def Open_Edit(self):
		self.tabWidget.setCurrentIndex(2)

	def Open_Settings(self):
		self.tabWidget.setCurrentIndex(3)




	def Get_data(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()
		command = """ SELECT * from parts_table """
		result = cursor.execute(command)
		
		self.table.setRowCount(0)

		for row_number, row_data in enumerate(result):
			self.table.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		cursor2 = db.cursor()
		cursor3 = db.cursor()

		parts_number = """ select count (distinct PartName) from parts_table """
		reference_number = """ select count (distinct Reference) from parts_table """

		result_parts_number = cursor3.execute(parts_number)
		result_reference_number = cursor2.execute(reference_number)

		self.lbl_ref_nbr.setText(str(result_reference_number.fetchone()[0]))
		self.lbl_parts_nbr.setText(str(result_parts_number.fetchone()[0]))

		cursor4 = db.cursor()
		cursor5 = db.cursor()

		min_hole = """ select MIN(NumberOfHoles), Reference from parts_table """
		max_hole = """ select MAX(NumberOfHoles), Reference from parts_table """


		result_min_hole = cursor4.execute(min_hole)
		result_max_hole = cursor5.execute(max_hole)

		r1 = result_min_hole.fetchone()
		r2 = result_max_hole.fetchone()


		self.lbl_min_hole.setText(str(r1[0]))
		self.lbl_max_hole.setText(str(r2[0]))

		self.lbl_min_hole_2.setText(str(r1[1]))
		self.lbl_max_hole_2.setText(str(r2[1]))

		self.first()
		self.navigate()


	def search(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()
		nbr = int(self.count_filter.text())
		
		command = """ select * from parts_table where count <= ? """

		result = cursor.execute(command, [nbr])
		self.table.setRowCount(0)

		for row_number, row_data in enumerate(result):
			self.table.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))



	def level(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()
		command = """ select Reference, PartName, Count from parts_table order by Count asc LIMIT 5 """

		result = cursor.execute(command)
		
		self.table2.setRowCount(0)

		for row_number, row_data in enumerate(result):
			self.table2.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))


	def navigate(self):
		global idx
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		command = """ select * from parts_table where ID=? """

		result = cursor.execute(command, [idx])
		val = result.fetchone()

		self.id.setText(str(val[0]))
		self.reference.setText(str(val[1]))
		self.part_name.setText(str(val[2]))
		self.min_area.setText(str(val[3]))
		self.max_area.setText(str(val[4]))
		self.number_of_holes.setText(str(val[5]))
		self.min_diameter.setText(str(val[6]))
		self.max_diameter.setText(str(val[7]))
		self.count.setValue(val[8])


	def next(self):
		db = sqlite3.connect(resource_path('data/parts.db'))
		cursor = db.cursor()

		command = """ select id from parts_table """
		result = cursor.execute(command)
		val = result.fetchall()
		tot = len(val)
		global x
		global idx
		x += 1
		
		if x < tot:
			idx = val[x][0]
			self.navigate()
		else:
			x = tot - 1
			print("End of file!!")

	def previous(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		command = """ select id from parts_table """
		result = cursor.execute(command)
		val = result.fetchall()
		tot = len(val)
		global x
		global idx
		x -= 1
		if x >- 1:
			idx = val[x][0]
			self.navigate()
		else:
			x = 0
			print("Begin of file")


	def last(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		command = """ select id from parts_table """
		result = cursor.execute(command)
		val = result.fetchall()
		tot = len(val)
		global x
		global idx
		x = tot - 1
		if x < tot:
			idx = val[x][0]
			self.navigate()
		else:
			x = tot - 1
			print("End of file")


	def first(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		command = """ select ID from parts_table """
		result = cursor.execute(command)
		val = result.fetchall()

		global x
		global idx

		x = 0
		if x >-1:
			idx = val[x][0]
			self.navigate()
		else:
			x = 0
			print("Begin of file....")

	def update(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		id_ = int(self.id.text())
		reference_ = self.reference.text()
		part_name_ = self.part_name.text()
		min_area_ = self.min_area.text()
		max_area_ = self.max_area.text()
		number_of_holes_ = self.number_of_holes.text()
		min_diameter_ = self.min_diameter.text()
		max_diameter_ = self.max_diameter.text()
		count_ = str(self.count.value())

		row = (reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_, id_)

		command = """ UPDATE parts_table set reference=?, PartName=?, MinArea=?, MaxArea=?, NumberOfHoles=?, MinDiameter=?, MaxDiameter=?, Count=? where ID=? """
		cursor.execute(command, row)
		db.commit()

	def delete(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		id_ = self.id.text()
		
		command = """ DELETE FROM parts_table where ID=? """
		cursor.execute(command, (id_,))
		db.commit()

	def add(self):
		db = sqlite3.connect(resource_path("data/parts.db"))
		cursor = db.cursor()

		reference_ = self.reference.text()
		part_name_ = self.part_name.text()
		min_area_ = self.min_area.text()
		max_area_ = self.max_area.text()
		number_of_holes_ = self.number_of_holes.text()
		min_diameter_ = self.min_diameter.text()
		max_diameter_ = self.max_diameter.text()
		count_ = str(self.count.value())

		row = (reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_)

		command = """ INSERT INTO parts_table (Reference, PartName, MinArea, MaxArea, NumberOfHoles, MinDiameter, MaxDiameter, Count) VALUES (?,?,?,?,?,?,?,?) """

		cursor.execute(command, row)
		db.commit()


	def Dark_Blue_Theme(self):
		style = open('data/themes/darkblue.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Gray_Theme(self):
		style = open('data/themes/darkgray.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Orange_Theme(self):
		style = open('data/themes/darkorange.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def QDark_Theme(self):
		style = open('data/themes/qdark.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)





def main():
	app = QApplication(sys.argv)
	window = Main()
	window.show()
	app.exec_()


if __name__ == "__main__":
	main()
