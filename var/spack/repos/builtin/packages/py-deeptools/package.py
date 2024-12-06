# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
    that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.python.org/pypi/deepTools/"
    pypi = "deepTools/deepTools-3.5.3.tar.gz"

    version("3.5.3", sha256="d57ede59417dcde09763d3c4e2aabd45abba1155200777a73a9cb0e94df73ff9")
    version("3.5.2", sha256="9367f9037b1822b7d69d5abaf47ca25bf0e5dc4cb8be85bd55b6f63c90781941")
    version("3.3.0", sha256="a9a6d2aff919f45e869acfb477e977db627da84f8136e4b4af0a5100057e6bc3")
    version("3.2.1", sha256="ccbabb46d6c17c927e96fadc43d8d4770efeaf40b9bcba3b94915a211007378e")
    version("2.5.2", sha256="305d0b85d75bd8af19dbe8947bb76c399fd5aaebd02f441455f4ba9e6c66ad9b")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.9.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.3.0:", when="@3.5.1:", type=("build", "run"))
    depends_on("py-matplotlib@2.1.2:", when="@:3.3.0", type=("build", "run"))
    depends_on("py-pysam@0.14.0:", type=("build", "run"))
    depends_on("py-numpydoc@0.5:", type=("build", "run"))
    depends_on("py-pybigwig@0.2.1:", type=("build", "run"))
    depends_on("py-py2bit@0.2.0:", type=("build", "run"))
    depends_on("py-plotly@4.9:", when="@3.5.1:", type=("build", "run"))
    depends_on("py-plotly@2.0.0:", when="@:3.5.0", type=("build", "run"))
    depends_on("py-deeptoolsintervals@0.1.8:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@3.5.3", type=("build", "run"))
