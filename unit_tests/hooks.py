import unittest
from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from pyrser.node import clean_tree

"""
This set of test check the generic hook class.
"""


class GenericHookTest(GenericHook, Grammar):
    """!grammar
    underscore ::= @_ sub
    ;

    next ::= @next("bar") sub
    ;

    push_at ::= @push_at("subs") sub [ ',' @push_at("subs") sub]*
    ;

    push_capture_at ::=         @push_capture_at("subs", "sub") sub
                        [ ',' @push_capture_at("subs", "sub") sub]*
    ;

    continue ::= [sub]? stack_trace_test
    ;

    stack_trace_test ::= @continue("La regle Sub a foire!") sub
    ;

    trace_hook ::= level1
    ;

    trace_wrapper ::= @trace('trace_wrapper') [level_1 sub level_1]
    ;

    level1 ::= level2
    ;

    level2 ::= #trace
    ;

    level_1 ::= level_2
    ;

    level_2 ::= level_3
    ;

    level_3 ::= #true
    ;

    consumed_wrapper ::= @consumed("test") sub
    ;

    sub ::= #identifier :sub
    ;
    """


class GenericHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(c_generated_code_class):
        c_generated_code_class.o_root = {}
        c_generated_code_class.o_grammar = GenericHookTest()

    def test_underscore__wrapper(self):
        GenericHookTests.o_grammar.parse("foo", self.o_root, "underscore"),
        self.assertEqual(self.o_root["sub"], "foo", "failed in @_")
        self.assertEqual(id(self.o_root) in self.o_root, False, "failed in @_")

    def test_next_wrapper(self):
        self.o_root = {}
        GenericHookTests.o_grammar.parse("foo", self.o_root, "next"),
        self.assertEqual(self.o_root["bar"]["sub"], "foo", "failed in @next")
        self.assertEqual(id(self.o_root) in self.o_root, False, "failed in @next")

    def test_push_at_wrapper(self):
        self.o_root = {}
        GenericHookTests.o_grammar.parse("foo, bar, rab, oof", self.o_root, "push_at"),
        clean_tree(self.o_root, "parent")
        clean_tree(self.o_root, "type")
        self.assertEqual(
            self.o_root["subs"],
            [{"sub": "foo"}, {"sub": "bar"}, {"sub": "rab"}, {"sub": "oof"}],
            "failed in @push_at",
        )
        self.assertEqual(id(self.o_root) in self.o_root, False, "failed in @push_at")

    def test_push_capture_at(self):
        self.o_root = {}
        GenericHookTests.o_grammar.parse(
            "foo, bar, rab, oof", self.o_root, "push_capture_at"
        ),
        self.assertEqual(
            self.o_root["subs"],
            ["foo", "bar", "rab", "oof"],
            "failed in @push_capture_at",
        )
        self.assertEqual(
            id(self.o_root) in self.o_root, False, "failed in @push_capture_at"
        )

    def test_continue(self):
        self.o_root = {}
        try:
            GenericHookTests.o_grammar.parse("id1 123 id3", self.o_root, "continue")
        except:
            print("THIS EXCEPTION IS PART OF THE TEST.")


# Visual tests
#      def test_trace_hook(self):
#          GenericHookTests.o_grammar.parse('', self.oRoot, 'trace_hook')

#      def test_trace_wrapper(self):
#          GenericHookTests.o_grammar.parse('foo', self.oRoot, 'trace_wrapper')

#      def test_consumed_wrapper(self):
# GenericHookTests.o_grammar.parse('foo', self.oRoot, 'consumed_wrapper')
