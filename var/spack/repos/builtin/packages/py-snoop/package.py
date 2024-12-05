# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySnoop(PythonPackage):
    """snoop is a powerful set of Python debugging tools. It's primarily meant
    to be a more featureful and refined version of PySnooper. It also includes
    its own version of icecream and some other nifty stuff."""

    pypi = "snoop/snoop-0.4.3.tar.gz"

    license("MIT", checked_by="jmlapre")

    version("0.4.3", sha256="2e0930bb19ff0dbdaa6f5933f88e89ed5984210ea9f9de0e1d8231fa5c1c1f25")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-cheap-repr@0.4.0:", type=("build", "run"))
    depends_on("py-executing", type=("build", "run"))
    depends_on("py-asttokens", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
