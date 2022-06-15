from PIL import Image, ImageOps
import easygui, os, sys, cv2, time
print('Pass "ext" as parameter to use extended character set if using command line')
print('Pass "cam" to use camera as live input video\n')

def show(text):
    os.system('cls')
    for line in text:
        print(line)

def save(text):
    if os.path.isdir("C:\\Users\\"+os.getlogin()+"\\Desktop"):
        file = open("C:\\Users\\"+os.getlogin()+"\\Desktop\\"+(filename[filename.rfind('\\')+1::]).split('.')[0]+".txt","a")
    else:
        print('Could not find desktop, saving to current working directory')
        file = open((filename[filename.rfind('\\')+1::]).split('.')[0]+".txt","a")
    for line in text:
        file.write(line+'\n')
    file.close()

def imageToAscii(image,inVideo):
    #image = ImageOps.grayscale(Image.open(filename))
    imgData = image.load()

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


    text = []
    line = ''
    for blockLine in charBlocks:
        line = ''
        for block in blockLine:
            avg = sum(block)/len(block)
            line += asciiCharacters[int(round((avg/255)*len(asciiCharacters),0))-1]
        text.append(line)

    if inVideo == False:
        if 'y' in input('Show Ascii (y for yes): ').lower():
            show(text)
        if 'y' in input('Save Ascii To Desktop (y for yes): ').lower():
            save(text)
    else:
        return text

def videoToAscii(filename):
    frames = []
    video = cv2.VideoCapture(filename)
    numFrames = int(video.get(cv2. CAP_PROP_FRAME_COUNT))
    curFrame = 0

    while True:
        os.system('cls')
        curFrame += 1
        print(str(curFrame) +'/'+ str(numFrames) + ' frames generated')

        ret,frame = video.read()

        if ret:
            frames.append(imageToAscii(ImageOps.grayscale(Image.fromarray(frame)),True))
        else:
            break
    
    input('Play ASCII Video (Press Enter): ')
    timePerFrame = 1/video.get(cv2.CAP_PROP_FPS)
    for frame in frames:
        show(frame)
        time.sleep(timePerFrame*0.2)

def camera():
    try:
        video = cv2.VideoCapture(0)
    except:
        print('Error getting camera input')
  
    while(True):
        ret, frame = video.read() #get current camera frame
        text = imageToAscii(ImageOps.grayscale(Image.fromarray(frame)),True) #get frame in ASCII
        show(text) #print frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

parameters = ''.join(sys.argv[1:]).lower()
if 'ext' in parameters:
    asciiCharacters = [' ', '.', "'", '`', '^', '"', ',', ':', ';', 'I', 'l', '!', 'i', '>', '<', '~', '+', '_', '-', '?', ']', '[', '}', '{', '1', ')', '(', 
        '|', '\\', '/', 't', 'f', 'j', 'r', 'x', 'n', 'u', 'v', 'c', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'O', 'Z', 'm', 'w', 'q', 'p', 'd', 'b', 'k', 
        'h', 'a', 'o', '*', '#', 'M', 'W', '&', '8', '%', 'B', '@', '$']
    print('Using extended chaarcter set')

else:
    asciiCharacters = [" ",".",":","-","=","+","*","#","%","@"]
    print('Using standard chaarcter set')


pixelNum = int(input('N.Pixels squared per character (1 = one character per pixel): ')) #number of pixels per character squared ; 10 = 10x10

if 'cam' in parameters:
    input('Using camera as live input (press enter to start):')
    camera()

else:
    filename = easygui.fileopenbox()

    vidFiles = ['mp4','webm','gif','mkv']
    imgFiles = ['png','jpg','jpeg']
    if filename.split('.')[1] in vidFiles:
        videoToAscii(filename)
    elif filename.split('.')[1] in imgFiles:
        imageToAscii(ImageOps.grayscale(Image.open(filename)),False)
