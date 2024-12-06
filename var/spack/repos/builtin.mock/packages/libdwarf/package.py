# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ["libdwarf", "dwarfdump2"]


class Libdwarf(Package):
    homepage = "http://www.prevanders.net/dwarf.html"
    url = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
    list_url = homepage

    version("20130729", md5="64b42692e947d5180e162e46c689dfbf")
    version("20130207", md5="0123456789abcdef0123456789abcdef")
    version("20111030", md5="0123456789abcdef0123456789abcdef")
    version("20070703", md5="0123456789abcdef0123456789abcdef")

    depends_on("libelf")

    def install(self, spec, prefix):
        touch(prefix.libdwarf)
