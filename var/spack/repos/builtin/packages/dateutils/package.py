# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Dateutils(AutotoolsPackage):
    """Dateutils are a bunch of tools that revolve around fiddling with dates
    and times in the command line with a strong focus on use cases that arise
    when dealing with large amounts of financial data."""

    homepage = "https://www.fresse.org/dateutils/"
    url = "https://github.com/hroptatyr/dateutils/releases/download/v0.4.6/dateutils-0.4.6.tar.xz"

    license("BSD-3-Clause")

    version("0.4.11", sha256="b8fea0b09714bbadf202b9b3434cce6b59c282e7869268d0c08b85880fdbb446")
    version("0.4.7", sha256="49725457f5bef45ea424baade8999a6e54496e357f64280474ff7134a54f599a")
    version("0.4.6", sha256="26a071317ae5710f226a3e6ba9a54d3764cd9efe3965aecc18e75372088757cd")
    version("0.4.5", sha256="16d6a0fe7b7d49ddbb303f33538dd7304a0d4af5a0369bcbf275db6a5060cbde")

    depends_on("c", type="build")  # generated

    build_directory = "spack-build"
