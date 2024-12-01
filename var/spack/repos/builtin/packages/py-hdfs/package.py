# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHdfs(PythonPackage):
    """API and command line interface for HDFS"""

    homepage = "https://hdfscli.readthedocs.io/en/latest/"
    pypi = "hdfs/hdfs-2.1.0.tar.gz"

    license("MIT")

    version("2.1.0", sha256="a40fe99ccb03b5c3247b33a4110eb21b57405dd7c3f1b775e362e66c19b44bc6")

    depends_on("py-setuptools", type="build")
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-requests@2.7.0:", type=("build", "run"))
    depends_on("py-six@1.9.0:", type=("build", "run"))
