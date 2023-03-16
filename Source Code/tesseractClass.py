import pytesseract
import cv2
import threading
import psutil

timeToRun = 600
fileNameGlobal = ""

def tessFile(fileName, angles, language,queue):
    fileNameLegible = fileName.split("/")[-1].split(".")[0]
    fileNameGlobal = fileNameLegible
    queue.put("Starting {0}...".format(fileNameLegible))
    custom_oem_psm_config = '--oem 3 --psm 11 -l {0} -c identifier={1}'.format(language,fileNameGlobal)
    img_rgb = cv2.cvtColor(cv2.imread(fileName),cv2.COLOR_BGR2RGB)
    excel_data_000 = []
    excel_data_090 = []
    excel_data_180 = []
    excel_data_270 = []
    if angles[0]:
        try:
            dataToSave = pytesseract.image_to_string(img_rgb, config=custom_oem_psm_config, timeout=timeToRun).splitlines()
            for i in range(len(dataToSave)-1,0, -1):
                if dataToSave[i] == "":
                    dataToSave.pop(i)
                elif "," in dataToSave[i]:
                    dataToSave[i] = dataToSave[i].replace(",", ".")
            if not dataToSave:
                dataToSave = [""]
            excel_data_000 = dataToSave
        except:
           queue.put("{0} 0 Degrees took too long...".format(fileNameLegible))
    if angles[1]:
        img_rot  = cv2.rotate(img_rgb,cv2.ROTATE_90_CLOCKWISE,1)
        try:
            dataToSave = pytesseract.image_to_string(img_rot, config=custom_oem_psm_config, timeout=timeToRun).splitlines()
            for i in range(len(dataToSave)-1,0, -1):
                if dataToSave[i] == "":
                    dataToSave.pop(i)
                elif "," in dataToSave[i]:
                    dataToSave[i] = dataToSave[i].replace(",", ".")
            if not dataToSave:
                dataToSave = [""]
            excel_data_090 = dataToSave
        except:
           queue.put("{0} 90 Degrees took too long...".format(fileNameLegible))
        del img_rot
    if angles[2]:
        img_rot  = cv2.flip(img_rgb,-1)
        try:
            dataToSave = pytesseract.image_to_string(img_rot, config=custom_oem_psm_config, timeout=timeToRun).splitlines()
            for i in range(len(dataToSave)-1,0, -1):
                if dataToSave[i] == "":
                    dataToSave.pop(i)
                elif "," in dataToSave[i]:
                    dataToSave[i] = dataToSave[i].replace(",", ".")
            if not dataToSave:
                dataToSave = [""]
            excel_data_180 = dataToSave
        except:
           queue.put("{0} 180 Degrees took too long...".format(fileNameLegible))
        del img_rot
    if angles[3]:
        img_rot  = cv2.rotate(img_rgb,cv2.ROTATE_90_COUNTERCLOCKWISE,1)
        try:
            dataToSave = pytesseract.image_to_string(img_rot, config=custom_oem_psm_config, timeout=timeToRun).splitlines()
            for i in range(len(dataToSave)-1,0, -1):
                if dataToSave[i] == "":
                    dataToSave.pop(i)
                elif "," in dataToSave[i]:
                    dataToSave[i] = dataToSave[i].replace(",", ".")
            if not dataToSave:
                dataToSave = [""]
            excel_data_270 = dataToSave
        except:
           queue.put("{0} 270 Degrees took too long...".format(fileNameLegible)) 
        del img_rot
    queue.put("Wrote {0}, continuing on...".format(fileNameLegible))
    return [excel_data_000,excel_data_090,excel_data_180,excel_data_270,fileNameLegible]