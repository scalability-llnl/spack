# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyZfitPhysics(PythonPackage):
    """Tools and models to extend zfit with physics specific content."""

    homepage = "https://github.com/zfit/zfit-physics"
    pypi = "zfit-physics/zfit_physics-0.7.0.tar.gz"

    maintainers("jonas-eschle", "ikrommyd")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    tags = ["likelihood", "statistics", "inference", "fitting", "hep"]

    version("0.7.0", sha256="5d65becff7265a12d9b62a8476c5359e75ec10d6ac0fd84dfa39eb82b6693cda")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")

    # TODO: remove "build" once fixed in spack that tests need "run", not "build"
    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@0.7:")
        depends_on("py-zfit@0.20:", when="@0.7:")
