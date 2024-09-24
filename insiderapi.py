import requests
from bs4 import BeautifulSoup

def fetch():
    cookies = {
        'chartsTheme': 'dark',
        '_ga': 'GA1.1.1622034105.1726512964',
        'usprivacy': '1---',
        'notice-newsletter': 'show',
        'insiderTradingUrl': 'tc%3D1',
        'pv_date': 'Wed Sep 18 2024 13:03:21 GMT-0500 (Central Daylight Time)',
        'ic_tagmanager': 'AY',
        '_lr_geo_location_state': 'NC',
        '_lr_geo_location': 'US',
        'pv_count': '2',
        '_ga_ZT9VQEWD4N': 'GS1.1.1726682601.2.1.1726682607.0.0.0',
        'IC_ViewCounter_finviz.com': '2',
        '_awl': '2.1726682608.5-4a0131738dc39a04958e692b157246d1-6763652d75732d6561737431-0',
        'cto_bundle': 'rr7wNF9NWSUyRmpKeXhGRmJYRkRZRDcwVTFuVUtGZDJQcnpRTyUyQm1lemtzNVFweThJemtZVVNnd3liWkglMkI3SjZGY0dLSzJWUDlkRFZ4TkpMNmpMOXcyS001UzVCN0NCU1hUOEJpbWhMeE9HR0lyT0V1S2QwckVkV2lMUVFsaUNJcGE2SldYbw',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,en-GB;q=0.8,es-MX;q=0.7,es;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'chartsTheme=dark; _ga=GA1.1.1622034105.1726512964; usprivacy=1---; notice-newsletter=show; insiderTradingUrl=tc%3D1; pv_date=Wed Sep 18 2024 13:03:21 GMT-0500 (Central Daylight Time); ic_tagmanager=AY; _lr_geo_location_state=NC; _lr_geo_location=US; pv_count=2; _ga_ZT9VQEWD4N=GS1.1.1726682601.2.1.1726682607.0.0.0; IC_ViewCounter_finviz.com=2; _awl=2.1726682608.5-4a0131738dc39a04958e692b157246d1-6763652d75732d6561737431-0; cto_bundle=rr7wNF9NWSUyRmpKeXhGRmJYRkRZRDcwVTFuVUtGZDJQcnpRTyUyQm1lemtzNVFweThJemtZVVNnd3liWkglMkI3SjZGY0dLSzJWUDlkRFZ4TkpMNmpMOXcyS001UzVCN0NCU1hUOEJpbWhMeE9HR0lyT0V1S2QwckVkV2lMUVFsaUNJcGE2SldYbw',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    }

    params = {
        'tc': '1',
    }

    response = requests.get('https://finviz.com/insidertrading.ashx', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all("table")[6]
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 8:
            ticker = cols[0].text
            owner = cols[1].text
            relationship = cols[2].text
            date = cols[3].text
            transaction = cols[4].text
            cost = cols[5].text
            shares = cols[6].text
            value = cols[7].text
            secform = cols[9].text
            data.append({"ticker": ticker, "owner": owner, "relationship": relationship, "date": date, "transaction": transaction, "cost": cost, "shares": shares, "value": value, "secform": secform})
    return data