# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCuml(PythonPackage):
    """cuML is a suite of libraries that implement machine
    learning algorithms and mathematical primitives functions
    that share compatible APIs with other RAPIDS projects."""

    homepage = "https://github.com/rapidsai/cuml"
    url = "https://github.com/rapidsai/cuml/archive/v0.15.0.tar.gz"

    license("Apache-2.0")

    version("0.15.0", sha256="5c9c656ae4eaa94a426e07d7385fd5ea0e5dc7abff806af2941aee10d4ca99c7")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-cudf", type=("build", "run"))
    depends_on("cuda")
    depends_on("py-cupy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("treelite+python", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))

    for v in ("11.0", "10.2", "10.1"):
        depends_on("libcumlprims@0.15.0-cuda{0}_gdbd0d39_0".format(v), when="^cuda@{0}".format(v))

    for v in ("@0.15.0",):
        depends_on("libcuml{0}".format(v), when=v)

    build_directory = "python"
