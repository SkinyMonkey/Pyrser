from pyrser.grammar import Grammar
from pprint import pprint

class Import(Grammar):
    # TODO : overwrite translation_unit
    """!grammar
    imports ::= [import]+
    ;

    import ::= "@import" #string :import #import
    ;
    """
    def __init__(self):
        self.imports = {}

    def importHook(self, node):
        if len(node["import"]) > 2:
            import_name = node["import"][1:-1]
            if import_name in self.imports:
                # TODO : add parsed file name and line number
                print "warning: double inclusion or recursive inclusion of file %s (ignored)" % import_name
                return True

            self.imports[import_name] = True

            # TODO : inject file into stream
            #        display kooc error if file dont exist
            # with open(import_name) as f:
            #   self.base_parser.parsedStream(f.read(), import_name)
            #   res = self.translation_unit(node)
            #   self.base_parser.popStream()
            #   return res
        else:
            # TODO : add parsed file name and line number
            print "warning: empty import"
        return True

if __name__ == "__main__":
    import unittest

    class KoocTest(unittest.TestCase):
        @classmethod
        def setUpClass(cKoocClass):
            cKoocClass.grammar = Import()
 
        def test_import(self):
            self.assertEqual(
                KoocTest.grammar.parse('@import "stdio.kh"', {}, "import"),
                True,
                "failed in import",
            )

#        def test_double_inclusion(self):
#            try:
#                KoocTest.grammar.parse('@import "stdio.kh" @import "stdio.kh"', {}, "import"),
#            except Exception as e:
#                pass

    unittest.main(failfast=True)
