# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Opencascade(CMakePackage):
    """Open CASCADE Technology is a software development kit (SDK)
    intended for development of applications dealing with 3D CAD data,
    freely available in open source. It includes a set of C++ class
    libraries providing services for 3D surface and solid modeling,
    visualization, data exchange and rapid application development."""

    homepage = "https://www.opencascade.com"
    url = "https://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=refs/tags/V7_4_0;sf=tgz"
    git = "https://git.dev.opencascade.org/repos/occt.git"

    maintainers("wdconinc")

    license("LGPL-2.1-only")

    with default_args(extension="tar.gz"):
        version("7.8.1", sha256="33f2bdb67e3f6ae469f3fa816cfba34529a23a9cb736bf98a32b203d8531c523")
        version("7.8.0", sha256="b9c8f0a9d523ac1a606697f95fc39d8acf1140d3728561b8010a604431b4e9cf")
        version("7.7.2", sha256="2fb23c8d67a7b72061b4f7a6875861e17d412d524527b2a96151ead1d9cfa2c1")
        version("7.7.1", sha256="f413d30a8a06d6164e94860a652cbc96ea58fe262df36ce4eaa92a9e3561fd12")
        version("7.7.0", sha256="075ca1dddd9646fcf331a809904925055747a951a6afd07a463369b9b441b445")
        version("7.6.3", sha256="baae5b3a7a38825396fc45ef9d170db406339f5eeec62e21b21036afeda31200")
        version("7.6.0", sha256="e7f989d52348c3b3acb7eb4ee001bb5c2eed5250cdcceaa6ae97edc294f2cabd")
        version(
            "7.5.3p5", sha256="29a4b4293f725bea2f32de5641b127452fc836a30e207d0daa5a0d1b746226b8"
        )
        version(
            "7.5.3p4", sha256="f7571462041694f6bc7fadd94b0c251762078713cb5b0484845b6b8a4d8a0b99"
        )
        version("7.5.3", sha256="cc3d3fd9f76526502c3d9025b651f45b034187430f231414c97dda756572410b")
        version("7.5.2", sha256="1a32d2b0d6d3c236163cb45139221fb198f0f3cdad56606c5b1c9a2a8869b3ac")
        version(
            "7.4.0p2", sha256="93565f9bdc9575e0d6fcb34c11c8f06d8f9394250bb427870da65424e8537f60"
        )
        version(
            "7.4.0p1", sha256="e00fedc221560fda31653c23a8f3d0eda78095c87519f338d4f4088e2ee9a9c0"
        )
        version("7.4.0", sha256="655da7717dac3460a22a6a7ee68860c1da56da2fec9c380d8ac0ac0349d67676")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # fix for numeric_limits in gcc-12; applies cleanly to all older versions
    patch(
        "https://git.dev.opencascade.org/gitweb/?p=occt.git;a=patch;h=2a8c5ad46cfef8114b13c3a33dcd88a81e522c1e",
        sha256="bd0d7463259f469f8fc06a2b11eec7b0c89882aeea2f8c8647cf750c44b3e656",
        when="@:7.7.0",
    )

    # Modules, per DAG at https://dev.opencascade.org/doc/refman/html/
    variant("modeling_data", default=True, description="Build Modeling Data module")
    variant(
        "modeling_algorithms",
        default=True,
        description="Build Modeling Algorithms module",
        when="+modeling_data",
    )
    variant(
        "visualization",
        default=True,
        description="Bulid Visualization module",
        when="+modeling_algorithms",
    )
    variant(
        "application_framework",
        default=True,
        description="Build Application Framework module",
        when="+visualization",
    )
    variant(
        "data_exchange",
        default=True,
        description="Build Data Exchange module",
        when="+application_framework",
    )
    variant("draw", default=True, description="Build Draw module", when="+data_exchange")

    # 3rd party
    variant("tbb", default=False, description="Build with Intel Threading Building Blocks")
    variant("tk", default=False, description="Build with Tk support")
    variant("vtk", default=False, description="Enable VTK support")
    variant("ffmpeg", default=False, description="Enable FFmpeg support")
    variant("freeimage", default=False, description="Build with FreeImage")
    variant("freetype", default=False, description="Build with freetype")
    variant("rapidjson", default=False, description="Build with rapidjson")

    depends_on("tbb", when="+tbb")
    depends_on("intel-tbb@2021.5: build_type=Release", when="@7.7 +tbb")
    depends_on("intel-tbb@:2020.3", when="@7.6 +tbb")

    depends_on("vtk", when="+vtk")
    depends_on("vtk", when="@7.6 +vtk")

    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("freeimage", when="+freeimage")
    depends_on("freetype", when="+freetype")
    depends_on("rapidjson", when="+rapidjson")

    depends_on("libxext")
    depends_on("libxmu")
    depends_on("libxi")
    depends_on("libxt")
    depends_on("tcl")
    depends_on("tk", when="+tk")
    depends_on("gl")

    conflicts("^vtk@9.2", when="@:7.7.0 +vtk")

    def url_for_version(self, version):
        url = (
            "https://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=refs/tags/V{0};sf=tgz"
        )
        return url.format(version.underscored)

    def cmake_args(self):
        spec = self.spec

        def build_module(occt_module):
            # CamelCase to snake_case
            spack_variant = re.sub(r"(?<!^)(?=[A-Z])", "_", occt_module).lower()
            enabled = spec.satisfies("+" + spack_variant)
            return self.define(f"BUILD_MODULE_{occt_module}", enabled)

        def use_3rdparty(feature, spack_variant=None, depends_on=None, extra_dirs=[]):
            if spack_variant is None:
                spack_variant = feature.lower()
            if depends_on is None:
                depends_on = feature.lower()
            if spack_variant in spec.variants:
                enabled = spec.satisfies("+" + spack_variant)
            else:
                enabled = True
            args = []
            args.append("-DUSE_{}={}".format(feature.upper(), enabled))
            if enabled:
                args.append(
                    "-D3RDPARTY_{}_DIR={}".format(feature.upper(), spec[depends_on].prefix)
                )
                for dir in extra_dirs:
                    args.append(
                        "-D3RDPARTY_{}_{}_DIR={}".format(
                            feature.upper(), dir.upper(), join_path(spec[depends_on].prefix, dir)
                        )
                    )
            return args

        args = []

        # Disable documentation building
        args.append("-DBUILD_DOC_Overview=OFF")

        # Always build the foundation classes
        args.append(self.define("BUILD_MODULE_FoundationClasses", True))
        # Specify which modules to build
        for module in [
            "ApplicationFramework",
            "Draw",
            "DataExchange",
            "ModelingAlgorithms",
            "ModelingData",
            "Visualization",
        ]:
            args.append(build_module(module))

        # Specify which 3rd party features to build
        args += use_3rdparty("tcl")
        args += use_3rdparty("tk")
        args += use_3rdparty("ffmpeg")
        args += use_3rdparty("freeimage")
        args += use_3rdparty("freetype")
        args += use_3rdparty("rapidjson")
        args += use_3rdparty("tbb", depends_on="intel-tbb")
        args += use_3rdparty("vtk", extra_dirs=["lib", "include"])

        return args
