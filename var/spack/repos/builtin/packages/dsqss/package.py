# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class Dsqss(CMakePackage):
    """DSQSS is a program package for solving quantum many-body
    problems defined on lattices. It is based on the quantum Monte
    Carlo method in Feynman's path integral representation."""

    homepage = "https://www.pasums.issp.u-tokyo.ac.jp/dsqss/en/"
    url = "https://github.com/issp-center-dev/dsqss/releases/download/v2.0.3/dsqss-v2.0.3.tar.gz"

    license("GPL-3.0-or-later")

    version("2.0.3", sha256="11255dd1f1317fb4ac2d6ae95535f027d627d03f5470717cd277dd9ab94496e0")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="build mpi support")

    depends_on("mpi", when="+mpi")
    depends_on("python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")

    patch("spackpip.patch")
    patch("ctest.patch")

    extends("python")

    # Built-in tests are stored as JSON files.
    # The archive contains "resource fork" files such as "._dimer_1.json".
    # In Linux, the test system tried to test "._dimer_1.json" and failed.
    @run_before("cmake")
    def rm_macos(self):
        if sys.platform != "darwin":
            for mfile in find("test", "._*.json", recursive=True):
                force_remove(mfile)

    def cmake_args(self):
        args = [self.define_from_variant("ENABLE_MPI", "mpi")]

        return args

    def test_dla(self):
        """prepare, run, and confirm dla results"""
        test01 = find(self.prefix.share, "01_spindimer")[0]
        copy(join_path(test01, "std.toml"), ".")

        # prepare
        opts = [self.spec.prefix.bin.dla_pre, "std.toml"]
        with test_part(self, "test_dla_pre", purpose="prepare dla"):
            python(*opts)

        # (mpi) run
        opts = []
        if self.spec.satisfies("+mpi"):
            exe_name = self.spec["mpi"].prefix.bin.mpirun
            opts.extend(["-n", "1"])
            opts.append(join_path(self.prefix.bin, "dla"))
        else:
            exe_name = "dla"
        opts.append("param.in")
        with test_part(self, "test_dla_run", purpose="run dla"):
            exe = which(exe_name)
            exe(*opts)

        with test_part(self, "test_dla_results", purpose="confirming dla results"):
            cat = which("cat")
            out = cat("sample.log", output=str.split, error=str.split)
            assert "R ene = -3.74300000e-01 2.96344394e-03" in out
