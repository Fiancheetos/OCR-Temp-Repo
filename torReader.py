import cv2
import pytesseract
import numpy
import dataCleaner
import os
from dotenv import load_dotenv
import upgConverter

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_LOCATION")

def detect_columns(pil_image):
    image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detect_vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Combine lines
    table_mask = cv2.add(detect_horizontal, detect_vertical)

    # Find contours (i.e., table/grid blocks)
    contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw table contours
    columns = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > image.shape[0] * 0.5 and w < image.shape[1] * 0.5:  # tall, not too wide

            new_column = [(x,y),(x+w,y+h)]
            columns.append(new_column)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    columns = sorted(columns, key=lambda box: box[0][0])
    return columns

def process(pil_image, cols, records_table, config):
    image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)

    data = []

    ## Assumes column order: Course code, course name, grade, credits

    for col in cols:
        cv2.rectangle(image, col[0], col[1], (0, 255, 0), 1)
        cropped_img = image[col[0][1]:col[1][1], col[0][0]:col[1][0]]
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        rgb_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        column = pytesseract.image_to_string(cropped_img, config='--psm 6')
        column = dataCleaner.clean_columns(column)
        data.append(column)

    dataCleaner.conjunct_name_overflow(data)

    # print("")
    # print("Extracted Transcript: ")
    # header = ["Course Code", "Course Name", "Grade", "Credits"]
    # print(f"{header[0]:<12} | {header[1]:<80} | {header[2]:<5} | {header[3]:<4}")
    for course_code, course_name, grade, credit in zip(data[0], data[1], data[2], data[4]):
        print(f"{course_code:<12} | {course_name:<80} | {grade:<5} | {credit:<4}")
        grade = upgConverter.converter(config, grade)
        if course_code not in records_table:
            records_table[course_code] = [course_name, grade, credit]  
        else: 
            temp = records_table[course_code]
            records_table[course_code] = [temp, grade, credit]

    return records_table


