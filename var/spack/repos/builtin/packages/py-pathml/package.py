# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathml(PythonPackage):
    """An open-source toolkit for computational pathology and machine learning."""

    homepage = "https://github.com/Dana-Farber-AIOS/pathml"
    pypi = "pathml/pathml-2.1.0.tar.gz"

    license("GPL-2.0-or-later")

    version("2.1.0", sha256="462bb2f16452dddad310c30f62678a1336ce492263355fd6722c07ee4840ea6a")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-numpy@1.16.4:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pydicom", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-openslide-python", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-dask +distributed", type=("build", "run"))
    depends_on("py-anndata@0.7.6:", type=("build", "run"))
    depends_on("py-scanpy", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("opencv+python3", type=("build", "run"))
    depends_on("py-python-bioformats@4.0.0:", type=("build", "run"))
    depends_on("py-loguru", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
