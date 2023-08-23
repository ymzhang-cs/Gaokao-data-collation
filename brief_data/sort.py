import re
fo = open("list.txt", 'r', encoding='utf-8')

# print(fo.read())
fo.seek(0)

entrys = {}

def text_process(itemSN, collageSN, content):
    SN = int(itemSN)
    collageSN = collageSN[:4]
    collageName = re.search(r"([\u4e00-\u9fa5\(\)]+)(?=[0-9])", content).group(1)
    print(collageName)
    majorgroupSN = re.search(r"([0-9]{2})(?=专业组)", content).group(1)
    print(majorgroupSN)
    majorSN = re.search(r"([0-9]{2})(?=向下)", content).group(1)
    print(majorSN)
    return {SN: [[collageSN, collageName], majorgroupSN, [majorSN, majorName]]}

while True:
    line_itmeSN = fo.readline().replace('\n','')
    line_collageSN = fo.readline().replace('\n','')
    line_content = fo.readline().replace('\n','')
    if line_itmeSN == '':
        break
    print((line_itmeSN, line_collageSN, line_content))
    entry = text_process(line_itmeSN, line_collageSN, line_content)
    print(entry)
    entrys |= entry
    
print(entrys)

