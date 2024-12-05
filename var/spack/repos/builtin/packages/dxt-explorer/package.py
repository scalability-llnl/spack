# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DxtExplorer(PythonPackage):
    """
    DXT Explorer is an interactive web-based log analysis tool to visualize
    Darshan DXT logs and help understand the I/O behavior of applications.
    """

    homepage = "http://dxt-explorer.readthedocs.io"
    git = "https://github.com/hpc-io/dxt-explorer"
    pypi = "dxt-explorer/dxt-explorer-0.3.tar.gz"

    maintainers("jeanbez", "sbyna")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="develop")

    version("0.3", sha256="fb73947b737c327154d03eeb0744c86774263878b893b365094ce4af8ac60b8b")

    depends_on("r", type=("run"))

    depends_on("darshan-util", type=("run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-pandas", type=("build", "run"))
