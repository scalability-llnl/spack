# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDistMeta(PythonPackage):
    """Parse and create Python distribution metadata."""

    homepage = "https://github.com/repo-helper/dist-meta"
    pypi = "dist_meta/dist-meta-0.8.0.tar.gz"

    license("MIT")

    version("0.8.0", sha256="541d51f75b7f580c80d8d7b23112d0b4bf3edbc9442e425a7c4fcd75f4138551")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6:", type="build")
    conflicts("^py-setuptools@61")
    depends_on("py-domdf-python-tools@3.1:", type=("build", "run"))
    depends_on("py-handy-archives@0.1:", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
