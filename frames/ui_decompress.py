import os
from pathlib import Path

from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QDialogButtonBox, QSizePolicy, QDialog, QCheckBox, \
	QFileDialog, QMessageBox
from pyunpack import PatoolError

from frames.ui_lang import Ui_lang
from modules.download_script import CustomException
from modules.ssaToSrt import ssaToSrt


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
		self.copyFiles.setEnabled(False)
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
		fileName = QFileDialog.getOpenFileName(self, "Open File", str(Path.home()/"Downloads"), "Zip files (*.zip)")
		self.subtitlePath.setText(fileName[0])
		self.copyFiles.setEnabled(True)

	def save_files(self):
		fileName = QFileDialog.getExistingDirectory(self, "Select Folder", str(Path.home() / "Downloads"))
		self.copyPath.setText(fileName)

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
		box = QMessageBox()
		box.setIcon(QMessageBox.Critical)
		box.setStandardButtons(QMessageBox.Ok)
		box.setWindowTitle("Error")
		srt = ssaToSrt()
		try:
			if not self.copyPath.isEnabled():
				srt.zip_to_srt(self.subtitlePath.text())
				self.canceled()
			else:
				lang = Ui_lang()
				lang.setupUi(lang)
				lang.show()
				if self.subtitlePath.text() and self.copyPath.text():
					if Path(self.copyPath.text()).exists() and Path(self.copyPath.text()).is_file():
						raise CustomException("That's a file, not a directory")
					elif not Path(self.copyPath.text()).exists():
						os.makedirs(self.copyPath.text())
					srt.zip_to_srt(self.subtitlePath.text())
					lang.accept.accepted.connect(lambda: lang.selectLang(srt, self.copyPath.text(), self))
					lang.accept.rejected.connect(lambda: lang.cancelCopy(self))
					lang.readList(srt)
				else:
					raise CustomException("No target directory selected")
		except FileNotFoundError:
			box.setText("That file does not exist")
			box.exec_()
		except PatoolError:
			box.setText("That file is corrupted")
			box.exec_()
		except CustomException as e:
			box.setText(e.message)
			box.exec_()
		except OSError:
			box.setText("Could not create folder (check path)")
			box.exec_()

	def canceled(self):
		self.subtitlePath.setText("")
		self.copyPath.setText("")
