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

# FIXME : better names than fn and fnb

# NOTE : we dont' pass the method itself because the parser will change between grammars
def fn(callback_name): # declaration
    def fn_wrapper(*args): # use in grammar (__init__)
        def inner_wrapper(): # call (__call__)
            return getattr(Parsing.o_base_parser, callback_name)(*args)
        return inner_wrapper
    return fn_wrapper

ReadText = fn("read_text")
ReadChar = fn("read_char")
ReadUntil = fn("read_until")
ReadRange = fn("read_range")
NotIgnore = fn("not_ignore")
FalseDirective = fn("false")

def fnb(cb, *args):
    def fn_wrapper():
        return cb(*args)
    return fn_wrapper

NonTerminal = fnb
Hook = fnb

def Super(o_parent_class, o_target, s_rule_name, o_node):
    def fn_wrapper():
        return getattr(__o_parent_class, __s_rule_name)(__o_target, __o_node)
    return fn_wrapper

def ResetIgnore():
    return Parsing.o_base_parser.reset_ignore()
