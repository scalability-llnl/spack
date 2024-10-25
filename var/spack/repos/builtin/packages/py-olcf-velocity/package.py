# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOlcfVelocity(PythonPackage):
    """A tool to help with the maintenance of container build scripts on multiple systems,
    backends (e.g podman or apptainer) and distros."""

    homepage = "https://olcf.github.io/velocity/index.html"
    pypi = "olcf_velocity/olcf_velocity-0.1.3.tar.gz"

    maintainers("AcerP-py")

    license("UNKNOWN", checked_by="AcerP-py")

    version("0.1.3", sha256="08bd82d464e8cab6c61cab095d460b927a18e082cadb663bd5f935cf651b5c03")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-pyyaml", type="run")
    depends_on("py-networkx", type="run")
    depends_on("py-colorama", type="run")
    depends_on("py-loguru", type="run")
    depends_on("py-typing-extensions", type="run")

    depends_on("py-setuptools", type="build")
