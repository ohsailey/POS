from ctypes import windll
import win32api
import string
import os
import shutil

class StorageDevice:
	def __init__(self):
		self.init_drives=self.get_pos_drive()
		self.current_drive = None

	def _is_detectable(self):

		if self.get_pos_drive() != self.init_drives:
			self.current_drive = self.get_pos_drive()[-1]
			return True
		return False

		#self.path = get_drive_location()

        #return drives

	def get_name(self):
		return win32api.GetVolumeInformation("F:\\")[0]

	def get_pos_drive(self):
		drives = []
		bitmask = windll.kernel32.GetLogicalDrives()
		for letter in string.uppercase:
			if bitmask & 1:
				drives.append(letter)
			bitmask >>= 1
		return drives

	def	obtain_data(self, source):
		destination_path = self.current_drive + ":\\"
		for files in os.listdir(source):
			if files:
				file_path = os.path.join(source, files)
    			try:
        			shutil.copy(file_path, destination_path)
    				# eg. src and dest are the same file
    			except shutil.Error as e:
        			print('Error: %s' % e)
 					# eg. source or destination doesn't exist
        		except IOError as e:
        			print('Error: %s' % e.strerror)
