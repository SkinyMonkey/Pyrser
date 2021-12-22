import unittest
from pyrser.grammar import Grammar


class Father(Grammar):
    """!grammar
    operand ::= #num
    ;

    sub ::= #identifier
    ;
    """


class Math(Father, Grammar):
    """!grammar
    operand ::= Father::operand '+' sub
    ;

    sub ::= #num
    ;
    """

    globals = globals()


class MultiMath(Father, Grammar):
    """!grammar
    operand ::=  Father::operand ['+' Father::operand ]+
    ;
    """

    globals = globals()


class generatedCode(unittest.TestCase):
    @classmethod
    def setUpClass(cGeneratedCodeClass):
        cGeneratedCodeClass.oRoot = {}
        cGeneratedCodeClass.oGrammar = Math()

    def test_inheritance(self):
        self.assertEqual(
            generatedCode.oGrammar.parse("12 + 4", self.oRoot, "operand"),
            True,
            "failed in inheritance",
        )

    def test_inheritance_multi_depth(self):
        self.assertEqual(
            MultiMath().parse("12 + 3 + 5", self.oRoot, "operand"),
            True,
            "failed in multi inheritance",
        )
