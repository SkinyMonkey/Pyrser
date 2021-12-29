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

from pyrser.code_generation.browse_grammar import BrowseGrammar


class Procedural(BrowseGrammar):
    def __init__(self, d_lang_conf):
        super(Procedural, self).__init__(d_lang_conf)

    def wrap_context(self, o_callback, o_argument):
        self.o_helper.push_count(0, 1)
        self.o_helper.inc_depth()
        self.o_helper.push_alt(False)
        o_callback(o_argument)
        self.o_helper.pop_alt()
        self.o_helper.dec_depth()
        self.o_helper.pop_count()

    def add_open_parenthesis(self, o_target):
        if o_target["terminal"]["type"] in ("multiplier", "alt"):
            self.s_res += "(\\\n"
            self.lang_terminal(o_target["terminal"])
        else:
            self.s_res += "("
            self.lang_terminal(o_target["terminal"], False)

    def unary(self, o_target, b_newline=True):
        self.wrap_context(self.add_open_parenthesis, o_target)
        if (
            o_target["terminal"]["type"] in ("multiplier", "alt", "terminal_range")
            and b_newline
        ):
            self.s_res += "\n"
            self.s_res += self.o_helper.indent()

    def capitalize_if_recurse(self, s_to_capitalize):
        if self.o_helper.in_recurse():
            # FIXME : temporary
            name = ''.join(word.title() for word in s_to_capitalize.split('_'))
            return self.o_helper.capitalize(name)
        return s_to_capitalize

    def lang_alternative_terminal(self, o_alt):
        self.s_res += self.capitalize_if_recurse(self.o_helper.alt())
        self.s_res += "(\\\n"
        self.o_helper.push_alt(True, len(o_alt["alternatives"]))
        self.o_helper.inc_depth()
        self.browse_clauses(o_alt)
        self.s_res += ")"
        self.o_helper.dec_depth()
        self.o_helper.pop_alt()

    def lang_terminal_range(self, terminal):
        self.s_res += self.capitalize_if_recurse(self.o_helper.multiplier("{}"))
        self.unary(terminal)
        self.s_res += ", %s" % terminal["from"]
        if "to" in terminal:
            self.s_res += ", %s" % terminal["to"]
        self.s_res += ")"

    def lang_not(self, negation):
        self.s_res += self.capitalize_if_recurse(self.o_helper.not_(negation["not"]))
        self.unary(negation, False)
        self.s_res += ")"

    def lang_multiplier(self, multiplier):
        self.s_res += self.capitalize_if_recurse(
            self.o_helper.multiplier(multiplier["multiplier"])
        )
        if multiplier["multiplier"] == "[]":
            self.s_res += "(\\\n"
            self.wrap_context(self.browse_clauses, multiplier["terminal"]["clauses"])
        else:
            self.unary(multiplier, False)
        self.s_res += ")"

    def lang_capture(self, capture):
        self.s_res += self.capitalize_if_recurse("capture")
        self.unary(capture)
        self.s_res += ', "%s", oNode)' % capture["name"]

    def lang_until(self, until):
        self.s_res += self.capitalize_if_recurse("until")
        self.unary(until, False)
        self.s_res += ")"

    def lang_look_ahead(self, look_ahead):
        self.s_res += capitalizeIfRecurse("lookAhead")
        unary(look_ahead, False)
        self.s_res += ")"

    def lang_syntax(self, indent=True):
        if indent == True:
            self.s_res += self.o_helper.indent()
        if not self.o_helper.in_recurse():
            self.s_res += self.o_helper.keyword("and")
        if self.o_helper.in_recurse() and (
            self.o_helper.count() > 0 or self.o_helper.alt_count() > 0
        ):
            self.s_res += ","
        else:
            self.s_res += " "

    def lang_terminal(self, terminal, indent=True):
        self.lang_syntax(indent)
        getattr(self, "lang_%s" % terminal["type"])(terminal)
        if (
            self.o_helper.count() < self.o_helper.length() - 1
            or self.o_helper.alt_count() < self.o_helper.alt_length() - 1
        ):
            self.s_res += "\\\n"
            self.o_helper.inc_count()

    def lang_alternative(self, loop, alternative):
        self.o_helper.push_count(0, len(alternative))
        self.browse_alternative(alternative)
        self.o_helper.inc_alt_count()
        self.o_helper.pop_count()

    def lang_clauses(self, clauses):
        self.o_helper.push_alt(False)
        self.browse_clauses(clauses)
        self.o_helper.pop_alt()
