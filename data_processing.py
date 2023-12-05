import os
import zipfile
import json

directory = '/Users/mingyeongseo/Desktop/대학/kpaas공모전/test_mountrack/'
extracted_data = []

for filename in os.listdir(directory):
    # print(filename)
    if filename.endswith('.zip') and 'geojson' in filename:
        zip_path = os.path.join(directory, filename)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_path = directory
            zip_ref.extractall(extract_path)

            for extracted_file in zip_ref.namelist():
                if 'PMNTN_' in extracted_file and 'PMNTN_S' not in extracted_file:
                    file_path = os.path.join(directory, extracted_file)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        print(f"파일 '{extracted_file}' 파싱 완료")
                        keys = ["MNTN_NM", "PMNTN_NM", "PMNTN_LT", "PMNTN_DFFL", "PMNTN_UPPL", "PMNTN_GODN",
                                "PMNTN_RISK"]
                        for feature in data.get("features", []):
                            attributes = feature.get("attributes", {})
                            extracted_feature = {key: attributes.get(key) for key in keys}
                            extracted_feature["geometry"] = feature.get("geometry")
                            extracted_data.append(extracted_feature)



print('모든 "geojson" 파일에 대한 압축 해제 완료')

with open("extracted_data.json", "w", encoding="utf-8") as file:
    json.dump(extracted_data, file, ensure_ascii=False, indent=4)

print("파일 저장 완료: extracted_data.json")