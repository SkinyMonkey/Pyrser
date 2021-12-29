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


class CodeGenerationHelper(object):
    """
    The code generation helper class.
    """

    def __init__(self, d_conf):
        self.__n_depth = 1
        self.__l_count = [self.Count(0, 0)]
        self.__l_alt = [False]
        self.__l_alt_count = [self.Count(0, 0)]
        self.__d_globals = {}
        self.__d_conf = d_conf

    class Count(object):
        def __init__(self, n_count, n_length):
            self.n_count = n_count
            self.n_length = n_length

    def builtin(self, s_name):
        return self.__d_conf["builtins"][s_name]

    def keyword(self, s_name):
        return self.__d_conf["keyword"][s_name]

    def multiplier(self, s_name):
        return self.__d_conf["multiplier"][s_name]

    def not_(self, s_name):
        return self.__d_conf["not"][s_name]

    def access_operator(self):
        return self.__d_conf["access_operator"]

    def alt(self):
        return self.__d_conf["alt"]

    def base_parser_access(self):
        return self.__d_conf["baseParserMethod"] + self.__d_conf["access_operator"]

    def base_parser(self):
        return (
            self.__d_conf["keyword"]["object"]
            + self.__d_conf["access_operator"]
            + self.__d_conf["baseParserMethod"]
        )

    def access_instance(self):
        return self.__d_conf["keyword"]["object"] + self.__d_conf["access_operator"]

    def up_primitives(self):
        return self.__d_conf["upPrimitives"]

    def capitalize(self, s_string):
        return "%s%s" % (s_string[0].capitalize(), s_string[1:])

    def push_count(self, n_count, n_length):
        self.__l_count.append(self.Count(n_count, n_length))
        return ""

    def pop_count(self):
        self.__l_count.pop()
        return ""

    def inc_count(self):
        self.__l_count[-1].n_count += 1
        return ""

    def inc_depth(self):
        self.__n_depth += 1
        return ""

    def dec_depth(self):
        self.__n_depth -= 1
        return ""

    def push_alt(self, b_alt, n_alt_length=0):
        self.__l_alt.append(b_alt)
        self.__l_alt_count.append(self.Count(0, n_alt_length))
        return ""

    def pop_alt(self):
        self.__l_alt.pop()
        self.__l_alt_count.pop()
        return ""

    def alt_count(self):
        return self.__l_alt_count[-1].n_count

    def alt_length(self):
        return self.__l_alt_count[-1].n_length

    def inc_alt_count(self):
        self.__l_alt_count[-1].n_count += 1
        return ""

    def count(self):
        return self.__l_count[-1].n_count

    def length(self):
        return self.__l_count[-1].n_length

    def in_alt(self):
        return self.__l_alt[-1] == True

    def in_depth(self):
        return self.__n_depth > 1

    def in_recurse(self):
        return self.in_depth() or self.in_alt()

    def getattr(self, o_object, s_name):
        return o_object._TemplateReference__context[s_name]

    def indent(self):
        return " " * self.__d_conf["indent"] * self.__n_depth

    def set_global(self, s_name, o_value):
        self.__d_globals[s_name] = o_value
        return ""

    def get_global(self, s_name):
        return self.__d_globals[s_name]
