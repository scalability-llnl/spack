# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kassiopeia(CMakePackage):
    """Simulation of electric and magnetic fields and particle tracking."""

    homepage = "https://katrin-experiment.github.io/Kassiopeia/"
    url = "https://github.com/KATRIN-Experiment/Kassiopeia/archive/v3.6.1.tar.gz"
    git = "https://github.com/KATRIN-Experiment/Kassiopeia.git"

    tags = ["hep"]

    maintainers("wdconinc")

    version("main", branch="main")
    version("3.8.2", sha256="9da59697365540a8b0d66e9a63f57aff6d868f7c5b39dfec28bb11ec83f31527")
    version("3.8.0", sha256="ae44c2d485fadaa6f562388064a211ae51b7d06bab7add2723ab0c8b21eb7e8f")
    version("3.7.7", sha256="b5f62b2e796fac57698794b46b63acbc47ce02010bd1f716996918a550b22a21")
    version("3.7.6", sha256="fa20cf0f29ee2312bf96b07661d7b5c9303782d907671acd01032cc1f13edd55")
    version("3.7.5", sha256="8f28d08c7ef51e64221e0a4705f3cee3a5d738b8cdde5ce9fa58a3a0dd14ae05")
    version("3.7.4", sha256="c1514163a084530930be10dbe487fb1950ccbc9662a4a190bdecffbd84a71fd4")
    version("3.7.3", sha256="a8753585b9fa0903e1f5f821c4ced3cddd72792ad7e6075a7e25318f81ad9eaa")
    version("3.7.2", sha256="bdfdf8c26fa5ad19e8b9c6eb600dfbd3c8218cd695ce067f10633b63bd192f92")
    version("3.7.1", sha256="b22ae2fe5c2271bdf6aaf65d9ecf57ff0d6a88d28ad26d176e1129f0e58faea4")
    version("3.7.0", sha256="32a3e98c77d1b97fe9862cf1d8c6ba8e6c82fb9295a6a217c7ce77cbec751046")
    version("3.6.1", sha256="30193d5384ad81b8570fdcd1bb35b15cc365ab84712819ac0d989c6f5cf6f790")
    version("3.5.0", sha256="b704d77bd182b2806dc8323f642d3197ce21dba3d456430f594b19a7596bda22")
    version("3.4.0", sha256="4e2bca61011e670186d49048aea080a06c3c95dacf4b79e7549c36960b4557f4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("root", default=False, description="Include support for writing ROOT files")
    variant("vtk", default=False, description="Include visualization support through VTK")
    variant("mpi", default=False, description="Include MPI support for field calculations")
    variant("tbb", default=False, description="Include Intel TBB support for field calculations")
    variant("opencl", default=False, description="Include OpenCL support for field calculations")
    variant("log4cxx", default=False, description="Use log4cxx for logging")
    variant("boost", default=False, description="Build Boost dependent modules")

    depends_on("cmake@3.13:", type="build")
    depends_on("zlib-api")
    depends_on("root@6.0.0:", when="+root")
    depends_on("vtk@6.1:", when="+vtk")
    depends_on("mpi", when="+mpi")
    depends_on("tbb", when="+tbb")
    depends_on("opencl", when="+opencl")
    depends_on("log4cxx", when="+log4cxx")
    depends_on("boost", when="+boost")

    @when("@:3.8.0")
    def patch(self):
        filter_file("LANGUAGES CXX", "LANGUAGES CXX C", "CMakeLists.txt")
        filter_file(
            '#include "vtkXMLPolyDataWriter.h"',
            '#include "vtkXMLPolyDataWriter.h"\n#include "vtkUnsignedCharArray.h"',
            "KGeoBag/Source/Visualization/Vtk/Source/KGVTKGeometryPainter.cc",
        )

    def cmake_args(self):
        if self.spec.satisfies("+root"):
            cxxstd = self.spec["root"].variants["cxxstd"].value
        else:
            if self.spec.satisfies("@:3.8.1"):
                cxxstd = "14"
            else:
                cxxstd = "17"
        args = [
            self.define_from_variant("KASPER_USE_BOOST", "boost"),
            self.define_from_variant("KASPER_USE_VTK", "vtk"),
            self.define_from_variant("KASPER_USE_TBB", "tbb"),
            self.define_from_variant("KEMField_USE_MPI", "mpi"),
            self.define_from_variant("KEMField_USE_OPENCL", "opencl"),
            self.define_from_variant("Kommon_USE_Log4CXX", "log4cxx"),
            self.define("CMAKE_CXX_STANDARD", cxxstd),
        ]
        return args
