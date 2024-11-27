# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySacremoses(PythonPackage):
    """LGPL MosesTokenizer in Python."""

    homepage = "https://github.com/alvations/sacremoses"
    pypi = "sacremoses/sacremoses-0.0.39.tar.gz"

    version("0.0.39", sha256="53fad38b93dd5bf1657a68d52bcca5d681d4246477a764b7791a2abd5c7d1f4c")

    depends_on("py-setuptools", type="build")
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
