import sys
import argparse
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import os
import csv
import webbrowser
import pytesseract
import platform
import time
from multiprocessing import Pool, freeze_support
import multiprocessing
from itertools import zip_longest
from tesseractClass import tessFile
# langOptions is a global variable which displays all of the available languages, it is left originally blank in case the user does not have Tesseract Installed yet
global langOptions
langOptions = [""]
# CpusOptions is just a list with percentages used to show to user, it's set here because I felt like it
cpusOptions = ["25%","50%","75%","100%"]
# This function serves to update the input button's label to reflect if Multiple Files? is selected or not
def update_label():
    if var.get() == 1:
        chooseBtn['text'] = "Choose the Input Directory"
    else:
        chooseBtn['text'] = "Choose the Input File"
# If the user doesn't have Tesseract on their path variable, they can use this function to manually assign the location to the pytesseract module, Only Works on Windows becuase I have no idea how to do it on other systems
def chooseTesseractDir():
    os_name = platform.system()
    if os_name == "Windows":
        dirName = filedialog.askopenfilename(title="Select Tesseract", filetypes=[("Application", "*.exe")])
        if dirName != "":
            if "tesseract.exe" not in dirName:
                messagebox.showinfo(title="Name Error", message="Application name is not Tesseract.exe, trying anyways.")
            try:
                pytesseract.pytesseract.tesseract_cmd = dirName
                if isinstance(pytesseract.get_languages()[0],str):
                    langOptions = pytesseract.get_languages()
                    langDrop['values'] = tuple(langOptions)
                    lblhyperlink.destroy()
                    frmHyp.destroy
                    lblMis = tk.Label(window,text="Tesseract not on PATH, but it was manually added.", font=("Courier New", "10", "italic"),bg= "#D6D6D6")
                    lblMis.grid(row=2,column=1)
            except:
                messagebox.showinfo(title="Error", message="There was an error manually assigning Tesseract.exe. This could be the wrong application or possibly Tesseract is unable to find a system language.")
# Function chooses the proper input file/directory for tesseract, checks to see if Multiple Files? is checked or not
def chooseInDirectory():
    if var.get() == 1:
        dirName = filedialog.askdirectory(title="Select the Directory for the files...")
    else:
        dirName = filedialog.askopenfilename(title="Select the file...")
    if dirName != "":
        fileDirEntry.delete(0, tk.END)
        fileDirEntry.insert(0, dirName)
    return fileDirEntry
# Function chooses the proper output directory for the CSV file
def chooseOutDirectory():
    dirName = filedialog.askdirectory(title="Select the Output Directory for the files...")
    outFDirEntry.delete(0, tk.END)
    outFDirEntry.insert(0, dirName)
    return outFDirEntry
# Function runs the function if it was submitted visually. This can be ignored as most people won't ever need it, I only wrote it like this so I could automate it with Batch files on Windows and because I wanted to try another language. To do this yourself, use pyinstaller to make your own exe without the windowed flag
def visualSubmit():
    window.withdraw()
    if fileDirEntry.get() == "":
            messagebox.showinfo(title="Error", message="Input directory was not specified.")
            window.deiconify()
            return()
    elif outFDirEntry.get() == "":
        messagebox.showinfo(title="Error", message="Output directory was not specified.")
        window.deiconify()
        return()       
    angles = []
    for i in range(len(chkBoxArr)):
        if chkBoxArr[i].get():angles.append(True)
        else:angles.append(False)
    if   "25%" in cpusDrop.get():  cpuFraction = 0.25
    elif "50%" in cpusDrop.get():  cpuFraction = 0.50
    elif "75%" in cpusDrop.get():  cpuFraction = 0.75
    elif "100%" in cpusDrop.get(): cpuFraction = 1.00
    languageChosen = langDrop.get()
    varVal = var.get()
    submitForm(fileDir=fileDirEntry.get(), outFDir=outFDirEntry.get(), angles=angles, varVal=varVal, languageChosen=languageChosen)
    window.deiconify()
    return
# This function is the main function, it runs the Tesseract Class Functions, along with the Multiprocessing code. It is written terribly inefficiently but I do not care.
def submitForm(fileDir, outFDir, angles, varVal, languageChosen, cpuFraction): #Params: fileDir, outFDir, angles
    if "\\" in fileDir:
        fileDir = fileDir.replace("\\", "/")
    if "\\" in outFDir:
        outFDir = outFDir.replace("\\", "/")
    if varVal == 1:
        fileList = os.listdir(fileDir)
        os.environ['OMP_THREAD_LIMIT'] = '1'
    else:
        file = fileDir.split("/")[-1]
        fileList = [file]
        fileDirList = fileDir.split("/")[:-1]
        fileDir = "/".join(fileDirList)
    root = tk.Tk()
    icon16Tk = Image.open(resource_path('16Icon.png'))
    icon32Tk = Image.open(resource_path('32Icon.png'))
    photo16Tk = ImageTk.PhotoImage(icon16Tk)
    photo32Tk = ImageTk.PhotoImage(icon32Tk)
    root.wm_iconphoto(False, photo16Tk, photo32Tk)


    root.title("Tesseract Visual Application")
    root.geometry("500x350")
    root.configure(background = "#D6D6D6")
    frm2222 = tk.Frame(root, bg='#EEEEEE')
    lbl222 = tk.Label(root,text="Tesseract Visual Application", font=("Courier New", "16", "bold"), bg= "#D6D6D6")
    scrlBar = ttk.Scrollbar(frm2222)
    listOfText = tk.Listbox(frm2222,yscrollcommand= scrlBar.set)
    scrlBar.config ( command= listOfText.yview)

    frm2222.grid_columnconfigure(0, weight=1);frm2222.grid_rowconfigure(0, weight=1);root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(4, weight=8)
    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(1, weight=1)
    listOfText.grid(row=0,column=0,sticky="NSEW")

    scrlBar.grid(row=0,column=2,sticky="NSW")
    lbl222.grid(row=0,column=1)
    frm2222.grid(row=4, column=1, sticky="NESW")
    root.update()
    starList = []
    resultsList = []
    queue = multiprocessing.Manager().Queue()
    if varVal == 1:
        # run if directory
        itemsOnList = 0
        for fileAHHH in fileList:
            FormattedName = fileDir + "/" + fileAHHH
            starList.append([FormattedName, angles,languageChosen, queue])
            root.update()
        with Pool(int(float(os.cpu_count())*cpuFraction)) as p:
            root.update()
            resultsObj = p.starmap_async(tessFile,starList, chunksize=2)
            while not resultsObj.ready() or not queue.empty():
                root.update()
                if not queue.empty():
                    queueVal = queue.get_nowait()
                    if "Starting" in queueVal:
                        itemsOnList += 1
                        listOfText.insert(tk.END, "{0}/{1} - {2}".format(itemsOnList,len(starList),queueVal))
                        listOfText.itemconfig(tk.END,{'fg':'red'})
                    elif "continuing on" in queueVal:
                        listOfText.insert(tk.END, "{0}/{1} - {2}".format(itemsOnList,len(starList),queueVal))
                        listOfText.itemconfig(tk.END,{'fg':'green'})
                    elif "took too long..." in queueVal:
                        listOfText.insert(tk.END, queueVal)
                        listOfText.itemconfig(tk.END,{'fg':'blue'})
            p.close()
            p.join()
            values = resultsObj.get()
    else:
        # run if individual file, no multiprocessing, because theres no need
        FormattedName = fileDir + "/" + file
        excel_data = tessFile(FormattedName, angles, languageChosen, queue)
        root.update()
        values = []
        values.append(excel_data)
    root.update()
    outputName = outFDir+ "/{0}Output.csv".format(fileDir.split("/")[-1])
    fieldNames = []
    with open(outputName, 'w', newline='') as csvfile:
        finalDataList = []
        for i in range(len(values)):
            if "," in values[i][4]:
                values[i][4] = values[i][4].replace(",", "")
            fieldNames.append('{0} 0 Degrees'.format(values[i][4]))
            fieldNames.append('{0} 90 Degrees'.format(values[i][4]))
            fieldNames.append('{0} 180 Degrees'.format(values[i][4]))
            fieldNames.append('{0} 270 Degrees'.format(values[i][4]))
            values[i].pop(4)
            finalDataList.append(values[i][0])
            finalDataList.append(values[i][1])
            finalDataList.append(values[i][2])
            finalDataList.append(values[i][3])
        zippedList = list(zip_longest(*finalDataList,fillvalue=""))
        writer = csv.writer(csvfile)
        writer.writerow(fieldNames)
        for i in range(len(zippedList)): writer.writerow(zippedList[i])
    listOfText.insert(tk.END, "Done running, will close soon.")
    for i in range(1000):
        root.update()
        time.sleep(0.001)
    root.deiconify()
    root.destroy()
    return
def callback(url):
    webbrowser.open_new_tab(url)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
if __name__ == "__main__":
    freeze_support()
    multiprocessing.set_start_method('spawn')
    parser = argparse.ArgumentParser(description="This command line utility is useful for automation with windows BATCH files, or what ever else you'd like to try",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
    parser.add_argument("-src","--source-file-location", type=str, help="Source location (Folder or Individual files)")
    parser.add_argument("-mult", "--multiple-files", type=bool, help="Multiple Files?")
    parser.add_argument("-dest", "--destination-file-location", type=str, help="Destination location")
    parser.add_argument("-a", "--angles", type=str, help="Angles to analyze, order Normal, 90" + chr(176) + " Clockwise, 180" + chr(176) + " Clockwise, 270" + chr(176) + " Clockwise (Ex: 0101, 0 for False, 1 for True)")
    parser.add_argument("-l", "--language",type=str, help="Language to search for")
    parser.add_argument("-c", "--cpu-fraction",type=float, help="Fraction of total CPU count to be used by the application")
    args=parser.parse_args()
    if args.source_file_location == None and args.multiple_files == None and args.destination_file_location == None and args.angles == None and args.language == None and args.cpu_fraction == None:
        # if running visually
        print("Running Normally")
        window = tk.Tk()
        icon16Tk = Image.open(resource_path('16Icon.png'))
        icon32Tk = Image.open(resource_path('32Icon.png'))
        photo16Tk = ImageTk.PhotoImage(icon16Tk)
        photo32Tk = ImageTk.PhotoImage(icon32Tk)
        window.wm_iconphoto(False, photo16Tk, photo32Tk)
        window.title("Tesseract Visual Application")
        window.geometry("500x400")
        frmMain = tk.Frame(window, bg='#D6D6D6')
        frmMult = tk.Frame(window, bg='#D6D6D6')
        try:
            langOptions = pytesseract.get_languages()
            lblMis = tk.Label(window,text="Tesseract is on PATH, good job!", font=("Courier New", "10", "italic"),bg= "#D6D6D6")
            lblMis.grid(row=2,column=1)
        except:
            langOptions = [""]
            frmHyp = tk.Frame(window, bg='#D6D6D6')
            lblMis = tk.Label(frmHyp,text="Tesseract is not on PATH, see ", font=("Courier New", "10", "italic"),fg="red",bg= "#D6D6D6")
            lblhyperlink = tk.Label(frmHyp,text="here.", font=("Courier New", "10", "italic", "underline"),fg="#3366CC",bg= "#D6D6D6")
            lblMis.grid(row=0,column=0, sticky="E")
            lblhyperlink.grid(row=0,column=1, sticky="W")
            lblhyperlink.bind("<Button-1>", lambda e:
            callback(r"https://github.com/WilliamTranch/Tesseract-Visual-Application/blob/main/README.md#it-says-tesseract-is-not-on-path"))
            if os.name == 'nt':
                lblMis.bind("<Double-Button-1>", lambda e:
            chooseTesseractDir())
            frmHyp.grid(row=2,column=1)
        chkBoxArr = []
        for i in range(4):
            chkBoxArr.append(tk.BooleanVar())

        window.configure(background = "#D6D6D6")
        global var
        global chooseBtn
        var = tk.IntVar()
        lblTtl = tk.Label(window,text="Tesseract Visual Application", font=("Courier New", "16", "bold"), bg= "#D6D6D6")
        lblSpc = tk.Label(window,text="created by William T", font=("Courier New", "10", "italic"), bg= "#D6D6D6",height=1, anchor="n")
        boxMlt = tk.Checkbutton(frmMult, bg='#D6D6D6',text="Multiple Files?",font=("Courier New", "12"),variable=var,onvalue=1, offvalue=0, command=update_label)
        box000 = tk.Checkbutton(frmMain, variable=chkBoxArr[0], bg='#D6D6D6',text="Normal           ",font=("Courier New", "12"))
        box090 = tk.Checkbutton(frmMain, variable=chkBoxArr[1], bg='#D6D6D6',text="90°  Clockwise",font=("Courier New", "12"))
        box180 = tk.Checkbutton(frmMain, variable=chkBoxArr[2], bg='#D6D6D6',text="180° Clockwise   ",font=("Courier New", "12"))
        box270 = tk.Checkbutton(frmMain, variable=chkBoxArr[3], bg='#D6D6D6',text="270° Clockwise",font=("Courier New", "12"))
        box270 = tk.Checkbutton(frmMain, variable=chkBoxArr[3], bg='#D6D6D6',text="270° Clockwise",font=("Courier New", "12"))
        langLb = tk.Label(frmMain,text="Tesseract Language:", font=("Courier New", "12"), bg= "#D6D6D6")
        cpusLb = tk.Label(frmMain,text="CPU Usage:", font=("Courier New", "12"), bg= "#D6D6D6")
        chooseBtn =tk.Button(frmMain, text="Choose the Input File",command=chooseInDirectory, font=("Courier New", "10"), width=27)
        outDirBtn =tk.Button(frmMain, text="Choose the Output Directory",command=chooseOutDirectory, font=("Courier New", "10"), width=27)
        submitBtn =tk.Button(window, text="Submit",command=visualSubmit, font=("Courier New", "10"), width=52)
        langDrop = ttk.Combobox(frmMain,values=langOptions,font=("Courier New", "10"),width=25)
        cpusDrop = ttk.Combobox(frmMain,values=cpusOptions,font=("Courier New", "10"),width=25)
        global fileDirEntry
        global outFDirEntry
        fileDirEntry = tk.Entry(frmMain, width=32)
        fileDirEntry.insert(0, "")
        outFDirEntry = tk.Entry(frmMain, width=32)
        outFDirEntry.insert(0, "")
        frmMain.grid(row=4, column=1, sticky="NESW")
        frmMain.grid_columnconfigure(0, weight=1)
        frmMain.grid_columnconfigure(1, weight=1)
        frmMult.grid(row=3, column=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.grid_rowconfigure(4, weight=2)
        window.grid_rowconfigure(6, weight=1)
        window.grid_columnconfigure(1, weight=1)
        boxMlt.grid(row=0,column=0, sticky="W",padx=3)
        fileDirEntry.grid(row=1,column=0, sticky="E",padx=3)
        outFDirEntry.grid(row=2,column=0, sticky="E",padx=3)
        box000.grid(row=5,column=0, sticky="E",padx=3)
        box090.grid(row=5,column=1, sticky="W",padx=3)
        box180.grid(row=6,column=0, sticky="E",padx=3)
        box270.grid(row=6,column=1, sticky="W",padx=3)
        chooseBtn.grid(row=1,column=1, sticky="W",padx=3,pady=2)
        outDirBtn.grid(row=2,column=1, sticky="W",padx=3,pady=2)
        langLb.grid(row=3,column=0, sticky="E",padx=6)
        langDrop.grid(row=3,column=1, sticky="W",padx=3,pady=2)
        cpusLb.grid(row=4,column=0, sticky="E",padx=6)
        cpusDrop.grid(row=4,column=1, sticky="W",padx=3,pady=2)
        submitBtn.grid(row=5,column=1, sticky="N",padx=3)
        lblTtl.grid(row=0,column=1)
        lblSpc.grid(row=1,column=1)
        window.mainloop()
    else:
        # if running from command line
        print("Running from command line")
        fileSrc = args.source_file_location
        fileDest = args.destination_file_location
        fileMult = args.multiple_files
        anglesStr = args.angles
        languageChosen = args.language
        cpuFraction = args.cpu_fraction
        try:
            langOptions = pytesseract.get_languages()
        except:
            parser.error(r"Tesseract is not on PATH: See https://github.com/WilliamTranch/Tesseract-Visual-Application/blob/main/README.md#it-says-tesseract-is-not-on-path")
        if languageChosen not in langOptions:
            parser.error(r"Language is not an option, options are: " + str(langOptions))
        if fileSrc == "":
            parser.error("Empty File String")
        if fileDest == "":
            parser.error("Empty Dest String")
        if len(anglesStr) != 4:
            parser.error("Invalid Angles Entry (must be 4 characters long)")
        angles = []
        for i in range(4):
            if anglesStr[i] in "0":
                angles.append(False)
            elif anglesStr[i] in "1":
                angles.append(True)
            else:
                parser.error("Invalid Angles Character (must be 1's or 0's only)")
        if cpuFraction > 1 or cpuFraction < 0:
            parser.error("--cpu-fraction should be a float value between 0 and 1")
        submitForm(fileDir=fileSrc, outFDir=fileDest, angles=angles, varVal=int(fileMult), languageChosen=languageChosen, cpuFraction=cpuFraction)
        print("Done running")
