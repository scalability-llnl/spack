# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Apfel(AutotoolsPackage, CMakePackage):
    """APFEL is a library able to perform DGLAP evolution up to NNLO in QCD and
    to NLO in QED, both with pole and MSbar masses. The coupled DGLAP
    QCD+QED evolution equations are solved in x-space by means of higher
    order interpolations and Runge-Kutta techniques."""

    homepage = "https://github.com/scarrazza/apfel"
    url = "https://github.com/scarrazza/apfel/archive/3.0.4.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    build_system(
        conditional("autotools", when="@:3.0"), conditional("cmake", when="@3.1:"), default="cmake"
    )

    version("3.1.1", sha256="9006b2a9544e504e8f6b5047f665054151870c3c3a4a05db3d4fb46f21908d4b")
    version("3.0.6", sha256="7063c9eee457e030b97926ac166cdaedd84625b31397e1dfd01ae47371fb9f61")
    version("3.0.4", sha256="c7bfae7fe2dc0185981850f2fe6ae4842749339d064c25bf525b4ef412bbb224")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    with when("build_system=cmake"):
        depends_on("cmake@03.15:")

    extends("python", when="+python")
    depends_on("swig", when="+python")
    depends_on("python", when="+python", type=("build", "run"))
    depends_on("lhapdf", when="+lhapdf", type=("build", "run"))

    variant("python", description="Build python wrapper", default=False)
    variant("lhapdf", description="Link to LHAPDF", default=False)


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define_from_variant("APFEL_ENABLE_PYTHON", "python"),
            self.define_from_variant("APFEL_ENABLE_LHAPDF", "lhapdf"),
        ]
        # ensure installation of python module under CMAKE_INSTALL_PREFIX
        if self.spec.satisfies("+python"):
            args.append(self.define("APFEL_Python_SITEARCH", "autoprefix"))
        return args


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        args += self.enable_or_disable("pywrap", variant="python")
        args += self.enable_or_disable("lhapdf")
        return args
