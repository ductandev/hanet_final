import time
from csv import reader, DictWriter
from json import dumps, loads, dump
from datetime import datetime

from requests import ConnectionError, HTTPError
from requests import get, post
from datetime import datetime
import requests

import threading

url = 'https://api-vietthang.systemkul.com/v1/'

def call_json():
    url = 'https://api-vietthang.systemkul.com/v1/'
    r = get(url + 'NhanVien/Kiosk', headers={'Content-Type': 'application/json',})
    data1 = loads(r.text)['data']
    with open('data/data5.json', 'w') as f:
        dump(data1, f)  

    ulr_getway = 'https://gateway.systemkul.com/api/VietThang/getListByPlace6900'

    r_getway = get(ulr_getway, headers={'Content-Type': 'application/json',})
    data_getway = loads(r_getway.text)
    with open('data/data3.json', 'w') as f_getway:
        dump(data_getway, f_getway) 
 

def save_statu_bug(dateTime, statueerr,data_request_new_text, erroText):
    with open ("data/hisory_bakup.csv", mode = "+a") as re_csv_file1:
        fieldnames = ['date','statu', 'data_request_new' , 'erroText']
        writer = DictWriter(re_csv_file1, fieldnames=fieldnames)
        writer.writerow({'date':dateTime,'statu': statueerr, 'data_request_new': str(data_request_new_text), 'erroText': erroText}) 
        re_csv_file1.close()

def post_data():
    with open('data/recognization.csv', 'r') as read_obj:
        csv_reader = reader(x.replace('\0', '') for x in read_obj)
        try:
            statu_network = 0
            for row in csv_reader:
                try:
                    name_student_recognite = row[0]
                    date = datetime.strptime(str(row[1]).split("+")[0], '%Y-%m-%d %H:%M:%S')
                    data = datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.%f')
                    idptChamCong = 2
                    tempt_student = row[2]
                    uuid_device = "a0643a31-de9e-3f86-87a9-a713e8b6fc6b" 
                    data_request_new = {"employeeCode": name_student_recognite, "time": str(date), "temperature": tempt_student, "deviceId": uuid_device}
                    r = post("https://api-vietthang.titkulhr.com/api/Attendances/AttendanceByDevice", timeout=10, data=dumps(data_request_new), headers={'Content-Type': 'application/json', })
                    print(r.status_code)
                    xstaute = r.status_code
                    try:
                        r.raise_for_status()
                    except requests.exceptions.HTTPError as errh:
                        print ("Http Error:",errh.response.text)
                        infor_s_Error = threading.Thread(target=save_statu_bug, args=(data, xstaute, data_request_new, errh.response.text, ))
                        infor_s_Error.start() 
                    except requests.exceptions.ConnectionError as errc:
                        print ("Error Connecting:",errc)
                        infor_s_ConnectionError = threading.Thread(target=save_statu_bug, args=(data, xstaute, data_request_new, errc, ))
                        infor_s_ConnectionError.start() 
                    except requests.exceptions.Timeout as errt:
                        print ("Timeout Error:",errt)
                        infor_s_Timeout = threading.Thread(target=save_statu_bug, args=(data, xstaute, data_request_new, errt, ))
                        infor_s_Timeout.start() 
                    except requests.exceptions.RequestException as err:
                        print ("OOps: Something Else",err)
                        infor_s_RequestException = threading.Thread(target=save_statu_bug, args=(data, xstaute, data_request_new, err, ))
                        infor_s_RequestException.start() 
                except ConnectionError:
                    print("No internet connection available.")
                    infor_s_ConnectionError = threading.Thread(target=save_statu_bug, args=(data,"No_internet",data_request_new, "No internet connection available", ))
                    infor_s_ConnectionError.start() 
                    statu_network = 1
                    return 1
                except Exception as e:
                    print("error 1 ",e)
                    pass 
            if  statu_network == 0:   
                with open ("data/recognization.csv", mode = "w") as re_csv_file:
                    fieldnames = ['ID', 'Date', 'Temperature']
                    writer = DictWriter(re_csv_file, fieldnames=fieldnames)
        except Exception as e :
            print("error 2 ",e)

if __name__ == "__main__":
    timeconut = 21600
    start = datetime.now()
    input_csv = "data/recognization.csv"
    output_json = "data/recognization.json"
    try:
        call_json()
        time.sleep(10)
    except Exception as e:
        print("hello2 ",e)
    while True:
        value_net = post_data()
        time.sleep(5)
        if value_net == 1:
            while True:
                try:
                    if get('https://google.com').ok:
                        print("You're Online")
                        infor_s_Connections = threading.Thread(target=save_statu_bug, args=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),"Connet_internet", "okie connect", "Connet internet {}".format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')), ))
                        infor_s_Connections.start() 
                        break
                except Exception as e:
                    print(e)
                    pass
        try:    
            now = datetime.now()
            if (now - start).total_seconds() > timeconut:
                call_json()
                start = now
        except Exception as e:
            print(e)
            pass
