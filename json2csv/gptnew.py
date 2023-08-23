import json
import csv

# 读取JSON文件
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将数据转换为CSV格式
csv_data = []
for sn, info in data.items():
    college = info['college']
    major_groups = info['majorGroups']
    for major_group_sn, major_group_info in major_groups.items():
        major_group_type = major_group_info['info']['类型']
        major_group_subject = major_group_info['info']['首选科目']
        major_group_batch = major_group_info['info']['批次']
        major_group_sn = major_group_info['info']['SN']
        major_group_reselect_subject = major_group_info['info']['再选科目']
        majors = major_group_info['majors']
        for major_sn, major_info in majors.items():
            major_name = major_info['name']
            print(major_info['data'])
            major_data_2022 = major_info['data']['2022'] if '2022' in major_info['data'] else ['','','','']
            major_data_2021 = major_info['data']['2021'] if '2021' in major_info['data'] else ['','','','']
            csv_data.append([sn, college, major_group_sn, major_group_type,
                             major_group_batch, major_group_subject, major_group_reselect_subject,
                             major_sn, major_name,
                             major_data_2022[0], major_data_2022[1], major_data_2022[2], major_data_2022[3],
                             major_data_2021[0], major_data_2021[1], major_data_2021[2], major_data_2021[3]])

# 将CSV数据写入文件
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['CollegeCode', 'CollegeName', 'MajorGroupCode', 'MajorGroupType', 'Batch', 'FirstSubject',
                     'ReselectSubject', 'MajorCode', 'MajorName', 'HighestScore2022', 'HighestRanking2022',
                     'LowestScore2022', 'LowestRanking2022', 'HighestScore2021', 'HighestRanking2021',
                     'LowestScore2021', 'LowestRanking2021'])
    for row in csv_data:
        writer.writerow(row)