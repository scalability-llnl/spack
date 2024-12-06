# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrian2(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "https://www.briansimulator.org"
    pypi = "Brian2/Brian2-2.2.2.1.tar.gz"

    license("BSD-2-Clause")

    version("2.5.0.2", sha256="70e6f88fb26f04ccafb91e0a29999774e45899771357aff7043951c853919a0f")
    version("2.5.0.1", sha256="1f719b563ae38658c4c59bac5aeb06b41970c6eedc52021ddf6d9254913733d3")
    version("2.4.2", sha256="7a711af40145d8c62b0bc0861d352dc64f341c3a738174d87ef9d71e50e959f2")
    version("2.2.2.1", sha256="02075f66d42fd243fc5e28e1add8862709ae9fdabaffb69858e6d7f684a91525")
    version("2.0.1", sha256="195d8ced0d20e9069917776948f92aa70b7457bbc6b5222b8199654402ee1153")
    version("2.0rc3", sha256="05f347f5fa6b25d1ce5ec152a2407bbce033599eb6664f32f5331946eb3c7d66")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@2.4:")
    depends_on("python@3.7:", type=("build", "run"), when="@2.5:")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")

    depends_on("py-numpy@1.10:", type=("build", "run"))
    depends_on("py-numpy@1.15:", type=("build", "run"), when="@2.4:")
    depends_on("py-numpy@1.17:", type=("build", "run"), when="@2.5:")
    depends_on("py-cython@0.29:", type=("build", "run"))
    depends_on("py-sympy@0.7.6:1.0,1.1.1:", type=("build", "run"))
    depends_on("py-sympy@1.2:", type=("build", "run"), when="@2.4:")
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-jinja2@2.7:", type=("build", "run"))
    depends_on("py-setuptools@21:", type=("build", "run"))
    depends_on("py-setuptools@24.2:", type=("build", "run"), when="@2.4:")

    def install_options(self, spec, prefix):
        return ["--with-cython"]
