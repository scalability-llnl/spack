# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cgal(CMakePackage):
    """The Computational Geometry Algorithms Library (CGAL) is a C++ library
    that aims to provide easy access to efficient and reliable algorithms in
    computational geometry. CGAL is used in various areas needing geometric
    computation, such as geographic information systems, computer aided design,
    molecular biology, medical imaging, computer graphics, and robotics.
    """

    homepage = "https://www.cgal.org/"
    url = "https://github.com/CGAL/cgal/releases/download/v5.4.1/CGAL-5.4.1.tar.xz"

    version("5.6", sha256="dcab9b08a50a06a7cc2cc69a8a12200f8d8f391b9b8013ae476965c10b45161f")
    version("5.5.3", sha256="0a04f662693256328b05babfabb5e3a5b7db2f5a58d52e3c520df9d0828ddd73")
    version("5.5.2", sha256="b2b05d5616ecc69facdc24417cce0b04fb4321491d107db45103add520e3d8c3")
    version("5.4.1", sha256="4c3dd7ee4d36d237111a4d72b6e14170093271595d5b695148532daa95323d76")
    version("5.3.2", sha256="af917dbc550388ebcb206f774e610fbdb914d95a4b2932fa952279129103852b")
    version("5.1.5", sha256="b1bb8a6053aa12baa5981aef20a542cd3e617a86826963fb8fb6852b1a0da97c")
    version("5.0.3", sha256="e5a3672e35e5e92e3c1b4452cd3c1d554f3177dc512bd98b29edf21866a4288c")
    version("5.0", sha256="e1e7e932988c5d149aa471c1afd69915b7603b5b31b9b317a0debb20ecd42dcc")
    version("4.13", sha256="3e3dd7a64febda58be54c3cbeba329ab6a73b72d4d7647ba4931ecd1fad0e3bc")
    version("4.12", sha256="442ef4fffb2ad6e4141e5a7902993ae6a4e73f7cb641fae1010bb586f6ca5e3f")
    version("4.11", sha256="27a7762e5430f5392a1fe12a3a4abdfe667605c40224de1c6599f49d66cfbdd2")
    version("4.9.1", sha256="56557da971b5310c2678ffc5def4109266666ff3adc7babbe446797ee2b90cca")
    version("4.9", sha256="63ac5df71f912f34f2f0f2e54a303578df51f4ec2627db593a65407d791f9039")
    version("4.7", sha256="50bd0a1cad7a8957b09012f831eebaf7d670e2a3467e8f365ec0c71fa5436369")
    version("4.6.3", sha256="e338027b8767c0a7a6e4fd8679182d1b83b5b1a0da0a1fe4546e7c0ca094fc21")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("header_only", default=False, description="Install in header only mode")

    # ---- See "7 CGAL Libraries" at:
    # https://doc.cgal.org/latest/Manual/installation.html

    # The CORE library provides exact arithmetic for geometric computations.
    # See: https://cs.nyu.edu/exact/core_pages/
    #      https://cs.nyu.edu/exact/core_pages/svn-core.html
    variant("core", default=False, description="Build the CORE library for algebraic numbers")
    variant("imageio", default=False, description="Build utilities to read/write image files")
    variant("demos", default=False, description="Build CGAL demos")
    variant("eigen", default=True, description="Build with Eigen support")

    depends_on("cmake@2.8.11:", type="build")

    # Essential Third Party Libraries
    depends_on("boost+exception+math+random+container", when="@5.0:")
    depends_on("boost+thread+system", when="@:5.0")
    depends_on("gmp")
    depends_on("mpfr")

    # Required for CGAL_ImageIO
    # depends_on('opengl', when='+imageio') # not yet in Spack
    depends_on("zlib-api")

    # Optional to build CGAL_Qt5 (demos)
    # depends_on('opengl', when='+demos')   # not yet in Spack
    depends_on("qt@5:", when="+demos")

    # Optional Third Party Libraries
    depends_on("eigen", when="+eigen")

    # depends_on('leda')
    # depends_on('mpfi')
    # depends_on('rs')
    # depends_on('rs3')
    # depends_on('ntl')
    # depends_on('libqglviewer')
    # depends_on('esbtl')
    # depends_on('intel-tbb')

    conflicts(
        "~header_only",
        when="@:4.9",
        msg="Header only builds became optional in 4.9," " default thereafter",
    )

    def url_for_version(self, version):
        url = "https://github.com/CGAL/cgal/releases/download/"
        if version <= Version("5.0.3"):
            url += "releases/CGAL-{0}/CGAL-{0}.tar.xz"
        else:
            url += "v{0}/CGAL-{0}.tar.xz"

        return url.format(version)

    def setup_build_environment(self, env):
        spec = self.spec

        env.set("BOOST_INCLUDEDIR", spec["boost"].headers.directories[0])
        env.set("BOOST_LIBRARYDIR", spec["boost"].libs.directories[0])

        if spec.satisfies("+eigen"):
            env.set("EIGEN3_INC_DIR", spec["eigen"].headers.directories[0])

    def cmake_args(self):
        # Installation instructions:
        # https://doc.cgal.org/latest/Manual/installation.html
        spec = self.spec
        variant_bool = lambda feature: str(feature in spec)
        cmake_args = []

        cmake_args.append("-DBUILD_SHARED_LIBS:BOOL=%s" % variant_bool("+shared"))
        cmake_args.append("-DWITH_CGAL_Core:BOOL=%s" % variant_bool("+core"))
        cmake_args.append("-DWITH_CGAL_ImageIO:BOOL=%s" % variant_bool("+imageio"))
        cmake_args.append("-DWITH_CGAL_Qt5:BOOL=%s" % variant_bool("+demos"))

        if spec.satisfies("@4.9:"):
            cmake_args.append("-DCGAL_HEADER_ONLY:BOOL=%s" % variant_bool("+header_only"))

        return cmake_args
