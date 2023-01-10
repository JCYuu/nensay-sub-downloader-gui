import shutil
from os import scandir, remove, makedirs
from pathlib import Path
from shutil import copyfile

from PyQt5.QtWidgets import QListWidgetItem
from pyasstosrt import Subtitle
from pyunpack import Archive

class ssaToSrt:
	def __init__(self):
		self.tempPath = ""

	def zip_to_srt(self, path):
		"""Uncompress the zip file obtained from the sub-downloader defined by the path into the corresponding .srt
		subtitles

		Parameters:
			path (str): zip filePath
		Raises:
			FileNotFoundError: if the file does not exist
		"""
		path = path.replace("/", "\\")
		if path != "" and Path(path).exists():
			self.tempPath = path[:path.rindex("\\") + 1] + "tmp"
			# I decompress the downloaded files
			self.uncompress_rec(path)
			# after that it converts all .ass and .ssa files into .srt
			[Subtitle(Path(route)).export(self.tempPath) for route in scandir(self.tempPath) if
			 route.path.endswith(".ass") or route.path.endswith(".ssa")]
			# and finally it deletes all files that are not .srt subtitles
			[remove(route) for route in scandir(self.tempPath) if
			 not route.path.endswith(".srt") and Path(route).is_file()]
		else:
			raise FileNotFoundError("Requested file not found, make sure of the route of the file")

	def list_languages(self):
		"""From the temp folder created with zipToSRT read the file names searching for [language] and return the
		languages as a list, it will return an empty list if the naming convention is not followed

		Returns:
			list: languages list
		Raises:
			FileNotFoundError: if the folder route is incorrect
		"""
		if Path(self.tempPath).exists():
			toGive = []
			for language in scandir(self.tempPath):
				realLang = language.path[language.path.rindex("[") + 1: language.path.rindex("]")]
				if realLang not in toGive:
					toGive.append(realLang)
			return toGive
		else:
			raise FileNotFoundError("Incorrect path (it does not exist)")

	def select_language(self, targetPath, language=[]):
		"""From the temp folder created with zipToSRT, selecting one of the languages from listLanguages (or none if empty)
		and giving a path to copy the files to: copy the selected language subtitles to the destination folder,
		if the folder does not exist it will create it along with all needed parent directories

		Parameters:
			language (str): selected language from listLanguages
			targetPath (str): destination folder to copy the corresponding files to
		"""
		if not Path(targetPath).exists():
			makedirs(targetPath)
		if not language:
			[copyfile(filePath, targetPath + filePath.path[filePath.path.rindex("\\"):]) for filePath in
			 scandir(self.tempPath)]
		else:
			for languages in language:
				[copyfile(filePath, targetPath + filePath.path[filePath.path.rindex("\\"):], follow_symlinks=False) for
				 filePath in
				 scandir(self.tempPath) if filePath.path.__contains__(languages.text())]
		shutil.rmtree(self.tempPath)

	def uncompress_rec(self, filePath):
		Archive(filePath).extractall(self.tempPath, auto_create_dir=True)
		remove(filePath)
		for files in scandir(self.tempPath):
			if files.path.endswith((".rar", ".zip", ".7z")) and Path(files).exists():
				self.uncompress_rec(files.path)
