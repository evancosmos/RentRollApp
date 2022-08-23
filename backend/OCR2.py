#Modified version of table-extraction from https://github.com/fazlurnu/Text-Extraction-Table-Image

import json

from preprocessing import get_grayscale, get_binary, draw_text, detect
from ROI_selection import detect_lines, get_ROI
import cv2 as cv

def OCR(filename, display = False, print_text = False, write = False):
    
    src = cv.imread(cv.samples.findFile(filename))
    
    horizontal, vertical = detect_lines(src, minLinLength=350, display=False, write = True)
    
    ## invert area (all 0 for no inverted area)
    left_line_index = 0
    right_line_index = 0
    top_line_index = 0
    bottom_line_index = 0
    
    cropped_image, (x, y, w, h) = get_ROI(src, horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
    
    gray = get_grayscale(src)
    bw = get_binary(gray)
    #cv.imshow("bw", bw)
    #bw = erode(bw, kernel_size=2)
    
    ## set keywords
    keywords = ['Tenant Name', 'Unit #', 'Area Rented', 'Lease Term', 'Rental Fee', 'Monthly Base Rent', 'Commencement Date',
            'Tenant Improvement', 'TI Payment', 'Fixturing Period', '# months free', 'Parking Stalls',
            'Deposit', 'Outstanding Rent Due', 'Annual']
    
    dict_kabupaten = {}
    for keyword in keywords:
        dict_kabupaten[keyword] = []
        
    ## set counter for image indexing
    counter = 0
    
    ## set line index
    first_line_index = 1
    last_line_index = 14
    
    ## read text
    print("Start detecting text...")
    for i in range(first_line_index, last_line_index):
        for j, keyword in enumerate(keywords):
            counter += 1
            
            progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
            percentage = "%.2f" % progress
            print("Progress: " + percentage + "%")
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1
            
            cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
            
            if (keywords[j]=='kabupaten'):
                text = detect(cropped_image)
                dict_kabupaten[keyword].append(text)
                
                if (print_text):
                    print("Not number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            else:
                text = detect(cropped_image, is_number=True)
                dict_kabupaten[keyword].append(text)
                
                if (print_text):
                    print("Is number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            
            if (display or write):
                    image_with_text = draw_text(src, x, y, w, h, text)
                    
            if (display):
                cv.imshow("detect", image_with_text)
                cv.waitKey(0)
                cv.destroyAllWindows()

            if (write):
                cv.imwrite("../Images/"+ str(counter) + ".png", image_with_text);
            
    filename = 'OCRout.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict_kabupaten, f, ensure_ascii=False, indent=4)

    return 0
    
if __name__ == "__main__":
    OCR("1650 lease rent roll.png")