# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libseccomp(AutotoolsPackage, PythonExtension):
    """The main libseccomp repository"""

    homepage = "https://github.com/seccomp/libseccomp"
    url = "https://github.com/seccomp/libseccomp/releases/download/v2.5.3/libseccomp-2.5.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.5.4", sha256="d82902400405cf0068574ef3dc1fe5f5926207543ba1ae6f8e7a1576351dcbdb")
    version("2.5.3", sha256="59065c8733364725e9721ba48c3a99bbc52af921daf48df4b1e012fbc7b10a76")
    version("2.3.3", sha256="7fc28f4294cc72e61c529bedf97e705c3acf9c479a8f1a3028d4cd2ca9f3b155")

    depends_on("c", type="build")

    variant("python", default=True, description="Build Python bindings")

    depends_on("gperf", type="build", when="@2.5:")

    with when("+python"):
        extends("python")
        depends_on("py-cython", type="build")
        # https://github.com/seccomp/libseccomp/commit/afbde6ddaec7c58c3b281d43b0b287269ffca9bd
        depends_on("python@:3.11", type=("run", "link", "build"), when="@:2.5.5")

    def configure_args(self):
        return self.enable_or_disable("python", variant="python")
