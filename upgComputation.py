import re

# sample_dict = {
#     "SBS-1234": ["Intro to Computer Literacy","P","3"],
#     "MMS 100":["Introduction to Multimedia Studies","1.0","3"],
#     "COMM 2":[[["Communication Skills II","2.5","3"], "3.0", "3"], "5.0", "3"],
# }

def compute_gwa(records_table):
    overall_gwa = 0.0
    total_units = 0

    for subj in records_table.values():
        if (re.match(r"^\d\.\d+$", subj[1]) and re.match(r"^\d+$", subj[2])):
            overall_gwa += float(subj[1]) * float(subj[2])
            total_units += int(subj[2])
            if isinstance(subj[0],list):
                temp = subj[0]
                while isinstance(temp, list):
                    overall_gwa += float(temp[1]) * float(temp[2])
                    total_units += int(temp[2])
                    temp = temp[0]

    return overall_gwa/total_units