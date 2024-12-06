# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyJobMetrics(PythonPackage):
    """The Galaxy job metrics framework and default plugins."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-job-metrics/galaxy-job-metrics-22.1.1.tar.gz"

    license("CC-BY-3.0")

    version("22.1.1", sha256="53d9c791d60372a90a59709863570246066f395b9e83f0011865f930a53a63b4")

    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-util", type=("build", "run"))
