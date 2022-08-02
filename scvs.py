#!/usr/bin/env python

''' SCVS document parser and converter class.

    Based upon code written for MASVS By Bernhard Mueller and later adopted for ASVS

    Copyright (c) 2017 OWASP Foundation

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    '''

import os
import re
import json
from xml.sax.saxutils import escape
import csv

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class SCVS:
    ''' Creates requirements list out of markdown files. '''
    requirements = []

    def __init__(self):
        for file in sorted(os.listdir("en")):

            if re.match("0x\d{2}-V", file):
                for line in open(os.path.join("en", file)):
                    regex = re.compile('\*\*([\d\.]+)\*\*\s\|\s{0,1}(.*?)\s{0,1}\|([\w\d,\. \u2713]*)\|([\w\d,\. \u2713]*)\|([\w\d,\. \u2713]*)\|')
                    if m := re.search(regex, line):
                        req = {'id': m[1], 'text': m[2], 'l1': bool(m[3].strip())}
                        req['l2'] = bool(m[4].strip())
                        req['l3'] = bool(m[5].strip())
                        req['file'] = file

                        self.requirements.append(req)

    def to_json(self):
        ''' Returns a JSON-formatted string '''
        return json.dumps(self.requirements)

    def to_xml(self):
        ''' Returns XML '''
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + "<scvs>\n"
        for r in self.requirements:

            xml += "\t<requirement id=\"" + escape(r['id']) \
                       + "\" l1=\"" + str(r['l1']).lower() \
                       + "\" l2=\"" + str(r['l2']).lower() \
                       + "\" l3=\"" + str(r['l3']).lower() + "\">" \
                       + escape(r['text']) + "</requirement>\n"

        xml += "</scvs>\n"
        return xml

    def to_csv(self):
        ''' Returns CSV '''
        si = StringIO()

        writer = csv.DictWriter(si, ['id', 'text', 'l1', 'l2', 'l3', 'file'])
        writer.writeheader()
        writer.writerows(self.requirements)

        return si.getvalue()
