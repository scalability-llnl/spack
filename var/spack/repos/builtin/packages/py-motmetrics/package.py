# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMotmetrics(PythonPackage):
    """The py-motmetrics library provides a Python implementation of
    metrics for benchmarking multiple object trackers (MOT)."""

    homepage = "https://github.com/cheind/py-motmetrics"
    pypi = "motmetrics/motmetrics-1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="7328d8468c948400b38fcc212f3e448bc1f2fdfc727e170d85a029e49f1cdbc6")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.12.1:", type=("build", "run"))
    depends_on("py-pandas@0.23.1:", type=("build", "run"))
    depends_on("py-scipy@0.19.0:", type=("build", "run"))
    depends_on("py-xmltodict@0.12.0:", type=("build", "run"))
    depends_on("py-flake8", type=("build", "run"))
    depends_on("py-flake8-import-order", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-pytest-benchmark", type=("build", "run"))
