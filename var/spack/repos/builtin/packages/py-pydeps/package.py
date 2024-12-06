# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPydeps(PythonPackage):
    """Python module dependency visualization."""

    pypi = "pydeps/pydeps-1.7.1.tar.gz"

    version("1.9.0", sha256="ba9b8c7d72cb4dfd3f4dd6b8a250c240d15824850a415fd428f2660ed371361f")
    version("1.7.1", sha256="7eeb8d0ec2713befe81dd0d15eac540e843b1daae13613df1c572528552d6340")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-stdlib-list", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
