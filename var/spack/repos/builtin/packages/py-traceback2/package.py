# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraceback2(PythonPackage):
    """Backports of the traceback module"""

    homepage = "https://github.com/testing-cabal/traceback2"
    pypi = "traceback2/traceback2-1.4.0.tar.gz"

    version("1.4.0", sha256="05acc67a09980c2ecfedd3423f7ae0104839eccb55fc645773e1caa0951c3030")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-linecache2", type=("build", "run"))
