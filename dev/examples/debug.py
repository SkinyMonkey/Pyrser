from pyrser import Grammar
from pyrser.hooks import GenericHook
from pyrser.node import clean_tree
from pprint import pprint


class Debug(Grammar, GenericHook):
    """!grammar
    debug ::= @next("sub") sub
    ;

    sub ::= @_ [subsub | foo]
    ;

    subsub ::= #identifier :id
    ;

    foo ::= #num :num
    ;
    """

    pass


o_grammar = Debug()
o_root = {}
print((o_grammar.parse("123", o_root, "debug")))
clean_tree(o_root, "parent")
clean_tree(o_root, "type")
pprint(o_root)
