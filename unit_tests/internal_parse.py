import unittest
from pyrser.parsing.python.AsciiParseWrapper import AsciiParseWrapper

class InternalParse_Test(unittest.TestCase):
    @classmethod
    def setUpClass(c_internal_parse_class):
        c_internal_parse_class.o_parse = AsciiParseWrapper()
        c_internal_parse_class.o_parse.pop_stream()

    def test_read_identifier(self):
        """
        Basic test for identifier parsing
        """
        o_parse = InternalParse_Test.o_parse
        o_parse.parsed_stream("ceci est un test", s_name="root")
        self.assertTrue(
            o_parse.set_tag("sujet") and o_parse.read_identifier(),
            "failed in read_identifier for sujet",
        )
        sujet = o_parse.get_tag("sujet")
        self.assertEqual(sujet, "ceci", "failed in capture sujet")
        self.assertTrue(
            o_parse.set_tag("verbe") and o_parse.read_identifier(),
            "failed in read_identifier for verbe",
        )
        verbe = o_parse.get_tag("verbe")
        self.assertEqual(verbe, "est", "failed in capture verbe")
        self.assertTrue(
            o_parse.set_tag("other") and o_parse.read_until_EOF(),
            "failed in read_identifier for other",
        )
        reste = o_parse.get_tag("other")
        self.assertEqual(reste, "un test", "failed in capture other")

    def test_read_integer(self):
        """
        Basic test for integer parsing
        """
        o_parse = InternalParse_Test.o_parse
        o_parse.parsed_stream("12 333 44444444444444444444444444", s_name="root")
        self.assertTrue(
            o_parse.set_tag("n1") and o_parse.read_integer(), "failed in read_integer for n1"
        )
        n1 = o_parse.get_tag("n1")
        self.assertEqual(n1, "12", "failed in capture n1")
        self.assertTrue(
            o_parse.set_tag("n2") and o_parse.read_integer(), "failed in read_integer for n2"
        )
        n2 = o_parse.get_tag("n2")
        self.assertEqual(n2, "333", "failed in capture n2")
        self.assertTrue(
            o_parse.set_tag("n3") and o_parse.read_integer(), "failed in read_integer for n3"
        )
        n3 = o_parse.get_tag("n3")
        self.assertEqual(n3, "44444444444444444444444444", "failed in capture n3")

    def test_linecol(self):
        """
        Basic test for line/col calculation
        """
        o_parse = InternalParse_Test.o_parse
        o_parse.parsed_stream("X\nXX\nXXX\n")
        line = o_parse.get_line_nbr()
        col = o_parse.get_column_nbr()
        self.assertTrue(line == 1 and col == 1, "failed line/col at beginning")
        o_parse.inc_pos()
        o_parse.inc_pos()
        line = o_parse.get_line_nbr()
        col = o_parse.get_column_nbr()
        self.assertTrue(line == 2 and col == 1, "failed line/col at second")
        o_parse.inc_pos()
        o_parse.inc_pos()
        o_parse.inc_pos()
        line = o_parse.get_line_nbr()
        col = o_parse.get_column_nbr()
        self.assertTrue(line == 3 and col == 1, "failed line/col at third")
        o_parse.inc_pos()
        o_parse.inc_pos()
        col = o_parse.get_column_nbr()
        self.assertTrue(line == 3 and col == 3, "failed line/col at col")
        o_parse.inc_pos()
        o_parse.inc_pos()
        line = o_parse.get_line_nbr()
        col = o_parse.get_column_nbr()
        self.assertTrue(line == 4 and col == 1, "failed line/col at forth")

    def test_read_c_char(self):
        """
        Basic test for read_c_char
        """
        o_parse = InternalParse_Test.o_parse
        o_parse.parsed_stream("'c' '\\t'", s_name="root")
        self.assertTrue(
            o_parse.set_tag("c1") and o_parse.read_c_char(), "failed in read_c_char for c1"
        )
        c1 = o_parse.get_tag("c1")
        self.assertEqual(c1, "'c'", "failed in capture c1")
        self.assertTrue(
            o_parse.set_tag("c2") and o_parse.read_c_char(), "failed in read_c_char for c2"
        )
        c2 = o_parse.get_tag("c2")
        self.assertEqual(c2, "'\\t'", "failed in capture c2")

    def test_read_c_string(self):
        """
        Basic test for read_c_string
        """
        o_parse = InternalParse_Test.o_parse
        o_parse.parsed_stream(
            '"premiere chaine" "deuxieme chaine\\n" "troisieme chainee \\"."',
            s_name="root",
        )
        self.assertTrue(
            o_parse.set_tag("s1") and o_parse.read_c_string(), "failed in read_c_string for s1"
        )
        s1 = o_parse.get_tag("s1")
        self.assertEqual(s1, '"premiere chaine"', "failed in capture s1")
        self.assertTrue(
            o_parse.set_tag("s2") and o_parse.read_c_string(), "failed in read_c_string for s2"
        )
        s2 = o_parse.get_tag("s2")
        self.assertEqual(s2, '"deuxieme chaine\\n"', "failed in capture s2")
        self.assertTrue(
            o_parse.set_tag("s3") and o_parse.read_c_string(), "failed in read_c_string for s3"
        )
        s3 = o_parse.get_tag("s3")
        self.assertEqual(s3, '"troisieme chainee \\"."', "failed in capture s3")
