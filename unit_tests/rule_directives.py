import unittest
from functools import wraps
from pyrser.grammar import Grammar


@Grammar.directive
def test(oRule):
    def wrapper(*lArgs):
        bRes = oRule(*lArgs)
        lArgs[1]["rule_directive_test"] = True
        return bRes

    return wrapper


class RuleDirective(Grammar):
    """!grammar
    rule_directive @test ::= #identifier
    ;
    """


class generatedCode(unittest.TestCase):
    @classmethod
    def setUpClass(oCls):
        generatedCode.oGrammar = RuleDirective()
        generatedCode.oRoot = {}

    def test_rule_directive(self):
        generatedCode.oGrammar.parse("identifier", self.oRoot, "rule_directive"),
        self.assertEqual(
            self.oRoot["rule_directive_test"], True, "failed in rule_directive"
        )
