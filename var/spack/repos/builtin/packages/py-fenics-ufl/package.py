# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsUfl(PythonPackage):
    """The Unified Form Language (UFL) is a domain specific language for
    declaration of finite element discretizations of variational forms. More
    precisely, it defines a flexible interface for choosing finite element
    spaces and defining expressions for weak forms in a notation close to
    mathematical notation."""

    homepage = "https://fenicsproject.org/"
    url = "https://github.com/FEniCS/ufl/archive/2019.1.0.tar.gz"
    git = "https://github.com/FEniCS/ufl.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("2024.2.0", sha256="d9353d23ccbdd9887f8d6edab74c04fe06d818da972072081dbf0c25bc86f5a7")
    version(
        "2024.1.0.post1", sha256="6e38e93a2c8417271c9fb316e0d0ea5fe1101c6a37b2496fff8290e7ea7ead74"
    )
    version("2023.2.0", sha256="d1d3209e8ebd4bd70513c26890f51823bac90edc956233c47bd8e686e064436e")
    version(
        "2023.1.1.post0", sha256="9e6e87f1447635029cec42604f62a76bba84899beb4b8822af10389d1f93a9b6"
    )
    version("2022.2.0", sha256="d6e18e06df5d7a626c3138d49a543914d68186afb6159c4d1a7cd72b2a199b02")
    version("2022.1.0", sha256="48359903d47fb397900d105fe4a60b459c50bbf9d9da78beb9accb54e4e4acaf")
    version("2021.1.0", sha256="130fdc09bb7fcd39dcd2618426912b8a25a03431d94575711068b38c666b4337")
    version("2019.1.0", sha256="46ac0df4e96327be10b9576d2b8fa8b2c4ca62d3c681d407f5718b162d3ca22d")
    version("2018.1.0", sha256="b0d4c2f43f396fd5609317b70d55b53b89c649962fc8a593f4e0e21607da211d")
    version(
        "2017.2.0.post0", sha256="111e77707cd6731584b1041f405c2fd3f1752a86c51fd9c430524bd396f293b0"
    )
    version("2017.2.0", sha256="0adff7a511185b20c38ddaccdeed6c1b2ecafe4b163c688bfd1316d5c3b1c00d")
    version(
        "2017.1.0.post1", sha256="82c8170f44c2392c7e60aa86495df22cc209af50735af8115dc35aeda4b0ca96"
    )
    version("2016.2.0", tag="ufl-2016.2.0", commit="962d56f65821fb9c50ca4a5a858882c472243431")

    depends_on("python@3.8:", when="@2023.2.0:", type=("build", "run"))

    depends_on("py-setuptools@62:", when="@2023.2.0:", type="build")
    depends_on("py-setuptools@58:", when="@2022.1.0:2023.1.1.post0", type="build")
    depends_on("py-setuptools@40:", when="@2016.2.0:2021.1.0", type="build")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            Executable("py.test")()
