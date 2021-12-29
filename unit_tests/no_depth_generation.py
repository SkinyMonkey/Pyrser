import unittest
from pyrser.grammar import Grammar

"""
This set of test check if the grammar is correctly generated in simple cases,
with no expression imbrications
"""


class NoDepthGeneration(Grammar):
    """!grammar
    directive ::= #identifier
     ;

    capture ::= #identifier : capture
     ;

    hook ::= #test
     ;

    wrapper ::= @test capture
     ;

    nonTerminal ::= directive
     ;

    range ::= 'a' .. 'z'
     ;

    until ::= ->['1']
     ;

    multiplier ::= ['1']?
     ;

    not ::= !"toto" #identifier
     ;

    complement ::= ~'1' '1'
     ;

    alt ::= #identifier | #num
     ;

    terminal_range1 ::= '0'{1}
     ;

    terminal_range2 ::= '0'{1, 3}
     ;
    """

    def test_hook(self, o_node):
        return True

    def test_wrapper(self, o_rule, o_node):
        b_res = o_rule()
        o_node["test"] = o_node["capture"]
        return b_res


class GeneratedCode(unittest.TestCase):
    @classmethod
    def setUpClass(c_generated_code_class):
        c_generated_code_class.o_root = {}
        c_generated_code_class.o_grammar = NoDepthGeneration()

    def test_directive(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("identifier", self.o_root, "directive"),
            True,
            "failed in directive",
        )

    def test_capture(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("identifier", self.o_root, "capture"),
            True,
            "failed in capture",
        )

    def test_hook(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("", self.o_root, "hook"), True, "failed in hook"
        )

    def test_wrapper(self):
        GeneratedCode.o_grammar.parse("id", self.o_root, "wrapper"),
        self.assertEqual("test" in self.o_root, True, "failed in wrapper")

    def test_non_terminal(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("identifier", self.o_root, "nonTerminal"),
            True,
            "failed in nonTerminal",
        )

    def test_range(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("i", self.o_root, "range"),
            True,
            "failed in range",
        )

    def test_until(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("321", self.o_root, "until"),
            True,
            "failed in until",
        )

    def test_multiplier(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("1", self.o_root, "multiplier"),
            True,
            "failed in multiplier",
        )

    def test_not(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("tata", self.o_root, "not"),
            True,
            "failed in not",
        )

    def test_complement(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("01", self.o_root, "complement"),
            True,
            "failed in complement",
        )

    def test_alt(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("123", self.o_root, "alt"),
            True,
            "failed in alt",
        )

    def test_terminal_range1(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("0", self.o_root, "terminal_range1"),
            True,
            "failed in terminal range #1",
        )

    def test_terminal_range2(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("00", self.o_root, "terminal_range2"),
            True,
            "failed in terminal range #2",
        )
