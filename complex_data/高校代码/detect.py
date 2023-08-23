import re, json

fi = open(r'数据/高校代码/combined.csv', 'r', encoding='utf-8')

result = {}

reverse_it = True

for line in fi:
    code, majorG = line.split(',')
    if reverse_it:
        result[re.search(r"^(.*?)(?=[0-9])", majorG).group(1)] = code
    else:
        result[code] = re.search(r"^(.*?)(?=[0-9])", majorG).group(1)

fi.close()

fo = open('college_code.json', 'w')

fo.write(json.dumps(result))

fo.close()