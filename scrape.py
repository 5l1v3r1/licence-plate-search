from mechanize import Browser
from bs4 import BeautifulSoup
from flask import Flask, url_for
from flask import jsonify
import json
import http.cookiejar as cookielib
import mechanize
import requests
import base64
app = Flask(__name__)


@app.errorhandler(500)
def not_found(error=None):
    message = {
        'status': 500,
        'message': 'Internal error please try again'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp





@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/num/<registrationnum>')
def api_article(registrationnum):
    url = "http://mis.mptransport.org/MPLogin/eSewa/VehicleSearch.aspx"
    br = mechanize.Browser()
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # br.set_handle_robots(False)
    br.open(url)
    br.select_form(name='aspnetForm')
    br["ctl00$ContentPlaceHolder1$txtRegNo"] = (registrationnum)
    res = br.submit()
    content = res.read()
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(
        "table", {"border": "1", "id": "ctl00_ContentPlaceHolder1_grvSearchSummary"})
    for row in table.findAll('tr', {'class': 'GridItem'}):
        col = row.findAll('td')
        a = col[2].find('a').string
        b = col[14].string
        c = col[5].string
        d = col[6].string
        e = col[8].string
        data = {
            'registration_num': a,
            'model': b,
            'owner_name': c,
            'rto_name': d,
            'regis_date': e
        }
        # response = jsonify(data)
        # print(data
        print(json.dumps(data, indent=1))

    # if registrationnum in pnr:
     #    	return response
    # else:
     #    	return error_404()

# if __name__ == '__main__':
#     app.run()
# # api_article("MP04A2300")


IMAGE_PATH = #add image path
SECRET_KEY = #add API key
with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ind&secret_key=%s' % (
    SECRET_KEY)
r = requests.post(url, data=img_base64)

r = r.json()
y = r["results"][0]["plate"]
# print(y)
api_article(y)
