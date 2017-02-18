# This file is part of MacroJudge.
#
# MacroJudge is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MacroJudge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from xml.etree import ElementTree

STANDARD_ERROR_TEXT = "ERROR"
STANDARD_ERROR_EXIT_CODE = "1"

difficulty_level = {
    "EASY" : 0,
    "NORMAL" : 1,
    "HARD" : 2,
}

def format_html_style(text):
    return "".join(filter(lambda x : x != " ", map(lambda x : x.strip() + " ", text.split('\n')))).rstrip(" ")

def format_preserve_left_spaces(text):
    count = 0;
    for c in text:
        if c == " ":
            count += 1
        else:
            break
    return " " * count + format_html_style(text)

def parse_paragraph(element, indent = False, para_sep = False):
    p = ""
    for paragraph in list(element):
        if indent:
            p += "  "
        p += format_html_style(paragraph.text) + '\n'
        if para_sep:
            p += '\n'
    return p.rstrip('\n')

def parse(xml):
    dom = ElementTree.parse(xml)
    p = Problem.parse(dom.getroot())
    return p


class Test:
    def __init__(self):
        self.stdin = None
        self.stdout = None
        self.return_code = 0

    @staticmethod
    def parsetest(elem, check_whitespace):
        self = Test()
        if check_whitespace:
            parse_function = format_html_style
        else:
            parse_function = format_preserve_left_spaces
        intag = elem.find("in")
        outtag = elem.find("out")
        rctag = elem.find("return-code")
        intext = ""
        if intag is None:
            self.stdin = None
        else:
            if len(list(intag)) == 0:
                intext = format_html_style(intag.text)
            else:
                for paragraph in list(intag):
                    intext += format_html_style(paragraph.text) + "\n"
            self.stdin = intext
        if elem.find("error-message") is not None:
            self.stdout = STANDARD_ERROR_TEXT
            self.return_code = STANDARD_ERROR_EXIT_CODE
            return self
        outtext = ""
        if len(list(outtag)) == 0:
            indent = outtag.get("indent")
            if indent is None:
                outtext += parse_function(outtag.text) + '\n'
            else:
                outtext += " " * int(indent) + format_html_style(outtag.text) + '\n'
        else:
            for paragraph in list(outtag):
                indent = paragraph.get("indent")
                if indent is None:
                    outtext += parse_function(paragraph.text) + '\n'
                else:
                    outtext += " " * int(indent) + format_html_style(paragraph.text) + '\n'
        self.stdout = outtext.rstrip("\n")
        if rctag is None:
            self.return_code = 0
        else:
            self.return_code = int(rctag.text)
        return self


class Problem:
    def __init__(self):
        self.title = ""
        self.id = [0, 0, 0]
        self.tags = []
        self.description = ""
        self.example_in = ""
        self.example_out = ""
        self.check_whitespace = False
        self.times = []
        self.tests = []
        self.errortests = []

    def parse_times(self, elem):
        self.times = [[0,0,0],[0,0,0],[0,0,0]]
        for group in list(elem):
            dif = difficulty_level[group.get('name')]
            self.times[dif][0] = int(group.find('ctime').text)
            self.times[dif][1] = int(group.find('btime').text)
            self.times[dif][2] = int(group.find('itime').text)
        if self.times[2] == [0,0,0]:
            self.times[2] = [1,1,1]
        if self.times[1] == [0,0,0]:
            self.times[1] = self.times[2]
        if self.times[0] == [0,0,0]:
            self.times[0] = self.times[1]

    def parse_tests(self, elem):
        self.tests = []
        self.errortests = []
        for t in elem:
            if t.tag == 'test':
                self.tests.append(Test.parsetest(t, self.check_whitespace))
            else:
                self.errortests.append(Test.parsetest(t, self.check_whitespace))

    @staticmethod
    def parse(elem):
        result = Problem()
        result.title = elem.find("title").text
        result.id = map(int, elem.find("id").text.split("."))
        result.tags = elem.find("tags").text.split()
        if not elem.find("time-easytask") is None:
            result.times = [[1,1,1],[1,1,1],[1,1,1]]
        elif elem.find('time-default') is not None:
            result.times = [[5,7,9],[2,3,5],[1,1,1]]
        else:
            result.parse_times(elem.find('time'))
        result.description = parse_paragraph(elem.find("description"), para_sep=True)
        result.example_in = parse_paragraph(elem.find("example-in"))
        result.example_out = parse_paragraph(elem.find("example-out"))
        result.check_whitespace = not elem.find("spacing-critical") is None
        result.parse_tests(elem.find("tests"))
        return result