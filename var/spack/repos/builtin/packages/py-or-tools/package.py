# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyOrTools(CMakePackage):
    """This project hosts operations research tools developed at
    Google and made available as open source under the Apache 2.0
    License."""

    homepage = "https://developers.google.com/optimization/"
    url = "https://github.com/google/or-tools/archive/v7.8.tar.gz"

    license("Apache-2.0")

    version("7.8", sha256="d93a9502b18af51902abd130ff5f23768fcf47e266e6d1f34b3586387aa2de68")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.14:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-protobuf@3.12.2:", type=("build", "run"))
    depends_on("protobuf@3.12.2:")
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("gflags@2.2.2")
    depends_on("glog@0.4.0")
    depends_on("protobuf@3.12.2")
    depends_on("abseil-cpp@20200225.2")
    depends_on("cbc@2.10.5")
    depends_on("cgl@0.60.3")
    depends_on("clp@1.17.4")
    depends_on("osi@0.108.6")
    depends_on("coinutils@2.11.4")
    depends_on("swig")
    depends_on("python", type=("build", "run"))
    depends_on("py-wheel", type="build")
    depends_on("py-virtualenv", type="build")
    depends_on("scipoptsuite")

    extends("python")

    def cmake_args(self):
        cmake_args = []
        cmake_args.append("-DBUILD_DEPS=OFF")
        cmake_args.append("-DBUILD_PYTHON=ON")
        cmake_args.append("-DBUILD_TESTING=OFF")
        return cmake_args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")
        with working_dir(join_path(self.build_directory, "python")):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
