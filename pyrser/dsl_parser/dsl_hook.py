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

from pyrser.node import new_node
from pyrser.dsl_parser.dsl_error import GrammarException

# FIXME : erase all 'del' : usefull for debug, nothing more

"""
Hook called to build the tree/work on the stream.
"""
d_builtins = (
    "identifier",
    "num",
    "string",
    "cchar",
    "char",
    "space",
    "end",
    "empty",
    "super",
    "not_ignore",
    "reset_ignore",
)


def inject_expression(l_alternative):
    return [
        {
            "multiplier": "[]",
            "terminal": {
                "clauses": {"alternatives": [l_alternative], "type": "clause"},
                "type": "expr",
            },
            "type": "multiplier",
        }
    ]


def inject_alternative(o_node):
    if len(o_node["clauses"]["alternatives"]) > 1:
        o_node["clauses"]["alternatives"] = [
            [
                {
                    "alternatives": o_node["clauses"]["alternatives"],
                    "type": "alternative_terminal",
                }
            ]
        ]
    return o_node


def inject_unary_terminal(o_node, s_field):
    o_tmp = new_node(None, s_field)
    o_tmp[s_field] = o_node[s_field]
    o_tmp["terminal"] = o_node["terminal"]
    o_node["terminal"] = o_tmp


def inject_aggregated(o_node):
    if "aggregation" in o_node:
        o_tmp = new_node(o_node["parent"], "aggregation")
        o_tmp["name"] = o_node["name"]
        o_node["name"] = o_node["aggregation"]
        o_tmp["non_terminal"] = o_node
        del o_node["aggregation"]
        del o_node["parent"]
        o_node = o_tmp
    return o_node


def swap_terminal(o_node):
    o_tmp = o_node["parent"]["terminal"]
    o_node["terminal"] = o_tmp
    o_node["parent"]["terminal"] = o_node


def rules_hook(o_node):
    if "rules" not in o_node["parent"]:
        o_node["parent"]["rules"] = []

    o_node = inject_alternative(o_node)
    o_node["parent"]["rules"].append(o_node)
    return True


def rule_name_hook(o_node):
    o_node["parent"]["prototype"] = o_node
    return True


def param_hook(o_node):
    o_node["parent"]["param"] = o_node["param"][1:-1]
    return True


def rule_directive_hook(o_node):
    if "rule_directive" not in o_node["parent"]:
        o_node["parent"]["rule_directive"] = []
    o_node["parent"]["rule_directive"].append(o_node)
    return True


def headclauses_hook(o_node):
    o_node["alternatives"] = [[]]
    return True


def tailclauses_hook(o_node):
    o_node["alternatives"].append([])
    return True


def clauses_hook(o_node):
    if len(o_node["alternatives"]) > 1:
        n_index = 0
        for i_alternative in o_node["alternatives"]:
            if len(i_alternative) > 1:
                o_node["alternatives"][n_index] = inject_expression(i_alternative)
            n_index += 1
    o_node["parent"]["clauses"] = o_node
    return True


def alternative_hook(o_node):
    if "wrapper" in o_node:
        o_node["type"] = "wrapper"
        inject_unary_terminal(o_node, "wrapper")
        if "param" in o_node:
            o_node["terminal"]["param"] = o_node["param"]
            del o_node["param"]
        o_node["terminal"]["name"] = o_node["name"]
        del o_node["wrapper"]

    o_node["parent"]["alternatives"][-1].append(o_node["terminal"])
    return True


def non_terminal_hook(o_node):
    o_node = inject_aggregated(o_node)

    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def aggregation_hook(o_node):
    del o_node["parent"]
    return True


def terminal_hook(o_node):
    for i_controller in ("multiplier", "not"):
        if i_controller in o_node:
            inject_unary_terminal(o_node, i_controller)

    o_node["parent"]["terminal"] = o_node["terminal"]
    return True


def directive_hook(o_node):
    if o_node["name"] not in d_builtins:
        o_node["type"] = "hook"
    elif "param" in o_node:
        raise GrammarException(
            "Using parameters on a builtin directive : %s." % o_node["name"]
        )
    if o_node["name"] == "super":
        o_node["type"] = "super"
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def c_string_hook(o_node):
    if len(o_node["string"][1:-1]) == 0:
        raise GrammarException("Using an empty string as string literal.")
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def check_c_char_length(c_char):
    if len(c_char[1:-1]) > 1 and c_char[1] != "\\":
        raise GrammarException(
            "Using a char literal which length is greater than 1 : %s" % c_char
        )
    elif len(c_char[1:-1]) == 0:
        raise GrammarException("Using an empty string as char literal.")


# FIXME : worst bug a ' alone make the readuntil fail and consume a big
# chunk of waste memory.


def c_char_hook(o_node):
    check_c_char_length(o_node["string"])
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def range_hook(o_node):
    check_c_char_length(o_node["from"])
    check_c_char_length(o_node["to"])
    if ord(o_node["from"][1:-1]) > ord(o_node["to"][1:-1]):
        raise GrammarException(
            "Range : first character should be < to second : %s > %s"
            % (o_node["from"], o_node["to"])
        )
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def expr_hook(o_node):
    o_node = inject_alternative(o_node)
    o_expression = {"type": "multiplier", "multiplier": "[]", "terminal": o_node}
    o_node["parent"]["terminal"] = o_expression
    del o_node["parent"]
    return True


def until_hook(o_node):
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def look_ahead_hook(o_node):
    o_node["parent"]["terminal"] = o_node
    del o_node["parent"]
    return True


def read_terminal_range_hook(o_node):
    swap_terminal(o_node)
    o_node["multiplier"] = "{}"
    o_node["type"] = "terminal_range"
    del o_node["parent"]
    return True


def capture_hook(o_node):
    swap_terminal(o_node)
    del o_node["parent"]
    return True
