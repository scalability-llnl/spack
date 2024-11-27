# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoto(PythonPackage):
    """Boto is a Python package that provides interfaces to
    Amazon Web Services."""

    homepage = "https://github.com/boto/boto"
    url = "https://github.com/boto/boto/archive/2.49.0.tar.gz"

    license("MIT")

    version("2.49.0", sha256="3dbefd4f4542f85a323d4f54601f31ed4d362fc87945245f32e4a85029513314")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
