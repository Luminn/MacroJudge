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
# along with MacroJudge.  If not, see <http://www.gnu.org/licenses/>.

def iswhitespace(s):
    for c in s:
        if not (c == ' ' or c == '\0' or c == '\r' or c == '\n' or c == '\t'):
            return False
    return True

def rtrim(s):
    for c in range(len(s) - 1, 0, -1):
        if not (s[c] == ' ' or s[c] == '\0' or s[c] == '\r' or s[c] == '\n' or s[c] == '\t'):
            return s[:c]
    return 0

# scan based on whitespace, only ignore whitespace characters at the end of line
def formatted_scan(s):
    splits = s.split('\n')
    result = []
    for split in splits:
        if not iswhitespace(split):
            result.append(rtrim(split))
    return result

# scan based on words between whitespace characters
def word_scan(s):
    splits = s.split('\n')
    result = []
    for split in splits:
        if not iswhitespace(split):
            result.append(split.split())
    return result
