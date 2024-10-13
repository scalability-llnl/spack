# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from pathlib import Path

from spack.package import *


class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
    libraries, emphasizing libraries that work well with the C++
    Standard Library.

    Boost libraries are intended to be widely useful, and usable
    across a broad spectrum of applications. The Boost license
    encourages both commercial and non-commercial use.
    """

    homepage = "https://www.boost.org"
    url = "https://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2"
    git = "https://github.com/boostorg/boost.git"
    list_url = "https://sourceforge.net/projects/boost/files/boost/"
    list_depth = 1
    maintainers("hainest")

    license("BSL-1.0")

    version("develop", branch="develop", submodules=True)
    version("1.86.0", sha256="1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b")
    version("1.85.0", sha256="7009fe1faa1697476bdc7027703a2badb84e849b7b0baad5086b087b971f8617")
    version("1.84.0", sha256="cc4b893acf645c9d4b698e9a0f08ca8846aa5d6c68275c14c3e7949c24109454")
    version("1.83.0", sha256="6478edfe2f3305127cffe8caf73ea0176c53769f4bf1585be237eb30798c3b8e")
    version("1.82.0", sha256="a6e1ab9b0860e6a2881dd7b21fe9f737a095e5f33a3a874afc6a345228597ee6")
    version("1.81.0", sha256="71feeed900fbccca04a3b4f2f84a7c217186f28a940ed8b7ed4725986baf99fa")
    version("1.80.0", sha256="1e19565d82e43bc59209a168f5ac899d3ba471d55c7610c677d4ccf2c9c500c0")
    version("1.79.0", sha256="475d589d51a7f8b3ba2ba4eda022b170e562ca3b760ee922c146b6c65856ef39")
    version("1.78.0", sha256="8681f175d4bdb26c52222665793eef08490d7758529330f98d3b29dd0735bccc")
    version("1.77.0", sha256="fc9f85fc030e233142908241af7a846e60630aa7388de9a5fafb1f3a26840854")
    version("1.76.0", sha256="f0397ba6e982c4450f27bf32a2a83292aba035b827a5623a14636ea583318c41")
    version("1.75.0", sha256="953db31e016db7bb207f11432bef7df100516eeb746843fa0486a222e3fd49cb")
    version("1.74.0", sha256="83bfc1507731a0906e387fc28b7ef5417d591429e51e788417fe9ff025e116b1")
    version("1.73.0", sha256="4eb3b8d442b426dc35346235c8733b5ae35ba431690e38c6a8263dce9fcbb402")
    version("1.72.0", sha256="59c9b274bc451cf91a9ba1dd2c7fdcaf5d60b1b3aa83f2c9fa143417cc660722")
    version("1.71.0", sha256="d73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee")
    version("1.70.0", sha256="430ae8354789de4fd19ee52f3b1f739e1fba576f0aded0897c3c2bc00fb38778")
    version("1.69.0", sha256="8f32d4617390d1c2d16f26a27ab60d97807b35440d45891fa340fc2648b04406")
    version("1.68.0", sha256="7f6130bc3cf65f56a618888ce9d5ea704fa10b462be126ad053e80e553d6d8b7")
    version("1.67.0", sha256="2684c972994ee57fc5632e03bf044746f6eb45d4920c343937a465fd67a5adba")
    version("1.66.0", sha256="5721818253e6a0989583192f96782c4a98eb6204965316df9f5ad75819225ca9")
    version("1.65.1", sha256="9807a5d16566c57fd74fb522764e0b134a8bbe6b6e8967b83afefd30dcd3be81")
    version("1.65.0", sha256="ea26712742e2fb079c2a566a31f3266973b76e38222b9f88b387e3c8b2f9902c")
    version("1.64.0", sha256="7bcc5caace97baa948931d712ea5f37038dbb1c5d89b43ad4def4ed7cb683332")
    version("1.63.0", sha256="beae2529f759f6b3bf3f4969a19c2e9d6f0c503edcb2de4a61d1428519fcb3b0")
    version("1.62.0", sha256="36c96b0f6155c98404091d8ceb48319a28279ca0333fba1ad8611eb90afb2ca0")
    version("1.61.0", sha256="a547bd06c2fd9a71ba1d169d9cf0339da7ebf4753849a8f7d6fdb8feee99b640")
    version("1.60.0", sha256="686affff989ac2488f79a97b9479efb9f2abae035b5ed4d8226de6857933fd3b")
    version("1.59.0", sha256="727a932322d94287b62abb1bd2d41723eec4356a7728909e38adb65ca25241ca")
    version("1.58.0", sha256="fdfc204fc33ec79c99b9a74944c3e54bd78be4f7f15e260c0e2700a36dc7d3e5")
    version("1.57.0", sha256="910c8c022a33ccec7f088bd65d4f14b466588dda94ba2124e78b8c57db264967")
    version("1.56.0", sha256="134732acaf3a6e7eba85988118d943f0fa6b7f0850f65131fff89823ad30ff1d")
    version("1.55.0", sha256="fff00023dd79486d444c8e29922f4072e1d451fc5a4d2b6075852ead7f2b7b52")
    version("1.54.0", sha256="047e927de336af106a24bceba30069980c191529fd76b8dff8eb9a328b48ae1d")
    version("1.53.0", sha256="f88a041b01882b0c9c5c05b39603ec8383fb881f772f6f9e6e6fd0e0cddb9196")
    version("1.52.0", sha256="222b6afd7723f396f5682c20130314a10196d3999feab5ba920d2a6bf53bac92")
    version("1.51.0", sha256="fb2d2335a29ee7fe040a197292bfce982af84a645c81688a915c84c925b69696")
    version("1.50.0", sha256="c9ace2b8c81fa6703d1d17c7e478de3bc51101c5adbdeb3f6cb72cf3045a8529")
    version("1.49.0", sha256="dd748a7f5507a7e7af74f452e1c52a64e651ed1f7263fce438a06641d2180d3c")
    version("1.48.0", sha256="1bf254b2d69393ccd57a3cdd30a2f80318a005de8883a0792ed2f5e2598e5ada")
    version("1.47.0", sha256="815a5d9faac4dbd523fbcf3fe1065e443c0bbf43427c44aa423422c6ec4c2e31")
    version("1.46.1", sha256="e1dfbf42b16e5015c46b98e9899c423ca4d04469cbeee05e43ea19236416d883")
    version("1.46.0", sha256="2f90f60792fdc25e674b8a857a0bcbb8d01199651719c90d5c4f8c61c08eba59")
    version("1.45.0", sha256="55ed3ec51d5687e8224c988e22bef215dacce04e037d9f689569a80c4377a6d5")
    version("1.44.0", sha256="45c328029d97d1f1dc7ff8c9527cd0c5cc356636084a800bca2ee4bfab1978db")
    version("1.43.0", sha256="344f100b1aa410e812cabf0e4130728a80be042bf346135516b9187853806120")
    version("1.42.0", sha256="4b1eb95bd250ce15ac66435d6167f225b072b0d3a7eb72477a31847a9ca9e609")
    version("1.41.0", sha256="1ef94e6749eaf13318284b4f629be063544c7015b45e38113b975ac1945cc726")
    version("1.40.0", sha256="36cf4a239b587067a4923fdf6e290525a14c3af29829524fa73f3dec6841530c")
    version("1.39.0", sha256="44785eae8c6cce61a29a8a51f9b737e57b34d66baa7c0bcd4af188832b8018fd")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with_default_variants = "boost" + "".join(
        [
            "+atomic",
            "+chrono",
            "+date_time",
            "+exception",
            "+filesystem",
            "+graph",
            "+iostreams",
            "+locale",
            "+log",
            "+math",
            "+program_options",
            "+random",
            "+regex",
            "+serialization",
            "+signals",
            "+system",
            "+test",
            "+thread",
            "+timer",
            "+wave",
        ]
    )

    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    #
    # Boost.Container can be both header-only and compiled. '+container'
    # indicates the compiled version which requires Extended Allocator
    # support. The header-only library is installed when no variant is given.
    all_libs = [
        "atomic",
        "charconv",
        "chrono",
        "cobalt",
        "container",
        "context",
        "contract",
        "coroutine",
        "date_time",
        "exception",
        "fiber",
        "filesystem",
        "graph",
        "graph_parallel",
        "iostreams",
        "json",
        "locale",
        "log",
        "math",
        "mpi",
        "nowide",
        "program_options",
        "python",
        "random",
        "regex",
        "serialization",
        "signals",
        "stacktrace",
        "system",
        "test",
        "thread",
        "timer",
        "type_erasure",
        "url",
        "wave",
    ]

    for lib in all_libs:
        variant(lib, default=False, description="Compile with {0} library".format(lib))

    @property
    def libs(self):
        query = self.spec.last_query.extra_parameters
        shared = "+shared" in self.spec

        libnames = (
            query if query else [lib for lib in self.all_libs if self.spec.satisfies("+%s" % lib)]
        )
        libnames += ["monitor"]
        libraries = ["libboost_*%s*" % lib for lib in libnames]

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    variant(
        "context-impl",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="Use the specified backend for boost-context",
        when="@1.65.0: +context",
    )

    variant(
        "cxxstd",
        default="11",
        values=(
            "98",
            "11",
            "14",
            # C++17 is not supported by Boost < 1.63.0.
            conditional("17", when="@1.63.0:"),
            # C++20/2a is not supported by Boost < 1.73.0
            conditional("2a", when="@1.73.0:"),
            conditional("20", when="@1.77.0:"),
            conditional("23", when="@1.79.0:"),
            conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # 1.84.0 dropped support for 98/03
    conflicts("cxxstd=98", when="@1.84.0:")

    variant("debug", default=False, description="Switch to the debug version of Boost")
    variant("shared", default=True, description="Additionally build shared libraries")
    variant(
        "multithreaded", default=True, description="Build multi-threaded versions of libraries"
    )
    variant(
        "singlethreaded", default=False, description="Build single-threaded versions of libraries"
    )
    variant("icu", default=False, description="Build with Unicode and ICU suport")
    variant("taggedlayout", default=False, description="Augment library names with build options")
    variant(
        "versionedlayout",
        default=False,
        description="Augment library layout with versioned subdirs",
    )
    variant(
        "clanglibcpp", default=False, description="Compile with clang libc++ instead of libstdc++"
    )
    variant("numpy", default=False, description="Build the Boost NumPy library (requires +python)")
    variant(
        "pic",
        default=False,
        description="Generate position-independent code (PIC), useful "
        "for building static libraries",
    )

    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    variant(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        description="Default symbol visibility in compiled libraries " "(1.69.0 or later)",
    )

    # Unicode support
    depends_on("icu4c", when="+icu")
    depends_on("icu4c cxxstd=11", when="+icu cxxstd=11")
    depends_on("icu4c cxxstd=14", when="+icu cxxstd=14")
    depends_on("icu4c cxxstd=17", when="+icu cxxstd=17")
    conflicts("cxxstd=98", when="+icu")  # Requires c++11 at least

    depends_on("python", when="+python")
    # https://github.com/boostorg/python/commit/cbd2d9f033c61d29d0a1df14951f4ec91e7d05cd
    depends_on("python@:3.9", when="@:1.75 +python")

    depends_on("mpi", when="+mpi")
    depends_on("bzip2", when="+iostreams")
    depends_on("zlib-api", when="+iostreams")
    depends_on("zstd", when="+iostreams")
    depends_on("xz", when="+iostreams")
    depends_on("py-numpy", when="+numpy", type=("build", "run"))
    # https://github.com/boostorg/python/issues/431
    depends_on("py-numpy@:1", when="@:1.85+numpy", type=("build", "run"))

    # Improve the error message when the context-impl variant is conflicting
    conflicts("context-impl=fcontext", when="@:1.65.0")
    conflicts("context-impl=ucontext", when="@:1.65.0")
    conflicts("context-impl=winfib", when="@:1.65.0")

    # Coroutine, Context, Fiber, etc., are not straightforward.
    conflicts("+context", when="@:1.50")  # Context since 1.51.0.
    conflicts("cxxstd=98", when="+context")  # Context requires >=C++11.
    conflicts("+coroutine", when="@:1.52")  # Context since 1.53.0.
    conflicts("~context", when="+coroutine")  # Coroutine requires Context.
    conflicts("+fiber", when="@:1.61")  # Fiber since 1.62.0.
    conflicts("cxxstd=98", when="+fiber")  # Fiber requires >=C++11.
    conflicts("~context", when="+fiber")  # Fiber requires Context.

    # NOTE: 1.64.0 seems fine for *most* applications, but if you need
    #       +python and +mpi, there seem to be errors with out-of-date
    #       API calls from mpi/python.
    #       See: https://github.com/spack/spack/issues/3963
    conflicts("@1.64.0", when="+python", msg="Errors with out-of-date API calls from Python")
    conflicts("@1.64.0", when="+mpi", msg="Errors with out-of-date API calls from MPI")

    conflicts("+taggedlayout", when="+versionedlayout")
    conflicts("+numpy", when="~python")

    # boost-python in 1.72.0 broken with cxxstd=98
    conflicts("cxxstd=98", when="+mpi+python @1.72.0")

    # Container's Extended Allocators were not added until 1.56.0
    conflicts("+container", when="@:1.55")

    # Boost.System till 1.76 (included) was relying on mutex, which was not
    # detected correctly on Darwin platform when using GCC
    #
    # More details here:
    # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878889166
    # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878913339
    conflicts("%gcc", when="@:1.76 +system platform=darwin")

    # Boost 1.80 does not build with the Intel oneapi compiler
    # (https://github.com/spack/spack/pull/32879#issuecomment-1265933265)
    conflicts("%oneapi", when="@1.80")

    # Boost 1.85.0 stacktrace added a hard compilation error that has to
    # explicitly be suppressed on some platforms:
    # https://github.com/boostorg/stacktrace/pull/150. This conflict could be
    # turned into a variant that allows users to opt-in when they know it is
    # safe to do so on affected platforms.
    conflicts("+clanglibcpp", when="@1.85: +stacktrace")

    # On Windows, the signals variant is required when building any of
    # the all_libs variants.
    for lib in all_libs:
        requires("+signals", when=f"+{lib} platform=windows")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11856
    patch("boost_11856.patch", when="@1.60.0%gcc@4.4.7")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120
    patch("python_jam-1_77.patch", when="@1.77:     ^python@3:")
    patch("python_jam.patch", when="@1.56:1.76 ^python@3:")
    patch("python_jam_pre156.patch", when="@:1.55.0   ^python@3:")

    # Patch fix for IBM XL compiler
    patch("xl_1_62_0_le.patch", when="@1.62.0%xl_r")
    patch("xl_1_62_0_le.patch", when="@1.62.0%xl")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125
    patch("call_once_variadic.patch", when="@1.54.0:1.55%gcc@5.0:")

    # Patch fix for PGI compiler
    patch("boost_1.67.0_pgi.patch", when="@1.67.0:1.68%pgi")
    patch("boost_1.63.0_pgi.patch", when="@1.63.0%pgi")
    patch("boost_1.63.0_pgi_17.4_workaround.patch", when="@1.63.0%pgi@17.4")

    # Patch to override the PGI toolset when using the NVIDIA compilers
    patch("nvhpc-1.74.patch", when="@1.74.0:1.75%nvhpc")
    patch("nvhpc-1.76.patch", when="@1.76.0:1.76%nvhpc")

    # Patch to workaround compiler bug
    patch("nvhpc-find_address.patch", when="@1.75.0:1.76%nvhpc")

    # Patch to workaround gcc-8.3 compiler issue https://github.com/boostorg/mpl/issues/44
    patch("boost_gcc83_cpp17_fix.patch", when="@1.69:%gcc@8.3")

    # Fix for version comparison on newer Clang on darwin
    # See: https://github.com/boostorg/build/issues/440
    # See: https://github.com/macports/macports-ports/pull/6726
    patch("darwin_clang_version.patch", level=0, when="@1.56.0:1.72.0 platform=darwin")

    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372
    patch(
        "https://482372.bugs.gentoo.org/attachment.cgi?id=356970",
        when="@1.53.0:1.54",
        sha256="b6f6ce68282159d46c716a1e6c819c815914bdb096cddc516fa48134209659f2",
    )

    # Fix: "Unable to compile code using boost/process.hpp"
    # See: https://github.com/boostorg/process/issues/116
    # Patch: https://github.com/boostorg/process/commit/6a4d2ff72114ef47c7afaf92e1042aca3dfa41b0.patch
    patch("1.72_boost_process.patch", level=2, when="@1.72.0")

    # Patch fix for warnings from commits 2d37749, af1dc84, c705bab, and
    # 0134441 on https://github.com/boostorg/system.
    patch("system-non-virtual-dtor-include.patch", when="@1.69.0", level=2)
    patch("system-non-virtual-dtor-test.patch", when="@1.69.0", working_dir="libs/system", level=1)

    # Change the method for version analysis when using Fujitsu compiler.
    patch("fujitsu_version_analysis.patch", when="@1.67.0:1.76.0%fj")
    patch("fujitsu_version_analysis-1.77.patch", when="@1.77.0:%fj")

    # Add option to C/C++ compile commands in clang-linux.jam
    patch("clang-linux_add_option.patch", when="@1.56.0:1.63.0")
    patch("clang-linux_add_option2.patch", when="@1.47.0:1.55.0")

    # C++20 concepts fix for Beast
    # See https://github.com/boostorg/beast/pull/1927 for details
    patch(
        "https://www.boost.org/patches/1_73_0/0002-beast-coroutines.patch",
        sha256="4dd507e1f5a29e3b87b15321a4d8c74afdc8331433edabf7aeab89b3c405d556",
        when="@1.73.0",
    )

    # Cloning a status_code with indirecting_domain leads to segmentation fault
    # See https://github.com/ned14/outcome/issues/223 for details
    patch(
        "https://www.boost.org/patches/1_73_0/0001-outcome-assert.patch",
        sha256="246508e052c44b6f4e8c2542a71c06cacaa72cd1447ab8d2a542b987bc35ace9",
        when="@1.73.0",
    )

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154
    patch("boost_154.patch", when="@1.56.0:1.63")

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218
    patch("boost_218.patch", when="@1.63.0:1.67")

    # Fix B2 bootstrap toolset during installation
    # See https://github.com/spack/spack/issues/20757
    # and https://github.com/spack/spack/pull/21408
    patch("bootstrap-toolset.patch", when="@1.75")

    # Fix compiler used for building bjam during bootstrap
    patch("bootstrap-compiler.patch", when="@1.76:")

    # Allow building context asm sources with GCC on Darwin
    # See https://github.com/spack/spack/pull/24889
    # and https://github.com/boostorg/context/issues/177
    patch("context-macho-gcc.patch", when="@1.65:1.76 +context platform=darwin %gcc")

    # Fix float128 support when building with CUDA and Cray compiler
    # See https://github.com/boostorg/config/pull/378
    patch(
        "https://github.com/boostorg/config/commit/fee1ad07968386b6d547f089311b7a2c1bf7fa55.patch?full_index=1",
        sha256="666eec8cfb0f71a87443ab27d179a9771bda32bcb8ff5e16afa3767f7b7f1e70",
        when="@:1.76%cce",
        level=2,
    )

    # Fix building with Intel compilers
    patch(
        "https://github.com/bfgroup/b2/commit/23212066f0f20358db54568bb16b3fe1d76f88ce.patch?full_index=1",
        sha256="4849671f9df4b8f3c962130d7f6d44eba3b20d113e84f9faade75e6469e90310",
        when="@1.77.0",
        working_dir="tools/build",
    )

    # Fix issues with PTHREAD_STACK_MIN not being a DEFINED constant in newer glibc
    # See https://github.com/spack/spack/issues/28273
    patch("pthread-stack-min-fix.patch", when="@1.69.0:1.72.0")

    # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html
    patch("intel-oneapi-linux-jam.patch", when="@1.76: %oneapi")

    # https://github.com/boostorg/phoenix/issues/111
    patch("boost_phoenix_1.81.0.patch", level=2, when="@1.81.0:1.82.0")

    # https://github.com/boostorg/filesystem/issues/284
    patch(
        "https://www.boost.org/patches/1_82_0/0002-filesystem-fix-win-smbv1-dir-iterator.patch",
        sha256="738ba8e0d7b5cdcf5fae4998f9450b51577bbde1bb0d220a0721551609714ca4",
        when="@1.82.0 platform=windows",
    )

    def patch(self):
        # Disable SSSE3 and AVX2 when using the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file("dump_avx2", "", "libs/log/build/Jamfile.v2")
            filter_file("<define>BOOST_LOG_USE_AVX2", "", "libs/log/build/Jamfile.v2")
            filter_file("dump_ssse3", "", "libs/log/build/Jamfile.v2")
            filter_file("<define>BOOST_LOG_USE_SSSE3", "", "libs/log/build/Jamfile.v2")

            filter_file("-fast", "-O1", "tools/build/src/tools/pgi.jam")
            filter_file("-fast", "-O1", "tools/build/src/engine/build.sh")

        # Fixes https://github.com/spack/spack/issues/29352
        if self.spec.satisfies("@1.78 %intel") or self.spec.satisfies("@1.78 %oneapi"):
            filter_file("-static", "", "tools/build/src/engine/build.sh")

    def url_for_version(self, version):
        if version >= Version("1.63.0"):
            url = "https://archives.boost.io/release/{0}/source/boost_{1}.tar.bz2"
        else:
            url = "https://downloads.sourceforge.net/project/boost/boost/{0}/boost_{1}.tar.bz2"

        return url.format(version.dotted, version.underscored)

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            if self.spec.satisfies("@1.79.0 %oneapi"):
                flags.append("-Wno-error=enum-constexpr-conversion")
        return (flags, None, None)

    def determine_toolset(self, spec):
        toolsets = {
            "%gcc": "gcc",
            "%intel": "intel",
            "%oneapi": "intel",
            "%clang": "clang",
            "%arm": "clang",
            "%xl": "xlcpp",
            "%xl_r": "xlcpp",
            "%pgi": "pgi",
            "%nvhpc": "pgi",
            "%fj": "clang",
        }

        if spec.satisfies("@1.47:"):
            toolsets["%intel"] += "-linux"
            toolsets["%oneapi"] += "-linux"

        for cc, toolset in toolsets.items():
            if self.spec.satisfies(cc):
                return toolset

        # fallback to gcc if no toolset found
        return "gcc"

    def bjam_python_line(self, spec):
        # avoid "ambiguous key" error
        if spec.satisfies("@:1.58"):
            return ""

        return "using python : {0} : {1} : {2} : {3} ;\n".format(
            spec["python"].version.up_to(2),
            Path(spec["python"].command.path).as_posix(),
            Path(spec["python"].headers.directories[0]).as_posix(),
            Path(spec["python"].libs[0]).parent.as_posix(),
        )

    def determine_bootstrap_options(self, spec, with_libs, options):
        boost_toolset_id = self.determine_toolset(spec)

        # Arm compiler bootstraps with 'gcc' (but builds as 'clang')
        if spec.satisfies("%arm") or spec.satisfies("%fj"):
            options.append("--with-toolset=gcc")
        else:
            options.append("--with-toolset=%s" % boost_toolset_id)
        if with_libs:
            options.append("--with-libraries=%s" % ",".join(sorted(with_libs)))
        else:
            options.append("--with-libraries=headers")

        if spec.satisfies("+python"):
            options.append("--with-python=%s" % spec["python"].command.path)

        if spec.satisfies("+icu"):
            options.append("--with-icu")
        else:
            options.append("--without-icu")

        self.write_jam_file(spec, boost_toolset_id)

    def write_jam_file(self, spec, boost_toolset_id=None):
        with open("user-config.jam", "w") as f:
            # Boost may end up using gcc even though clang+gfortran is set in
            # compilers.yaml. Make sure this does not happen:
            if not spec.satisfies("platform=windows"):
                # Skip this on Windows since we don't have a cl.exe wrapper in spack
                f.write("using {0} : : {1} ;\n".format(boost_toolset_id, spack_cxx))

            if spec.satisfies("+mpi"):
                # Use the correct mpi compiler.  If the compiler options are
                # empty or undefined, Boost will attempt to figure out the
                # correct options by running "${mpicxx} -show" or something
                # similar, but that doesn't work with the Cray compiler
                # wrappers.  Since Boost doesn't use the MPI C++ bindings,
                # that can be used as a compiler option instead.
                mpi_line = "using mpi : %s" % Path(spec["mpi"].mpicxx).as_posix()
                f.write(mpi_line + " ;\n")

            if spec.satisfies("+python"):
                f.write(self.bjam_python_line(spec))

    def determine_b2_options(self, spec, options):
        if spec.satisfies("+debug"):
            options.append("variant=debug")
        else:
            options.append("variant=release")

        if spec.satisfies("+icu"):
            options.extend(["-s", "ICU_PATH=%s" % spec["icu4c"].prefix])
        else:
            options.append("--disable-icu")

        if spec.satisfies("+iostreams"):
            options.extend(
                [
                    "-s",
                    "BZIP2_INCLUDE=%s" % spec["bzip2"].prefix.include,
                    "-s",
                    "BZIP2_LIBPATH=%s" % spec["bzip2"].prefix.lib,
                    "-s",
                    "ZLIB_INCLUDE=%s" % spec["zlib-api"].prefix.include,
                    "-s",
                    "ZLIB_LIBPATH=%s" % spec["zlib-api"].prefix.lib,
                    "-s",
                    "LZMA_INCLUDE=%s" % spec["xz"].prefix.include,
                    "-s",
                    "LZMA_LIBPATH=%s" % spec["xz"].prefix.lib,
                    "-s",
                    "ZSTD_INCLUDE=%s" % spec["zstd"].prefix.include,
                    "-s",
                    "ZSTD_LIBPATH=%s" % spec["zstd"].prefix.lib,
                ]
            )
            # At least with older Xcode, _lzma_cputhreads is missing (#33998)
            if self.spec.satisfies("platform=darwin"):
                options.extend(["-s", "NO_LZMA=1"])

        link_types = ["static"]
        if spec.satisfies("+shared"):
            link_types.append("shared")

        threading_opts = []
        if spec.satisfies("+multithreaded"):
            threading_opts.append("multi")
        if spec.satisfies("+singlethreaded"):
            threading_opts.append("single")
        if not threading_opts:
            raise RuntimeError(
                "At least one of {singlethreaded, " + "multithreaded} must be enabled"
            )

        # If we are building context, tell b2 which backend to use
        if "+context" in spec and "context-impl" in spec.variants:
            options.extend(["context-impl=%s" % spec.variants["context-impl"].value])

        if spec.satisfies("+taggedlayout"):
            layout = "tagged"
        elif spec.satisfies("+versionedlayout"):
            layout = "versioned"
        else:
            if len(threading_opts) > 1:
                raise RuntimeError(
                    "Cannot build both single and " + "multi-threaded targets with system layout"
                )
            layout = "system"

        options.extend(["link=%s" % ",".join(link_types), "--layout=%s" % layout])

        if spec.satisfies("platform=windows"):
            # The runtime link must either be shared or static, not both.
            if "+shared" in spec:
                options.append("runtime-link=shared")
            else:
                options.append("runtime-link=static")
            for lib in self.all_libs:
                if f"+{lib}" not in spec:
                    options.append(f"--without-{lib}")

        if not spec.satisfies("@:1.75 %intel") and not spec.satisfies("platform=windows"):
            # When building any version >= 1.76, the toolset must be specified.
            # Earlier versions could not specify Intel as the toolset
            # as that was considered to be redundant/conflicting with
            # --with-toolset in bootstrap.
            # (although it is not currently known if 1.76 is the earliest
            # version that requires specifying the toolset for Intel)
            options.extend(["toolset=%s" % self.determine_toolset(spec)])

        # Other C++ flags.
        cxxflags = []

        # Deal with C++ standard.
        if spec.satisfies("@1.66:"):
            options.append("cxxstd={0}".format(spec.variants["cxxstd"].value))
        else:  # Add to cxxflags for older Boost.
            cxxstd = spec.variants["cxxstd"].value
            flag = getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
            if flag:
                cxxflags.append(flag)

        if self.spec.satisfies("+pic"):
            cxxflags.append(self.compiler.cxx_pic_flag)

        # clang is not officially supported for pre-compiled headers
        # and at least in clang 3.9 still fails to build
        #   https://www.boost.org/build/doc/html/bbv2/reference/precompiled_headers.html
        #   https://svn.boost.org/trac/boost/ticket/12496
        if spec.satisfies("%apple-clang") or spec.satisfies("%clang") or spec.satisfies("%fj"):
            options.extend(["pch=off"])
            if spec.satisfies("+clanglibcpp"):
                cxxflags.append("-stdlib=libc++")
                options.extend(["toolset=clang", 'linkflags="-stdlib=libc++"'])
        elif spec.satisfies("%xl") or spec.satisfies("%xl_r"):
            # see also: https://lists.boost.org/boost-users/2019/09/89953.php
            # the cxxstd setting via spack is not sufficient to drive the
            # change into boost compilation
            if spec.variants["cxxstd"].value == "11":
                cxxflags.append("-std=c++11")

        # See conflict above and
        # https://github.com/boostorg/stacktrace/pull/150. This suppresses a
        # compilation error that must be explicitly suppressed. Because of the
        # conflict we can suppress the error without input from a user.
        if spec.satisfies("@1.85: +stacktrace"):
            cxxflags.append("-DBOOST_STACKTRACE_LIBCXX_RUNTIME_MAY_CAUSE_MEMORY_LEAK")

        if cxxflags:
            options.append('cxxflags="{0}"'.format(" ".join(cxxflags)))

        # Visibility was added in 1.69.0.
        if spec.satisfies("@1.69.0:"):
            options.append("visibility=%s" % spec.variants["visibility"].value)

        return threading_opts

    def add_buildopt_symlinks(self, prefix):
        with working_dir(prefix.lib, create=True):
            for lib in os.listdir(os.curdir):
                if os.path.isfile(lib):
                    prefix, remainder = lib.split(".", 1)
                    symlink(lib, "%s-mt.%s" % (prefix, remainder))

    def bootstrap_windows(self):
        """Run the Windows-specific bootstrap.bat. The only bootstrapping command
        line option that is accepted by the bootstrap.bat script is the compiler
        information: either the vc version (e.g. MSVC 14.3.x would be vc143)
        or gcc or clang.
        """
        bootstrap_options = list()
        if self.spec.satisfies("%msvc"):
            bootstrap_options.append(f"vc{self.compiler.platform_toolset_ver}")
        elif self.spec.satisfies("%gcc"):
            bootstrap_options.append("gcc")
        elif self.spec.satisfies("%clang"):
            bootstrap_options.append("clang")

        bootstrap = Executable("cmd.exe")
        bootstrap("/c", ".\\bootstrap.bat", *bootstrap_options)

    def install(self, spec, prefix):
        # On Darwin, Boost expects the Darwin libtool. However, one of the
        # dependencies may have pulled in Spack's GNU libtool, and these two
        # are not compatible. We thus create a symlink to Darwin's libtool
        # and add it at the beginning of PATH.
        if sys.platform == "darwin":
            newdir = os.path.abspath("darwin-libtool")
            mkdirp(newdir)
            force_symlink("/usr/bin/libtool", join_path(newdir, "libtool"))
            env["PATH"] = newdir + ":" + env["PATH"]

        with_libs = {f"{lib}" for lib in Boost.all_libs if f"+{lib}" in spec}

        # Remove libraries that the release version does not support
        if not spec.satisfies("@1.85.0:"):
            with_libs.discard("charconv")
        if not spec.satisfies("@1.84.0:"):
            with_libs.discard("cobalt")
        if not spec.satisfies("@1.81.0:"):
            with_libs.discard("url")
        if not spec.satisfies("@1.75.0:"):
            with_libs.discard("json")
        if spec.satisfies("@1.69.0:"):
            with_libs.discard("signals")
        if not spec.satisfies("@1.54.0:"):
            with_libs.discard("log")
        if not spec.satisfies("@1.53.0:"):
            with_libs.discard("atomic")
        if not spec.satisfies("@1.48.0:"):
            with_libs.discard("locale")
        if not spec.satisfies("@1.47.0:"):
            with_libs.discard("chrono")
        if not spec.satisfies("@1.43.0:"):
            with_libs.discard("random")
        if not spec.satisfies("@1.39.0:"):
            with_libs.discard("exception")
        if spec.satisfies("+graph") and spec.satisfies("+mpi"):
            with_libs.add("graph_parallel")

        if self.spec.satisfies("platform=windows"):
            self.bootstrap_windows()
        else:
            # to make Boost find the user-config.jam
            env["BOOST_BUILD_PATH"] = self.stage.source_path
            bootstrap_options = ["--prefix=%s" % prefix]
            self.determine_bootstrap_options(spec, with_libs, bootstrap_options)
            bootstrap = Executable("./bootstrap.sh")
            bootstrap(*bootstrap_options)

        # strip the toolchain to avoid double include errors (intel) or
        # user-config being overwritten (again intel, but different boost version)
        filter_file(
            r"^\s*using {0}.*".format(self.determine_toolset(spec)),
            "",
            os.path.join(self.stage.source_path, "project-config.jam"),
        )

        # b2 used to be called bjam, before 1.47 (sigh)
        b2name = "./b2" if spec.satisfies("@1.47:") else "./bjam"
        if self.spec.satisfies("platform=windows"):
            b2name = "b2.exe" if spec.satisfies("@1.47:") else "bjam.exe"

        b2 = Executable(b2name)
        jobs = make_jobs
        # in 1.59 max jobs became dynamic
        if jobs > 64 and spec.satisfies("@:1.58"):
            jobs = 64

        if self.spec.satisfies("platform=windows"):

            def is_64bit():
                # TODO: This method should be abstracted to a more general location
                #  as it is repeated in many places (msmpi.py for one)
                return "64" in str(self.spec.target.family)

            b2_options = [f"--prefix={self.prefix}", f"address-model={64 if is_64bit() else 32}"]
            if not self.spec.satisfies("+python"):
                b2_options.append("--without-python")

            self.write_jam_file(self.spec)
        else:
            b2_options = ["-j", "%s" % jobs]
        path_to_config = "--user-config=%s" % os.path.join(
            self.stage.source_path, "user-config.jam"
        )
        b2_options.append(path_to_config)
        threading_opts = self.determine_b2_options(spec, b2_options)

        # Create headers if building from a git checkout
        if spec.satisfies("@develop"):
            b2("headers", *b2_options)

        b2("--clean", *b2_options)

        # In theory it could be done on one call but it fails on
        # Boost.MPI if the threading options are not separated.
        if not self.spec.satisfies("platform=windows"):
            for threading_opt in threading_opts:
                b2("install", "threading=%s" % threading_opt, *b2_options)
        else:
            b2("install", *b2_options)

        if spec.satisfies("+multithreaded") and spec.satisfies("~taggedlayout"):
            self.add_buildopt_symlinks(prefix)

        # The shared libraries are not installed correctly
        # on Darwin; correct this
        if (sys.platform == "darwin") and ("+shared" in spec):
            fix_darwin_install_name(prefix.lib)

    def setup_run_environment(self, env):
        env.set("BOOST_ROOT", self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        # Disable find package's config mode for versions of Boost that
        # didn't provide it. See https://github.com/spack/spack/issues/20169
        # and https://cmake.org/cmake/help/latest/module/FindBoost.html
        if self.spec.satisfies("boost@:1.69.0") and dependent_spec.satisfies("build_system=cmake"):
            args_fn = type(dependent_spec.package.builder).cmake_args

            def _cmake_args(self):
                return ["-DBoost_NO_BOOST_CMAKE=ON"] + args_fn(self)

            type(dependent_spec.package.builder).cmake_args = _cmake_args

    def setup_dependent_build_environment(self, env, dependent_spec):
        if "+context" in self.spec and "context-impl" in self.spec.variants:
            context_impl = self.spec.variants["context-impl"].value
            # fcontext, as the default, has no corresponding macro
            if context_impl == "ucontext":
                env.append_flags("CXXFLAGS", "-DBOOST_USE_UCONTEXT")
            elif context_impl == "winfib":
                env.append_flags("CXXFLAGS", "-DBOOST_USE_WINFIB")
