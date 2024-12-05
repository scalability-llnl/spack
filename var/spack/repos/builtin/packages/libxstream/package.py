# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxstream(Package):
    """LIBXSTREAM is a library to work with streams, events, and code regions
    that are able to run asynchronous while preserving the usual stream
    conditions."""

    homepage = "https://github.com/hfp/libxstream"
    url = "https://github.com/hfp/libxstream/archive/0.9.0.tar.gz"

    license("BSD-3-Clause")

    version("0.9.0", sha256="03365f23b337533b8e5a049a24bc5a91c0f1539dd042ca5312abccc8f713b473")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def patch(self):
        kwargs = {"ignore_absent": False, "backup": True, "string": True}
        makefile = FileFilter("Makefile.inc")

        makefile.filter("CC =", "CC ?=", **kwargs)
        makefile.filter("CXX =", "CXX ?=", **kwargs)
        makefile.filter("FC =", "FC ?=", **kwargs)

    def install(self, spec, prefix):
        make()
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
        install_tree("documentation", prefix.share + "/libxstream/doc/")
