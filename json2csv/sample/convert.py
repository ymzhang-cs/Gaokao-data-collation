import json

def convert_unicode_to_text(obj):
    """递归地将Unicode码点转换为对应的字符"""
    if isinstance(obj, str):
        return obj.encode('utf-8').decode('unicode_escape')
    elif isinstance(obj, dict):
        return {convert_unicode_to_text(key): convert_unicode_to_text(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_unicode_to_text(element) for element in obj]
    else:
        return obj

# 读取JSON文件，并将Unicode码点转换为对应的字符
with open('json2csv\\sample\\sample.json', 'r') as jsonfile:
    original_data = json.load(jsonfile)

converted_data = convert_unicode_to_text(original_data)

# 将转换后的Python对象写入到新的JSON文件中
with open('json2csv\\sample\\converted.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(converted_data, jsonfile, ensure_ascii=False, indent=4)