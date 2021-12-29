# Copyright (C) 2012 Candiotti Adrien
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

c = {
    "builtins": {
        "identifier": "read_identifier",
        "num": "read_integer",
        "string": "read_c_string",
        "cchar": "read_c_char",
        "char": "read_a_char",
        "space": "read_ws",
        "end": "read_untilEOF",
        "empty": "read_eof",
        "super": "super",
        "not_ignore": "not_ignore",
        "false": "false",
        "readThisChar": "read_char",
        "readThisText": "read_text",
    },
    "not": {"!": "negation", "~": "complementary"},
    "multiplier": {"?": "zero_or_one", "+": "one_or_n", "*": "zero_or_n", "[]": "expression"},
    "keyword": {"and": "&&", "object": ""},
    "access_operator": "",
    "alt": "alt",
    "baseParserMethod": "",
    "upPrimitives": "False",
    "indent": 6,
    "file_extension": ".c",
}

from imp import load_source


def cPostGeneration(sModuleName, sFile, sToFile, sGrammar, oInstance):
    print("c file generation over")
    # FIXME : add compilation of example
    # generate a main function and call start rule in it
    # compile with gcc -I lib/lang/c/includes -L lib/lang/clib
    exit(0)
