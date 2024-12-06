# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dyninst(Package):
    homepage = "https://paradyn.org"
    url = "http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz"

    version(
        "8.2",
        md5="0123456789abcdef0123456789abcdef",
        url="http://www.paradyn.org/release8.2/DyninstAPI-8.2.tgz",
    )
    version(
        "8.1.2",
        md5="fedcba9876543210fedcba9876543210",
        url="http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz",
    )
    version(
        "8.1.1",
        md5="123456789abcdef0123456789abcdef0",
        url="http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz",
    )

    depends_on("libelf")
    depends_on("libdwarf")

    def install(self, spec, prefix):
        mkdirp(prefix)
        touch(join_path(prefix, "dummyfile"))
