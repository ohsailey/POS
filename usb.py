import win32api
import string
from ctypes import windll

class StorageDevice:
	def __init__(self):
		print 'what the'
		self.init_drives=self.get_pos_drive()
		print self.init_drives
	def _is_detectable(self):

		current_drive = self.get_pos_drive()
		print current_drive

		if current_drive != self.init_drives:
			return True
		return False

		#self.path = get_drive_location()

        #return drives

	def get_name(self):
		print win32api.GetVolumeInformation("F:\\")[0]
		return win32api.GetVolumeInformation("F:\\")[0]

	def get_pos_drive(self):
		drives = []
		bitmask = windll.kernel32.GetLogicalDrives()
		for letter in string.uppercase:
			if bitmask & 1:
				drives.append(letter)
			bitmask >>= 1
		return drives
#print fileSystemNameBuffer.value
