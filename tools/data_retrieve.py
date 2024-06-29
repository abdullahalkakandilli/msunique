import json


companies = ['ABB', 'IBM', 'PostFinance', 'Raiffeisen', 'Siemens', 'UBS']
years = ['2021', '2022', '2023']
for comp in companies:
    for year in years:
        f = open(f'./Data/{comp}/{year}.json', 'r')
        data = json.load(f)
        content = data["analyzeResult"]["content"]

        with open(f'./Data/{comp}/{comp}_{year}_annual_report.txt', 'w+') as f:
            f.write(content)
        