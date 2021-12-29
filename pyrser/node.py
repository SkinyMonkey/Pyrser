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

# from types import DictType, ListType
from copy import copy

from functools import wraps


def new_node(o_parent, s_type=None):
    if o_parent != None and id(o_parent) in o_parent:
        o_node = o_parent[id(o_parent)]
        o_node["parent"] = o_parent
    # FIXME : faire tests pour savoir si c'est bon
    # del o_parent[id(o_parent)]
    else:
        o_node = {"parent": o_parent}

    if s_type != None and "type" not in o_node:
        o_node["type"] = s_type
    return o_node


def node(s_type=None):
    def wrapper(o_target):
        @wraps(o_target)
        def wrapped(*l_args):
            # if type(l_args[0]) != DictType:
            if not isinstance(l_args[0], dict):
                o_node = new_node(l_args[1], s_type)
                b_res = o_target(l_args[0], o_node)
            else:
                o_node = new_node(l_args[0], s_type)
                b_res = o_target(o_node)
            return b_res

        return wrapped

    return wrapper


def clean_tree(o_parent, s_name):
    # if type(o_parent) == DictType:
    if isinstance(o_parent, dict):
        for i_key, i_value in list(o_parent.items()):
            if i_key != "parent" and i_value != o_parent:
                clean_tree(i_value, s_name)
        if s_name in o_parent:
            del o_parent[s_name]
    # elif type(o_parent) == ListType:
    elif isinstance(o_parent, list):
        for i_value in o_parent:
            if i_value != o_parent:
                clean_tree(i_value, s_name)


def clean_tree_from_metadata(o_root):
    clean_tree(o_root, "parent")
    clean_tree(o_root, "type")


def slide(o_node, s_name):
    o_tmp = copy(o_node)
    o_node.clear()
    if id(o_node) in o_tmp:
        del o_tmp[id(o_node)]
    o_node[s_name] = o_tmp

    o_node["parent"] = o_tmp["parent"]
    o_tmp["parent"] = o_node
    return o_node


def next(o_node, s_name):
    if s_name not in o_node:
        o_node[s_name] = {"parent": o_node}
    o_node[id(o_node)] = o_node[s_name]
    return o_node


def next_is(o_node, o_sub_node):
    o_node[id(o_node)] = o_sub_node
    return o_node


def next_clean(o_node):
    if id(o_node) in o_node:
        del o_node[id(o_node)]
    return o_node


def has_next(o_node):
    return id(o_node) in o_node
