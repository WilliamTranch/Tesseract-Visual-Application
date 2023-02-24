# Tesseract-Visual-Application
This project is a visual interface version of Tesseract developped in Python, it serves as a simple way to use the tool without needing to install any programming languages to make use of it.
## Table of Contents  
- [What is Tesseract?](#What-is-Tesseract?)  
- [How do I use this?](#How-do-I-use-this?)  
- [Common Issues](#Common-Issues)  

## What is Tesseract?
Tesseract is an Open Source Optical Character Recognition (OCR). Originally developed by HP in the 1980s as proprietary software, its been open source for nearly 20 years now. It is still undergoing development and is currently sponsored by Google. 

Normally Tesseract is a command line based tool used to identify words/characters present in a single image. This program allows you to use it to identify the text in one or several images, to change the specific parameters to optimize for the types of characters are searching for, and to choose the language that the text you intend to read is in.
## How do I use this?
To use this application, you must first download Tesseract.

There are several ways to do this, two recommended ways are:

  a. Download and compile it [directly](https://github.com/tesseract-ocr/tesseract#installing-tesseract "This is a bit more complex")

  b. Download it from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki#tesseract-installer-for-Windows "Much simpler")

***Tesseract is also available for both Linux and macOS, the processes to download them are outlined [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).***

Once you have a version of Tesseract downloaded (this version was developped with version 5.3.0.20221214, but any should work), choose the version of the program for your operation system from below:
- [Windows](https://1drv.ms/u/s!AoTWwASznsXMg_hyqFE_xDvr70utlA?e=fJF9XY)
- [Linux](https://1drv.ms/u/s!AoTWwASznsXMg_hxzjpeyAakCgfBUg?e=bwFYa7)
- [macOS](https://1drv.ms/u/s!AoTWwASznsXMg_hzp3HyjS2Um9W1vA?e=4gQ0WW) (currently in-progress)

Then simply run the application and select the files which you'd like to be processed.

## Common Issues
### It says "Tesseract is not on PATH"
This error can appear if you do not have Tesseract installed, or the Tesseract folder (not the executable) is not on your PATH environment variable. See how to add it to your PATH variable for your specific OS below.
- [Windows](https://www.computerhope.com/issues/ch000549.htm)
- [Linux](https://phoenixnap.com/kb/linux-add-to-path)
- [macOS](https://techpp.com/2021/09/08/set-path-variable-in-macos-guide)

If you can't add it to your PATH variable due to a lack of administrator priviledges, double click on the red text in the application to manually find the folder, this will need to be redone everytime you run the application. This only works on Windows as of now.
### I can't find the language that I want to read in the options menu
The language options available to you are the languages which your system currently has installed as found by Tesseract. You might need to download the language and restart your computer to fix this issue.
