# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTransforms3d(PythonPackage):
    """Functions for 3D coordinate transformations."""

    homepage = "https://github.com/matthew-brett/transforms3d"
    pypi = "transforms3d/transforms3d-0.3.1.tar.gz"

    version("0.3.1", sha256="404c7797c78aa461cb8043081901fc5517cef342d5ff56becd74a7967ba88d78")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.5.1:", type=("build", "run"))
