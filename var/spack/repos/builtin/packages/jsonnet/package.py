# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Jsonnet(MakefilePackage):
    """A data templating language for app and tool developers based on JSON"""

    homepage = "https://jsonnet.org/"
    git = "https://github.com/google/jsonnet.git"
    url = "https://github.com/google/jsonnet/archive/refs/tags/v0.18.0.tar.gz"

    maintainers("jcpunk")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.18.0", sha256="85c240c4740f0c788c4d49f9c9c0942f5a2d1c2ae58b2c71068107bc80a3ced4")
    version("0.17.0", sha256="076b52edf888c01097010ad4299e3b2e7a72b60a41abbc65af364af1ed3c8dbe")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@:5.4.99", when="@0.18.0:")

    variant("python", default=False, description="Provide Python bindings for jsonnet")
    extends("python", when="+python")
    depends_on("py-setuptools", type=("build",), when="+python")
    depends_on("py-pip", type=("build",), when="+python")
    depends_on("py-wheel", type=("build",), when="+python")

    @property
    def install_targets(self):
        return ["PREFIX={0}".format(self.prefix), "install"]

    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
