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


oGrammar = Debug()
oRoot = {}
print(oGrammar.parse("123", oRoot, "debug"))
clean_tree(oRoot, "parent")
clean_tree(oRoot, "type")
pprint(oRoot)
