# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cloc(Package):
    """Count, or compute differences of, physical lines of source code in the
    given files (may be archives such as compressed tarballs or zip files)
    and/or recursively below the given directories."""

    homepage = "https://github.com/AlDanial/cloc/"
    url = "https://github.com/AlDanial/cloc/archive/v1.90.tar.gz"

    license("GPL-2.0")

    version("2.00", sha256="ed2422fb5d35b65379d0e63875d78a9f6037e711de47db806d4cb204dddfcc9c")
    version("1.96.1", sha256="f0551d98dcce9ca2e78b984adf8e8cc7c6002037a1155e5294338c435e4a1af1")
    version("1.90", sha256="60b429dd2aa5cd65707b359dcbcbeb710c8e4db880886528ced0962c67e52548")
    version("1.84", sha256="c3f0a6bd2319110418ccb3e55a7a1b6d0edfd7528bfd2ae5d530938abe90f254")
    version("1.80", sha256="082f53530eee3f9ee84ec449eca59a77ff114250cd7daf9519679537b5b21d67")
    version("1.74", sha256="55ac423d5766c74236700a47838ed66bea47ba42e1d594fdd894074ba3eb0567")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("perl")

    def install(self, spec, prefix):
        # rewrite the script's #! line to call the perl dependency
        shbang = "#!" + spec["perl"].command.path
        filter_file(r"^#!/usr/bin/env perl", shbang, "cloc")
        filter_file(r"^#!/usr/bin/env perl", shbang, "sqlite_formatter")

        # cloc doesn't have a build system. We have to do our own install here.
        mkdirp(prefix.bin)
        install("cloc", join_path(prefix.bin, "cloc"))
        install("sqlite_formatter", join_path(prefix.bin, "sqlite_formatter"))
        install("./LICENSE", f"{prefix}")
        install("./README.md", f"{prefix}")
