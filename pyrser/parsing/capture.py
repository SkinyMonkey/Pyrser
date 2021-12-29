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

from pyrser.parsing import Parsing


def capture(o_predicat, s_name, d_dict, b_consume_ws=True):
    """
    Capture the bytes consumed by a predicat.
    """
    if b_consume_ws:
        Parsing.o_base_parser.read_ignored()
    Parsing.o_base_parser.set_tag(s_name)
    b_res = o_predicat()
    if b_res:
        if (s_name in d_dict) == False or not isinstance(d_dict[s_name], type({})):
            d_dict[s_name] = Parsing.o_base_parser.get_tag(s_name)
    return b_res


class Capture(object):
    """
    Capture function functor.
    """

    def __init__(self, o_predicat, s_name, d_dict, b_consume_ws=True):
        self.__o_predicat = o_predicat
        self.__s_name = s_name
        self.__d_dict = d_dict
        self.__b_consume_ws = b_consume_ws

    def __call__(self):
        return capture(self.__o_predicat, self.__s_name, self.__d_dict, self.__b_consume_ws)
