# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stress(AutotoolsPackage):
    """stress is a deliberately simple workload generator for POSIX systems.
    It imposes a configurable amount of CPU, memory, I/O, and disk stress on
    the system. It is written in C, and is free software licensed under the
    GPLv2."""

    # Moved from original homepage
    # homepage = "https://people.seas.harvard.edu/~apw/stress/"
    homepage = "https://github.com/javiroman/system-stress"
    url = "https://github.com/javiroman/system-stress/archive/v1.0.4.tar.gz"

    license("GPL-2.0-or-later")

    version("1.0.4", sha256="b03dbb9664d7f8dcb3eadc918c2e8eb822f5a3ba47d9bd51246540bac281bd75")

    depends_on("c", type="build")  # generated
