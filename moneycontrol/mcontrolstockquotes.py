from bs4 import BeautifulSoup
import requests
from moneycontrol import ratios
import collections
import json


def get_nested_doms(dom, dom_element,attr=False, attribute_name=None):
    doms=[]
    for x in dom :
        if attr and attribute_name is not None:
            doms.append(str(x.attrs[attribute_name]))
        else:
            doms.extend(x.find_all(dom_element))
    return doms


def get_all_stocks_url(url, attrs, dom_element, attributes=None):
    markup = requests.get(url=url).text
    soup = BeautifulSoup(markup, "lxml")
    dom = soup.find_all(dom_element[0] , attrs=attrs)
    for i in range(1, len(dom_element)):
        dom = get_nested_doms(dom, dom_element[i])
    if attributes is not None and len(attributes)>0:
        for i in range(0, len(attributes)):
            dom = get_nested_doms(dom,dom_element=None,attr=True, attribute_name=attributes[i])
    return dom


def get_stock_symbols_frm_m_cntrl_url(m_cntrl_url):
    markup = requests.get(url=m_cntrl_url).text
    soup = BeautifulSoup(markup, "lxml")
    """Get the BSE and NSE symbols for now"""
    bse_nse_code = soup.find_all(
        "div",
        attrs={"class":"FL gry10"}
    )
    if len(bse_nse_code) > 0:
        __t = bse_nse_code[0]
        bse_code = __t.contents[0]
        nse_code = __t.contents[2]
        return bse_code, nse_code


def get_stock_financials(m_cntrl_url):
    print "Hitting URL : "+m_cntrl_url
    session = requests.Session()
    session.max_redirects = 60
    markup = session.get(url=m_cntrl_url).text
    soup = BeautifulSoup(markup, "lxml")
    details = soup.find_all(
        "div",
        attrs={"class":"boxBg1"}
    )
    table_soup = details[0].find_all(
        "table",
        attrs={"class" : "table4"}
    )
    table_data = table_soup[1].find_all(
        "tr",
        attrs={"height":"22px"}
    )
    columns = table_data[0].find_all(
        "td",
        attrs={"class": "detb"}
    )
    __columns = []
    __i=0
    for c in columns:
        if __i < len(columns):
            __columns.append(c.text)
            __i+=1
    __ratio_type = None
    for t in table_data:
        ratio_type = t.find_all(
            "td",
            attrs={"class":"detb","colspan":"2","width":"40%"}
        )
        if len(ratio_type) > 0 and ratio_type[0].text is not None:
            __ratio_type = ratio_type[0].text

        keys = t.find_all(
            "td",
            attrs={"class" : "det"}
        )
        if len(keys) == 0:
            continue
        ratios[str(__ratio_type)][str(keys[0].text)] = {}
        j=1
        for i in range(1, len(keys)):
            if j < len(__columns):
                ratios[str(__ratio_type)][str(keys[0].text)][str(__columns[j])] = str(keys[i].text)
                j+=1
    return ratios

if __name__ == '__main__':
    urls = []
    for alphabet in range(ord('A'), ord('Z') + 1):
        __urls = get_all_stocks_url("http://www.moneycontrol.com/india/stockpricequote/"+chr(alphabet),
                                 {"class": "pcq_tbl MT10"},
                                 dom_element = ['table','td','a'], attributes=['href'])
        urls.extend(__urls)
    for u in urls:
        print (get_stock_symbols_frm_m_cntrl_url(u))
        array = u.split("/")
        print get_stock_financials("http://www.moneycontrol.com/financials"+"/"+array[-2]+"/ratiosVI/"+array[-1]+"#"+array[-1])