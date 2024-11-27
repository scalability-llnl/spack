# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpileaks(Package):
    """Mpileaks is a mock package that passes audits"""

    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version("2.3", sha256="2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825")
    version("2.2", sha256="2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825")
    version("2.1", sha256="2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825")
    version("1.0", sha256="2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825")

    variant("debug", default=False, description="Debug variant")
    variant("opt", default=False, description="Optimized variant")
    variant("shared", default=True, description="Build shared library")
    variant("static", default=True, description="Build static library")

    depends_on("mpi")
    depends_on("callpath")

    # Will be used to try raising an exception
    libs = None

    def install(self, spec, prefix):
        touch(prefix.mpileaks)
        mkdirp(prefix.man)

    def setup_run_environment(self, env):
        env.set("FOOBAR", self.name)
