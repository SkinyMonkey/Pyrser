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

def functor(fn):
    def functor_wrapper(*l):
        return fn(*l)
    return functor_wrapper

# TODO : replace all this by a simple wrapper

class ReadText(object):
    """
    Encapsulation of the 'read_text' primitive into a functor.
    """

    __slots__ = {"__name__": "ReadText", "__s_text": None}

    def __init__(self, s_text):
        self.__s_text = s_text

    def __call__(self):
        return Parsing.o_base_parser.read_text(self.__s_text)


class ReadChar(object):
    """
    Encapsulation of the 'read_char' primitive into a functor.
    """

    __slots__ = {"__name__": "ReadChar", "__c_char": None}

    def __init__(self, c_char):
        self.__c_char = c_char

    def __call__(self):
        return Parsing.o_base_parser.read_char(self.__c_char)


class ReadUntil(object):
    """
    Encapsulation of the 'read_until' primitive into a functor.
    """

    __slots__ = {"__name__": "ReadUntil", "__c_char": None}

    def __init__(self, c_char):
        self.__c_char = c_char

    def __call__(self):
        return Parsing.o_base_parser.read_until(self.__c_char)


class ReadRange:
    """
    Encapsulation of the 'readRange' primitive into a functor.
    """

    __slots__ = {"__name__": "ReadRange", "__c_begin": None, "__c_end": None}

    def __init__(self, c_begin, c_end):
        self.__c_begin = c_begin
        self.__c_end = c_end

    def __call__(self):
        return Parsing.o_base_parser.read_range(self.__c_begin, self.__c_end)


class NonTerminal:
    """
    Encapsulate non_terminal rule execution into a functor.
    """

    __slots__ = ("__o_predicat", "__o_node")

    def __init__(self, o_predicat, o_node):
        self.__o_predicat = o_predicat
        self.__o_node = o_node

    def __call__(self):
        return self.__o_predicat(self.__o_node)


class Hook:
    """
    Encapsulate hook execution into a functor.
    """

    __slots__ = ("__o_predicat", "__o_node", "__l_args")

    def __init__(self, o_predicat, o_node, *l_args):
        self.__o_predicat = o_predicat
        self.__o_node = o_node
        self.__l_args = l_args

    def __call__(self):
        return self.__o_predicat(self.__o_node, *self.__l_args)


class Super:
    """
    Encapsulate super() function into a functor.
    """

    __slots__ = ("__o_parent_class", "__o_target", "__s_rule_name", "__o_node")

    def __init__(self, o_parent_class, o_target, s_rule_name, o_node):
        self.__o_parent_class = o_parent_class
        self.__o_target = o_target
        self.__s_rule_name = s_rule_name
        self.__o_node = o_node

    def __call__(self):
        return getattr(self.__o_parent_class, self.__s_rule_name)(
            self.__o_target, self.__o_node
        )


class NotIgnore:
    """
    Encapsulate not_ignore directive into a functor.
    """

    __slots__ = ()

    def __call__(self):
        return Parsing.o_base_parser.not_ignore()


class FalseDirective:
    """
    Return false to ease debug.
    """

    __slots__ = ()

    def __call__(self):
        return Parsing.o_base_parser.false()


class ResetIgnore(object):
    """
    Encapsulate ResetIgnore directive into a functor.
    """

    __slots__ = ()

    def __init__(self):
        return Parsing.o_base_parser.resetIgnore()
