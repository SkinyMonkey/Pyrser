import unittest
from pyrser.grammar import Grammar


class CompositionMath(Grammar):
    """!grammar
    operand ::=  #num '+' #num
    ;
    """


class Composition(Grammar):
    """!grammar
    composition ::= CompositionMath::operand
    ;
    """

    globals = globals()


class GeneratedCode(unittest.TestCase):
    @classmethod
    def setUpClass(c_generated_code_class):
        c_generated_code_class.o_root = {}
        c_generated_code_class.o_grammar = Composition()

    def test_composition(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("12 + 12", self.o_root, "composition"),
            True,
            "failed in composition",
        )
