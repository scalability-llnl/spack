# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *


class Zpp(PythonPackage):
    """ZPP, the Z Pre-Processor. ZPP transforms bash in a pre-processor for F90
    source files. It offers a set of functions specifically tailored to build
    clean Fortran90 interfaces by generating code for all types, kinds, and
    array ranks supported by a given compiler."""

    homepage = "https://github.com/jbigot/zpp"
    pypi = "zpp/zpp-1.0.16.tar.gz"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("1.1.0", sha256="4cd07ef18df5d44798e213aaaf17af78449739b01c0bf41e046c95b8a1aad6bd")
    version("1.0.16", sha256="3238d27b4158edabb09ee6d82ba6331540950cb4dcdcf4978f19370b4e384241")
    version("1.0.15", sha256="33d49280ca0d8e5221faa4c694949647146d15f16dacc09c36f20e7c34831135")
    version("1.0.14", sha256="c52962a9d9c3aa28d513090ef327e05eccc7923473415d9dcbdacf22911d6c9f")
    version("1.0.13", sha256="c76985c172491667677eba01072656eb04a59791d8b6a4e396721eddb570c548")
    version("1.0.12", sha256="1fcc206096a144d24dd8cc7d2278d1eb4d0b4a5e2e3aa4936e7de30fe2d435ce")
    version("1.0.11", sha256="e6a3e98b6be5ae7853fd0f66f58e9607cecaa66caefc57418d3163df695a2a90")
    version("1.0.10", sha256="b0bb95303fe2f09918f1ce833027fda429746c3e51a859f7e051f9deb360c4d5")
    version(
        "1.0.9-fixed", sha256="6aa5f4a42b8ba7c000e7b186d5ef2be99fd0f8f47e1d360c42c1b371d0bacf23"
    )
    version(
        "1.0.8-fixed", sha256="dc5f423f019f1af92ff020372b458ab539890d2de2133bb9602cce419486faea"
    )

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
