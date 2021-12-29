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

from pyrser.parsing import *
from pyrser.parsing.parsing_context import parsing_context
from pyrser.parsing.capture import *
from pyrser.parsing.bnf_primitives import *
from pyrser.parsing.directive_functor import *
from pyrser.node import node
from pyrser.dsl_parser.dsl_hook import *
from pyrser.dsl_parser.dsl_error import *


def parse(s_source, o_root, s_current_file):
    """
    Entry point of the BNF parsing.
    """
    Parsing.o_base_parser.parsed_stream(s_source, s_current_file)

    global_desc_rule(o_root)
    reset_base_parser()
    return o_root


def global_desc_rule(o_root):
    """
    global_desc ::= [rules]+
    ;
    """
    if not one_or_n(NonTerminal(rules_rule, o_root)):
        raise GrammarException(
            "%s doesn't seems to be a valid grammar file."
            % Parsing.o_base_parser.getName()
        )
    Parsing.o_base_parser.read_ignored()
    return Parsing.o_base_parser.read_eof()


@node("rule")
@parsing_context
def rules_rule(o_node):
    """
    rules ::= rule_name "::=" clauses ';'
    ;
    """
    if (
        rule_name_rule(o_node)
        and alt(ReadText("::="), Error("'::=' missing"))
        and alt(
            NonTerminal(clauses_rule, o_node),
            Error("No clauses found in this rule : %s" % o_node["prototype"]["name"]),
        )
        and alt(ReadChar(";"), Error("';' missing"))
        and rules_hook(o_node)
    ):
        return True
    return False


# FIXME : how to know if it is name or '{' the pb
# 	    	or Error('No name given to current rule.')():
#    and alt(Capture(Parsing.o_base_parser.read_identifier, 'name', oNode)
#  		,Error('No name given to current rule.'))\


@node("rule_name")
@parsing_context
def rule_name_rule(o_node):
    """
    rule_name ::= #identifier [rule_directive]*
    ;
    """
    if (
        capture(Parsing.o_base_parser.read_identifier, "name", o_node)
        and zero_or_n(NonTerminal(rule_directive_rule, o_node))
        and rule_name_hook(o_node)
    ):
        return True
    return False


@node("param")
@parsing_context
def param_rule(o_node):
    """
    param ::= '(' -> ')'
    """
    if capture(Expression(ReadChar("("), ReadUntil(")")), "param", o_node) and param_hook(
        o_node
    ):
        return True
    return False


# FIXME : type is useles, remove after debug


@node("rule_directive")
@parsing_context
def rule_directive_rule(o_node):
    """
    rule_directive ::= '@' #identifier [ param ]?
    ;
    """
    if (
        Parsing.o_base_parser.read_char("@")
        and capture(Parsing.o_base_parser.read_identifier, "name", o_node)
        and zero_or_one(NonTerminal(param_rule, o_node))
        and rule_directive_hook(o_node)
    ):
        return True
    return False


@node("clause")
@parsing_context
def clauses_rule(o_node):
    """
    clauses ::= alternative ['|' alternative ]*
    ;
    """
    if (
        headclauses_hook(o_node)
        and alternative_rule(o_node)
        and clauses_hook(o_node)
        and zero_or_n(
            ReadChar("|"),
            Hook(tailclauses_hook, o_node),
            Alt(
                Expression(
                    NonTerminal(alternative_rule, o_node), Hook(clauses_hook, o_node)
                ),
                Error("Alternative found but no clauses in it."),
            ),
        )
    ):
        return True
    return False


@node("capture")
@parsing_context
def capture_rule(o_node):
    """
    capture ::= ':' #identifier
    ;
    """
    if (
        Parsing.o_base_parser.read_char(":")
        and capture(Parsing.o_base_parser.read_identifier, "name", o_node)
        and capture_hook(o_node)
    ):
        return True
    return False


@node("alternative")
@parsing_context
def alternative_rule(o_node):
    """
    alternative ::= [
                    [ '@' #identifier param ]?
                    [terminal | nonterminal | until | lookAhead ]
                    [capture]?
                  ]+
    ;
    """
    if one_or_n(
        Expression(
            ZeroOrOne(
                Expression(
                    Capture(ReadChar("@"), "wrapper", o_node),
                    Capture(Parsing.o_base_parser.read_identifier, "name", o_node),
                    ZeroOrOne(NonTerminal(param_rule, o_node)),
                )
            ),
            Alt(
                NonTerminal(terminal_rule, o_node),
                NonTerminal(non_terminal_rule, o_node),
                NonTerminal(until_rule, o_node),
                NonTerminal(look_ahead_rule, o_node),
            ),
            ZeroOrOne(NonTerminal(capture_rule, o_node)),
            Hook(alternative_hook, o_node),
        )
    ):
        return True
    return False


@node("non_terminal")
@parsing_context
def non_terminal_rule(o_node):
    """
    NonTerminal ::= #identifier [ "::" #identifier ]?
    ;
    """
    if (
        capture(Parsing.o_base_parser.read_identifier, "name", o_node)
        and zero_or_one(
            ReadText("::"),
            Alt(
                Capture(Parsing.o_base_parser.read_identifier, "aggregation", o_node),
                Error("Malformed composed non_terminal."),
            ),
        )
        and non_terminal_hook(o_node)
    ):
        return True
    return False


@node("directive")
@parsing_context
def directive_rule(o_node):
    """
    directive ::= '#' #identifier [ param ]?
    ;
    """
    if (
        Parsing.o_base_parser.read_char("#")
        and alt(
            Capture(Parsing.o_base_parser.read_identifier, "name", o_node),
            Error("Uncomplete directive."),
        )
        and zero_or_one(NonTerminal(param_rule, o_node))
        and directive_hook(o_node)
    ):
        return True
    return False


@node("cstring")
@parsing_context
def c_string(o_node):
    if capture(Parsing.o_base_parser.read_c_string, "string", o_node) and c_string_hook(o_node):
        return True
    return False


@node("cchar")
@parsing_context
def c_char(o_node):
    if capture(Parsing.o_base_parser.read_c_char, "string", o_node) and c_char_hook(o_node):
        return True
    return False


def car_rule(o_node):
    """
    car::= '"' ->'"' | "'" -> "'"
    ;
    """
    return alt(NonTerminal(c_string, o_node), NonTerminal(c_char, o_node))


@node("range")
@parsing_context
def range_rule(o_node):
    """
    range ::= car ".." car
    ;
    """
    if (
        capture(Parsing.o_base_parser.read_c_char, "from", o_node)
        and Parsing.o_base_parser.read_text("..")
        and alt(
            Capture(Parsing.o_base_parser.read_c_char, "to", o_node),
            Error("Range incomplete."),
        )
        and range_hook(o_node)
    ):
        return True
    return False


@node("expr")
@parsing_context
def expr_rule(o_node):
    """
    expr ::= '[' clauses ']'
    ;
    """
    if (
        Parsing.o_base_parser.read_char("[")
        and alt(NonTerminal(clauses_rule, o_node), Error("Empty expression."))
        and alt(ReadChar("]"), Error("']' missing."))
        and expr_hook(o_node)
    ):
        return True
    return False


@node("until")
@parsing_context
def until_rule(o_node):
    """
    until ::= "->" terminal
    ;
    """
    if (
        Parsing.o_base_parser.read_text("->")
        and alt(
            NonTerminal(terminal_rule, o_node),
            Error("No expression found after until ('->') sign."),
        )
        and until_hook(o_node)
    ):
        return True
    return False


@node("lookAhead")
@parsing_context
def look_ahead_rule(o_node):
    """
    lookAhead ::= "=" terminal
    ;
    """
    if (
        Parsing.o_base_parser.read_text("=")
        and alt(
            NonTerminal(terminal_rule, o_node),
            Error("No expression found after a look ahead ('=') sign."),
        )
        and lookAheadHook(o_node)
    ):
        return True
    return False


@node("terminal")
@parsing_context
def terminal_rule(o_node):
    """
    terminal ::=
              ['~'|'!']?
              [directive | expr | range, car]
              [
                ['+'|'?'|'*']
                |
                terminal_range
              ]?
    ;
    """
    if (
        zero_or_one(
            Alt(
                Capture(ReadChar("!"), "not", o_node),
                Capture(ReadChar("~"), "not", o_node),
            )
        )
        and alt(
            NonTerminal(directive_rule, o_node),
            NonTerminal(expr_rule, o_node),
            NonTerminal(range_rule, o_node),
            NonTerminal(car_rule, o_node),
        )
        and zero_or_one(
            Alt(
                Alt(
                    Capture(ReadChar("*"), "multiplier", o_node),
                    Capture(ReadChar("+"), "multiplier", o_node),
                    Capture(ReadChar("?"), "multiplier", o_node),
                    NonTerminal(read_terminal_range_rule, o_node),
                )
            )
        )
        and terminal_hook(o_node)
    ):
        return True
    return False


# FIXME : complete error gestion


@node("terminal_range")
@parsing_context
def read_terminal_range_rule(o_node):
    """
    terminal_range = '{' #num ["," #num]? '}'
    ;
    """
    if (
        Parsing.o_base_parser.read_char("{")
        and alt(
            Capture(Parsing.o_base_parser.read_integer, "from", o_node),
            Error("No number found in terminal Range."),
        )
        and zero_or_one(
            ReadChar(","),
            Alt(
                Capture(Parsing.o_base_parser.read_integer, "to", o_node),
                Error("Second number missing in terminal range."),
            ),
        )
        and Parsing.o_base_parser.read_char("}")
        and read_terminal_range_hook(o_node)
    ):
        return True
    return False
