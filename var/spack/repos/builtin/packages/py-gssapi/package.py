# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGssapi(PythonPackage):
    """Python-GSSAPI provides both low-level and high level wrappers
    around the GSSAPI C libraries."""

    homepage = "https://github.com/pythongssapi/python-gssapi"
    pypi = "gssapi/gssapi-1.8.2.tar.gz"

    maintainers("wdconinc")

    version("1.9.0", sha256="f468fac8f3f5fca8f4d1ca19e3cd4d2e10bd91074e7285464b22715d13548afe")
    version("1.8.3", sha256="aa3c8d0b1526f52559552bb2c9d2d6be013d76a8e5db00b39a1db5727e93b0b0")
    version("1.8.2", sha256="b78e0a021cc91158660e4c5cc9263e07c719346c35a9c0f66725e914b235c89a")

    depends_on("py-cython@0.29.29:2", type="build", when="@:1.8.2")
    depends_on("py-cython@0.29.29:3", type="build", when="@1.8.3:")
    depends_on("py-cython@3.0.3:3", type="build", when="@1.9.0:")
    depends_on("py-setuptools@40.6.0:", type="build")

    depends_on("py-decorator", type=("build", "run"))
    depends_on("krb5", type=("build", "link"))
