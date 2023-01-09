from zipfile import BadZipFile

from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QDialogButtonBox, QSizePolicy, QDialog, QCheckBox, \
	QFileDialog, QMessageBox

from modules import ssaToSrt


class Ui_ToSrtDialog(QDialog):
	def setupUi(self, ToSrtDialog):
		if not ToSrtDialog.objectName():
			ToSrtDialog.setObjectName(u"ToSrtDialog")
		ToSrtDialog.setWindowModality(Qt.NonModal)
		ToSrtDialog.resize(480, 280)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ToSrtDialog.sizePolicy().hasHeightForWidth())
		ToSrtDialog.setSizePolicy(sizePolicy)
		ToSrtDialog.setMinimumSize(QSize(480, 280))
		ToSrtDialog.setMaximumSize(QSize(480, 280))
		ToSrtDialog.setModal(False)
		self.acceptCancel = QDialogButtonBox(ToSrtDialog)
		self.acceptCancel.setObjectName(u"acceptCancel")
		self.acceptCancel.setGeometry(QRect(300, 230, 161, 32))
		font = QFont()
		font.setFamily(u"OCR A Extended")
		font.setPointSize(11)
		self.acceptCancel.setFont(font)
		self.acceptCancel.setCursor(QCursor(Qt.PointingHandCursor))
		self.acceptCancel.setOrientation(Qt.Horizontal)
		self.acceptCancel.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
		self.subtitlePath = QLineEdit(ToSrtDialog)
		self.subtitlePath.setObjectName(u"subtitlePath")
		self.subtitlePath.setGeometry(QRect(20, 60, 351, 21))
		self.subtitleFile = QLabel(ToSrtDialog)
		self.subtitleFile.setObjectName(u"subtitleFile")
		self.subtitleFile.setGeometry(QRect(20, 40, 201, 16))
		self.subtitleFile.setFont(font)
		self.browse = QPushButton(ToSrtDialog)
		self.browse.setObjectName(u"browse")
		self.browse.setGeometry(QRect(380, 60, 75, 23))
		self.browse.setFont(font)
		self.copyFiles = QCheckBox(ToSrtDialog)
		self.copyFiles.setObjectName(u"copyFiles")
		self.copyFiles.setGeometry(QRect(20, 120, 221, 17))
		font1 = QFont()
		font1.setFamily(u"OCR A Extended")
		font1.setPointSize(9)
		self.copyFiles.setFont(font1)
		self.copyPath = QLineEdit(ToSrtDialog)
		self.copyPath.setObjectName(u"copyPath")
		self.copyPath.setEnabled(False)
		self.copyPath.setGeometry(QRect(20, 170, 351, 20))
		self.copyRoute = QLabel(ToSrtDialog)
		self.copyRoute.setObjectName(u"copyRoute")
		self.copyRoute.setEnabled(False)
		self.copyRoute.setGeometry(QRect(20, 150, 47, 13))
		self.copyRoute.setFont(font)
		self.browseCopy = QPushButton(ToSrtDialog)
		self.browseCopy.setObjectName(u"browseCopy")
		self.browseCopy.setEnabled(False)
		self.browseCopy.setGeometry(QRect(380, 170, 75, 23))
		self.browseCopy.setFont(font)

		self.retranslateUi(ToSrtDialog)
		self.acceptCancel.accepted.connect(ToSrtDialog.accept)
		self.acceptCancel.rejected.connect(ToSrtDialog.reject)

		QMetaObject.connectSlotsByName(ToSrtDialog)

	# setupUi

	def retranslateUi(self, ToSrtDialog):
		ToSrtDialog.setWindowTitle(
			QCoreApplication.translate("ToSrtDialog", u"Seleccionar subtitulos a descomprimir", None))
		self.subtitleFile.setText(QCoreApplication.translate("ToSrtDialog", u"Archivo de subtitulos", None))
		self.browse.setText(QCoreApplication.translate("ToSrtDialog", u"Browse", None))
		self.copyFiles.setText(QCoreApplication.translate("ToSrtDialog", u"Copiar al descomprimir", None))
		self.copyRoute.setText(QCoreApplication.translate("ToSrtDialog", u"Ruta", None))
		self.browseCopy.setText(QCoreApplication.translate("ToSrtDialog", u"Browse", None))

	# retranslateUi

	def browse_files(self):
		fileName = QFileDialog.getOpenFileName(self, "Open File", "downloads", "Zip files (*.zip)")
		self.subtitlePath.setText(fileName[0])

	def checker(self):
		if self.copyFiles.isChecked():
			self.copyPath.setEnabled(True)
			self.copyRoute.setEnabled(True)
			self.browseCopy.setEnabled(True)
		else:
			self.copyPath.setEnabled(False)
			self.copyRoute.setEnabled(False)
			self.browseCopy.setEnabled(False)

	def accepted(self):
		if not self.copyPath.isEnabled():
			box = QMessageBox()
			box.setIcon(QMessageBox.Critical)
			box.setStandardButtons(QMessageBox.Ok)
			box.setWindowTitle("Error")
			try:
				ssaToSrt.zip_to_srt(self.subtitlePath.text())
			except FileNotFoundError:
				box.setText("That file does not exist")
				box.exec_()
			except BadZipFile:
				box.setText("That file is corrupted")
				box.exec_()
		else:
			pass
