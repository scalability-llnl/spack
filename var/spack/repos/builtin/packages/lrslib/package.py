# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lrslib(Package):
    """lrslib Ver 6.2 is a self-contained ANSI C implementation of the
    reverse search algorithm for vertex enumeration/convex hull
    problems and comes with a choice of three arithmetic packages"""

    homepage = "http://cgm.cs.mcgill.ca/~avis/C/lrs.html"
    url = "http://cgm.cs.mcgill.ca/~avis/C/lrslib/archive/lrslib-062.tar.gz"

    license("GPL-2.0-only")

    version("6.2", sha256="adf92f9c7e70c001340b9c28f414208d49c581df46b550f56ab9a360348e4f09")
    version("6.1", sha256="6d5b30ee67e1fdcd6bf03e14717616f18912d59b3707f6d53f9c594c1674ec45")
    version("6.0", sha256="1a569786ecd89ef4f2ddee5ebc32e321f0339505be40f4ffbd2daa95fed1c505")
    version("5.1", sha256="500893df61631944bac14a76c6e13fc08e6e729727443fa5480b2510de0db635")
    version("4.3", sha256="04fc1916ea122b3f2446968d2739717aa2c6c94b21fba1f2c627fd17fcf7a963")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Note: lrslib can also be built with Boost, and probably without gmp

    # depends_on("boost")
    depends_on("gmp")
    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")
    # Ref: https://github.com/mkoeppe/lrslib/commit/2e8c5bd6c06430151faea5910f44aa032c4178a9
    patch("fix-return-value.patch")

    def url_for_version(self, version):
        url = "http://cgm.cs.mcgill.ca/~avis/C/lrslib/archive/lrslib-0{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = [
            "-f",
            "Makefile.spack",
            "PREFIX=%s" % prefix,
            # "BOOST_PREFIX=%s" % spec["boost"].prefix,
            "GMP_PREFIX=%s" % spec["gmp"].prefix,
        ]
        make(*makeargs)
        make("install", *makeargs)
