# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySysrsync(PythonPackage):
    """Python module that wraps system calls to rsync."""

    pypi = "sysrsync/sysrsync-1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="435f9eb620e68ffb18ca5cbad32b113396a432361c7722038eab65c97dd83bd5")

    depends_on("py-toml@0.10.0:0.10", type=("build", "run"))
    depends_on("rsync", type="run")

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
