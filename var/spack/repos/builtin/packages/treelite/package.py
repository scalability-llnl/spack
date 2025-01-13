# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Treelite(CMakePackage):
    """Treelite is a model compiler for efficient deployment of
    decision tree ensembles."""

    homepage = "https://github.com/dmlc/treelite"
    url = "https://github.com/dmlc/treelite/archive/0.93.tar.gz"

    license("Apache-2.0")

    version("0.93", sha256="7d347372f7fdc069904afe93e69ed0bf696ba42d271fe2f8bf6835d2ab2f45d5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("protobuf", default=False, description="Build with protobuf")
    variant("python", default=True, description="Build with python support")

    depends_on("protobuf", when="+protobuf")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", when="+python", type="build")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    # https://github.com/dmlc/treelite/issues/560
    depends_on("py-numpy@:1", when="@:4.2.0+python", type=("build", "run"))
    depends_on("py-scipy", when="+python", type=("build", "run"))

    build_directory = "build"

    def cmake_args(self):
        args = []

        if "+protobuf" in self.spec:
            args.append("-DENABLE_PROTOBUF:BOOL=ON")
            args.append("-DProtobuf_LIBRARY={0}".format(self.spec["protobuf"].prefix))
        else:
            args.append("-DENABLE_PROTOBUF:BOOL=OFF")

        return args

    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            with working_dir("python"):
                pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
