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

from pyrser.parsing.parsing_context import parsing_context
from pyrser.parsing.dont_consume import dont_consume

from pyrser.parsing import Parsing


class SlotExpressionFunctor(type):
    def __new__(o_cls, s_name, l_bases, d_dct):
        """
        A metaclass to slot the bnf primitive functors.
        """
        d_dct["__slots__"] = {"__l_predicats": None}
        return type.__new__(o_cls, s_name, l_bases, d_dct)


def all_true(*l_predicats):
    """
    Check if i_each predicats is True
    """
    for i_each in l_predicats:
        if i_each() == False:
            return False
    return True


@parsing_context
def zero_or_one(*l_predicats):
    """
    []? bnf primitive
    """
    all_true(*l_predicats)
    return True


@parsing_context
def zero_or_n(*l_predicats):
    """
    []* bnf primitive
    """
    if all_true(*l_predicats):
        while all_true(*l_predicats):
            pass
    return True


@parsing_context
def one_or_n(*l_predicats):
    """
    []+ bnf primitive
    """
    if all_true(*l_predicats):
        while all_true(*l_predicats):
            pass
        return True
    return False


def alt(*l_predicats):
    """
    [] | [] bnf primitive
    """
    for i_each in l_predicats:
        if i_each():
            return True
    return False


@parsing_context
def expression(*l_predicats):
    """
    [] bnf primitive
    """
    return all_true(*l_predicats)


@parsing_context
def until(*l_predicats):
    """
    ->[] bnf primitive
    """
    while all_true(*l_predicats) == False:
        Parsing.o_base_parser.inc_pos()
        if Parsing.o_base_parser.read_eof():
            return False
    return True


@dont_consume
def negation(*l_predicats):
    """
    ![] bnf primitive
    """
    if all_true(*l_predicats):
        return False
    return True


@parsing_context
def complement(*l_predicats):
    """
    ~[] bnf primitive
    """
    if all_true(*l_predicats):
        return False
    Parsing.o_base_parser.inc_pos()
    return True


@dont_consume
def look_ahead(*l_predicats):
    """
    =[] bnf primitive
    """
    return all_true(*l_predicats)


# FIXME : context pb?


@parsing_context
def n(o_predicat, n_from, n_to=None):
    """
    {} bnf primitive
    """
    if n_to == None:
        n_to = n_from

    n_count = 0
    n_index = 0

    while n_index < n_to:
        if o_predicat() == True:
            n_count += 1
        n_index += 1

    if n_to == None:
        return n_count == n_from
    return n_count >= n_from and n_count <= n_to


##### functors:


class ZeroOrOne(metaclass=SlotExpressionFunctor):
    """
    []? bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return zero_or_one(*self.__l_predicats)


class ZeroOrN(metaclass=SlotExpressionFunctor):
    """
    []* bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return zero_or_n(*self.__l_predicats)


class OneOrN(metaclass=SlotExpressionFunctor):
    """
    []+ bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return one_or_n(*self.__l_predicats)


class Expression(metaclass=SlotExpressionFunctor):
    """
    [] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return expression(*self.__l_predicats)


class Alt(metaclass=SlotExpressionFunctor):
    """
    [] | [] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return alt(*self.__l_predicats)


class Until(metaclass=SlotExpressionFunctor):
    """
    ->[] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return until(*self.__l_predicats)


class Negation(metaclass=SlotExpressionFunctor):
    """
    ![] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return negation(*self.__l_predicats)


class Complement(metaclass=SlotExpressionFunctor):
    """
    ~[] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return complement(*self.__l_predicats)


class LookAhead(object, metaclass=SlotExpressionFunctor):
    """
    =[] bnf primitive as a functor
    """

    def __init__(self, *l_predicats):
        self.__l_predicats = l_predicats

    def __call__(self):
        return look_ahead(*self.__l_predicats)


class N:
    """
    {} bnf primitive as a functor
    """

    def __init__(self, o_predicat, n_from, n_to=None):
        self.__o_predicat = o_predicat
        self.__n_from = n_from
        self.__n_to = n_to

    def __call__(self):
        return n(self.__o_predicat, self.__n_from, self.__n_to)
