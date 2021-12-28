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


class MultiMath(Father, Grammar):
    """!grammar
    operand ::=  Father::operand ['+' Father::operand ]+
    ;
    """

class GeneratedCode(unittest.TestCase):
    @classmethod
    def setUpClass(c_generated_code_class):
        c_generated_code_class.o_root = {}
        c_generated_code_class.o_grammar = Math()

    def test_inheritance(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("12 + 4", self.o_root, "operand"),
            True,
            "failed in inheritance",
        )

    def test_inheritance_multi_depth(self):
        self.assertEqual(
            MultiMath().parse("12 + 3 + 5", self.o_root, "operand"),
            True,
            "failed in multi inheritance",
        )
