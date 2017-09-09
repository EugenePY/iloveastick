import re
from collections import OrderedDict


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_res_by_res_name(name, res_type):
    pass



