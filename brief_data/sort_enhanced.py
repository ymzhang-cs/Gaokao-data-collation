import regex as re
import csv

fo = open("list-riched.txt", 'r', encoding='utf-8')
content = fo.read()
fo.close()

# 格式：{序号: [(院校代码, 院校名称), 专业组序号, [(专业序号, 专业名称), (专业序号, 专业名称)]]}
entrys = {}

print(content)

# 数据读取
content_groups = re.findall(r"([0-9]{1,2}(?:.|\s)+?)(?=\n[0-9]{1,2}\n|\n\n)", content)
print(content_groups)

# 数据处理

## 单个项目处理
def transformSingle(text):
    text_list = text.split("\n")
    SN = text_list[0]
    print("SN: " + SN)
    print("text_list[3] is " + text_list[3])
    collegeSN = text_list[3][0:4]
    collegeName = re.search(r"(?<=[0-9]{6}-)(.*)(?=[0-9]{2})", text_list[3]).group(0)
    majorGroupSN = re.search(r"(?<=[\u4e00-\u9fa5\(\)])([0-9]{2})", text_list[3]).group(0)
    print(str(text_list[4:]))
    majors = re.findall(r"'([0-9]{2})-(.*?)'", str(text_list[4:]))
    return {SN: [(collegeSN,collegeName), majorGroupSN, majors]}

## 遍历处理
for collegeGroup in content_groups:
    entrys |= transformSingle(collegeGroup)

print(entrys)

with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['序号', '院校代码', '院校名称', '专业组序号', '专业序号', '专业名称'])
    for k, v in entrys.items():
        for i, j in enumerate(v[2]):
            if i == 0:
                writer.writerow([k, v[0][0], v[0][1], v[1], j[0], j[1]])
            else:
                writer.writerow(['', '', '', '', j[0], j[1]])