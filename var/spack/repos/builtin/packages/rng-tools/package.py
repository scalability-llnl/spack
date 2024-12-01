# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RngTools(AutotoolsPackage):
    """This is a random number generator daemon.
    It monitors a set of entropy sources, and supplies
    entropy from them to the system kernel's /dev/random
    machinery."""

    homepage = "https://github.com/nhorman/rng-tools/"
    url = "https://github.com/nhorman/rng-tools/archive/v6.10.tar.gz"

    license("GPL-2.0-or-later")

    version("6.10", sha256="2e462821aaa7d6dc24646aa0d2239d97cb8b07b3e60715159a9edcaa9189f8ef")
    version("6.9", sha256="a57a7f51a2e3c0faa8afb979709a4c0cbea36d0b52fd835b104f8fb4fd1fa610")
    version("6.8", sha256="93e548d4aaf2a1897d4b677f41d8473db1c7f57648adeca18cafa1907e410bb3")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext")
    depends_on("curl")
    depends_on("jansson")
    depends_on("libp11")
    depends_on("librtlsdr")
    depends_on("sysfsutils")
