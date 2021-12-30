from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from dev.cnorm.expression import CExpression


class CStatement(GenericHook, Grammar):
    __grammar__ = open("./dev/cnorm/grammar/statement.pw").read()

    def type_hook(self, o_node, s_sub_expr, s_type="__statement__"):
        """
        Type should attribute an automatic name: per grammar function.
        """
        o_node["type"] = s_type
        o_node["sub_type"] = s_sub_expr
        return o_node


if __name__ != "__main__":
    CStatement()
else:
    from dev.cnorm.tests.test import test
    from dev.cnorm.tests.statement import l_test

    test(l_test, CStatement(), "test_statement.tpl", "statement")
    print("All test passed.")
