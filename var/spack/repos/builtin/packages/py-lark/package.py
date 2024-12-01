# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLark(PythonPackage):
    """Lark is a modern general-purpose parsing library for Python."""

    homepage = "https://github.com/lark-parser/lark/"
    pypi = "lark/lark-1.0.0.tar.gz"

    license("MIT")

    version("1.1.2", sha256="7a8d0c07d663da9391d7faee1bf1d7df4998c47ca43a593cbef5c7566acd057a")
    version("1.1.1", sha256="5115193433051f079374c4f81059fa4bf2afa78cc87dd87817ed4435e8647c82")
    version("1.1.0", sha256="669eab99a9627b2b9e0c6fb97f23113c64d673c93d804bca40b05b2a765f13c0")
    version("1.0.0", sha256="2269dee215e6c689d5ce9d34fdc6e749d0c1c763add3fc7935938ebd7da159cb")
    version("0.12.0", sha256="7da76fcfddadabbbbfd949bbae221efd33938451d90b1fefbbc423c3cccf48ef")
    version("0.11.3", sha256="3100d9749b5a85735ec428b83100876a5da664804579e729c23a36341f961e7e")
    version("0.11.1", sha256="f2c6ed79ae128a89714bbaa4a6ecb61b6eec84d1b5d63b9195ad461762f96298")
    version("0.11.0", sha256="29868417eb190fe7d6b1ff6bcd9446903e0c73a1ca69cec58c92a01cae0abc24")
    version("0.10.1", sha256="98f2c6f8e41fe601fd103476eb759ac1ad4d3dc8094633133a16cef5a32b0f65")

    depends_on("python@3.6:", when="@1.0.0:")
    depends_on("py-setuptools", type="build")
