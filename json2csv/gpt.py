import json
import csv

# 从JSON文件中读取数据
with open('json2csv\\sample\\sample.json', 'r') as jsonfile:
    fullsize_data = json.load(jsonfile)
    print(fullsize_data)

# 创建csv文件并写入表头
with open('major_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['大学代码', '大学名称', '专业组代码', '专业组类型', '批次', '首选科目', '再选科目',
                     '专业代码', '专业名称', '2022年录取最高分', '2022年录取最高名次',
                     '2022年录取最低分', '2022年录取最低名次', '2021年录取最高分', '2021年录取最高名次', '2021年录取最低分', '2021年录取最低名次'])

    # 遍历每个专业，并将数据写入csv文件
    for major_group in fullsize_data.values():
        college_code = major_group['SN']
        college_name = major_group['college']
        
        for group_code, group_info in major_group['majorGroups'].items():
            group_type = group_info['info']['类型']
            batch = group_info['info']['批次']
            first_subject = group_info['info']['首选科目']
            second_subject = group_info['info']['再选科目']
            
            for major_code, major_info in group_info['majors'].items():
                major_name = major_info['name']
                major_sn = major_info['majorSN']
                data = major_info['data']
                row_data = [college_code, college_name, group_code, group_type, batch, first_subject, second_subject, major_sn, major_name]
                
                if '2022' in data:
                    row_data.extend(data['2022'])
                else:
                    row_data.extend(['', '', '', ''])
                
                if '2021' in data:
                    row_data.extend(data['2021'])
                else:
                    row_data.extend(['', '', '', ''])
                
                writer.writerow(row_data)