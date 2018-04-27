import fractions
import re
import hashlib
import json
from difflib import SequenceMatcher


def similar(a, b):
    # calculate similarity between words based on character
    return SequenceMatcher(None, a, b).ratio()

def category():

    '''
    for search_dic = {
                        category {
                            subcategory

                            or

                            subcategory | subsection
                        }
                    }

    for category_id = {
                        category: id   or
                        category|subcategory: id    or
                        category|subcategory|subsection : id
                    }

    :return:
    '''
    search_dic = {}
    category_id = {}
    with open('categories.json') as file:
        data = json.load(file)
        for line in data:
            sub_categories = data[line]['subCategory']
            category_id[line]=data[line]['categoryId']
            search_dic.setdefault(line, [])
            for sub_cate in sub_categories:
                if isinstance(data[line]['subCategory'][sub_cate], dict):
                    for sub_sec in data[line]['subCategory'][sub_cate]['subSection']:
                        category_id[line + '|' + sub_cate + '|' + sub_sec] = data[line]['subCategory'][sub_cate]['subSection'][sub_sec]
                        search_dic[line].append(sub_cate + '|' + sub_sec)

                    category_id[line + '|' + sub_cate] = data[line]['subCategory'][sub_cate]['subCategoryId']
                else:
                    category_id[line + '|' + sub_cate] = data[line]['subCategory'][sub_cate]
                    search_dic[line].append(sub_cate)

    return search_dic, category_id


def getSubcategory(candidates, search_dic, category_name):
    candidates = [e.lower() for e in candidates]
    candidates = list(set(candidates))

    # pre-process the candidates
    if 'and' in candidates:
        candidates.remove('and')
    if 'home' in candidates:
        candidates.remove('home')
    if '' in candidates:
        candidates.remove('')


    for name in candidates:
        for sub_cate in search_dic[category_name]:
            if name == sub_cate:
                return name

        for sub_cate in search_dic[category_name]:
            if name in sub_cate or similar(name, sub_cate) > 0.5:
                return sub_cate

    return "others"

# def getSubId()
import requests
def get_proxy():
    proxy = requests.get("http://127.0.0.1:5010/get/").content

    host = proxy.split(':')[0]
    port = proxy.split(':')[1]

    return host, port



# use pyQt5 to render webpage
def render(source_url):
    """Fully render HTML, JavaScript and all."""

    import sys
    from PyQt5.QtCore import QEventLoop
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QEventLoop, QUrl

    class Render(QWebEngineView):
        def __init__(self, url):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            # self.show()
            self.load(QUrl(url))
            self.loadFinished.connect(self._loadFinished)
            # self.setHtml(html)

            # self.show()
            # self.app.exec_()
            while self.html is None:
                self.app.processEvents(
                    QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(source_url).html


# dummy_url = 'https://www.crateandbarrel.com/dryden-leather-3-seat-sofa-with-nailheads/s526252'
# print(render(dummy_url))



def dimension_helper(tmp_dim):
    width = 0
    depth = 0
    height = 0
    if re.search(r"[d|D]epth\s*:\s*(\d+(\.\d+)?)", tmp_dim) or re.search(r"[w|W]idth\s*:\s*(\d+(\.\d+)?)", tmp_dim) or re.search(r"[h|H]eight\s*:\s*(\d+(\.\d+)?)", tmp_dim):
        # Depth, Width, Height     Depth,Diameter,   height,diameter, width,diameter
        tmp_D = re.search(r"[d|D]epth\s*:\s*(\d+(\.\d+)?)", tmp_dim)
        if tmp_D is not None:
            depth = tmp_D.group(1)
            tmp_W = re.search(r"[w|W]idth\s*:\s*(\d+(\.\d+)?)", tmp_dim)
            if tmp_W is not None:
                tmp_H = re.search(r"[h|H]eight\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                if tmp_H is not None:
                    width = tmp_W.group(1)
                    height = tmp_H.group(1)
                else:  # depth, width
                    width = tmp_W.group(1)
                    height = depth
                    depth = 0
            else:  # depth, diameter
                tmp_Dia = re.search(r"[d|D]iameter\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                if tmp_Dia is not None:
                    width = tmp_Dia.group(1)
                    height = tmp_Dia.group(1)
        else:  # width, height,     height,diameter, width,diameter
            tmp_W = re.search(r"[w|W]idth\s*:\s*(\d+(\.\d+)?)", tmp_dim)
            if tmp_W is not None:
                width = tmp_W.group(1)
                tmp_H = re.search(r"[h|H]eight\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                if tmp_H is not None:
                    height = tmp_H.group(1)
                else:  # width,diameter
                    tmp_Dia = re.search(r"[d|D]iameter\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                    if tmp_Dia is not None:
                        height = tmp_Dia.group(1)
                        depth = tmp_Dia.group(1)

            else:  # height,diameter    height
                tmp_Dia = re.search(r"[d|D]iameter\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                if tmp_Dia is not None:
                    width = tmp_Dia.group(1)
                    depth = width
                    tmp_H = re.search(r"[h|H]eight\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                    height = tmp_H.group(1)
                else:  # only has height
                    tmp_H = re.search(r"[h|H]eight\s*:\s*(\d+(\.\d+)?)", tmp_dim)
                    height = tmp_H.group(1)
                    width = 0
                    depth = 0

    else:

        # LW, three number, LH,WH, LWH, DWH, DiaH, LWD, DH, LDH, WD
        tmp_D = re.search(r"(\d+(\.\d+)?)\"\s*D", tmp_dim)
        if tmp_D is not None and not ('Dia' in tmp_dim):  # DHW, LWD, WD
            tmp_H = re.search(r"(\d+(\.\d+)?)\"\s*[h|H]", tmp_dim)
            if tmp_H is not None:  # DHW DH
                height = tmp_H.group(1)
                depth = tmp_D.group(1)
                tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                if tmp_W is not None:
                    width = tmp_W.group(1)
                else:  # DH LDH
                    tmp_L = re.search(r"(\d+(\.\d+)?)\"\s*L", tmp_dim)
                    if tmp_L is not None:
                        width = tmp_L.group(1)
                    else:
                        width = tmp_D.group(1)
                        depth = 0

            else:  # LWD, WD
                tmp_L = re.search(r"(\d+(\.\d+)?)\"\s*L", tmp_dim)
                if tmp_L is not None:
                    height = tmp_L.group(1)
                    depth = tmp_D.group(1)
                    tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                    width = tmp_W.group(1)
                else:  # WD
                    tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                    if tmp_W is not None:
                        width = tmp_W.group(1)
                        height = tmp_D.group(1)
                        depth = 0

        else:  # without D
            tmp_H = re.search(r"(\d+(\.\d+)?)\"\s*H", tmp_dim)
            if tmp_H is not None:  # LH,WH,LWH,Dia H
                height = tmp_H.group(1)

                tmp_L = re.search(r"(\d+(\.\d+)?)\"\s*L", tmp_dim)
                if tmp_L is not None:  # LH, LWH
                    width = tmp_L.group(1)
                    tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                    if tmp_W is not None:  # LWH
                        depth = tmp_L.group(1)
                        width = tmp_W.group(1)
                    else:  # LH
                        depth = 0  # should not show depth

                else:  # WH, Dia H
                    tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                    if tmp_W is None:
                        tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*Dia", tmp_dim)
                        if tmp_W is not None:  # diah
                            width = tmp_W.group(1)
                            depth = width
                    else:  # WH
                        width = tmp_W.group(1)
                        depth = 0
            else:  # LW, three numbers
                tmp_W = re.search(r"(\d+(\.\d+)?)\"\s*W", tmp_dim)
                if tmp_W is not None:  # LW
                    width = tmp_W.group(1)
                    tmp_L = re.search(r"(\d+(\.\d+)?)\"\s*L", tmp_dim)
                    if tmp_L is not None:
                        height = tmp_L.group(1)
                    else:
                        height = 0
                    depth = 0

                else:  # three numbers 2.5" x 5.25" x 5.25"     13 3/8"  x  16"
                    list = re.findall(r"(\d+\s*(\.\d+)?(\d/\d)?)\"", tmp_dim)
                    if len(list) > 0 and len(list) % 3 == 0:
                        height = (list[0])[0]
                        width = (list[1])[0]
                        depth = (list[2])[0]
                    elif len(list) > 0 and len(list) % 2 == 0:
                        if (list[0])[0] == (list[1])[0]:
                            height = (list[0])[0]
                            width = (list[1])[0]
                            depth = 0
                        else:
                            width = (list[0])[0]
                            height = (list[1])[0]
                            depth = 0

                    # process the fraction 3/8
                    if width != 0 and '/' in width:
                        whole, frac = width.split(' ')
                        width = float(whole) + fractions.Fraction(frac)
                    if depth != 0 and '/' in depth:
                        whole, frac = width.split(' ')
                        depth = float(whole) + fractions.Fraction(frac)
                    if height != 0 and '/' in height:
                        whole, frac = width.split(' ')
                        height = float(whole) + fractions.Fraction(frac)

    return float(width), float(depth), float(height)


def aws_image_url_helper(imageUrls):
    awsImageUrls = []
    for url in imageUrls:
        # use hash to generate image file name
        hash_url_to_name = hashlib.sha1(url.encode('utf8')).hexdigest()
        awsImageUrls.append(
            "https://s3-us-west-1.amazonaws.com/decormatters-prod/processed-images/" + hash_url_to_name + "_final.png")
    return awsImageUrls

def generate_hash_name(title, image_urls):
    hash_image_urls = []
    idx = 0
    for url in image_urls:
        name = title + idx
        idx += 1
        hash_name = hashlib.sha1(name.encode('utf8')).hexdigest()
        hash_image_urls.append(
            "https://s3-us-west-1.amazonaws.com/decormatters-prod/processed-images/" + hash_name + "_final.png"
        )

    return hash_image_urls


# this helper can used for ikea and yliving
# not for dimension of ikea
def dimension_helper_new(dimension):
    dimension = dimension.replace('\u00be', '')
    dimension = dimension.replace('\u00bc', '')
    dimension = dimension.replace('\u00bd', '')
    length = 0
    diameter = 0
    width = 0
    depth = 0
    height = 0

    if len(dimension) > 0:

        tmp_width = re.search('[w|W]idth\w*:\s*(\d+)(\s*\d+/\d+)?\s*\"', dimension)
        tmp_width_1 = ''
        tmp_width_2 = ''
        if tmp_width is None:
            tmp_width_1 = re.search('Width\w*:\s*(\d+)\s*\'\s*(\d+)\s*\"', dimension)
        if tmp_width_1 is None:
            tmp_width_2 = re.search('(\d+(\.\d+)?)\s*\"\s*W', dimension)

        tmp_diameter = re.search('[d|D]iameter\w*:\s*(\d+)(\s*\d+/\d+)?\s*\"', dimension)
        tmp_diameter_1 = ''
        tmp_diameter_2 = ''
        if tmp_diameter is None:
            tmp_diameter_1 = re.search('[d|D]iameter\w*:\s*(\d+)\s*\'\s*(\d+)\s*\"', dimension)
        if tmp_diameter_1 is None:
            tmp_diameter_2 = re.search('(\d+(\.\d+)?)\s*\"\s*Dia', dimension)

        tmp_height = re.search('[h|H]eight\w*:\s*(\d+)(\s*\d+/\d+)?\s*\"', dimension)
        tmp_height_1 = ''
        tmp_height_2 = ''
        if tmp_height is None:
            tmp_height_1 = re.search('[h|H]eight\w*:\s*(\d+)\s*\'\s*(\d+)\s*\"', dimension)
        if tmp_height_1 is None:
            tmp_height_2 = re.search('(\d+(\.\d+)?)\s*\"\s*H', dimension)

        tmp_length = re.search('[l|L]ength\w*:\s*(\d+)(\s*\d+/\d+)?\s*\"', dimension)
        tmp_length_1 = ''
        tmp_length_2 = ''
        if tmp_length is None:
            tmp_length_1 = re.search('[l|L]ength\w*:\s*(\d+)\s*\'\s*(\d+)\s*\"', dimension)
        if tmp_length_1 is None:
            tmp_length_2 = re.search('(\d+(\.\d+)?)\s*\"\s*L', dimension)

        tmp_depth = re.search('[d|D]epth\w*:\s*(\d+)(\s*\d+/\d+)?\s*\"', dimension)
        tmp_depth_1 = ''
        tmp_depth_2 = ''
        if tmp_depth is None:
            tmp_depth_1 = re.search('[d|D]epth\w*:\s*(\d+)\s*\'\s*(\d+)\s*\"', dimension)
        if tmp_depth_1 is None:
            tmp_depth_2 = re.search('(\d+(\.\d+)?)\s*\"\s*D[^a-z]', dimension)

        if tmp_width is not None:
            whole = tmp_width.group(1)
            frac = tmp_width.group(2)

            if frac is not None:
                width = float(whole) + fractions.Fraction(frac)
            else:
                width = float(whole)
        elif tmp_width_1 is not None:
            feet = tmp_width_1.group(1)  # 7'7"
            inch = tmp_width_1.group(2)
            width = float(feet) * 12 + float(inch)
        elif tmp_width_2 is not None:  # width for yliving
            width = tmp_width_2.group(1)

        if tmp_diameter is not None:
            whole = tmp_diameter.group(1)
            frac = tmp_diameter.group(2)

            if frac is not None:
                diameter = float(whole) + fractions.Fraction(frac)
            else:
                diameter = float(whole)
        elif tmp_diameter_1 is not None:
            feet = tmp_diameter_1.group(1)  # 7'7"
            inch = tmp_diameter_1.group(2)
            diameter = float(feet) * 12 + float(inch)
        elif tmp_diameter_2 is not None:  # diameter for yliving
            diameter = tmp_diameter_2.group(1)

        if tmp_height is not None:
            whole = tmp_height.group(1)
            frac = tmp_height.group(2)

            if frac is not None:
                height = float(whole) + fractions.Fraction(frac)
            else:
                height = float(whole)
        elif tmp_height_1 is not None:
            feet = tmp_height_1.group(1)  # 7'7"
            inch = tmp_height_1.group(2)
            height = float(feet) * 12 + float(inch)
        elif tmp_height_2 is not None:  # height for yliving
            height = tmp_height_2.group(1)

        if tmp_length is not None:
            whole = tmp_length.group(1)
            frac = tmp_length.group(2)

            if frac is not None:
                length = float(whole) + fractions.Fraction(frac)
            else:
                length = float(whole)
        elif tmp_length_1 is not None:
            feet = tmp_length_1.group(1)  # 7'7"
            inch = tmp_length_1.group(2)
            length = float(feet) * 12 + float(inch)
        elif tmp_length_2 is not None:  # length for yliving
            length = tmp_length_2.group(1)

        if tmp_depth is not None:
            whole = tmp_depth.group(1)
            frac = tmp_depth.group(2)

            if frac is not None:
                depth = float(whole) + fractions.Fraction(frac)
            else:
                depth = float(whole)
        elif tmp_depth_1 is not None:
            feet = tmp_depth_1.group(1)  # 7'7"
            inch = tmp_depth_1.group(2)
            depth = float(feet) * 12 + float(inch)
        elif tmp_depth_2 is not None:  # depth for yliving
            depth = tmp_depth_2.group(1)

        # return filter for yliving
        if width > 0 and depth > 0 and height > 0:
            pass
        elif width > 0 and height > 0:
            pass
        elif depth > 0 and height > 0:
            pass
        elif diameter > 0 and height > 0:
            width = diameter
            depth = diameter
        elif diameter > 0 and depth > 0:
            width = diameter
        elif length > 0 and width > 0:
            height = length
        elif length > 0 and height > 0:
            width = length
        elif diameter > 0:
            width = diameter
            depth = diameter
            height = diameter

    return float(width), float(depth), float(height)


def get_width(dim_str):
    tmp_wid = re.search('(\d+([,.]\d+)?)\"\s+long', dim_str)
    if tmp_wid is None:
        tmp_wid = re.search('(\d+([,.]\d+)?)\"\s+wide', dim_str)

    if tmp_wid is not None:
        tmp_wid = tmp_wid.group(1)
    else:
        tmp_wid = 0

    return float(tmp_wid)


def get_depth(dim_str):
    tmp_dep = re.search('(\d+([,.]\d+)?)\"\s+deep', dim_str)
    if tmp_dep is None:
        tmp_dep = re.search('(\d+([,.]\d+)?)\"\s+wide', dim_str)

    if tmp_dep is not None:
        tmp_dep = tmp_dep.group(1)
    else:
        tmp_dep = 0
    return float(tmp_dep)


def get_height(dim_str):
    tmp_hei = re.search('(\d+([,.]\d+)?)\"\s+high', dim_str)

    if tmp_hei is not None:
        tmp_hei = tmp_hei.group(1)
    else:
        tmp_hei = 0
    return float(tmp_hei)


def get_diameter(dim_str):
    tmp_dia = re.search('(\d+([,.]\d+)?)\"\s+diameter', dim_str)

    if tmp_dia is not None:
        tmp_dia = tmp_dia.group(1)
    else:
        tmp_dia = 0

    return float(tmp_dia)


