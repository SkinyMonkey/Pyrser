from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from .expression import CExpression
from .statement import CStatement
from copy import copy


class CDeclaration(GenericHook, Grammar):
    __grammar__ = open("./dev/cnorm/grammar/declaration.pw").read()

    def __init__(self):
        super(Grammar, self).__init__()
        super(GenericHook, self).__init__()
        self.__d_default_c_type = {
            "type": "__primary__",
            "sign": "signed",
            "type_specifier": "int",
            "type_qualifier": None,
            "storage_class_specifier": "auto",
        }

    def empty_list_at_hook(self, o_node, s_key):
        """
        Called when no parameter is found
        Example:
            char (*funcptr)();
        """
        o_node[s_key] = []
        return o_node

    def type_hook(self, o_node, s_sub_expr, s_type="__declaration__"):
        """
        Type should attribute an automatic name: per grammar function.
        """
        o_node["type"] = s_type
        o_node["sub_type"] = s_sub_expr
        return o_node

    def set_hook(self, o_node, s_key, s_value, s_sub_key=None):
        if s_sub_key != None:
            o_node = o_node[s_sub_key]
        o_node[s_key] = s_value
        return True

    def ctype_hook(self, o_node, s_c_type):
        o_node["ctype"]["type"] = s_c_type
        return True

    def reset_hook(self, o_node):
        o_node.clear()
        return True

    def clean_hook(self, o_node, s_key, s_sub_key=None):
        if s_sub_key != None and s_sub_key in o_node:
            o_node = o_node[s_sub_key]
        if s_key in o_node:
            del o_node[s_key]
        return True

    def push_root_hook(self, o_node, s_field):
        o_root = self.root()
        o_root[s_field].append(copy(o_node))
        next_is(o_node, o_root[s_field][-1])
        return True

    def push_parent_hook(self, o_node, s_field):
        # FIXME : solve the parent referencing problem
        return True
        o_parent = o_node["parent"]
        o_parent[s_field].append(copy(o_node))
        next_is(o_node, o_parent[s_field][-1])
        return True

    def cdecl_hook(self, o_node):
        if "ctype" not in o_node:
            o_node["ctype"] = copy(self.__d_default_c_type)
        else:
            for i_key, iValue in list(self.__d_default_c_type.items()):
                if i_key not in o_node["ctype"]:
                    o_node["ctype"][i_key] = iValue
        return True

    def insert_ptr_hook(self, o_node):
        self.cdecl_hook(o_node)
        if ("pointer" in o_node["ctype"]) == False:
            o_node["ctype"]["pointer"] = []
        o_node["ctype"]["pointer"].append({})
        return True

    def add_qualifier_hook(self, o_node):
        o_node["ctype"]["pointer"][-1]["type_qualifier"] = o_node["type_qualifier"]
        del o_node["type_qualifier"]
        return True

    def composed_type_rewrite_hook(self, o_node):
        if "sub_type" in o_node["ctype"]:
            o_node["ctype"]["type"] = o_node["ctype"]["sub_type"]
            del o_node["ctype"]["sub_type"]
        return True

    def func_ptr_or_prototype_hook(self, o_node):
        if "pointer" in o_node["ctype"] and "return" in o_node["ctype"]:
            self.ctype_hook(o_node, "__func_ptr__")
            self.type_hook(o_node, "__declaration__")
        # elif o_node["ctype"].has_key('params')\
        elif (
            "array" not in o_node
            and "body" not in o_node
            and o_node["ctype"]["type"] not in ["__union__", "__enum__", "__struct__"]
        ):
            self.type_hook(o_node, "__prototype__")
            if "return" in o_node["ctype"]:
                o_node["ctype"].update(o_node["ctype"]["return"])
                del o_node["ctype"]["return"]
        if o_node["ctype"]["type"] == "declaration_specifiers":
            self.ctype_hook(o_node, "__variable__")
        return True

    def is_hook(self, o_node, s_type, s_sub_key=None):
        if s_sub_key != None:
            o_node = o_node[s_sub_key]
        print((o_node["type"]))
        return o_node["type"] == s_type


if __name__ != "__main__":
    CDeclaration()
else:
    from .tests.test import test
    from .tests.declaration import l_test

    b_res = test(l_test, CDeclaration(), "declaration.tpl", "translation_unit")
    if b_res == False:
        print("All test passed.")
    else:
        print("Some exceptions were raised in the hooks.")
