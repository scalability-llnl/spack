# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Fribidi(AutotoolsPackage):
    """GNU FriBidi: The Free Implementation of the Unicode Bidirectional
    Algorithm."""

    homepage = "https://github.com/fribidi/fribidi"
    url = "https://github.com/fribidi/fribidi/releases/download/v1.0.5/fribidi-1.0.5.tar.bz2"

    license("LGPL-2.1-or-later")

    version("1.0.12", sha256="0cd233f97fc8c67bb3ac27ce8440def5d3ffacf516765b91c2cc654498293495")
    version("1.0.8", sha256="94c7b68d86ad2a9613b4dcffe7bbeb03523d63b5b37918bdf2e4ef34195c1e6c")
    version("1.0.5", sha256="6a64f2a687f5c4f203a46fa659f43dd43d1f8b845df8d723107e8a7e6158e4ce")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        url = "https://github.com/fribidi/fribidi/releases/download/"
        ext = ".tar.bz2" if version <= Version("1.0.8") else ".tar.xz"
        return url + "/v%s/fribidi-%s%s" % (version, version, ext)
