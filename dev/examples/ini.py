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

    def map_hook(self, o_node, s_key, s_value):
        o_node[o_node[s_key]] = o_node[s_value]
        del o_node[s_key]
        del o_node[s_value]
        return True


def parse_ini(s_source):
    o_grammar = Ini()
    o_root = {}
    b_res = o_grammar.parse(s_source, o_root, "ini")
    clean_tree_from_metadata(o_root)
    pprint(o_root)
    return b_res


if __name__ == "__main__":
    print((
        parse_ini(
            """
  [title]
  foo = bar;
  bar = foo;
  server = 127.0.0.1;

  [foo]
  bar = foobar;"""
        )
    ))

    print((
        parse_ini(
            """
  [title]
  foo = bar;
  bar = foo;
  server = 127.0.0.1;
  """
        )
    ))
