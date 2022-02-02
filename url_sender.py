import urllib.request
#to be saved
import urllib.parse
def send_thanks(num):
    url = f'sendsms?uname=akash12&pwd=akash12&senderid=GAGRWL&to={num}&msg=Thanks%20for%20shopping%20with%20us,%20Akash%20Jewellers,%20Gondia.GAGRWL&route=T&peid=1701160940418217001&tempid=1707163230443114798'
    urllib.request.urlopen('http://site.bulksmsnagpur.net/'+url)