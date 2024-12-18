# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.boost import Boost


class Polymake(Package):
    """polymake is open source software for research in polyhedral geometry"""

    homepage = "https://polymake.org/doku.php"
    url = "https://polymake.org/lib/exe/fetch.php/download/polymake-3.0r1.tar.bz2"

    license("GPL-2.0-or-later")

    version("3.5", sha256="c649f8536ccef5a5e22b82c514a09278ebcd99d0815aa7170461fe12843109bd")
    version("3.0r2", sha256="e7c0f8e3a45ea288d2fb4ae781a1dcea913ef9c275fed401632cdb11a672d6dc")
    version("3.0r1", sha256="cdc223716b1cc3f4f3cc126089a438f9d12390caeed78291a87565717c7b504d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Note: Could also be built with nauty instead of bliss
    depends_on("bliss")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("cddlib")
    depends_on("gmp")
    depends_on("lrslib")
    depends_on("mpfr")
    depends_on("ninja", type="build", when="@3.2:")
    depends_on("perl")
    depends_on("perl-json")
    depends_on("perl-termreadkey")
    depends_on("perl-term-readline-gnu")
    depends_on("perl-xml-libxml")
    depends_on("perl-xml-libxslt")
    depends_on("perl-xml-writer")
    depends_on("ppl")
    depends_on("ppl@1.2:", when="@3.2:")
    depends_on("readline")

    def install(self, spec, prefix):
        configure(
            "--prefix=%s" % prefix,
            "--with-bliss=%s" % spec["bliss"].prefix,
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-cdd=%s" % spec["cddlib"].prefix,
            "--with-gmp=%s" % spec["gmp"].prefix,
            "--with-lrs=%s" % spec["lrslib"].prefix,
            "--with-mpfr=%s" % spec["mpfr"].prefix,
            "--with-ppl=%s" % spec["ppl"].prefix,
        )
        make()
        make("install")
