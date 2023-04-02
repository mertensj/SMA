import json
#from numpy import False_
import requests
import datetime

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

DEBUG = False

class SMA:
  ##url = 'https://SMA_IP_ADDRESS'
  url = 'https://XX.XX.XX.XX'
  keys = {'productivity_total': '6400_00260100', 
          'productivity_day'  : '6400_00262200',
          'ip'                : '6180_104A9A00',
          'model'             : '6800_10821E00',
          'serialNbr'         : '6800_00A21E00'
         }
  ##json_login = {'right': 'usr', 'pass': 'XXXXSecretXXXX'} 
  json_login = {'right': 'usr', 'pass': '____________'} 
  ssid = None

  def __init__(self):
    pass

  def login(self):
    if DEBUG: print('[+] login')
    response = requests.post(self.url + '/dyn/login.json', json=self.json_login, verify=False)
    json_data = json.loads(response.text)
    if DEBUG: print(json_data)
    if 'err' in json_data:
      return False
    else:
      self.ssid = json_data['result']['sid']
      return True

  def checkSession(self):
    if DEBUG: print('[+] check session')
    if self.ssid == None:
        if DEBUG: print('[-] No ssid found. Please login first.')
        return(False)
    response = requests.post(self.url + '/dyn/sessionCheck.json?sid=' + self.ssid, json={}, verify=False)
    json_data = json.loads(response.text)
    if DEBUG: print(json_data)
    if 'result' not in json_data:
        return False
    if 'cntDwnGg' not in json_data['result']:
        return False
    return True

  def logout(self):
    if DEBUG: print('[+] logout')
    response = requests.post(self.url + '/dyn/logout.json?sid=' + self.ssid, json={}, verify=False)
    json_data = json.loads(response.text)
    if DEBUG: print(json_data)
    if 'err' in json_data:
        return False
    else:
        self.ssid = None
        return True


  def value(self, key):
    params = {
            'destDev': [],
            'keys': [ self.keys[key] ]
            }

    if self.checkSession() == False:
        self.login()
        if self.checkSession() == False:
            if DEBUG: print('[-] Error login to the device. Check authorization.')
            exit()

    response = requests.post(self.url + '/dyn/getValues.json?sid=' + self.ssid, json=params, verify=False)
    json_data = json.loads(response.text)
    if DEBUG: print(json_data)
    data = json_data['result']
    first_key = list(data.keys())[0]
    dataList = data[first_key]
    value = dataList[self.keys[key]]['1'][0]['val']
    #print(key , ' : ', value )
    return(value)

  def id(self):
    self.value('model')
    self.value('serialNbr')
    self.value('ip')
    
  def getLogger(self, dump='screen'):
    if self.checkSession() == False:
      self.login()
      if self.checkSession() == False:
        if DEBUG:
          print('[-] Error login to the device. Check authorization.')
          exit()
    time = datetime.datetime.utcnow()
    today = time.date()
    d_start = datetime.datetime(today.year,today.month,today.day,3,55)
    d_end = datetime.datetime(today.year,today.month,today.day,22,0)
    if dump == 'txt':
      f = open(str(today)+'.txt', "w")
    params = {
           'destDev': [],
           'key': 28672,
           'tStart': d_start.timestamp(),
           'tEnd': d_end.timestamp()
            }
    response = requests.post(self.url + '/dyn/getLogger.json?sid=' + self.ssid, json=params, verify=False)
    json_data = json.loads(response.text)
    if DEBUG: print(json_data)
    data = json_data['result']
    first_key = list(data.keys())[0]
    dataList = data[first_key]
    power=0
    total_power=0
    mysteryConstant = 12; # To convert inverter power data to W
    #print(dataList)
    for dic in dataList:
        #print(dic)
        ts=dic['t']    # timestamp from SMA in seconds (not nano sec!!)
        dt = datetime.datetime.fromtimestamp(ts)
        old_power = power
        power = int(dic['v'])
        #print(dt , "---->" , dic['v'])
        if isinstance(power,int) and old_power != 0:
            delta = power - old_power
            if delta > 0:
                delta = delta * mysteryConstant # convert to Watt
                if dump == 'screen':
                  print(dt , "---->" , delta)
                if dump == 'txt':
                  f.write(str(ts)+';'+str(delta)+'\n')
                total_power = total_power + delta
    Wh = round(total_power / 12)
    print('Total Power      : ', Wh , ' Wh')
    if dump == 'txt':
      f.close

