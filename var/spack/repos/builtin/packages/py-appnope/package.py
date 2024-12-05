# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAppnope(PythonPackage):
    """Disable App Nap on OS X 10.9"""

    homepage = "https://github.com/minrk/appnope"
    pypi = "appnope/appnope-0.1.0.tar.gz"

    version("0.1.3", sha256="02bd91c4de869fbb1e1c50aafc4098827a7a54ab2f39d9dcba6c9547ed920e24")
    version("0.1.0", sha256="8b995ffe925347a2138d7ac0fe77155e4311a0ea6d6da4f5128fe4b3cbe5ed71")

    depends_on("py-setuptools", type="build")
