# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fossil(AutotoolsPackage):
    """Fossil.

    Fossil is a simple, high-reliability, distributed software
    configuration management system.
    """

    homepage = "https://fossil-scm.org/"
    url = "https://github.com/drdcd/fossil-scm"

    maintainers("eschnett")

    license("BSD-2-Clause")

    version(
        "2.18",
        url="https://fossil-scm.org/home/tarball/84f25d7eb10c0714109d69bb2809abfa8b4b5c3d73b151a5b10df724dacd46d8/fossil-src-2.18.tar.gz",
        sha256="300c1d5cdd6224ec6e8c88ab3f38d50f80e4071b503731b75bd61274cf310733",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openssl")
