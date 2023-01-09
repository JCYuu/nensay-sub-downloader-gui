import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from frames.MainWindow import Ui_MainWindow
from frames.ui_decompress import Ui_ToSrtDialog
from frames.ui_download import Ui_Download_Dialog


def windowActions():
	window.setupUi(window)
	window.download_btn.clicked.connect(d_dialog.open)
	window.edit_btn.clicked.connect(dialog.open)
	window.exit_btn.clicked.connect(sys.exit)


def dialogActions():
	dialog.setupUi(dialog)
	dialog.browse.clicked.connect(dialog.browse_files)
	dialog.copyFiles.stateChanged.connect(dialog.checker)
	dialog.acceptCancel.accepted.connect(dialog.accepted)
	d_dialog.setupUi(d_dialog)
	d_dialog.exit_btn.clicked.connect(d_dialog.accept)
	d_dialog.search_btn.clicked.connect(d_dialog.search_anime)
	#d_dialog.n_page_anime.clicked.connect(lambda: d_dialog.next_anime_page(d_dialog.n_page_anime))
	d_dialog.loadChaptersBtn.clicked.connect(d_dialog.load_chapters)
	d_dialog.dl_btn.clicked.connect(d_dialog.download_sub)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	dialog = Ui_ToSrtDialog()
	d_dialog = Ui_Download_Dialog()
	windowActions()
	dialogActions()
	widget = QtWidgets.QStackedWidget()
	widget.setFixedSize(490, 315)
	widget.addWidget(window)
	widget.show()
	sys.exit(app.exec_())
