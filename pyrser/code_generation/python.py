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

from pyrser.code_generation.procedural import *
from pyrser.code_generation.docstring import Docstring

# FIXME : transform all this into templates

class Python(Procedural):
    def __init__(self, d_lang_conf):
        super(Python, self).__init__(d_lang_conf)
        self.__o_docstring = Docstring(self)

    def lang_range(self, range):
        if not self.o_helper.in_recurse():
            self.s_res += self.o_helper.base_parser_access()
        self.s_res += "%s(%s, %s)" % (
            self.capitalize_if_recurse(self.o_helper.builtin("range")),
            range["from"],
            range["to"],
        )

    def lang_directive(self, directive):
        self.s_res += "%s%s" % (
            self.o_helper.base_parser_access(),
            self.o_helper.builtin(directive["name"]),
        )
        if not self.o_helper.in_recurse():
            self.s_res += "()"

    def lang_non_terminal(self, non_terminal):
        if not self.o_helper.in_recurse():
            self.s_res += "%s%s_rule(oNode)" % (
                self.o_helper.access_instance(),
                non_terminal["name"],
            )
        else:
            self.s_res += "NonTerminal(%s%s_rule, oNode)" % (
                self.o_helper.access_instance(),
                non_terminal["name"],
            )

    def lang_wrapper(self, wrapper):
        name = wrapper["name"]
        if name == "_": # special case for the wrapper name '_' (_wrapper)
            name = ""

        if not self.o_helper.in_recurse():
            self.s_res += "%s%s_wrapper" % (
                self.o_helper.access_instance(),
                name,
            )
            self.unary(wrapper)
            self.s_res += ",oNode"
        else:
            self.s_res += "Hook(%s%s_wrapper," % (
                self.o_helper.access_instance(),
                name,
            )
            self.unary(wrapper, False)
            self.s_res += "),oNode"
        if "param" in wrapper:
            self.s_res += ", %s" % wrapper["param"]
        self.s_res += ")"

    def lang_hook(self, hook):
        if not self.o_helper.in_recurse():
            self.s_res += "%s%s_hook(oNode" % (
                self.o_helper.access_instance(),
                hook["name"],
            )
            if "param" in hook:
                self.s_res += ", %s" % hook["param"]
        else:
            self.s_res += "Hook("
            self.s_res += self.o_helper.access_instance()
            self.s_res += "%s_hook, oNode" % hook["name"]
            if "param" in hook:
                self.s_res += ", %s" % hook["param"]
        self.s_res += ")"

    def lang_aggregation(self, aggregation):
        if self.o_helper.in_recurse():
            self.s_res += "NonTerminal(%s()%s%s_rule, oNode)" % (
                aggregation["name"],
                self.o_helper.access_operator(),
                aggregation["non_terminal"]["name"],
            )
        else:
            self.s_res += "%s()%s%s_rule(oNode)" % (
                aggregation["name"],
                self.o_helper.access_operator(),
                aggregation["non_terminal"]["name"],
            )

    def lang_cchar(self, char):
        if not self.o_helper.in_recurse():
            self.s_res += self.o_helper.base_parser_access()
        self.s_res += self.capitalize_if_recurse(self.o_helper.builtin("readThisChar"))
        self.s_res += "(%s)" % char["string"]

    def lang_cstring(self, text):
        if not self.o_helper.in_recurse():
            self.s_res += self.o_helper.base_parser_access()
        self.s_res += self.capitalize_if_recurse(self.o_helper.builtin("readThisText"))
        self.s_res += "(%s)" % text["string"]

    def lang_rule_directive(self, rule):
        if "rule_directive" in rule["prototype"]:
            for rule_directive in rule["prototype"]["rule_directive"]:
                self.s_res += "      @%s" % rule_directive["name"]
                if "param" in rule_directive:
                    self.s_res += "(%s)" % {{rule_directive.param}}
                self.s_res += "\n"

    def lang_rule(self, grammar_name, rule):
        self.o_helper.set_global("current_rule", rule["prototype"]["name"])
        #      @staticmethod
        self.s_res += (
            """
      @parsing_context
      @node.node('%s')
"""
            % rule["prototype"]["name"]
        )
        self.lang_rule_directive(rule)
        self.s_res += (
            """      def %s_rule(self, oNode):
          \"\"\"
          """
            % rule["prototype"]["name"]
        )
        self.s_res += self.__o_docstring.lang_rule(grammar_name, rule)
        self.s_res += '''          """
          return (True
'''
        self.browse_rule(rule, self.lang_clauses)
        self.s_res += ")\n"

    def translation(self, s_grammar_name, l_rules):
        self.s_res = """class %sGrammar:\n""" % s_grammar_name
        self.browse_rules(s_grammar_name, l_rules, self.lang_rule)
        return self.s_res
