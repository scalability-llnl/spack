# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bliss(Package):
    """bliss: A Tool for Computing Automorphism Groups and Canonical
    Labelings of Graphs"""

    homepage = "http://www.tcs.hut.fi/Software/bliss/"
    url = "http://www.tcs.hut.fi/Software/bliss/bliss-0.73.zip"

    license("LGPL-3.0-only")

    version("0.73", sha256="f57bf32804140cad58b1240b804e0dbd68f7e6bf67eba8e0c0fa3a62fd7f0f84")

    # Note: Bliss can also be built without gmp, but we don't support this yet

    depends_on("gmp")
    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def install(self, spec, prefix):
        filter_file("__DATE__", " __DATE__ ", "bliss.cc")
        # The Makefile isn't portable; use our own instead
        makeargs = [
            "-f",
            "Makefile.spack",
            "PREFIX=%s" % prefix,
            "GMP_PREFIX=%s" % spec["gmp"].prefix,
        ]
        make(*makeargs)
        make("install", *makeargs)
