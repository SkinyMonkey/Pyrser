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

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from os.path import abspath
from os import chdir

compile_path = abspath(".") + "/pyrser/parsing/cpp/"

ascii_parse = Extension(
    "ascii_parse",
    include_dirs=[
        "/usr/include",
        "/usr/local/include",
        compile_path,
        compile_path + "csrcs",
    ],
    sources=[
        compile_path + "ascii_parse.pyx",
        compile_path + "csrcs/asciiParsePrimitives.cpp",
        compile_path + "csrcs/Stream.cpp",
    ],
    # Uncomment to add GDB debug symbols.
    extra_compile_args=["-g3"],
    extra_link_args=["-g3"],
    language="c++",
)

setup(cmdclass={"build_ext": build_ext}, ext_modules=[ascii_parse])
