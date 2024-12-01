# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCertipy(PythonPackage):
    """A simple python tool for creating certificate authorities
    and certificates on the fly."""

    pypi = "certipy/certipy-0.1.3.tar.gz"

    version("0.1.3", sha256="695704b7716b033375c9a1324d0d30f27110a28895c40151a90ec07ff1032859")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyopenssl", type=("build", "run"))
