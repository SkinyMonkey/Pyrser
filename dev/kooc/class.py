from pyrser.grammar import Grammar
from pprint import pprint

from dev.cnorm.declaration import CDeclaration

# TODO:
# - @member
# - alloc
# - new
# - init
# - clean
# - delete
# - @virtual
class Class(CDeclaration):
    """!grammar
    type_specifier ::=   CDeclaration::type_specifier
                       | class_specifier
                       | callback
    ;

    class_specifier ::= "@class" #type("__class__") [#identifier :type_specifier]?
                        [ @_ extend]?
                        '{'
                            [ @next("class_decls") class_decls ]*
                        "};"
    ;

    class_decls ::= [ visibility ]? [ @push_at("declarations") declaration #visibility ]+
    ;

    extend ::= [ visibility ]? "extends" @push_at("extends") extend_name
    ;

    extend_name ::= #identifier [ ',' #identifier ]*
    ;

    visibility ::= [ "public" | "private" | "protected" ] :visibility #set_visibility ':'
    ;

    callback ::= "@callback" #identifier ';'
    ;
    """
    def set_visibilityHook(self, node_):
        self.visibility = node_["visibility"]
        del node_["visibility"]
        return True

    def visibilityHook(self, node_):
        if not hasattr(self, "visibility"):
            node_["declarations"][-1]["visibility"] = "public" # public by default
            return True

        node_["declarations"][-1]["visibility"] = self.visibility
        return True

if __name__ == "__main__":
    import unittest

    class ClassTest(unittest.TestCase):
        @classmethod
        def setUpClass(cClassClass):
            cClassClass.oRoot = {}
            cClassClass.oGrammar = Class()
    
        def test_class(self):
            self.assertEqual(
                ClassTest.oGrammar.parse("@class AClassName {};", {}, "class_specifier"),
                True,
                "failed in class",
            )

        def test_class_with_decl(self):
            self.assertEqual(
                    ClassTest.oGrammar.parse("@class AClassName { int a;};", {}, "class_specifier"),
                True,
                "failed in class_with_decl",
            )

        def test_class_with_visibility(self):
           self.assertEqual(
                   ClassTest.oGrammar.parse("@class AClassName { public: int a;};", {}, "class_specifier"),
               True,
               "failed in class_with_decl",
           )

        def test_class_with_extend(self):
            self.assertEqual(
                    ClassTest.oGrammar.parse("@class A extends A { int a;};", {}, "class_specifier"),
                True,
                "failed in class_with_extend",
            )

        # FIXME : push names into "extends"
        def test_class_with_extend_multiple(self):
            self.assertEqual(
                    ClassTest.oGrammar.parse("@class A extends A,B { int a;};", {}, "class_specifier"),
                True,
                "failed in class_with_extend_multiple",
            )

        def test_class_with_callback(self):
            self.assertEqual(
                    ClassTest.oGrammar.parse("@callback test;", {}, "callback"),
                True,
                "failed in class_with_extend_multiple",
            )

    unittest.main(failfast=True)
