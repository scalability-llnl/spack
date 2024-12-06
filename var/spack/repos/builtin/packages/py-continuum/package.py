# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContinuum(PythonPackage):
    """A clean and simple data loading library for Continual Learning"""

    homepage = "https://continuum.readthedocs.io/en/latest/"
    pypi = "continuum/continuum-1.2.7.tar.gz"

    maintainers("thomas-bouvier")

    license("MIT")

    version("1.2.7", sha256="baadcdbe2f5b3c05254307c73434a012f2a3d663e1be9469a03d4b82559e98e1")

    # This patch moves the `prospector` dependency of package continuum to the
    # dev dependencies, as it is not called from any Python code.
    # https://github.com/Continvvm/continuum/pull/280
    patch("move_prospector_dev_requires.patch", when="@:1.2.7")

    depends_on("python@3.6:")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.2.0:", type=("build", "run"))
    depends_on("py-torchvision@0.4.0:", type=("build", "run"))
    depends_on("py-numpy@1.17.2:", type=("build", "run"))
    depends_on("pil@6.2.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.0:", type=("build", "run"))
    depends_on("py-scipy@1.3.3:", type=("build", "run"))
    depends_on("py-scikit-image@0.15.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.24.1:", type=("build", "run"))
    depends_on("py-pandas@1.1.5:", type=("build", "run"))
    depends_on("py-pytest@5.0.1:", type=("build", "run"))
    depends_on("py-pytest-mock@3.6.1:", type=("build", "run"))
    depends_on("py-h5py@3.1.0:", type=("build", "run"))
    depends_on("py-requests@2.24.0:", type=("build", "run"))
    depends_on("py-datasets@1.6.0:", type=("build", "run"))
    depends_on("py-imagehash@4.2.1:", type=("build", "run"))
