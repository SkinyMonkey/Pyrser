from pprint import pprint
from pyrser.node import clean_tree
from cnorm_to_c.cnorm_to_c import c_ast_to_c


def test(l_test, o_grammar_parser, s_template_name, s_first):
    b_exception_in_hook = False
    s_tr = "-" * 80
    for i_test in l_test:
        print(("%s\n%s" % (s_tr, i_test)))
        o_root = {}
        b_res = o_grammar_parser.parse(i_test, o_root, s_first)
        if not b_res:
            raise Exception("Parse test failed : %s" % i_test)
        s_res = c_ast_to_c(o_root, s_template_name)
        pprint(o_root)
        if s_res != i_test:
            print(("!=\n%s" % s_res))
            raise Exception("CNorm2c test failed")
    return b_exception_in_hook
