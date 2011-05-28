#!/usr/bin/env python2

try:
    import web
except ImportError, e:
    import sys
    print >> sys.stderr, "You need to install web.py"
    sys.exit(1)

from itweetas import LabelBuilder, LabelFormat, TwitterUser
from calibration import CalibrationPage


urls = (
    '/', 'index',
    '/calibrate', 'calibrate',
    '/(\d+)/([^/]+)/(-?\d+)/(-?\d+)/?', 'pdf'
    )

class index:
    def GET(self):
        return '''<html>
<head>
<title>Hello, I tweet as...</title>
<link rel="stylesheet" type="text/css" href="static/styles/main.css"></style>
</head>

<body>
<h1>Hello, I Tweet As</h1>
<form>
<div class="step">
<h2 id="calibrate_header">Calibrate</h2>
<div id="calibrate" class="collapse">
<p>We strongly recommend that you calibrate the software using <a href="/calibrate">this PDF</a> before generating name tags. This step minimizes misprinted label sheets.</p>
<p>Your fudge values</p>
1.<input id="fudge_x" value="0"/> 2.<input id="fudge_y" value="0"/>
</div>
</div>
<div class="step">
<h2>Names</h2>
<div id="handles" class="collapse">
<p>Enter your Twitter ID for a single nametag</p>
@<input id="twitter_id"/>
</div>
</div>
<div class="step">
<h2 id="layout_header">Layout</h2>
<div id="layout" class="collapse">
<p>How many labels would you like to skip?</p>
<input id="skip_n_labels" value="0"/><br/>
</div>
</div>
<input type="submit" value="Generate nametags"/>
</form>
</body>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.min.js"></script>
<script type="text/javascript" src="static/js/itweetas.js"></script>
</html>
'''


class calibrate:
    def GET(self):
        calibrationPDF = CalibrationPage()

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="calibration.pdf"')
        return format(calibrationPDF.getPDF())


class pdf:
    def GET(self, offset, users, fudge_x, fudge_y):
        users = users.split(',')

        builder = LabelBuilder(LabelFormat())
        builder.setFudge(int(fudge_x), int(fudge_y))

        for user in users:
            builder.addUser(TwitterUser(user))

        builder.generatePDF(offset=int(offset))

        web.header('Content-Type', 'application/pdf')
        web.header('Content-Disposition', 'attachment; filename="nametags.pdf"')
        return format(builder.getPDF())


app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()