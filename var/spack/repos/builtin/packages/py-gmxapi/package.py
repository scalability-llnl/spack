# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class PyGmxapi(PythonPackage):
    """Python bindings and ensemble workflow management for GROMACS.

    The GROMACS C++ API is affected by its package variants. You can
    specify a particular GROMACS API by making the dependency variant explicit.
    E.g. ``spack install gmxapi ^gromacs+mpi~double``
    """

    homepage = "https://manual.gromacs.org/current/gmxapi/index.html"
    maintainers("eirrgang", "peterkasson")

    pypi = "gmxapi/gmxapi-0.4.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.4.2", sha256="c746c6498c73a75913d7fcb01c13cc001d4bcb82999e9bf91d63578565ed1a1f")
    version("0.4.1", sha256="cc7a2e509ab8a59c187d388dcfd21ea78b785c3b355149b1818085f34dbda62a")
    version("0.4.0", sha256="7fd58e6a4b1391043379e8ba55555ebeba255c5b394f5df9d676e6a5571d7eba")

    depends_on("cxx", type="build")  # generated

    depends_on("gromacs@2022.1:~mdrun_only+shared")
    depends_on("mpi")
    depends_on("cmake@3.16:", type="build")
    depends_on("py-importlib-metadata", type="test", when="^python@:3.7")
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-networkx@2.0:", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pybind11@2.6:", type="build")
    depends_on("py-pybind11@2.6:", when="@:0.4", type=("build", "run"))
    depends_on("py-pytest@4.6:", type="test")

    def setup_build_environment(self, env):
        env.set("GROMACS_DIR", self.spec["gromacs"].prefix)
        env.set("gmxapi_ROOT", self.spec["gromacs"].prefix)
        env.set("Python3_ROOT", self.spec["python"].home)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            # test include helper points to right location
            python("-m", "pytest", "-x", os.path.join(self.build_directory, "test"))
