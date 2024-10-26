# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpi4py(PythonPackage):
    """This package provides Python bindings for the Message Passing
    Interface (MPI) standard. It is implemented on top of the
    MPI-1/MPI-2 specification and exposes an API which grounds on the
    standard MPI-2 C++ bindings.
    """

    pypi = "mpi4py/mpi4py-3.0.3.tar.gz"
    git = "https://github.com/mpi4py/mpi4py.git"

    license("BSD-3-Clause", when="@4:")
    license("BSD-2-Clause", when="@:3")

    version("master", branch="master")
    version("4.0.0", sha256="820d31ae184d69c17d9b5d55b1d524d56be47d2e6cb318ea4f3e7007feff2ccc")
    version("3.1.6", sha256="c8fa625e0f92b082ef955bfb52f19fa6691d29273d7d71135d295aa143dee6cb")
    version("3.1.5", sha256="a706e76db9255135c2fb5d1ef54cb4f7b0e4ad9e33cbada7de27626205f2a153")
    version("3.1.4", sha256="17858f2ebc623220d0120d1fa8d428d033dde749c4bc35b33d81a66ad7f93480")
    version("3.1.3", sha256="f1e9fae1079f43eafdd9f817cdb3fd30d709edc093b5d5dada57a461b2db3008")
    version("3.1.2", sha256="40dd546bece8f63e1131c3ceaa7c18f8e8e93191a762cd446a8cfcf7f9cce770")
    version("3.1.1", sha256="e11f8587a3b93bb24c8526addec664b586b965d83c0882b884c14dc3fd6b9f5c")
    version("3.1.0", sha256="134fa2b2fe6d8f91bcfcc2824cfd74b55ca3dcbff4d185b1bda009beea9232ec")
    version("3.0.3", sha256="012d716c8b9ed1e513fcc4b18e5af16a8791f51e6d1716baccf988ad355c5a1f")
    version("3.0.1", sha256="6549a5b81931303baf6600fa2e3bc04d8bd1d5c82f3c21379d0d64a9abcca851")
    version("3.0.0", sha256="b457b02d85bdd9a4775a097fac5234a20397b43e073f14d9e29b6cd78c68efd7")
    version("2.0.0", sha256="6543a05851a7aa1e6d165e673d422ba24e45c41e4221f0993fe1e5924a00cb81")
    version("1.3.1", sha256="e7bd2044aaac5a6ea87a87b2ecc73b310bb6efe5026031e33067ea3c2efc3507")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40.9:", type="build")
    depends_on("py-cython@3:", when="@4:", type="build")
    depends_on("py-cython@0.27:2", when="@:3.1.6", type="build")
    depends_on("py-cython@0.27:3", when="@master", type="build")
    depends_on("mpi")

    def setup_build_environment(self, env):
        env.set("MPICC", self.spec["mpi"].mpicc)

    @run_before("install")
    def cythonize(self):
        with working_dir(self.build_directory):
            python(join_path("conf", "cythonize.py"))
