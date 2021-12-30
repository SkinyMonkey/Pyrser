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

from pyrser.parsing.python.asciiParseStream import Stream


class AsciiParseWrapper:
    """
    An ascii parsing primitive library.
    """

    def __init__(
        self, s_stream="", s_ignore=" \r\n\t", s_c_line="//", s_c_begin="/*", s_c_end="*/"
    ):
        if len(s_c_line) == 0:
            raise Exception(
                "Line comment open tag should be 1 character long at minimum"
            )
        if len(s_c_begin) < 2 or len(s_c_end) < 2:
            raise Exception(
                "comment open tag and close tag should be 2 character long at minimum."
            )
        self.__d_tag = {}
        self.__l_stream = [Stream(s_stream, "root", s_ignore)]
        self.__s_c_line = s_c_line
        # TODO: Not HERE
        self.__s_c_begin = s_c_begin
        self.__s_c_end = s_c_end
        self.__s_ignore = s_ignore

    ### PRIVATE

    def __get_char(self):
        """
        Return byte pointed by current stream index.
        """
        return self.get_stream().get_char()

    def __get_char_at(self, n_index):
        """
        Return byte pointed by the given index.
        """
        return self.get_stream().get_charAt(n_index)

    def __eof_pos(self):
        """
        Return True if eof is reached.
        """
        return self.get_stream().eof_pos()

    def __line_comment(self):
        """
        Read a one line comment.
        """
        if self.peek_text(self.__s_c_line):
            while self.read_eof() == False and self.__get_char() != "\n":
                self.inc_pos()
            return True
        return False

    def __peek_text_from(self, s_text, n_index):
        """
        Same behaviour as peekText except that it begin at a certain index.
        """
        n_len = len(s_text)
        n_text_index = 0
        while n_index != self.__eof_pos() and n_text_index < n_len:
            if self.__get_char_at(n_index) != s_text[n_text_index]:
                return False
            n_index += 1
            n_text_index += 1
        if n_text_index == n_len:
            return True
        return False

    def __peek_comment(self, n_index):
        """
        Check for the end tag of a comment.
        """
        # FIXME : context save? compare perfs
        n_inner = 0
        while n_index != self.__eof_pos():
            if self.__get_char_at(n_index) == self.__s_c_end[0] and self.__peek_text_from(
                self.__s_c_end, n_index
            ):
                self.get_stream().inc_posOf((n_index - self.index()) + len(self.__s_c_end))
                return n_index
            if self.__get_char_at(n_index) == self.__s_c_begin[0] and self.__peek_text_from(
                self.__s_c_begin, n_index
            ):
                n_index += len(self.__s_c_begin)
                n_inner = self.__peek_comment(n_index)
                if n_inner != 0:
                    n_index = n_inner
            n_index += 1
        return 0

    ### PUBLIC ACCESSOR
    # TODO: READ ONLY

    def not_ignore(self):
        return False

    def get_stream(self):
        """
        Return current used Stream.
        """
        return self.__l_stream[-1]

    def get_name(self):
        """
        Return current Stream name.
        """
        return self.get_stream().get_name()

    def get_stream_len(self):
        """
        Return the len of the current stream.
        """
        return self.__eof_pos()

    def get_column_nbr(self):
        """
        Return the number of column that was parsed.
        """
        return self.get_stream().get_column_nbr()

    def get_line_nbr(self):
        """
        Return the number of line that was parsed.
        """
        return self.get_stream().get_line_nbr()

    def print_stream(self, n_index=0):
        """
        Print current real stream contained.
        """
        return self.get_stream().print_stream(n_index)

    ### PARSING PRIMITIVE

    def peek_char(self, c_c):
        """
        Test if head byte is equal to c and return true else return false.
        """
        return not self.read_eof() and self.__get_char() == c_c

    def peek_text(self, s_text):
        """
        Same as read_text but doesn't consume the stream.
        """
        n_length = len(s_text)
        n_index = self.index()
        n_text_index = 0
        while n_index != self.__eof_pos() and n_text_index < n_length:
            if self.__get_char_at(n_index) != s_text[n_text_index]:
                return False
            n_index += 1
            n_text_index += 1
        return n_index == n_length

    ### READ PRIMITIVE

    def read_char(self, c_c):
        """
        Consume the c head byte, increment current index and return True
        else return False. It use peekchar and it's the same as '' in BNF.
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if self.peek_char(c_c):
            self.inc_pos()
            return self.valid_context()
        return self.restore_context()

    def read_ws(self):
        """
        Consume head byte while it is contained in the WS liste.
        """
        while not self.read_eof():
            if self.__get_char() not in self.get_ws_list():
                # print("<%s> not in <%s>" % (bytes(self.__get_char(), "ascii"), bytes(self.get_ws_list(), "ascii")))
                return True
            self.inc_pos()
        return False

    def read_a_char(self):
        """
        Consume a character if possible.
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if self.index() + 1 < self.__eof_pos():
            c_c = self.__get_char()
            self.inc_pos()
            return self.valid_context()
        return self.restore_context()

    def read_comment(self):
        # TODO: Faux
        """
        Consume all that is between and open and a close comment tag.
        """
        if self.__line_comment():
            return True
        if self.peek_text(self.__s_c_begin) == False:
            return False
        if self.__peek_comment(self.index() + len(self.__s_c_begin)) != 0:
            return True
        raise Exception("No comment close tag found " + self.__s_c_begin + " .")

    def read_ignored(self):
        # TODO: must be a rule forwarder
        """
        Consume comments and whitespace characters.
        """
        self.save_context()
        self.read_ws()
        return self.valid_context()

    def read_eof(self):
        """
        Returns true if reach end of the stream.
        """
        return self.index() >= self.__eof_pos()

    def read_eol(self):
        """
        Return True if the parser can consume an EOL byte sequence.
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        self.read_char("\r")
        if self.read_char("\n"):
            return self.valid_context()
        return self.restore_context()

    def read_until(self, c_c, c_inhibitor="\\"):
        """
        Consume the stream while the c byte is not read, else return false
        ex : if stream is " abcdef ", read_until("d"); consume "abcd".
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        while not self.read_eof():
            if self.peek_char(c_inhibitor):
                self.inc_pos()  # Deletion of the inhibitor.
                self.inc_pos()  # Deletion of the inhibited character.
            if self.peek_char(c_c):
                self.inc_pos()
                return self.valid_context()
            self.inc_pos()
        return self.restore_context()

    def read_until_EOF(self):
        """
        Consume all the stream. Same as EOF in BNF
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        while self.index() != self.__eof_pos():
            self.inc_pos()
        return self.valid_context()

    def read_text(self, s_text):
        """
        Consume a strlen(text) text at current position in the stream
        else return False.
        Same as "" in BNF
        ex : read_text("ls");.
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        n_length = len(s_text)
        n_index = 0
        while not self.read_eof() and n_index < n_length:
            if self.__get_char() != s_text[n_index]:
                return self.restore_context()
            self.inc_pos()
            n_index += 1
        if n_index == n_length:
            return self.valid_context()
        return self.restore_context()

    def read_integer(self):
        """
        Read following BNF rule else return False
        read_integer ::= ['0'..'9']+ ;
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if self.read_eof() == False and self.__get_char().isdigit():
            self.inc_pos()
            while not self.read_eof() and self.__get_char().isdigit():
                self.inc_pos()
            return self.valid_context()
        return self.restore_context()

    def read_identifier(self):
        """
        Read following BNF rule else return False
        read_identifier ::= ['a'..'z'|'A'..'Z'|'_']['0'..'9'|'a'..'z'|'A'..'Z'|'_']* ;
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if not self.read_eof() and (self.__get_char().isalpha() or self.peek_char("_")):
            self.inc_pos()
            while not self.read_eof() and (
                self.__get_char().isalpha()
                or self.__get_char().isdigit()
                or self.peek_char("_")
            ):
                self.inc_pos()
            return self.valid_context()
        return self.restore_context()

    def read_range(self, begin, end):
        """
        Consume head byte if it is >= begin and <= end else return false
        Same as 'a'..'z' in BNF
        """
        self.read_ignored()  # TODO: in engine
        if self.__get_char() >= begin and self.__get_char() <= end:
            self.inc_pos()
            return True
        return False

    def read_c_string(self):
        """
        Read following BNF rule else return False
        '"' -> ['/'| '"']
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if self.read_char('"') and self.read_until('"', "\\"):
            return self.valid_context()
        return self.restore_context()

    def read_c_char(self):
        # TODO: octal digit, hex digit
        """
        Read following BNF rule else return False
        "'" -> [~"/" "'"]
        """
        self.read_ignored()  # TODO: in engine
        self.save_context()
        if self.read_char("'") and self.read_until("'", "\\"):
            return self.valid_context()
        return self.restore_context()

    ### CONTEXT

    def save_context(self):
        """
        Stack the current index position.
        """
        return self.get_stream().save_context()

    def restore_context(self):
        """
        Pop the last index position and set current stream index to this value.
        """
        return self.get_stream().restore_context()

    def valid_context(self):
        """
        Pop all useless contexts to keep one context only.
        """
        return self.get_stream().valid_context()

    ### STREAM

    def parsed_stream(self, s_new_stream, s_name="new", s_ignore=" \r\n\t"):
        """
        Push a new Stream into the parser.
        All subsequent called functions will parse this new stream,
        until the 'pop_stream' function is called.
        """
        self.__l_stream.append(Stream(s_new_stream, s_name, s_ignore))

    def pop_stream(self):
        """
        Pop the last Stream pushed on to the parser stack.
        """
        self.__l_stream.pop()

    def index(self):
        """
        Return the index value.
        This value is used by the parser to point current byte.
        """
        return self.get_stream().index()

    def get_ws_list(self):
        """
        Return a string containing the ignored characters.
        """
        # return self.get_stream().getWsList()
        return self.__s_ignore

    def set_ws_list(self, s_new_ws_list):
        """
        Set the list of caracter ignored by the parser.
        """
        self.get_stream().setWsList(s_new_ws_list)

    def inc_pos(self):
        """
        Increment current index, column and line count.
        Should not be used, or only when sure.
        """
        return self.get_stream().inc_pos()

    # TODO: change for beginTag,endTag,get_tag for multicapture, and typesetting at endTag (i.e: read_c_char,read_c_string need transcoding)
    def set_tag(self, s_name):
        """
        Save the current index under the given name.
        """
        self.read_ignored()  # TODO: in engine
        self.__d_tag[s_name] = self.index()
        return True

    def get_tag(self, s_name):
        """
        Extract the string between the saved index value and the current one.
        """
        return self.get_stream().get_content_relative(self.__d_tag[s_name])

    def get_stream_nbr(self):
        return len(self.__l_stream)
