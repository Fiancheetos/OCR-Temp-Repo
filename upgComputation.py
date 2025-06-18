import re

sample_dict = {
    "SBS-1234": ["Intro to Computer Literacy","P","3"],
    "MMS 100":["Introduction to Multimedia Studies","1.0","3"],
    "COMM 2":["Communication Skills II","2.5","3"],
}

overall_gwa = 0.0
total_units = 0

for subj in sample_dict.values():
    if (re.match(r"^\d\.\d+$", subj[1]) and re.match(r"^\d+$", subj[2])):
        overall_gwa += float(subj[1]) * float(subj[2])
        total_units += int(subj[2])


print(overall_gwa, total_units)
print(overall_gwa/total_units)





