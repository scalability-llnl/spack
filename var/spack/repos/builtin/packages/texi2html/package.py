# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Texi2html(MakefilePackage):
    """A highly customizable texinfo to HTML and other formats translator."""

    homepage = "https://www.nongnu.org/texi2html/"
    url = "http://download.savannah.nongnu.org/releases/texi2html/texi2html-5.0.tar.gz"

    license("GPL-2.0-or-later", checked_by="Buldram")

    version("5.0", sha256="e60edd2a9b8399ca615c6e81e06fa61946ba2f2406c76cd63eb829c91d3a3d7d")

    depends_on("gettext", type="build")
    depends_on("perl", type=("build", "run"))

    def edit(self, spec, prefix):
        Executable("./configure")("--prefix=" + prefix)

        perl_files = FileFilter(
            "gettext_to_separated.pl",
            "manage_i18n.pl",
            "parse_8bit_makeinfo_maps.pl",
            "regenerate_documentlanguages.pl",
            "separated_to_hash.pl",
            "lib/Unicode-EastAsianWidth/Makefile.PL",
            "lib/Unicode-EastAsianWidth/t/0-signature.t",
            "lib/Unicode-EastAsianWidth/t/1-basic.t",
        )
        perl_files.filter("/usr/bin/perl", spec["perl"].prefix.bin.perl, string=True)

        set_executable("install-sh")
