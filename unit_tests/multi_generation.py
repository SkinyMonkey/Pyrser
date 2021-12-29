import unittest
from pyrser.grammar import Grammar

"""
This set of test check if the grammar is correctly generated in tests
that implies expression imbrications.
"""


class MultiDepthGeneration(Grammar):
    """!grammar
    directive ::= [#identifier #string #num]
      ;

    capture ::= [#identifier : c #identifier : c #identifier : c]
      ;

    hook ::= [#test #test2 #test3]
      ;

    wrapper ::=  	@test #identifier :test
                [ ',' @test #identifier :test ]*
      ;

    nonTerminal ::= [directive directive directive]
      ;

    range ::= ['a' .. 'z' '0' .. '9' 'A' .. 'Z']
      ;

    until ::= [->'1' ->'2' ->'3']
      ;

    multiplier ::= [['1']? ['2']? ['3']?]
      ;

    not ::= [!"toto" #identifier !"tata" #identifier !"titi" #identifier]
      ;

    alt ::= [[#identifier | #num] [ #char | #string] [#cchar | #not_ignore]]
      ;

    terminal_range1 ::= ['0'{1} '1'{2} '2'{3}]
      ;

    terminal_range2 ::= ['0'{1, 3} '1'{2, 4} '2'{4, 6}]
      ;
    """

    def test_hook(self, o_node):
        return True

    def test2_hook(self, o_node):
        return True

    def test3_hook(self, o_node):
        return True

    def test_wrapper(self, o_rule, o_node):
        if "list" not in o_node:
            o_node["list"] = []
        b_res = o_rule()
        o_node["list"].append(o_node["test"])
        del o_node["test"]
        return b_res


class GeneratedCode(unittest.TestCase):
    @classmethod
    def setUpClass(c_generated_code_class):
        c_generated_code_class.o_root = {}
        c_generated_code_class.o_grammar = MultiDepthGeneration()

    def test_directive(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse('id "ok" 123', self.o_root, "directive"),
            True,
            "failed in directive",
        )

    def test_capture(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("id id2 id3", self.o_root, "capture"),
            True,
            "failed in capture",
        )

    def test_hook(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("", self.o_root, "hook"), True, "failed in hook"
        )

    def test_wrapper(self):
        GeneratedCode.o_grammar.parse("foo, bar, rab", self.o_root, "wrapper"),
        self.assertEqual(
            self.o_root["list"] == ["foo", "bar", "rab"], True, "failed in hook"
        )

    def test_range(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("i 8 U", self.o_root, "range"),
            True,
            "failed in range",
        )

    def test_non_terminal(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse(
                'id "ok" 123 id "ko" 456 la "to" 789', self.o_root, "nonTerminal"
            ),
            True,
            "failed in nonTerminal",
        )

    def test_until(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("155525553", self.o_root, "until"),
            True,
            "failed in nonTerminal",
        )

    def test_multiplier(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("123", self.o_root, "multiplier"),
            True,
            "failed in multiplier",
        )

    def test_not(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("lol ok haha", self.o_root, "not"),
            True,
            "failed in not",
        )

    #      def test_complement(self):
    #          self.assertEqual(
    # 	      GeneratedCode.o_grammar.parse('01 0022 000333', self.oRoot, 'not'),
    # 	      True,
    # 	      'failed in complement')

    def test_alt(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("id a 'a'", self.o_root, "alt"),
            True,
            "failed in alt",
        )

    def test_terminal_range1(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("0 11 222", self.o_root, "terminal_range1"),
            True,
            "failed in terminal_range #1",
        )

    def test_terminal_range2(self):
        self.assertEqual(
            GeneratedCode.o_grammar.parse("00 111 22222", self.o_root, "terminal_range2"),
            True,
            "failed in terminal_range #2",
        )
