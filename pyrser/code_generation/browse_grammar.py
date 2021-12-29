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

from pyrser.code_generation.helper import CodeGenerationHelper


class BrowseGrammar(object):
    def __init__(self, d_lang_conf):
        self.s_res = ""
        self.d_lang_conf = d_lang_conf
        self.o_helper = CodeGenerationHelper(d_lang_conf)

    def browse_multiplier(self, o_multiplier):
        if o_multiplier["multiplier"] == "expression":
            browse_clauses(o_multiplier["terminal"]["clauses"])
        else:
            browse_terminal(o_multiplier["terminal"])

    def browse_alternative(self, l_alternative):
        for i_alternative in l_alternative:
            self.lang_terminal(i_alternative)

    def browse_clauses(self, l_clauses):
        n_count = 0
        for i_alternative in l_clauses["alternatives"]:
            self.lang_alternative(n_count, i_alternative)
            n_count += 1

    def browse_rule(self, o_rule, o_callback):
        o_callback(o_rule["clauses"])

    def browse_rule_directives(self, l_rule_directives, o_callback):
        for rule_directive in l_rule_directives:
            o_callback(rule_directive)

    def browse_hooks(self, o_grammar, o_callback):
        for i_hook in o_grammar["hooks"]:
            o_callback(o_grammar["name"], i_hook)

    def browse_wrappers(self, o_grammar, o_callback):
        for i_wrapper in o_grammar["wrappers"]:
            o_callback(o_grammar["name"], i_wrapper)

    def browse_rules(self, s_grammar_name, l_rules, o_callback):
        for i_rule in l_rules:
            o_callback(s_grammar_name, i_rule)
