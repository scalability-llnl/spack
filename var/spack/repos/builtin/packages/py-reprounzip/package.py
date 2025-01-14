# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReprounzip(PythonPackage):
    """A tool simplifying creating reproducible experiments from CLI executions.

    It tracks operating system calls and creates a bundle that contains all the
    binaries, files and dependencies required to run a given command on the
    author’s computational environment (packing step). A reviewer can then
    extract the experiment in his environment to reproduce the results
    (unpacking step).

    This is the component responsible for the unpacking step on Linux
    distributions.

    Please refer to reprozip, reprounzip-vagrant, and reprounzip-docker for
    other components and plugins.

    """

    homepage = "https://www.reprozip.org/"

    pypi = "reprounzip/reprounzip-1.2.1.tar.gz"

    maintainers("charmoniumQ")

    version("1.2.1", md5="051364ff599d2ae7fb9ca0bd0dc3da446be63dd0c251f2fdea125a8114100097")

    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-rpaths@0.8:", type=("build", "run"))
    depends_on("py-usagestats@0.3:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"))
    depends_on("py-pyelftools", type=("build", "run"))
