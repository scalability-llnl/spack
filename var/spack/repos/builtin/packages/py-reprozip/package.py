# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReprozip(PythonPackage):
    """A tool simplifying creating reproducible experiments from CLI executions.

    It tracks operating system calls and creates a bundle that contains all the
    binaries, files and dependencies required to run a given command on the
    author’s computational environment (packing step). A reviewer can then
    extract the experiment in his environment to reproduce the results
    (unpacking step).

    This is the component responsible for the packing step on Linux
    distributions.

    Please refer to reprounzip, reprounzip-vagrant, and reprounzip-docker for
    other components and plugins.

    """

    homepage = "https://www.reprozip.org/"

    pypi = "reprozip/reprozip-1.2.tar.gz"

    maintainers("charmoniumQ")

    version("1.2", md5="a98b7f04c52c60072e3c42da21997d3ad41161ff6cb1139e18cda8d3012120f9")

    def setup_build_environment(self, env) -> None:
        env.set("CFLAGS", " -I%s/include" % self.spec["sqlite"].prefix)

    # reprozip/tracer/trace.py imports pkg_resources, so we will need setuptools
    # at runtime too.
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("sqlite", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-rpaths@0.8:", type=("build", "run"))
    depends_on("py-usagestats@0.3:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"))
