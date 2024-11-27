# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParalleltask(PythonPackage):
    """Paralleltask is a simple and lightweight parallel task engine. It can launch a given
    number of tasks from a batch of independent tasks, and keep this number of running tasks
    until all tasks are completed."""

    homepage = "https://github.com/moold/ParallelTask"
    pypi = "Paralleltask/Paralleltask-0.2.2.tar.gz"

    license("GPL-3.0-only")

    version("0.2.2", sha256="f00945e2bd5b6aff9cdc48fbd92aa7b48d23bb530d7f6643ac966fea11a7a9d5")

    depends_on("py-setuptools", type="build")
    depends_on("py-psutil", type=("build", "run"))
