import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from frames.MainWindow import Ui_MainWindow
from frames.ui_decompress import Ui_ToSrtDialog
from frames.ui_download import Ui_Download_Dialog


def windowActions():
	window.setupUi(window)
	window.download_btn.clicked.connect(d_dialog.open)
	window.edit_btn.clicked.connect(s_dialog.open)
	window.exit_btn.clicked.connect(sys.exit)


def dialogActions():
	d_dialog.setupUi(d_dialog)
	d_dialog.exit_btn.clicked.connect(d_dialog.accept)
	d_dialog.search_btn.clicked.connect(d_dialog.search_anime)
	d_dialog.n_page_anime.clicked.connect(lambda: d_dialog.change_page('anime', 'next'))
	d_dialog.p_page_anime.clicked.connect(lambda: d_dialog.change_page('anime', 'previous'))
	d_dialog.n_page_chapter.clicked.connect(lambda: d_dialog.change_page('chapters', 'next'))
	d_dialog.p_page_chapter.clicked.connect(lambda: d_dialog.change_page('chapters', 'previous'))
	d_dialog.loadChaptersBtn.clicked.connect(d_dialog.load_chapters)
	d_dialog.dl_btn.clicked.connect(d_dialog.download_sub)
	s_dialog.setupUi(s_dialog)
	s_dialog.browse.clicked.connect(s_dialog.browse_files)
	s_dialog.copyFiles.stateChanged.connect(s_dialog.checker)
	s_dialog.acceptCancel.accepted.connect(s_dialog.accepted)
	s_dialog.browseCopy.clicked.connect(s_dialog.save_files)
	s_dialog.acceptCancel.rejected.connect(s_dialog.canceled)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	s_dialog = Ui_ToSrtDialog()
	d_dialog = Ui_Download_Dialog()
	windowActions()
	dialogActions()
	widget = QtWidgets.QStackedWidget()
	widget.setFixedSize(490, 315)
	widget.addWidget(window)
	widget.show()
	sys.exit(app.exec_())
