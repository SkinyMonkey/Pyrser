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

from pyrser.code_generation.browse_grammar import *


class Docstring(BrowseGrammar):
    def __init__(self, o_renderer):
        super(Docstring, self).__init__(o_renderer.d_lang_conf)
        self.s_res = ""

    def lang_multiplier(self, multiplier):
        if multiplier["multiplier"] == "[]":
            self.s_res += " ["
            self.browse_clauses(multiplier["terminal"]["clauses"])
            self.s_res += " ]"
        else:
            self.lang_terminal(multiplier["terminal"])
            self.s_res += multiplier["multiplier"]

    def lang_directive(self, terminal):
        self.s_res += " #%s" % terminal["name"]

    def lang_capture(self, terminal):
        self.lang_terminal(terminal["terminal"])
        self.s_res += " :%s" % terminal["name"]

    def lang_non_terminal(self, terminal):
        self.s_res += " %s" % terminal["name"]

    def lang_hook(self, terminal):
        self.s_res += " %%%s" % terminal["name"]

    def lang_wrapper(self, terminal):
        self.s_res += " @%s" % terminal["name"]
        self.lang_terminal(terminal["terminal"])

    def lang_until(self, terminal):
        self.s_res += " ->"
        self.lang_terminal(terminal["terminal"])

    def lang_look_ahead(self, terminal):
        self.s_res += " ="
        self.lang_terminal(terminal["terminal"])

    def lang_cchar(self, terminal):
        self.s_res += " %s" % terminal["string"]

    def lang_cstring(self, terminal):
        self.s_res += " %s" % terminal["string"]

    def lang_not(self, terminal):
        self.s_res += " %s" % terminal["not"]
        self.lang_terminal(terminal["terminal"])

    def lang_aggregation(self, terminal):
        self.s_res += " %s::%s" % (terminal["name"], terminal["non_terminal"]["name"])

    def lang_alternative_terminal(self, terminal):
        self.browse_clauses(terminal)

    def lang_range(self, terminal):
        self.s_res += " %s .. %s" % (terminal["from"], terminal["to"])

    def lang_terminal_range(self, terminal):
        self.lang_terminal(terminal["terminal"])
        self.s_res += "{%s" % (terminal["from"])
        if "to" in terminal:
            self.s_res += ", %s}" % (terminal["to"])
        else:
            self.s_res += "}"

    def lang_terminal(self, terminal):
        getattr(self, "lang_%s" % terminal["type"])(terminal)
        pass

    def lang_alternative(self, n_count, l_alternative):
        if n_count > 0:
            self.s_res += " |"
        self.browse_alternative(l_alternative)

    def lang_clauses(self, clauses):
        self.browse_clauses(clauses)

    def lang_rule_directive(self, rule_directive):
        self.s_res += " @%s" % rule_directive["name"]
        if "params" in rule_directive:
            self.s_res += "(%s" % rule_directive["params"]

    def lang_template_rule_name(self, rule):
        """
        if rule.prototype.has_key('template'):
          if rule.prototype.template.string == '?':
            <{{rule.prototype.template.string}}>
        else:
          <"{{rule.prototype.template.string}}">
        """

    def lang_rule(self, grammar_name, rule):
        self.s_res = "%s::%s" % (grammar_name, rule["prototype"]["name"])
        #    	  lang_template_rule_name(rule)
        # FIXME
        # browse_rule_directives(rule['prototype']['rule_directive'],
        # lang_rule_directive)
        self.s_res += " ::="
        self.browse_rule(rule, self.lang_clauses)
        self.s_res += "\n          ;\n"
        return self.s_res
