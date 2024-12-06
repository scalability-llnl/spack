# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEzSetup(PythonPackage):
    """Setuptools bootstrap module, which is not always packaged with
    setuptools."""

    homepage = "https://github.com/ActiveState/ez_setup"
    url = "https://github.com/ActiveState/ez_setup/archive/v0.9.tar.gz"

    version("0.9", sha256="a35cb03142cc10b6bb2cf59999cf2f4e127ec0901606d02be57da5b34e6897fb")

    depends_on("py-setuptools", type="build")
