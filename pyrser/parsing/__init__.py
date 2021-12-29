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

from pyrser.parsing.python.AsciiParseWrapper import AsciiParseWrapper


class Parsing(object):
    o_parser_class = AsciiParseWrapper
    o_base_parser = o_parser_class("")


#      oFinalParser = o_base_parser


def get_parser_class():
    return Parsing.o_parser_class


def set_base_parser(o_base_parser):
    Parsing.o_base_parser = o_base_parser


def reset_base_parser(
    s_stream="", s_ignore=" \r\n\t", s_c_line="//", s_c_begin="/*", s_c_end="*/"
):
    set_base_parser(get_parser_class()(s_stream, s_ignore, s_c_line, s_c_begin, s_c_end))
