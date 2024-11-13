# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Args(CMakePackage):
    """A simple header-only C++ argument parser library. Supposed to be
    flexible and powerful, and attempts to be compatible with the
    functionality of the Python standard argparse library (though not
    necessarily the API)."""

    homepage = "https://taywee.github.io/args"
    url = "https://github.com/Taywee/args/archive/6.2.3.tar.gz"

    license("MIT")

    version("6.4.6", sha256="41ed136bf9b216bf5f18b1de2a8d22a870381657e8427d6621918520b6e2239c")
    version("6.2.3", sha256="c202d15fc4b30519a08bae7df9e6f4fdc40ac2434ba65d83a108ebbf6e4822c2")
    version("6.2.2", sha256="8016fb0fc079d746433be3df9cf662e3e931e730aaf9f69f2287eac79ac643c1")
    version("6.2.1", sha256="699b91fae4509b09974274838e2038612da24eeae89e62d0bc580457a9e261b0")

    depends_on("cxx", type="build")  # generated
