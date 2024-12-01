# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDipy(PythonPackage):
    """Diffusion MRI utilities in python.

    DIPY is the paragon 3D/4D+ imaging library in Python. Contains generic
    methods for spatial normalization, signal processing, machine learning,
    statistical analysis and visualization of medical images. Additionally, it
    contains specialized methods for computational anatomy including diffusion,
    perfusion and structural imaging.
    """

    homepage = "https://dipy.org/"
    pypi = "dipy/dipy-1.4.1.tar.gz"

    version("1.7.0", sha256="59bb647128aae7793215c813bb8ea35dae260ac9f0d938c724064f0af5a05cc3")
    version("1.4.1", sha256="b4bf830feae751f3f985d54cb71031fc35cea612838320f1f74246692b8a3cc0")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@:3.9", type=("build", "run"), when="@:1.4")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29:", type=("build"))
    depends_on("py-cython@0.29.24:", type=("build"), when="@1.7:")
    depends_on("py-numpy@1.12.0:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@1.7:")
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-scipy@1.1:", type=("build", "run"), when="@1.7:")
    depends_on("py-nibabel@3.0.0:", type=("build", "run"))
    depends_on("py-h5py@2.5.0:", type=("build", "run"))
    depends_on("py-h5py@2.8.0:", type=("build", "run"), when="@1.7:")
    depends_on("py-packaging@19.0:", type=("build", "run"))
    depends_on("py-tqdm@4.30.0:", type=("build", "run"))
