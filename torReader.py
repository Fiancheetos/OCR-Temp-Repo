import cv2
import pytesseract
from pdf2image import convert_from_path
import parser
import numpy

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def process(pil_image):
    image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)

    cCodeCol = [(155, 500), (330, 2035)]
    courseNameCol = [(330, 500), (1090, 2035)]
    finalGradesCol = [(1090, 495), (1205, 2035)]
    reExamCol = [(1205, 500), (1355, 2035)]
    credsCol = [(1355, 500), (1480, 2035)]

    cols = [cCodeCol, courseNameCol, finalGradesCol, reExamCol, credsCol]
    data = []

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
        column = parser.cleanCol(column)
        data.append(column)

    parser.match(data)

    print("")
    print("Extracted Transcript: ")
    header = ["Course Code", "Course Name", "Grade", "Credits"]
    print(f"{header[0]:<12} | {header[1]:<80} | {header[2]:<5} | {header[3]:<4}")
    for course_code, course_name, grade, credit in zip(data[0], data[1], data[2], data[4]):
        print(f"{course_code:<12} | {course_name:<80} | {grade:<5} | {credit:<4}")


images = convert_from_path('./TOR_Sample.pdf', fmt='png')

for image in images:
    process(image)

