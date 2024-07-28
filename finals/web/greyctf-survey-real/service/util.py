import requests
import re
import zipfile
import io
from lxml import etree as ET

parser = ET.XMLParser(load_dtd=True, no_network=False)


def download_xlsx(fid):
    if not re.match(r"^[0-9A-Za-z_]+$", fid):
        return False

    # XLSX file
    url = f'https://drive.google.com/uc?id={fid}'
    content = requests.get(url).content
    if len(content):
        return content
    # Google sheets
    url = f'https://docs.google.com/spreadsheets/d/{fid}/export?format=xlsx'
    return requests.get(url).content

def parse_xlsx(data):
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        ss = zf.open("xl/sharedStrings.xml", "r").read()
        shared_strings_data = ET.fromstring(ss, parser=parser)
        shared_strings = []
        for child in shared_strings_data:
            shared_strings.append(child[0].text)
        out = []
        data = zf.open("xl/worksheets/sheet1.xml", "r").read()
        ns = {"d":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        rows = ET.fromstring(data, parser=parser).findall("d:sheetData/d:row", ns)
        headers = []
        for row in rows:
            row_num = int(row.attrib["r"])
            # Table headers
            if row_num == 1:
                for col in row.findall("d:c", ns):
                    str_index = int(col[0].text)
                    headers.append(shared_strings[str_index])
            else:
                cur = {}
                for i, col in enumerate(row.findall("d:c", ns)):
                    str_index = int(col[0].text)
                    cur[headers[i]] = shared_strings[str_index]
                out.append(cur)
        return out

def get_challenge_author(file_id, challenge_name):
    try:
        data = download_xlsx(file_id)
        if not data:
            return False
        data = parse_xlsx(data)
        for challenge in data:
            if challenge["Name"] == challenge_name:
                return challenge["Author"]
    except:
        return False
