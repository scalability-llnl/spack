# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalSaga(PythonPackage):
    """RADICAL-SAGA (RS) implements the interface specification of the Open
    Grid Forum (OGF) Simple API for Grid Applications (SAGA) standard. RS works
    as a light-weight access layer for distributed computing infrastructures,
    providing adaptors for different middleware systems and services."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.saga.git"
    pypi = "radical.saga/radical.saga-1.47.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.47.0", sha256="fc9a8fc060e708852ce6c40b08a65111f8d72b9ad5f8afef9ceaa866c1351233")
    version("1.39.0", sha256="0fea8103d3f96c821c977bcb55ff1c6a9844de727539b182dda4cbc2570df791")

    version(
        "1.20.0",
        sha256="d85f3ed564d9eaf3ead2aa349c854e944ca459492ebf88542404106fce4204ab",
        deprecated=True,
    )
    version(
        "1.18.0",
        sha256="544d4ffafc0b311151724db371ee11e27744103068748962866351ce31ccb810",
        deprecated=True,
    )
    version(
        "1.17.0",
        sha256="e48b42c232ac0ad53a410c1317746a5f15214fd3108fad773d098714fb4c40a0",
        deprecated=True,
    )
    version(
        "1.16.0",
        sha256="d269e2e7043f05e8f1d45ca3d50be973857150d7928d53bedd6844f39b224786",
        deprecated=True,
    )
    version(
        "1.14.0",
        sha256="337d8778bf392fd54845b1876de903c4c12f6fa938ef16220e1847561b66731a",
        deprecated=True,
    )
    version(
        "1.13.0",
        sha256="90d8e875f48402deab87314ea5c08d591264fb576c461bd9663ac611fc2e547e",
        deprecated=True,
    )
    version(
        "1.12.0",
        sha256="769c83bab95c0e3ef970da0fa6cb30878d7a31216ff8b542e894686357f7cb5b",
        deprecated=True,
    )
    version(
        "1.11.1",
        sha256="edb1def63fadd192a4be4f508e9e65669745843e158ce27a965bf2f43d18b84d",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="6edf94897102a08dcb994f7f107a0e25e7f546a0a9488af3f8b92ceeeaaf58a6",
        deprecated=True,
    )
    version(
        "1.6.10",
        sha256="8fe7e281e9f81234f34f5c7c7986871761e9e37230d2a874c65d18daeccd976a",
        deprecated=True,
    )
    version(
        "1.6.8",
        sha256="d5e9f95a027087fb637cef065ff3af848e5902e403360189e36c9aa7c3f6f29b",
        deprecated=True,
    )

    depends_on("py-radical-utils@1.40:", type=("build", "run"), when="@1.40:")

    depends_on("py-radical-utils@1.39", type=("build", "run"), when="@1.39")

    depends_on("py-radical-utils@1.12:1.20", type=("build", "run"), when="@1.12:1.20")

    depends_on("py-radical-utils@:1.11", type=("build", "run"), when="@:1.11")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-apache-libcloud", type=("build", "run"))
    depends_on("py-parse", type=("build", "run"))
    depends_on("py-setuptools", type="build")
