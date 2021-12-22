from pprint import pprint
from pyrser.grammar import Grammar
from pyrser.hooks import GenericHook
from pyrser.node import clean_tree_from_metadata


class Ini(Grammar, GenericHook):
    """!grammar
    ini ::= [ @push_at("sections") section ]+
    ;

    section ::= @_ header [ @next("content") map]* #map('header', 'content')
    ;

    header ::= '[' #identifier :header ']'
    ;

    map ::= #identifier :key '=' ->';' :value #map('key', 'value')
    ;
    """

    def mapHook(self, oNode, sKey, sValue):
        oNode[oNode[sKey]] = oNode[sValue]
        del oNode[sKey]
        del oNode[sValue]
        return True


def parse_ini(sSource):
    oGrammar = Ini()
    oRoot = {}
    bRes = oGrammar.parse(sSource, oRoot, "ini")
    clean_tree_from_metadata(oRoot)
    pprint(oRoot)
    return bRes


if __name__ == "__main__":
    print(
        parse_ini(
            """
  [title]
  foo = bar;
  bar = foo;
  server = 127.0.0.1;

  [foo]
  bar = foobar;"""
        )
    )

    print(
        parse_ini(
            """
  [title]
  foo = bar;
  bar = foo;
  server = 127.0.0.1;
  """
        )
    )
