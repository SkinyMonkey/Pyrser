# Copyright (C) 2012 Candiotti Adrien
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyrser import node
from pyrser.dsl_parser import dsl_parser
from pyrser.code_generation import python

# TODO(bps): factor those imports for generated code
from pyrser.parsing.capture import capture, Capture
from pyrser.parsing.parsing_context import parsing_context, Parsing
from pyrser.parsing.directive_functor import (
    NonTerminal,
    ReadChar,
    Hook,
    ReadText,
    ReadRange,
)
from pyrser.parsing.bnf_primitives import (
    alt,
    Alt,
    complement,
    Complement,
    expression,
    Expression,
    n,
    N,
    negation,
    Negation,
    one_or_n,
    OneOrN,
    until,
    Until,
    zero_or_n,
    ZeroOrN,
    zero_or_one,
    ZeroOrOne,
)
from pyrser.lang.python import python as d_lang_conf

grammar_marker = "!grammar"


class GrammarBase(type):
    """
    A metaclass that augment a class based on a grammar definition.
    It stores defined grammars into $grammars so it can be reused when doing composition
    """

    grammars = {}
    directives = {}

    @staticmethod
    def directive(fn):
        GrammarBase.directives[fn.__name__] = fn
        return fn

    def __new__(mcs, name, bases, dict_):
        grammar = dict_.get("__grammar__")
        if grammar is None:
            grammar = dict_.get("__doc__")
            if grammar is not None and grammar.startswith(grammar_marker):
                grammar = grammar[len(grammar_marker) :]
            else:
                grammar = None

        if grammar is not None:
            # We parse the grammar, generate code from it and compile it to bytecode
            ast = dsl_parser.parse(grammar, {}, name)
            generated_code = python.Python(d_lang_conf).translation(name, ast["rules"])
            # FIXME : remove, DEBUG
            open("/tmp/res", 'w+').write(generated_code)
            byte_code = compile(generated_code, "<%s>" % name, "exec")

            # We add the previously generated grammars and the defined directives to the global definitions
            # that should be used by the evaluated code
            # so that it can call them
            augmented_globals = globals().copy()
            augmented_globals.update(GrammarBase.grammars)
            augmented_globals.update(GrammarBase.directives)

            # The byte code is added to the current runtime
            eval(byte_code, augmented_globals, locals())

            # We add the compiled functions to the dict_ of the class
            # we are creating with the metaclass
            compiled_grammar = locals()["%sGrammar" % name]
            for key, value in list(compiled_grammar.__dict__.items()):
                if callable(value):
                    dict_[key] = value

        elif name != "Grammar":
            print(("Grammar could not be found in %s" % name))

        # instantiate the new class
        cls = type.__new__(mcs, name, bases, dict_)
        if grammar is not None:
            GrammarBase.grammars[name] = cls
        return cls


class Grammar(object, metaclass=GrammarBase):
    """
    Base class for all grammars.

    This class turn any class A that inherit it into a grammar.
    Taking the description of the grammar in parameter it will add
    all what is what is needed for A to parse it.
    """

    @staticmethod
    def directive(fn):
        return GrammarBase.directive(fn)

    def parse(self, source, ast, rule_name="main"):
        """Parse the grammar"""

        func_name = "%s_rule" % rule_name
        node.next_is(ast, ast)
        dsl_parser.Parsing.o_base_parser.parsed_stream(source)
        if not hasattr(self, func_name):
            raise Exception("First rule doesn't exist : %s" % func_name)
        result = getattr(self, func_name)(ast)
        if not result:
            return False
        dsl_parser.Parsing.o_base_parser.read_ws()
        return dsl_parser.Parsing.o_base_parser.read_eof()
