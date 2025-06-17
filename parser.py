import re
def cleanCol(col):
    ignore_keywords = r'(?i)\b(note|remarks|prepared by|checked by|issued by|updated by|nothing follows|semester|trimester|credits|university|bachelor|college|enrollment|credit|grade)\b'
    lines = col.split('\n')
    cleaned = [line for line in lines if line != '' and not re.search(ignore_keywords, line)]
    return cleaned

def match(data):
    allowed_one_word_names = {"Thesis"}

    while True:
        lengths = {len(data[0]), len(data[1]), len(data[2]), len(data[4])}
        if len(set(lengths)) == 1:
            break  # All lengths match

        invalidIndices = []
        for i in range(len(data[1])):
            course_name = data[1][i].strip()
            if len(course_name.split()) == 1 and course_name not in allowed_one_word_names:
                invalidIndices.append(i)

        if not invalidIndices:
            print("Mismatch remains but no mergeable entries found.")
            break

        for j in reversed(invalidIndices):
            data[1][j - 1] = data[1][j - 1] + " " + data[1][j]
            del data[1][j]






