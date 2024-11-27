# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThreadpoolctl(PythonPackage):
    """Python helpers to limit the number of threads used in the
    threadpool-backed of common native libraries used for scientific
    computing and data science (e.g. BLAS and OpenMP)."""

    homepage = "https://github.com/joblib/threadpoolctl"
    pypi = "threadpoolctl/threadpoolctl-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version("3.1.0", sha256="a335baacfaa4400ae1f0d8e3a58d6674d2f8828e3716bb2802c44955ad391380")
    version("3.0.0", sha256="d03115321233d0be715f0d3a5ad1d6c065fe425ddc2d671ca8e45e9fd5d7a52a")
    version("2.0.0", sha256="48b3e3e9ee079d6b5295c65cbe255b36a3026afc6dde3fb49c085cd0c004bbcf")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.6:", when="@3.0.0:", type=("build", "run"))
    depends_on("py-flit", when="@:3.0.0", type="build")
    depends_on("py-flit-core", when="@3.1.0:", type="build")
