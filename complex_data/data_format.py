from datetime import datetime
import json, csv

def data_format(raw_data_dir, college_code_reversed):
    '''
    data_format("file_dir(txt)", "college_code_reversed(json)")
    Help to format the data copied from JSEEA.
    
    Before Using: 处理数据：将"\n该"替换为" 该"，将"\n\("替换为" \("

    数据结构
        
        fullsize_data = {
            "1111": {
                college: "清华大学",
                SN: "1111"
                majorGroups: {
                    "01": {                                                                       ### thisGroup
                        "info": {"类型": "普通类", "首选科目": "历史", "批次": "提前本科其他院校", "SN": 01, "再选科目": "思想政治"},
                        "majors": {
                            "马克思主义理论": {                                                               ### thisMajor
                                "name": "马克思主义理论", 
                                "majorSN": "01"
                                "data": {"2022": ("633", "前107", "633", "前107"), "2021": ("633", "前107", "633", "前107")}}
                        }
                    }        
                }
            }
        }

    程序逻辑

    按行遍历原始数据内容，并根据有无"各专业录取分数"来判断每一部分的范围，将这一部分叫做块（block）
    并即时调用子函数processBlock(block)来处理该块内容，返回值为info={"SN": SN, "college": college, "SN": SN, "majorGroups": majorGroups}
    然后将info融合到fullsize_data字典内
    返回fullsize_data

    '''
    import re, json, copy
    
    with open(college_code_reversed, 'r') as code:
    #TEST with open(college_code_reversed.json, 'r') as code:
        collegeCode = json.loads(code.read())

    fullsize_data = {}

    fo = open(raw_data_dir, 'r', encoding='utf-8')
    #TEST fo = open("数据/data_raw.txt", 'r', encoding='utf-8')

    def merge_dict(dict1, dict2):
        '''
        将作为值的字典融合，用到了递归！（ChatGPT写的）
        '''
        # 遍历dict2中的键值对，将其合并到dict1中
        for key, value in dict2.items():
            # 如果dict1中已经存在相同的键，则递归合并两个字典
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                merge_dict(dict1[key], value)
            # 否则直接将dict2中的键值对添加到dict1中
            else:
                dict1[key] = value
        return dict1

    def processBlock(block):
        '''
        对传入的块进行数据处理。每个块的内容为某年该院校所有专业组与其专业的信息。
        处理逻辑为遍历每一行，通过特殊字符与行间关系判断每行内容并获取相应信息。
        由于专业组序号并非出现在其数据的首行，所以需要临时变量thisGroup进行数据存储
            在进入下一专业组或遍历结束时，thisGroup的内容被转存到majorGroups内
        thisMajor同理

        返回值为一个字典，包含大学信息与majorGroups这一字典。
        格式为{"SN": SN, "college": college, "SN": SN, "majorGroups": majorGroups}
        '''
        
        # 块库
        majorGroups = {}
        # 该组库
        thisGroup = {}
        # 该专业库
        thisMajor = {}

        # 四个mark标记，用于通过行间关系判断数据类型
            # 即将到来的是专业组批次（提前本科其他院校），处理完毕后移除
        markI = False
            # 即将到来的是专业组编号与首选科目（清华大学01专业组(思想政治)），处理完毕后移除
        markII = False
            # 下面要处理的数据可能是具体专业的数据，也可能是下一专业组。进入下一专业组后移除。
        holdMode = False
            # 这一轮遍历已经处理完啦
        rest = False

        def updateMajor2Group():
            print("thisGroup: ", thisGroup)
            print("thisMajor: ", thisMajor)
            if "majors" not in thisGroup:
                thisGroup["majors"] = {}
            thisGroup["majors"][thisMajor['name']] = copy.deepcopy(thisMajor)
        
        def updateGroup2majorGroups():
            majorGroups[thisGroup["info"]["SN"]] = copy.deepcopy(thisGroup)


        for sentence in block:
            s = sentence.replace("\n", "")
            print("majorGroups: ", majorGroups)
            print("thisGroup: ", thisGroup)
            print("thisMajor: ", thisMajor)

            rest = False
            
            if ("\t" not in s) and ("专业代号" not in s) and (thisMajor != {}):
                updateMajor2Group()
            
            # "清华大学2022年各专业录取分数"
            if "各专业录取分数" in s:
                holdMode = False
                college = re.search(r"^(.*?)(?=[0-9])", s).group(1)
                SN = collegeCode[college]
                year = re.search(r"([0-9]{4})", s).group(1)
            
            # "普通类（历史等科目类）"
            if "等科目类" in s:
                # Collect Previous One
                if thisGroup != {}:
                    if ("\t" not in s) and ("专业代号" not in s) and (thisMajor != {}):
                        updateMajor2Group()
                    updateGroup2majorGroups()
                thisGroup = {"info": {"类型": s.split("（")[0], "首选科目": s.split("（")[1][0:2]}}
                thisMajor = {}
                holdMode = False # just added
                markI = True
                rest = True

            # "提前本科其他院校"
            if markI and not rest:
                thisGroup["info"]["批次"] = s
                markI = False
                markII = True
                rest = True
            
            # "清华大学01专业组(思想政治)"
            if markII and not rest:
                print(s)
                thisGroup["info"]["SN"] = s.split("专业组")[0].split(college)[-1]
                thisGroup["info"]["再选科目"] = s.split(r"(")[1].split(r")")[0]
                markII = False
                holdMode = True
                rest = True

            # Potential existing major
            if holdMode and not rest:
                if ("\t" not in s) and ("专业代号" not in s) and (thisMajor != {}):
                    updateMajor2Group()
                if ("\t" not in s) and ("专业代号" not in s):
                    thisMajor["name"] = s
                if "专业代号" in s:
                    thisMajor["majorSN"] = s.split("：")[1]
                if "\t" in s:
                    d = s.split("\t")
                    thisMajor["data"] = {year: (d[0], d[1], d[2], d[3])}
            
        updateMajor2Group()
        updateGroup2majorGroups()
        
        print({"college": college, "SN": SN, "majorGroups": majorGroups})

        return {"SN": SN, "college": college, "SN": SN, "majorGroups": majorGroups}
        
        # if SN not in fullsize_data:
        #     fullsize_data[SN] = {"college": college, "SN": SN, "majorGroups": majorGroups}
        # else:
        #     merge_dict(fullsize_data[SN]["majorGroups"], majorGroups)

    # read data block by block
    block = []
    for line in fo:
        if "各专业录取分数" in line and block != []:
            print(block)
            info = processBlock(block)
            if info["SN"] not in fullsize_data:
                fullsize_data[copy.deepcopy(info)["SN"]] = {"college": copy.deepcopy(info)["college"], "SN": copy.deepcopy(info)["SN"], "majorGroups": copy.deepcopy(info)["majorGroups"]}
            else:
                merge_dict(fullsize_data[copy.deepcopy(info)["SN"]]["majorGroups"], copy.deepcopy(info)["majorGroups"])

            del block
            block=[]
        block.append(line)

    print(block)
    info = processBlock(block)
    if info["SN"] not in fullsize_data:
        fullsize_data[copy.deepcopy(info)["SN"]] = {"college": copy.deepcopy(info)["college"], "SN": copy.deepcopy(info)["SN"], "majorGroups": copy.deepcopy(info)["majorGroups"]}
    else:
        merge_dict(fullsize_data[copy.deepcopy(info)["SN"]]["majorGroups"], copy.deepcopy(info)["majorGroups"])

    del block
    print("FULLSIZE_DATA\n"+str(fullsize_data))

    # 返回整个文件的data
    return fullsize_data
 
if __name__ == "__main__":
    #file_name = 'Output-' + datetime.today().strftime('%Y-%m-%d') + ".json"
    file_name = "data.json"
    data_dir = [
        #'complex_data\\data_sample.txt'
        'complex_data\\data_raw_1.txt',
        'complex_data\\data_raw_2.txt',
        'complex_data\\data_raw_3.txt',
        'complex_data\\data_raw_4.txt',
        'complex_data\\data_raw_5.txt',
        ]
    college_code_reversed = "complex_data\\college_code_reversed.json"
    # with open(file_name, 'w') as code:
    #     for data_file in data_dir:
    #         data_formatted = data_format(data_file, college_code_reversed)
    #         print(data_formatted)
    #         code.write(json.dumps(data_formatted))

    fout = open("majors.csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(fout)
    writer.writerow(['大学代码', '大学名称', '专业组代码', '专业组类型', '批次', '首选科目', '再选科目', '专业代码', '专业名称', '2022年录取最高分', '2022年录取最高名次', '2022年录取最低分', '2022年录取最低名次', '2021年录取最高分', '2021年录取最高名次', '2021年录取最低分', '2021年录取最低名次'])

    for data_file in data_dir:
        data_formatted = data_format(data_file, college_code_reversed)
        for collage_sn, data in data_formatted.items():
            print(data)
            for major_group in data['majorGroups']:
                for major_code, major_data in data['majorGroups'][major_group]['majors'].items():
                    row = [
                        data['SN'],
                        data['college'],
                        major_group,
                        data['majorGroups'][major_group]['info']['类型'],
                        data['majorGroups'][major_group]['info']['批次'],
                        data['majorGroups'][major_group]['info']['首选科目'],
                        data['majorGroups'][major_group]['info']['再选科目'],
                        major_data['majorSN'],
                        major_data['name'],
                        major_data['data']['2022'][0] if "2022" in major_data['data'] else "",
                        major_data['data']['2022'][1] if "2022" in major_data['data'] else "",
                        major_data['data']['2022'][2] if "2022" in major_data['data'] else "",
                        major_data['data']['2022'][3] if "2022" in major_data['data'] else "",
                        major_data['data']['2021'][0] if "2021" in major_data['data'] else "",
                        major_data['data']['2021'][1] if "2021" in major_data['data'] else "",
                        major_data['data']['2021'][2] if "2021" in major_data['data'] else "",
                        major_data['data']['2021'][3] if "2021" in major_data['data'] else ""
                    ]
                    writer.writerow(row)
        
    fout.close()