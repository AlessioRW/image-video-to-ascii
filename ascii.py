from PIL import Image, ImageOps
import easygui, os, sys

def show(text):
    for line in text:
        print(line)

def save(test):
    if os.path.isdir("C:\\Users\\"+os.getlogin()+"\\Desktop"):
        file = open("C:\\Users\\"+os.getlogin()+"\\Desktop\\"+(filename[filename.rfind('\\')+1::]).split('.')[0]+".txt","a")
    else:
        print('Could not find desktop, saving to current working directory')
        file = open((filename[filename.rfind('\\')+1::]).split('.')[0]+".txt","a")
    for line in text:
        file.write(line+'\n')
    file.close()

filename = easygui.fileopenbox()
image = ImageOps.grayscale(Image.open(filename))
imgData = image.load()

pixelNum = int(input('N.Pixels squared per character (1 = one character per pixel): ')) #number of pixels per character squared ; 10 = 10x10
width, height = image.size[0], image.size[1]

charBlocks = []
for yBlock in range(height // pixelNum):
    blockLine = []
    for xBlock in range(width // pixelNum):
        curBlock = []
        for x in range(pixelNum):
            for y in range(pixelNum):
                curBlock.append(imgData[(xBlock*pixelNum)+x,(yBlock*pixelNum)+y])
        blockLine.append(curBlock)
    charBlocks.append(blockLine)

try:
    if 'c' in ''.join(sys.argv[1:]).lower():
        asciiCharacters = [' ', '.', "'", '`', '^', '"', ',', ':', ';', 'I', 'l', '!', 'i', '>', '<', '~', '+', '_', '-', '?', ']', '[', '}', '{', '1', ')', '(', 
        '|', '\\', '/', 't', 'f', 'j', 'r', 'x', 'n', 'u', 'v', 'c', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'O', 'Z', 'm', 'w', 'q', 'p', 'd', 'b', 'k', 
        'h', 'a', 'o', '*', '#', 'M', 'W', '&', '8', '%', 'B', '@', '$']
    else:
        asciiCharacters = [" ",".",":","-","=","+","*","#","%","@"]
except:
    if 'y' in input('Use complex character set (y for yes)').lower():
        asciiCharacters = [' ', '.', "'", '`', '^', '"', ',', ':', ';', 'I', 'l', '!', 'i', '>', '<', '~', '+', '_', '-', '?', ']', '[', '}', '{', '1', ')', '(', 
        '|', '\\', '/', 't', 'f', 'j', 'r', 'x', 'n', 'u', 'v', 'c', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'O', 'Z', 'm', 'w', 'q', 'p', 'd', 'b', 'k', 
        'h', 'a', 'o', '*', '#', 'M', 'W', '&', '8', '%', 'B', '@', '$']
    else:
        asciiCharacters = [" ",".",":","-","=","+","*","#","%","@"]

text = []
line = ''
for blockLine in charBlocks:
    line = ''
    for block in blockLine:
        avg = sum(block)/len(block)
        line += asciiCharacters[int(round((avg/255)*len(asciiCharacters),0))-1]
    text.append(line)

if 'y' in input('Show Ascii (y for yes): ').lower():
    show(text)
if 'y' in input('Save Ascii To Desktop (y for yes): ').lower():
    save(text)

