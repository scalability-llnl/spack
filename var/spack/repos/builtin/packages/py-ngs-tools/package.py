# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNgsTools(PythonPackage):
    """Reusable tools for working with next-generation sequencing (NGS)
    data."""

    homepage = "https://github.com/Lioscro/ngs-tools"
    pypi = "ngs-tools/ngs-tools-1.8.1.tar.gz"

    license("MIT")

    version("1.8.1", sha256="59d606d6c3ff3024e5e1ccad947c4d7608098fca105762e344742e16aa2f0de3")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-joblib@1.0.1:", type=("build", "run"))
    depends_on("py-numba@0.53.1:", type=("build", "run"))
    depends_on("py-numpy@1.19.0:", type=("build", "run"))
    depends_on("py-pysam@0.16.0.1:", type=("build", "run"))
    depends_on("py-shortuuid@1.0.1:", type=("build", "run"))
    depends_on("py-tqdm@4.50.0:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"))
