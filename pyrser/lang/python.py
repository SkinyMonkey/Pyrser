python = {
    "builtins": {
        "identifier": "read_identifier",
        "num": "read_integer",
        "string": "read_c_string",
        "cchar": "read_c_char",
        "char": "read_a_char",
        "space": "read_ws",
        "end": "read_untilEOF",
        "empty": "read_eof",
        "super": "super",
        "false": "false",
        "readThisChar": "read_char",
        "readThisText": "read_text",
        "range": "read_range",
        "not_ignore": "not_ignore",
        "resetIgnore": "reset_ignore",
    },
    "not": {"!": "negation", "~": "complement"},
    "multiplier": {
        "?": "zero_or_one",
        "+": "one_or_n",
        "*": "zero_or_n",
        "[]": "expression",
        "{}": "n",
    },
    "keyword": {"and": "and", "object": "self"},
    "access_operator": ".",
    "alt": "alt",
    "baseParserMethod": "Parsing.o_base_parser",
    "indent": 15,
    "file_extension": ".py",
}

from imp import load_source


def python_post_generation(s_module_name, s_file, s_to_file, s_grammar, o_instance):
    # 	    try:
    o_module = load_source(s_module_name, s_to_file)
    # 	    except:
    # 	      self.error(\
    # 		'Generated source is wrong, please report on redmine.lse.epita.fr')
    # 	      exit(0)

    if s_grammar != None:
        try:
            o_class = getattr(o_module, s_grammar)
            return o_class
        except:
            o_instance.error('No grammar called "%s" in %s' % (s_grammar, s_file))
            exit(0)
    return o_module
