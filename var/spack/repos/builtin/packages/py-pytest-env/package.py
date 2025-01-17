# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestEnv(PythonPackage):
    """Pytest plugin that enables you to set environment variables in a
    pytest.ini or pyproject.toml file."""

    homepage = "https://github.com/pytest-dev/pytest-env"
    pypi = "pytest-env/pytest_env-1.1.5.tar.gz"

    license("MIT")

    version("1.1.5", sha256="91209840aa0e43385073ac464a554ad2947cc2fd663a9debf88d03b01e0cc1cf")
    version("1.1.4", sha256="86653658da8f11c6844975db955746c458a9c09f1e64957603161e2ff93f5133")
    version("1.1.3", sha256="fcd7dc23bb71efd3d35632bde1bbe5ee8c8dc4489d6617fb010674880d96216b")
    version("1.1.2", sha256="8a7c46317d708407b0d6c38767f68a34155afe72cd42b74b4edd5c04c7851372")
    version("1.1.1", sha256="1efb8acce1f6431196150f3b30673443ff05a6fabff64539a9495cd2248adf9e")
    version("1.1.0", sha256="ea0a710f1b6a3571ed971fb6d6e5db05a2ae6b91b0fbcafe30fb5ea40e9987c4")

    with when("@1.1.1:1.1.3"):
        depends_on("python@3.8:3.12", type=("build", "run"))
        depends_on("py-hatchling@1.18:", type=("build"))
        depends_on("py-hatch-vcs@0.3:", type=("build"))
        depends_on("py-pytest@7.4.2:", type=("build", "run"))

    with when("@1.1.4:1.1.5"):
        depends_on("python@3.8:3.13", type=("build", "run"))
        depends_on("py-hatchling@1.25:", type=("build"))
        depends_on("py-hatch-vcs@0.4", type=("build"))

    depends_on("py-pytest@8.3.3:", type=("build", "run"), when="@1.1.5:")
    depends_on("py-pytest@8.3.2:", type=("build", "run"), when="@1.1.4:")

    depends_on("py-tomli@2.0.1:", type=("build", "run"), when="^python@:3.10")
