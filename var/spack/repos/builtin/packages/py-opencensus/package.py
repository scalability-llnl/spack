# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOpencensus(PythonPackage):
    """A stats collection and distributed tracing framework."""

    homepage = "https://github.com/census-instrumentation/opencensus-python"
    pypi = "opencensus/opencensus-0.7.10.tar.gz"

    license("Apache-2.0")

    version("0.7.10", sha256="2921e3e570cfadfd123cd8e3636a405031367fddff74c55d3fe627a4cf8b981c")

    depends_on("py-setuptools", type="build")
    depends_on("py-opencensus-context@0.1.1", type=("build", "run"))
    depends_on("py-google-api-core@1.0:1", type=("build", "run"))
