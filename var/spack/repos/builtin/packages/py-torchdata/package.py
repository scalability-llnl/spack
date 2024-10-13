# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchdata(PythonPackage):
    """Composable data loading modules for PyTorch."""

    homepage = "https://github.com/pytorch/data"
    git = "https://github.com/pytorch/data.git"
    url = "https://github.com/pytorch/data/archive/refs/tags/v0.4.0.tar.gz"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("0.8.0", sha256="d5d27b264e79d7d00ad4998f14d097b770332d979672dceb6d038caf204f1208")
    version("0.7.1", sha256="ef9bbdcee759b53c3c9d99e76eb0a66da33d36bfb7f859a25a9b5e737a51fa23")
    version("0.7.0", sha256="0b444719c3abc67201ed0fea92ea9c4100e7f36551ba0d19a09446cc11154eb3")
    version("0.6.1", sha256="c596db251c5e6550db3f00e4308ee7112585cca4d6a1c82a433478fd86693257")
    version("0.6.0", sha256="048dea12ee96c0ea1525097959fee811d7b38c2ed05f44a90f35f8961895fb5b")
    version("0.5.1", sha256="69d80bd33ce8f08e7cfeeb71cefddfc29cede25a85881e33dbae47576b96ed29")
    version("0.5.0", sha256="b4e1a7015b34e3576111d495a00a675db238bfd136629fc443078bab9383ec36")
    version("0.4.1", sha256="71c0aa3aca3b04a986a2cd4cc2e0be114984ca836dc4def2c700bf1bd1ff087e")
    version("0.4.0", sha256="b4ec446a701680faa620fcb828b98ba36a63fa79da62a1e568d4a683889172da")
    version("0.3.0", sha256="ac36188bf133cf5f1041a28ccb3ee82ba52d4b5d99617be37d64d740acd6cfd4")

    depends_on("cxx", type="build")

    # https://github.com/pytorch/data#version-compatibility
    depends_on("python@3.8:3.12", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:3.11", when="@0.6:0.7", type=("build", "run"))
    depends_on("python@3.7:3.10", when="@:0.5", type=("build", "run"))

    # pyproject.toml
    depends_on("py-setuptools", type="build")

    # CMakeLists.txt
    depends_on("cmake@3.13:", when="@0.4:", type="build")
    depends_on("ninja", when="@0.4:", type="build")

    # https://github.com/pytorch/data#version-compatibility
    depends_on("py-torch@main", when="@main", type=("build", "run"))
    depends_on("py-torch@2.4.0", when="@0.8.0", type=("build", "run"))
    depends_on("py-torch@2.1.1", when="@0.7.1", type=("build", "run"))
    depends_on("py-torch@2.1.0", when="@0.7.0", type=("build", "run"))
    depends_on("py-torch@2.0.1", when="@0.6.1", type=("build", "run"))
    depends_on("py-torch@2.0.0", when="@0.6.0", type=("build", "run"))
    depends_on("py-torch@1.13.1", when="@0.5.1", type=("build", "run"))
    depends_on("py-torch@1.13.0", when="@0.5.0", type=("build", "run"))
    depends_on("py-torch@1.12.1", when="@0.4.1", type=("build", "run"))
    depends_on("py-torch@1.12.0", when="@0.4.0", type=("build", "run"))
    depends_on("py-torch@1.11.0", when="@0.3.0", type=("build", "run"))

    # requirements.txt
    depends_on("py-urllib3@1.25:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-portalocker@2:", when="@0.4:0.5", type=("build", "run"))

    # third_party/CMakeLists.txt
    depends_on("py-pybind11", when="@0.4:")
    depends_on("aws-sdk-cpp", when="@0.4:")

    def setup_build_environment(self, env):
        env.set("USE_SYSTEM_LIBS", "ON")
