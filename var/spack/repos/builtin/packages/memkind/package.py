# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Memkind(AutotoolsPackage):
    """The memkind library is a user extensible heap manager built on top of
    jemalloc which enables control of memory characteristics and a partitioning
    of the heap between kinds of memory. The kinds of memory are defined by
    operating system memory policies that have been applied to virtual address
    ranges. Memory characteristics supported by memkind without user extension
    include control of NUMA and page size features. The jemalloc non-standard
    interface has been extended to enable specialized arenas to make requests
    for virtual memory from the operating system through the memkind partition
    interface. Through the other memkind interfaces the user can control and
    extend memory partition features and allocate memory while selecting
    enabled features."""

    homepage = "https://github.com/memkind/memkind"
    url = "https://github.com/memkind/memkind/archive/v1.7.0.tar.gz"

    license("BSD-3-Clause")

    version("1.14.0", sha256="ab366b20b5a87ea655483631fc762ba6eb59eb6c3a08652e643f1ee3f06a6a12")
    version("1.13.0", sha256="3f0d919b61fdd4d2ebce14e0b7dbb856e2144138778940107c13549523f3bdc0")
    version("1.12.0", sha256="b0781d493dec0da0089884fd54bcfdde03311019c56f90505ed0b884100bfbad")
    version("1.10.1", sha256="c203615d964a0bb151756ad8a5c9565391ee77d79c1f8b59d2ea8ff87989b294")
    version("1.10.0", sha256="0399a1d6a179d065cdbc59bb687fcd00d09dfbb1789334acfdf7431a48707d26")
    version("1.9.0", sha256="491f21c8d09904ad23700c755b9134fbed08bf227506c2fde135429688158b84")
    version("1.8.0", sha256="8b57c5afa8afa6793e4662322e37620bbb11f119cd8d29654ec00945bbe13a17")
    version("1.7.0", sha256="5048eaaa1bc484203c685a019f3f428ab6c9b1cf94ef6d264e299bc0127ec572")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("numactl")

    # memkind includes a copy of jemalloc; see
    # <https://github.com/memkind/memkind#jemalloc>.
    conflicts("jemalloc")

    # https://github.com/spack/spack/issues/37292
    parallel = False

    def patch(self):
        with open("VERSION", "w") as version_file:
            version_file.write(f"{self.version}\n")
        # Remove `-Werror`
        filter_file(r" -Werror ", " ", "Makefile.am", "configure.ac")

    @run_before("autoreconf")
    def build_jemalloc(self):
        if os.path.exists("build_jemalloc.sh"):
            bash = which("bash")
            bash("./build_jemalloc.sh")

    def autoreconf(self, spec, prefix):
        if os.path.exists("autogen.sh"):
            bash = which("bash")
            bash("./autogen.sh")
