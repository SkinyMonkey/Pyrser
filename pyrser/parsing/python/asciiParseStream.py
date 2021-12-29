from copy import copy


class AsciiParseContext:
    def __init__(self, n_index=0, n_col=1, n_line=1, s_ws_list=" \r\n\t"):
        self.n_index = n_index
        self.n_col = n_col
        self.n_line = n_line
        self.s_ws_list = s_ws_list


class Stream:
    def __init__(self, s_string="", s_name="stream", s_ignore=" \r\n\t"):
        self.__neof_pos = len(s_string)
        self.__s_string = s_string
        self.__s_name = s_name
        self.__l_context = [AsciiParseContext()]

    def __context(self):
        return self.__l_context[-1]

    ##### public:
    def save_context(self):
        self.__l_context.append(copy(self.__context()))

    def restore_context(self):
        self.__l_context.pop()
        return False

    def valid_context(self):
        n_ctxt = len(self.__l_context)
        self.__l_context[n_ctxt - 2] = self.__context()
        self.__l_context.pop()
        return True

    def set_ws_list(self, s_ws_list):
        self.__context().s_ws_list = s_ws_list

    def get_ws_list(self):
        return self.__context().s_ws_list

    def index(self):
        return self.__context().n_index

    def inc_pos(self):
        if self.get_char() == "\n":
            self.__context().n_line += 1
            self.__context().n_col = 0
        self.__context().n_col += 1
        self.__context().n_index += 1

    def inc_pos_of(self, n_inc):
        while n_inc > 0:
            self.inc_pos()
            n_inc -= 1

    def get_char(self):
        #        print(self.__context().n_index, "/", len(self.__s_string))
        #        try:
        return self.__s_string[self.__context().n_index]

    #        except Exception as e:
    #            print("FAILED ON GETCHAR:")
    #            print(self.__sString[self.__context().nIndex - 20: self.__context().nIndex - 1])

    def get_char_at(self, n_index):
        return self.__s_string[n_index]

    def eof_pos(self):
        return self.__neof_pos

    def get_column_nbr(self):
        return self.__context().n_col

    def get_line_nbr(self):
        return self.__context().n_line

    def get_name(self):
        return self.__s_name

    def last_read(self):
        if self.__context().n_index > 0:
            return self.__s_string[self.__context().n_index - 1]
        return self.__s_string[0]

    def get_content(self):
        return self.__s_string

    def get_content_absolute(self, begin, end):
        return self.__s_string[begin:end]

    def get_content_relative(self, begin):
        return self.__s_string[begin : self.__context().n_index]

    def print_stream(self, n_index):
        while n_index < self.__neof_pos:
            if self.get_char_at(n_index).isalnum() == False:
                print(("0x%x" % ord(self.get_char_at(n_index))))
            else:
                print((self.get_char_at(n_index)))
        n_index += 1
