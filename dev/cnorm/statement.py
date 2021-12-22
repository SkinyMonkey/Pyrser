from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from expression import CExpression


class CStatement(GenericHook, Grammar):
    __grammar__ = open("./dev/cnorm/grammar/statement.pw").read()

    def typeHook(self, oNode, sSubExpr, sType="__statement__"):
        """
        Type should attribute an automatic name: per grammar function.
        """
        oNode["type"] = sType
        oNode["sub_type"] = sSubExpr
        return oNode


print(__name__)
if __name__ != "__main__":
    CStatement()
else:
    from tests.test import test
    from tests.statement import lTest

    test(lTest, CStatement(), "test_statement.tpl", "statement")
    print("All test passed.")
