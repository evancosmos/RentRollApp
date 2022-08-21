#Read text from images https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
from PIL import Image
from pytesseract import pytesseract #Requires the tesseract executable on the system. https://linuxhint.com/install-tesseract-ocr-linux/

import cv2 as cv
import numpy

#Credit to https://github.com/fazlurnu/Text-Extraction-Table-Image
def readImage(filename):
    img = cv.imread(cv.samples.findFile(filename))
    cImage = numpy.copy(img) #image to draw 
    #cv.imshow("image", img) #name the window as "image"
    #cv.waitKey(0)
    #cv.destroyWindow("image") #close the window

    img = toGreyScale(img)
    hor, vert = detect_lines(img)

    text = pytesseract.image_to_string(img)
    print(text)
    return 

def toGreyScale(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 50, 150)
    cv.imshow("canny", canny)
    cv.waitKey(0)
    cv.destroyWindow("canny")
    return canny

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]
    
def overlapping_filter(lines, sorting_index):
    filtered_lines = []
    
    lines = sorted(lines, key=lambda lines: lines[sorting_index])
    
    for i in range(len(lines)):
            l_curr = lines[i]
            if(i>0):
                l_prev = lines[i-1]
                if ( (l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                    filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)
                
    return filtered_lines
               
def detect_lines(image, title='default', rho = 1, theta = numpy.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 6, display = False, write = False):
    
    # Copy edges to the images that will display the results in BGR
    cImage = numpy.copy(image)
    
    #linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
    linesP = cv.HoughLinesP(image, rho , theta, threshold, None, minLinLength, maxLineGap)
    
    horizontal_lines = []
    vertical_lines = []
    
    if linesP is not None:
        #for i in range(40, nb_lines):
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)
                
            elif (is_horizontal(l)):
                horizontal_lines.append(l)
        
        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)
    
    display = False
    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv.LINE_AA)
            
            cv.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        for i, line in enumerate(vertical_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        cv.imshow("Source", cImage)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    return (horizontal_lines, vertical_lines)

if __name__ == "__main__":
    readImage("1650 lease rent roll.png")