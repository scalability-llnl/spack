# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lemon(CMakePackage):
    """LEMON stands for Library for Efficient Modeling and Optimization in
    Networks. It is a C++ template library providing efficient implementations
    of common data structures and algorithms with focus on combinatorial
    optimization tasks connected mainly with graphs and networks."""

    homepage = "https://lemon.cs.elte.hu/trac/lemon"
    url = "https://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz"

    version("1.3.1", sha256="71b7c725f4c0b4a8ccb92eb87b208701586cf7a96156ebd821ca3ed855bad3c8")

    depends_on("cxx", type="build")  # generated

    # variant("coin", default=False, description="Enable Coin solver backend") #TODO build fails
    variant("ilog", default=False, description="Enable ILOG (CPLEX) solver backend")
    variant("glpk", default=True, description="Enable GLPK solver backend")
    # soplex not mentioned in docs but shown in cmakecache
    # variant("soplex", default=False, description="Enable SOPLEX solver backend") #TODO

    depends_on("glpk", when="+glpk")
    depends_on("cplex", when="+ilog")
    # depends_on("coinutils", when="+coin")  # just a guess
    # depends_on("cbc", when="+coin")
    # depends_on("clp", when="+coin")
    # depends_on("bzip2", when="+coin")
    # depends_on("soplex", when="+soplex") # no such package in Spack yet. TODO

    def cmake_args(self):
        spec = self.spec
        args = []
        args.extend(
            [
                # f"-DLEMON_ENABLE_COIN={spec.variants['coin'].value}", #TODO
                f"-DLEMON_ENABLE_ILOG={spec.variants['ilog'].value}",
                f"-DLEMON_ENABLE_GLPK={spec.variants['glpk'].value}",
                # f"-DLEMON_ENABLE_SOPLEX={spec.variants['soplex'].value}", #TODO
            ]
        )
        return args
