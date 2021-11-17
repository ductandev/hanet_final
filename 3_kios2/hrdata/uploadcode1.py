import time
from csv import reader, DictWriter, DictReader, QUOTE_NONE
from json import dumps, loads, dump
from datetime import datetime

from requests import ConnectionError, HTTPError
from requests import get, post
from datetime import datetime
import requests

url = 'https://api-vietthang.titkulhr.com/v1/'

def call_json():
    url = 'https://api-vietthang.titkulhr.com/v1/'
    r = get(url + 'NhanVien?isPaged=false', headers={'Content-Type': 'application/json',})
    data1 = loads(r.text)['data']
    with open('data/data5.json', 'w') as f:
        dump(data1, f)  

def post_data():
    with open('data/recognization.csv', 'r') as read_obj:
        try:
            csv_reader = reader(x.replace('\0', '') for x in read_obj)
            for row in csv_reader:
                try:
                    name_student_recognite = row[0]
                    date = datetime.strptime(str(row[1]).split("+")[0], '%Y-%m-%d %H:%M:%S')
                    data = datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.%f')
                    idptChamCong = 2
                    tempt_student = row[2]
                    uuid_device = "2db5af4f-ed76-390e-9b71-e5704b0fd1a8" 
                    data_request_new = {"employeeCode": name_student_recognite, "time": str(date), "temperature": tempt_student, "deviceId": uuid_device}
                    print(data_request_new)
                    try:
                        r = post("https://api-vietthang.titkulhr.com/api/Attendances/AttendanceByDevice", timeout=100, data=dumps(data_request_new), headers={'Content-Type': 'application/json', })
                        print(r.status_code)
                        try:
                            r.raise_for_status()
                        except requests.exceptions.HTTPError as errh:
                            print ("Http Error:",errh.response.text)
                        except requests.exceptions.ConnectionError as errc:
                            print ("Error Connecting:",errc)
                        except requests.exceptions.Timeout as errt:
                            print ("Timeout Error:",errt)
                        except requests.exceptions.RequestException as err:
                            print ("OOps: Something Else",err)
                    except ConnectionError:
                        print("No internet connection available.")
                        return
                except Exception as e:
                    print(e)
            with open ("data/recognization.csv", mode = "w") as re_csv_file:
                fieldnames = ['ID', 'Date', 'Temperature']
                writer = DictWriter(re_csv_file, fieldnames=fieldnames)
        except Exception as e :
            print(e)

if __name__ == "__main__":
    timeconut = 21600
    start = datetime.now()
    try:
        call_json()
        time.sleep(10)
    except Exception as e:
        print(e)
    while True:
        post_data()
        time.sleep(5)
        try:    
            now = datetime.now()
            if (now - start).total_seconds() > timeconut:
                call_json()
                start = now
        except Exception as e:
            print(e)
            pass

