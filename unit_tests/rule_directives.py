import unittest
from functools import wraps
from pyrser.grammar import Grammar


@Grammar.directive
def test(o_rule):
    def wrapper(*l_args):
        b_res = o_rule(*l_args)
        l_args[1]["rule_directive_test"] = True
        return b_res

    return wrapper


class RuleDirective(Grammar):
    """!grammar
    rule_directive @test ::= #identifier
    ;
    """


class GeneratedCode(unittest.TestCase):
    @classmethod
    def setUpClass(o_cls):
        GeneratedCode.oGrammar = RuleDirective()
        GeneratedCode.oRoot = {}

    def test_rule_directive(self):
        GeneratedCode.oGrammar.parse("identifier", self.oRoot, "rule_directive"),
        self.assertEqual(
            self.oRoot["rule_directive_test"], True, "failed in rule_directive"
        )
