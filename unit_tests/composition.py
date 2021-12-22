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


class generatedCode(unittest.TestCase):
    @classmethod
    def setUpClass(cGeneratedCodeClass):
        cGeneratedCodeClass.oRoot = {}
        cGeneratedCodeClass.oGrammar = Composition()

    def test_composition(self):
        self.assertEqual(
            generatedCode.oGrammar.parse("12 + 12", self.oRoot, "composition"),
            True,
            "failed in composition",
        )
