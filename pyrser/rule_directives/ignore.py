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

from parsing import Parsing

d_ws_list = {"base": " \t\r\n"}


def add_ws_list(s_name, s_ws_list):
    d_ws_list[s_name] = s_ws_list


class Ignore(object):
    """
    A decorator that specify the wsList
    """

    def __init__(self, s_ws_list):
        if s_ws_list.upper() in d_ws_list:
            self.__s_ws_list = d_ws_list[s_ws_list.upper()]
        else:
            self.__s_ws_list = s_ws_list

    def __call__(self, o_rule):
        def wrapper(*l_args):
            s_old_ws_list = Parsing.o_base_parser.getWsList()
            Parsing.o_base_parser.setWsList(self.__s_ws_list)
            b_res = o_rule(*l_args)
            Parsing.o_base_parser.setWsList(s_old_ws_list)
            return b_res

        return wrapper
