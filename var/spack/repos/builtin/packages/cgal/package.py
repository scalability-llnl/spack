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

    version("6.0.1", sha256="0acdfbf317c556630dd526f3253780f29b6ec9713ee92903e81b5c93c0f59b7f")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # @5: is header only and doesn't build shared libs
    variant(
        "shared", default=True, description="Enables the build of shared libraries", when="@:4.14"
    )

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    # header only is the default and only option for 5+
    # https://doc.cgal.org/latest/Manual/installation.html
    variant("header_only", default=False, description="Install in header only mode", when="@:4.13")

    # ---- See "7 CGAL Libraries" at:
    # https://doc.cgal.org/latest/Manual/installation.html

    # The CORE library provides exact arithmetic for geometric computations.
    # See: https://cs.nyu.edu/exact/core_pages/
    #      https://cs.nyu.edu/exact/core_pages/svn-core.html
    variant("core", default=False, description="Build the CORE library for algebraic numbers")
    variant("imageio", default=False, description="Build utilities to read/write image files")
    variant("demos", default=False, description="Build CGAL demos", when="@:5")
    variant("eigen", default=True, description="Build with Eigen support")

    # Starting with cgal 6, GMP/MPFR are no longer mandatory and Core library
    # is based on on Boost.Multiprecision. However, either GMP backend or Boost
    # backend can be used. Downstream cmake users must also set -DCGAL_DISABLE_GMP=1
    # or the macro CMAKE_OVERRIDDEN_DEFAULT_ENT_BACKEND if GMP is disabled.
    # This variant doesn't change how cgal is installed, but it does change spack to
    # not depend on gmp & mpfr.
    # More details here https://github.com/CGAL/cgal/issues/8606
    variant("gmp", default=True, description="Enable the GMP backend", when="@6:")

    # Upper bound follows CGAL's @6: CMakeLists.txt
    depends_on("cmake@3.12:3.29", type="build", when="@6:")
    depends_on("cmake@2.8.11:", type="build", when="@:5")

    # Essential Third Party Libraries
    depends_on("boost+exception+math+random+container", when="@5.0:")
    depends_on("boost@1.72.0:+exception+math+random+container", when="@6:")
    depends_on("boost+thread+system", when="@:5.0")

    depends_on("gmp", when="@:5")
    depends_on("mpfr", when="@:5")

    depends_on("gmp", when="@6: +gmp")
    depends_on("mpfr", when="@6: +gmp")

    # Required for CGAL_ImageIO
    # depends_on('opengl', when='+imageio') # not yet in Spack
    depends_on("zlib-api")

    # Optional to build CGAL_Qt5 (demos)
    # depends_on('opengl', when='+demos')   # not yet in Spack
    depends_on("qt@5:", when="@:5 +demos")

    # Demos are now based on qt6, but at the moment qt6 is not in spack
    # depends_on("qt@6:", when="@6: +demos")

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

    # @6: requires C++17 or later. The table gives tested
    # compilers, so use the lwoer limit of that as the bounds
    # https://www.cgal.org/2024/10/22/cgal601/
    with when("@6:"):
        # Gnu g++ 11.4.0 or later (on Linux or macOS)
        conflicts("%gcc @:11.3.0", when="platform=darwin")
        conflicts("%gcc @:11.3.0", when="platform=linux")

        # LLVM Clang version 15.0.7 or later (on Linux)
        conflicts("%clang @:15.0.6", when="platform=linux")

        # Apple Clang compiler versions 10.0.1, 12.0.5, and 15.0.0 (on macOS)
        # (10+ has C++17 support)
        conflicts("%apple-clang @:10.0.0", when="platform=darwin")

        # Visual C++ 15.9 or later
        conflicts("%msvc @:15.8", when="platform=windows")

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

        if spec.satisfies("@6:"):
            cmake_args.append("-DCXX_STANDARD=17")

        if spec.satisfies("@4.9:"):
            cmake_args.append("-DCGAL_HEADER_ONLY:BOOL=%s" % variant_bool("+header_only"))

        if spec.satisfies("~gmp"):
            cmake_args.append("-DCGAL_DISABLE_GMP:BOOL=1")

        return cmake_args
