from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from pyrser.node import slide, next, next_is


class CExpression(GenericHook, Grammar):
    __grammar__ = open("./dev/cnorm/grammar/expression.pw").read()

    def __type(self, o_node, s_sub_expr, s_type="__expression__"):
        """
        Type should attribute an automatic name: per grammar function.
        """
        o_node["type"] = s_type
        o_node["sub_type"] = s_sub_expr
        return o_node

    def to_post_expr_hook(self, o_node, s_type):
        if "postfix" not in o_node:
            o_node["postfix"] = []
        o_index = {"expr": {}}
        self.__type(o_index, s_type)
        o_node["postfix"].append(o_index)
        next_is(o_node, o_node["postfix"][-1]["expr"])
        return True

    def type_next_hook(self, o_node, s_sub_type, s_next):
        next(o_node, s_next)
        self.__type(o_node, s_sub_type)
        return True

    def nnary_op_hook(self, o_node, s_sub_type, s_side, s_next):
        slide(o_node, s_side)
        self.__type(o_node, s_sub_type)
        next(o_node, s_next)
        return True

    def primary_hook(self, o_node, s_operator):
        self.__type(o_node, "terminal")
        o_node["operator"] = s_operator
        return True

    def to_post_op_hook(self, o_node, s_type):
        self.to_post_expr_hook(o_node, s_type)
        o_node["postfix"][-1]["expr"]["op"] = o_node["op"]
        del o_node["op"]
        return True

    def sizeof_hook(self, o_node):
        if "primary_id" in o_node and o_node["primary_id"] == "sizeof":
            o_expr = o_node["postfix"][0]["expr"]
            o_node.clear()
            self.__type(o_node, "sizeof")
            o_node["expr"] = o_expr
        return True

    def captured_something_hook(self, o_node):
        # FIXME : workaround degueu car dans certains cas
        # 	    la grammaire d'expression capture .. du vide
        b_res = len(o_node["captured"]) > 0
        del o_node["captured"]
        return b_res


if __name__ != "__main__":
    CExpression()
else:
    from dev.cnorm.tests.test import test
    from dev.cnorm.tests.expression import l_test

    test(l_test, CExpression(), "test_expression.tpl", "expression")
    print("All test passed.")
