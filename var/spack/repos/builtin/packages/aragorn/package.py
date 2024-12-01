# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aragorn(Package):
    """ARAGORN, a program to detect tRNA genes and tmRNA genes in nucleotide
    sequences."""

    homepage = "http://mbio-serv2.mbioekol.lu.se/ARAGORN"
    url = "http://www.ansikte.se/ARAGORN/Downloads/aragorn1.2.41.c"

    version(
        "1.2.41",
        sha256="92a31cc5c0b0ad16d4d7b01991989b775f07d2815df135fe6e3eab88f5e97f4a",
        expand=False,
    )
    version(
        "1.2.38",
        sha256="28aae803d191524b038da582c62c92f190c1925ec69beda56bc21310d8ece522",
        expand=False,
    )
    version(
        "1.2.36",
        sha256="16e5283d890ff74e52e885c9c34b1c2ba2de72770631122e9178079cd06ea8d2",
        expand=False,
    )

    # fix checksum error
    def url_for_version(self, version):
        return f"http://www.ansikte.se/ARAGORN/Downloads/aragorn{version}.c"

    def install(self, spec, prefix):
        cc = Executable(spack_cc)
        cc(
            "-O3",
            "-ffast-math",
            "-finline-functions",
            "-oaragorn",
            "aragorn" + format(spec.version.dotted) + ".c",
        )
        mkdirp(prefix.bin)
        install("aragorn", prefix.bin)
