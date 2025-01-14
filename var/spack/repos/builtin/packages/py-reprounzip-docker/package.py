# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReprounzipDocker(PythonPackage):
    """A tool simplifying creating reproducible experiments from CLI executions.

    It tracks operating system calls and creates a bundle that contains all the
    binaries, files and dependencies required to run a given command on the
    author’s computational environment (packing step). A reviewer can then
    extract the experiment in his environment to reproduce the results
    (unpacking step).

    This is the component responsible for the unpacking step on different
    environments (Linux, Windows, and Mac OS X) by using a Docker container.

    Please refer to reprozip, reprounzip, and reprounzip-vagrant for other
    components and plugins.

    """

    homepage = "https://www.reprozip.org/"

    pypi = "reprounzip-docker/reprounzip-docker-1.2.tar.gz"

    maintainers("charmoniumQ")

    version("1.2", md5="ccde16c7502072693afd7ab9d8b58f478e575efe3806ec4951659869a571fa2f")

    depends_on("py-setuptools", type="build")

    depends_on("py-reprounzip@1.1:", type=("build", "run"))
    depends_on("py-rpaths@0.8:", type=("build", "run"))
