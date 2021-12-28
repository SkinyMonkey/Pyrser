from pyrser.grammar import Grammar
from pprint import pprint

from dev.cnorm.declaration import CDeclaration
from dev.kooc.mangling import mangling

class Module(CDeclaration):
    # TODO : - overwrite the right rule. translation_unit?
    # translation_unit ::= CDeclaration::translation_unit
    # ;
    # - allow only declarations but implementation => CDeclaration::declaration?
    # - declaration can NOT be done outside of a module
    # - module variable [ModuleName variable]
    # - module function call [ModuleName func :param1 :param2]
    # - disambiguation/cast @!(int)[ModuleName var]
    # - mangle names found in the module
    """!grammar

    modules ::= [module]+
    ;

    module ::= "@module" #identifier :module_name '{' [ @push_at("declarations") declaration #mangling ]* '}'
    ;
    """
    def manglingHook(self, node):
        module_name = node["module_name"]
        for decl in node["declarations"]:
            decl["name"] = mangling(module_name, decl)
        return True

if __name__ == "__main__":
    import unittest

    class KoocTest(unittest.TestCase):
        @classmethod
        def setUpClass(cKoocClass):
            cKoocClass.grammar = Module()
 
        def test_empty_module(self):
            self.assertEqual(
                KoocTest.grammar.parse('@module ModuleName {}', {}, "module"),
                True,
                "failed in module",
            )

        def test_module_decl(self):
            self.assertEqual(
                KoocTest.grammar.parse('@module ModuleName { int a; }', {}, "module"),
                True,
                "failed in module",
            )

#        def test_double_inclusion(self):
#            try:
#                KoocTest.grammar.parse('@module "stdio.kh" @module "stdio.kh"', {}, "module"),
#            except Exception as e:
#                pass

    unittest.main(failfast=True)
