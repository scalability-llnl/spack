# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tskit(PythonPackage):
    """The tskit library provides the underlying functionality used to load,
    examine, and manipulate tree sequences"""

    homepage = "https://tskit.readthedocs.io/en/latest/"
    pypi = "tskit/tskit-0.3.1.tar.gz"

    license("MIT")

    version("0.5.6", sha256="ddfe213f1cb063cdb6982177230a2805ecd7dfc7ccd73026e13878abffd2ce46")
    version("0.3.1", sha256="b9c5a9b2fb62a615e389036946345ef8a35b09f1ffee541995b16f97fedb3d36")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-svgwrite", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-attrs@19.1.0:", type=("build", "run"))
