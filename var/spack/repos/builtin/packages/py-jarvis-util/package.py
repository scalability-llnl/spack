# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJarvisUtil(PythonPackage):
    """Jarvis-util is a library which contains various utilities to aid with
    creating shell scripts within Python. This library contains wrappers
    for executing shell commands locally, SSH, SCP, MPI, argument parsing,
    and various other random utilities."""

    homepage = "https://github.com/scs-lab/jarvis-util"
    git = "https://github.com/scs-lab/jarvis-util.git"
    url = "https://github.com/scs-lab/jarvis-util/archive/refs/tags/v0.0.1.tar.gz"
    maintainers("lukemartinlogan", "hyoklee")

    version("master", branch="master")
    version("0.0.1", sha256="1c5fbbfec410f1df8dc28edc87dd4421c3708f5bd22bf7ef010138d5c4a1ff8f")

    depends_on("py-setuptools", type="build")
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyaml", type=("build", "run"))
