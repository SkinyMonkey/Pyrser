import unittest
from pyrser.grammar import Grammar


class CaptureGeneration(Grammar):
    """!grammar
    parentTest ::= #num :test captureTest
    ;

    captureTest ::= #identifier :test #test
    ;
    """

    def test_hook(self, o_tree_context):
        return True


class Capture_Test(unittest.TestCase):
    @classmethod
    def setUpClass(c_capture_class):
        c_capture_class.o_root = {}
        c_capture_class.o_grammar = CaptureGeneration()

    def test_capture(self):
        self.assertEqual(
            Capture_Test.o_grammar.parse("123 id", self.o_root, "parentTest"),
            True,
            "failed in capture",
        )
