import guizero as gz
from tkinter.filedialog import askopenfilename
import shutil
import os
import datetime as dt
import zipfiler



try:
	os.mkdir("tobedeleted")
except:pass
today = dt.datetime.today()
tictoc = dt.timedelta(hours=48)

try:
	file = open("data.txt", "r")
	data = file.readlines()
	file.close()
except:
	file = open("data.txt", "x")
	data = file.readlines()
	file.close()


def filebutton():
	filebox.value = askopenfilename() # show an "Open" dialog box and return the path to the selected file

def movefolder():
	try:
		filename = os.path.basename(filebox.value)
		fileadressold = filebox.value
		fileadressnew = "tobedeleted/"+filename
		shutil.move(fileadressold, fileadressnew)
		report.append("⮚ File ("+ filename +") moved to tobedeleted.")
		data.append(filename+"&&&"+fileadressold+"&&&"+fileadressnew+"&&&"+str(dt.datetime.today().isoformat())+"\n")
		file = open("data.txt", "w")
		for i in data:
			file.write(i)
		file.close
	except:
		report.append("⮚ ERROR IN FILE DELETE, TRY AGAIN")

def deleteold():
	try:
		deletedfiles = []
		for i in data:
			filename, fileadressold, fileadressnew, deletedate = i.split("&&&")
			deletedate = dt.datetime.fromisoformat(deletedate.replace("\n", ""))
			if (today-deletedate > tictoc):
				os.remove(fileadressnew)
				report.append("⮚ Permanently removed "+str(filename))
				deletedfiles.append(i)
		for i in deletedfiles:
			data.remove(i)
		file = open("data.txt", "w")
		for i in data:
			file.write(i)
		file.close
		if deletedfiles ==[]:
			report.append('⮚ No old file deleted')
		else:
			report.append('⮚ All old files deleted')

	except:
		report.append("⮚ ERROR IN DELETING FILES")


app = gz.App(title="PizzaDeleter")
app.tk.iconbitmap('pizzicon.ico')

deletebar = gz.Box(app, width="fill", height=25)
filebutton = gz.PushButton(deletebar, text="File", align="left", height="fill", command=filebutton)
filebox = gz.TextBox(deletebar, align="left", width="fill", height="fill")
deletebutton = gz.PushButton(deletebar, text="DELETE", align="right", height="fill", command=movefolder)


report = gz.TextBox(app, text="⮚ Deleting older than 48 hours",  width="fill", height="fill", multiline=True, scrollbar=True)
deleteold()
report.append('⮚ Select a file and click on DELETE')



app.display()
zipfiler.zipper()

