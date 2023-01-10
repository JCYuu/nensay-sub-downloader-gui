from PyQt5.QtCore import QSize, QRect, Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QSizePolicy, QDialogButtonBox, QListWidget, QAbstractItemView, QDialog, QApplication

from modules.download_script import CustomException


class Ui_lang(QDialog):
	def setupUi(self, lang):
		if not lang.objectName():
			lang.setObjectName(u"lang")
		lang.resize(400, 300)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(lang.sizePolicy().hasHeightForWidth())
		lang.setSizePolicy(sizePolicy)
		lang.setMinimumSize(QSize(400, 300))
		lang.setMaximumSize(QSize(400, 300))
		self.accept = QDialogButtonBox(lang)
		self.accept.setObjectName(u"accept")
		self.accept.setGeometry(QRect(240, 260, 151, 32))
		font = QFont()
		font.setFamily(u"OCR A Extended")
		self.accept.setFont(font)
		self.accept.setCursor(QCursor(Qt.PointingHandCursor))
		self.accept.setOrientation(Qt.Horizontal)
		self.accept.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
		self.listLang = QListWidget(lang)
		self.listLang.setObjectName(u"listLang")
		self.listLang.setGeometry(QRect(10, 10, 381, 241))
		self.listLang.setSelectionMode(QAbstractItemView.MultiSelection)
		self.setModal(True)
		self.retranslateUi(lang)

		QMetaObject.connectSlotsByName(lang)

	# setupUi

	def retranslateUi(self, lang):
		lang.setWindowTitle(QCoreApplication.translate("lang", u"select language", None))
	# retranslateUi

	def readList(self, srt):
		for items in srt.list_languages():
			self.listLang.addItem(items)
		self.listLang.update()

	def selectLang(self, srt, path, instance):
			srt.select_language(targetPath=path, language=self.listLang.selectedItems())
			instance.canceled()
			self.close()


	def cancelCopy(self, instance):
		instance.canceled()
		self.close()
