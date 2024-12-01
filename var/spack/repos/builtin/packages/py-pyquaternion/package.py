# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyquaternion(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://kieranwynn.github.io/pyquaternion/"
    pypi = "pyquaternion/pyquaternion-0.9.5.tar.gz"

    license("MIT")

    version("0.9.5", sha256="2d89d19259d62a8fbd25219eee7dacc1f6bb570becb70e1e883f622597c7d81d")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-numpy", type="run")
