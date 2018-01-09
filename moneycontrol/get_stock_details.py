from moneycontrol import mcontrolstockquotes

money_control_stock_quote_root = "http://www.moneycontrol.com/india/stockpricequote/"
money_control_financial_url = "http://www.moneycontrol.com/financials"


def get_all_quotes():
    urls = []
    for alphabet in range(ord('A'), ord('Z')+1):
        __urls = mcontrolstockquotes.get_all_stocks_url(money_control_stock_quote_root+chr(alphabet))
        urls.extend(__urls)
    return urls


def extract_name_abbrv(str):
    urls = get_all_quotes()
    name_abbrv = {}
    for u in urls:
        array = u.split("/")
        name_abbrv[array[-2]]= array[-1]

def extract_balance_sheet(stocks):
    pass