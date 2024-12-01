# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8Polyfill(PythonPackage):
    """flake8-polyfill is a package that provides some compatibility helpers
    for Flake8 plugins that intend to support Flake8 2.x and 3.x
    simultaneously.
    """

    homepage = "https://gitlab.com/pycqa/flake8-polyfill"
    pypi = "flake8-polyfill/flake8-polyfill-1.0.2.tar.gz"

    license("MIT")

    version("1.0.2", sha256="e44b087597f6da52ec6393a709e7108b2905317d0c0b744cdca6208e670d8eda")

    depends_on("py-setuptools", type="build")
    depends_on("py-flake8", type=("build", "run"))
