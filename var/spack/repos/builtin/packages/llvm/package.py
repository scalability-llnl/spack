# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import re
import sys

import llnl.util.tty as tty
from llnl.util.lang import classproperty

import spack.compilers
from spack.build_systems.cmake import get_cmake_prefix_path
from spack.operating_systems.mac_os import macos_sdk_path
from spack.package import *
from spack.package_base import PackageBase


class LlvmDetection(PackageBase):
    """Base class to detect LLVM based compilers"""

    compiler_version_argument = "--version"
    c_names = ["clang"]
    cxx_names = ["clang++"]

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        # Executables like lldb-vscode-X are daemon listening on some port and would hang Spack
        # during detection. clang-cl, clang-cpp, etc. are dev tools that we don't need to test
        reject = re.compile(
            r"-(vscode|cpp|cl|ocl|gpu|tidy|rename|scan-deps|format|refactor|offload|"
            r"check|query|doc|move|extdef|apply|reorder|change-namespace|"
            r"include-fixer|import-test|dap|server)"
        )
        return [x for x in exes_in_prefix if not reject.search(x)]


class Llvm(CMakePackage, CudaPackage, LlvmDetection, CompilerPackage):
    """The LLVM Project is a collection of modular and reusable compiler and
    toolchain technologies. Despite its name, LLVM has little to do
    with traditional virtual machines, though it does provide helpful
    libraries that can be used to build them. The name "LLVM" itself
    is not an acronym; it is the full name of the project.
    """

    homepage = "https://llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    list_url = "https://releases.llvm.org/download.html"
    git = "https://github.com/llvm/llvm-project"
    maintainers("trws", "haampie", "skosukhin")

    tags = ["e4s", "compiler"]

    generator("ninja")

    license("Apache-2.0")

    version("main", branch="main")
    version("19.1.6", sha256="f07fdcbb27b2b67aa95e5ddadf45406b33228481c250e65175066d36536a1ee2")
    version("19.1.5", sha256="e2204b9903cd9d7ee833a2f56a18bef40a33df4793e31cc090906b32cbd8a1f5")
    version("19.1.4", sha256="010e1fd3cabee8799bd2f8a6fbc68f28207494f315cf9da7057a2820f79fd531")
    version("19.1.3", sha256="e5106e2bef341b3f5e41340e4b6c6a58259f4021ad801acf14e88f1a84567b05")
    version("19.1.2", sha256="622cb6c5e95a3bb7e9876c4696a65671f235bd836cfd0c096b272f6c2ada41e7")
    version("19.1.1", sha256="115dfd98a353d05bffdab3f80db22f159da48aca0124e8c416f437adcd54b77f")
    version("19.1.0", sha256="0a08341036ca99a106786f50f9c5cb3fbe458b3b74cab6089fd368d0edb2edfe")
    version("18.1.8", sha256="09c08693a9afd6236f27a2ebae62cda656eba19021ef3f94d59e931d662d4856")
    version("18.1.7", sha256="b60df7cbe02cef2523f7357120fb0d46cbb443791cde3a5fb36b82c335c0afc9")
    version("18.1.6", sha256="01390edfae5b809e982b530ff9088e674c62b13aa92cb9dc1e067fa2cf501083")
    version("18.1.5", sha256="d543309f55ae3f9b422108302b45c40f5696c96862f4bda8f5526955daa54284")
    version("18.1.4", sha256="deca5a29e8b1d103ecc4badb3c304aca50d5cac6453364d88ee415dc55699dfb")
    version("18.1.3", sha256="fc5a2fd176d73ceb17f4e522f8fe96d8dde23300b8c233476d3609f55d995a7a")
    version("18.1.2", sha256="8d686d5ece6f12b09985cb382a3a530dc06bb6e7eb907f57c7f8bf2d868ebb0b")
    version("18.1.1", sha256="62439f733311869dbbaf704ce2e02141d2a07092d952fc87ef52d1d636a9b1e4")
    version("18.1.0", sha256="eb18f65a68981e94ea1a5aae4f02321b17da9e99f76bfdb983b953f4ba2d3550")
    version("17.0.6", sha256="81494d32e6f12ea6f73d6d25424dbd2364646011bb8f7e345ca870750aa27de1")
    version("17.0.5", sha256="432c1eda3d1c9379cd52a9bee8e0ea6f7b204bff5075895f963fd8e575aa4fb8")
    version("17.0.4", sha256="46200b79f52a02fe26d0a43fd856ab6ceff49ab2a0b7c240ac4b700a6ada700c")
    version("17.0.3", sha256="1e3d9d04fb5fbd8d0080042ad72c7e2a5c68788b014b186647a604dbbdd625d2")
    version("17.0.2", sha256="dcba3eb486973dce45b6edfe618f3f29b703ae7e6ef9df65182fb50fb6fe4235")
    version("17.0.1", sha256="d51b10be66c10a6a81f4c594b554ffbf1063ffbadcb810af37d1f88d6e0b49dd")
    version("16.0.6", sha256="56b2f75fdaa95ad5e477a246d3f0d164964ab066b4619a01836ef08e475ec9d5")
    version("16.0.5", sha256="e0fbca476693fcafa125bc71c8535587b6d9950293122b66b262bb4333a03942")
    version("16.0.4", sha256="10c3fe1757d2e4f1cd7745dc548ecf687680a71824ec81701c38524c2a0753e2")
    version("16.0.3", sha256="0bd71bc687a4e5a250c40afb0decefc50c85178fcce726137b682039de63919b")
    version("16.0.2", sha256="97c3c6aafb53c4bb0ed2781a18d6f05e75445e24bb1dc57a32b74f8d710ac19f")
    version("16.0.1", sha256="b5a9ff1793b1e2d388a3819bf35797002b1d2e40bb35a10c65605e0ea1435271")
    version("16.0.0", sha256="cba969a0782a3a398658d439f047b5e548ea04724f4fbfdbe17cfc946f4cd3ed")
    version("15.0.7", sha256="42a0088f148edcf6c770dfc780a7273014a9a89b66f357c761b4ca7c8dfa10ba")
    version("15.0.6", sha256="4d857d7a180918bdacd09a5910bf9743c9861a1e49cb065a85f7a990f812161d")
    version("15.0.5", sha256="c47640269e0251e009ae18a25162df4e20e175885286e21d28c054b084b991a4")
    version("15.0.4", sha256="e24b4d3bf7821dcb1c901d1e09096c1f88fb00095c5a6ef893baab4836975e52")
    version("15.0.3", sha256="8ac8e4c0982bf236526d737d385db5e1e66543ab217a9355d54159659eae3774")
    version("15.0.2", sha256="dc11d35e60ab61792baa607dff080c993b39de23fb93b3d3369ba15b0601c307")
    version("15.0.1", sha256="20bccb964e39f604fdc16d1258f94d2053fbdcdab2b2f6d5e20e6095ec403c00")
    version("15.0.0", sha256="36d83cd84e1caf2bcfda1669c029e2b949adb9860cff01e7d3246ac2348b11ae")
    version("14.0.6", sha256="98f15f842700bdb7220a166c8d2739a03a72e775b67031205078f39dd756a055")
    version("14.0.5", sha256="a4a57f029cb81f04618e05853f05fc2d21b64353c760977d8e7799bf7218a23a")
    version("14.0.4", sha256="1333236f9bee38658762076be4236cb5ebf15ae9b7f2bfce6946b96ae962dc73")
    version("14.0.3", sha256="0e1d049b050127ecf6286107e9a4400b0550f841d5d2288b9d31fd32ed0683d5")
    version("14.0.2", sha256="ca52232b3451c8e017f00eb882277707c13e30fac1271ec97015f6d0eeb383d1")
    version("14.0.1", sha256="c8be00406e872c8a24f8571cf6f5517b73ae707104724b1fd1db2f0af9544019")
    version("14.0.0", sha256="87b1a068b370df5b79a892fdb2935922a8efb1fddec4cc506e30fe57b6a1d9c4")
    version("13.0.1", sha256="09c50d558bd975c41157364421820228df66632802a4a6a7c9c17f86a7340802")
    version("13.0.0", sha256="a1131358f1f9f819df73fa6bff505f2c49d176e9eef0a3aedd1fdbce3b4630e8")
    version("12.0.1", sha256="66b64aa301244975a4aea489f402f205cde2f53dd722dad9e7b77a0459b4c8df")
    version("12.0.0", sha256="8e6c99e482bb16a450165176c2d881804976a2d770e0445af4375e78a1fbf19c")
    version("11.1.0", sha256="53a0719f3f4b0388013cfffd7b10c7d5682eece1929a9553c722348d1f866e79")
    version("11.0.1", sha256="9c7ad8e8ec77c5bde8eb4afa105a318fd1ded7dff3747d14f012758719d7171b")
    version("11.0.0", sha256="8ad4ddbafac4f2c8f2ea523c2c4196f940e8e16f9e635210537582a48622a5d5")
    version("10.0.1", sha256="c7ccb735c37b4ec470f66a6c35fbae4f029c0f88038f6977180b1a8ddc255637")
    version("10.0.0", sha256="b81c96d2f8f40dc61b14a167513d87c0d813aae0251e06e11ae8a4384ca15451")
    version("9.0.1", sha256="be7b034641a5fda51ffca7f5d840b1a768737779f75f7c4fd18fe2d37820289a")
    version("9.0.0", sha256="7807fac25330e24e9955ca46cd855dd34bbc9cc4fdba8322366206654d1036f2")
    version("8.0.1", sha256="5b18f6111c7aee7c0933c355877d4abcfe6cb40c1a64178f28821849c725c841")
    version("8.0.0", sha256="d81238b4a69e93e29f74ce56f8107cbfcf0c7d7b40510b7879e98cc031e25167")
    version("7.1.0", sha256="71c93979f20e01f1a1cc839a247945f556fa5e63abf2084e8468b238080fd839")
    version("7.0.1", sha256="f17a6cd401e8fd8f811fbfbb36dcb4f455f898c9d03af4044807ad005df9f3c0")
    version("6.0.1", sha256="aefadceb231f4c195fe6d6cd3b1a010b269c8a22410f339b5a089c2e902aa177")
    version("6.0.0", sha256="1946ec629c88d30122afa072d3c6a89cc5d5e4e2bb28dc63b2f9ebcc7917ee64")
    version("5.0.2", sha256="fe87aa11558c08856739bfd9bd971263a28657663cb0c3a0af01b94f03b0b795")
    version("5.0.1", sha256="84ca454abf262579814a2a2b846569f6e0cb3e16dc33ca3642b4f1dff6fbafd3")
    version("5.0.0", sha256="1f1843315657a4371d8ca37f01265fa9aae17dbcf46d2d0a95c1fdb3c6a4bab6")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant(
        "clang", default=True, description="Build the LLVM C/C++/Objective-C compiler frontend"
    )

    variant(
        "flang",
        default=False,
        description="Build the LLVM Fortran compiler frontend "
        "(experimental - parser only, needs GCC)",
    )
    conflicts("+flang", when="@:10")
    conflicts("+flang", when="~clang")

    variant("lldb", default=True, description="Build the LLVM debugger")
    conflicts("+lldb", when="~clang")

    variant("lld", default=True, description="Build the LLVM linker")
    variant("mlir", default=False, when="@10:", description="Build with MLIR support")
    variant(
        "libunwind",
        values=(
            "none",
            conditional("project", when="@:15"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM unwinder library"
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "polly",
        default=True,
        description="Build the LLVM polyhedral optimization plugin, only builds for 3.7.0+",
    )
    variant(
        "libcxx",
        values=(
            "none",
            conditional("project", when="@:15"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM C++ standard library "
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )

    variant("offload", default=True, when="@19:", description="Build the Offload subproject")
    conflicts("+offload", when="~clang")

    variant("libomptarget", default=True, description="Build the OpenMP offloading library")
    conflicts("+libomptarget", when="~clang")
    conflicts("+libomptarget", when="~offload @19:")
    for _p in ["darwin", "windows"]:
        conflicts("+libomptarget", when="platform={0}".format(_p))
    del _p

    variant(
        "libomptarget_debug",
        default=False,
        description="Allow debug output with the environment variable LIBOMPTARGET_DEBUG=1",
    )
    conflicts("+libomptarget_debug", when="~libomptarget")

    variant(
        "compiler-rt",
        values=(
            "none",
            conditional("project", when="+clang"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM compiler runtime, including sanitizers, "
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "gold",
        default=(sys.platform != "darwin"),
        description="Add support for LTO with the gold linker plugin",
    )
    variant("split_dwarf", default=False, description="Build with split dwarf information")
    variant(
        "llvm_dylib",
        default=True,
        description="Build a combined LLVM shared library with all components",
    )
    variant(
        "link_llvm_dylib",
        default=False,
        when="+llvm_dylib",
        description="Link LLVM tools against the LLVM shared library",
    )
    variant(
        "targets",
        default="all",
        description=(
            "What targets to build. Spack's target family is always added "
            "(e.g. X86 is automatically enabled when targeting znver2)."
        ),
        values=(
            "all",
            "none",
            "aarch64",
            "amdgpu",
            "arm",
            "avr",
            "bpf",
            "cppbackend",
            "hexagon",
            "lanai",
            "mips",
            "msp430",
            "nvptx",
            "powerpc",
            "riscv",
            "sparc",
            "systemz",
            "webassembly",
            "x86",
            "xcore",
        ),
        multi=True,
    )
    variant(
        "libomp_tsan",
        default=False,
        # Added in https://reviews.llvm.org/D13072
        # Removed in https://reviews.llvm.org/D103767
        when="@4:12",
        description="Build with OpenMP capable thread sanitizer",
    )
    variant(
        "openmp",
        values=("project", conditional("runtime", when="+clang @12:")),
        default="runtime",
        description="Build OpenMP either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "code_signing",
        default=False,
        when="+lldb platform=darwin",
        description="Enable code-signing on macOS",
    )
    variant("python", default=False, description="Install python bindings")
    variant("lua", default=True, description="Enable lua scripting inside lldb")
    variant("version_suffix", default="none", description="Add a symbol suffix")
    variant(
        "shlib_symbol_version",
        default="none",
        description="Add shared library symbol version",
        when="@13:",
    )
    variant("z3", default=False, description="Use Z3 for the clang static analyzer")
    conflicts("+z3", when="@:7")
    conflicts("+z3", when="~clang")
    conflicts("+lua", when="@:10")
    conflicts("+lua", when="~lldb")
    # Python distutils were removed with 3.12 and are required to build LLVM <= 14
    conflicts("^python@3.12:", when="@:14")

    variant(
        "zstd",
        default=False,
        when="@15:",
        description="Enable zstd support for static analyzer / lld",
    )

    provides("libllvm@19", when="@19.0.0:19")
    provides("libllvm@18", when="@18.0.0:18")
    provides("libllvm@17", when="@17.0.0:17")
    provides("libllvm@16", when="@16.0.0:16")
    provides("libllvm@15", when="@15.0.0:15")
    provides("libllvm@14", when="@14.0.0:14")
    provides("libllvm@13", when="@13.0.0:13")
    provides("libllvm@12", when="@12.0.0:12")
    provides("libllvm@11", when="@11.0.0:11")
    provides("libllvm@10", when="@10.0.0:10")
    provides("libllvm@9", when="@9.0.0:9")
    provides("libllvm@8", when="@8.0.0:8")
    provides("libllvm@7", when="@7.0.0:7")
    provides("libllvm@6", when="@6.0.0:6")
    provides("libllvm@5", when="@5.0.0:5")
    provides("libllvm@4", when="@4.0.0:4")
    provides("libllvm@3", when="@3.0.0:3")

    extends("python", when="+python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on("cmake@3.13.4:", type="build", when="@12:")
    depends_on("cmake@3.20:", type="build", when="@16:")
    with when("@:10"):
        # Versions 10 and older cannot build runtimes with cmake@3.17:
        # See https://reviews.llvm.org/D77284
        for runtime in ["libunwind", "libcxx", "compiler-rt"]:
            depends_on("cmake@:3.16", type="build", when="{0}=runtime".format(runtime))
        del runtime
    depends_on("python", when="~python", type="build")
    depends_on("pkgconfig", type="build")

    # Universal dependency
    depends_on("python", when="+python")

    # clang and clang-tools dependencies
    depends_on("z3@4.7.1:", when="+z3")

    # openmp dependencies
    depends_on("perl-data-dumper", type=("build"))
    depends_on("hwloc")
    depends_on("hwloc@2.0.1:", when="@13")
    with when("@:15"):
        depends_on("elf", when="+cuda")
        depends_on("elf", when="+libomptarget")
    depends_on("libffi", when="+libomptarget")

    # llvm-config --system-libs libraries.
    depends_on("zlib-api")

    # needs zstd cmake config file, which is not added when built with makefile.
    depends_on("zstd build_system=cmake", when="+zstd")

    # lldb dependencies
    with when("+lldb"):
        depends_on("libedit")
        depends_on("libxml2")
        depends_on("lua@5.3", when="+lua")  # purposefully not a range
        depends_on("ncurses")
        depends_on("py-six", when="+python")
        depends_on("swig", when="+lua")
        depends_on("swig", when="+python")
        depends_on("xz")

    for _when_spec in ("+lldb+python", "+lldb+lua"):
        with when(_when_spec):
            depends_on("swig@2:", when="@10:")
            depends_on("swig@3:", when="@12:")
            depends_on("swig@4:", when="@17:")
            # Commits f0a25fe0b746f56295d5c02116ba28d2f965c175 and
            # 81fc5f7909a4ef5a8d4b5da2a10f77f7cb01ba63 fixed swig 4.1 support
            depends_on("swig@:4.0", when="@:15")

    # gold support, required for some features
    depends_on("binutils+gold+ld+plugins+headers", when="+gold")

    # Older LLVM do not build with newer compilers, and vice versa
    with when("@16:"):
        conflicts("%gcc@:7.0")
        conflicts("%clang@:4")
        conflicts("%apple-clang@:9")
    conflicts("%gcc@8:", when="@:5")
    conflicts("%gcc@:5.0", when="@8:")
    # Internal compiler error on gcc 8.4 on aarch64 https://bugzilla.redhat.com/show_bug.cgi?id=1958295
    conflicts("%gcc@8.4:8.4.9", when="@12: target=aarch64:")

    # libcxx=project imposes compiler conflicts
    # see https://libcxx.llvm.org/#platform-and-compiler-support for the latest release
    # and https://github.com/llvm/www-releases for older releases
    with when("libcxx=project"):
        for v, compiler_conflicts in {
            "@7:": {"clang": "@:3.4", "gcc": "@:4.6"},
            "@9:": {"clang": "@:3.4", "gcc": "@:4"},
            "@11:": {"clang": "@:3", "gcc": "@:4"},
            "@13:": {"clang": "@:10", "gcc": "@:10", "apple-clang": "@:11"},
            "@14:": {
                "clang": "@:11",
                "gcc": "@:10",
                "apple-clang": "@:11",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
            "@15:": {
                "clang": "@:12",
                "gcc": "@:11",
                "apple-clang": "@:12",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
            "@16:": {
                "clang": "@:13",
                "gcc": "@:11",
                "apple-clang": "@:13",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
        }.items():
            with when(v):
                for comp in spack.compilers.supported_compilers():
                    conflicts("%{0}{1}".format(comp, compiler_conflicts.get(comp, "")))
        del v, compiler_conflicts, comp

    # libomptarget
    conflicts("+cuda", when="@15:")  # +cuda variant is obselete since LLVM 15
    conflicts(
        "targets=none",
        when="+libomptarget",
        msg="Non-host backends needed for offloading, set targets=all",
    )
    # See https://github.com/spack/spack/pull/32476#issuecomment-1573770361
    conflicts("~lld", when="+libomptarget")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    # clang/test/Misc/target-invalid-cpu-note.c
    conflicts("cuda_arch=10")
    conflicts("cuda_arch=11")
    conflicts("cuda_arch=12")
    conflicts("cuda_arch=13")
    conflicts("cuda_arch=75", when="@:13")
    conflicts("cuda_arch=80", when="@:13")
    conflicts("cuda_arch=86", when="@:13")
    conflicts("cuda_arch=87", when="@:15")
    conflicts("cuda_arch=89", when="@:15")
    conflicts("cuda_arch=90", when="@:15")
    conflicts("cuda_arch=90a", when="@:17")

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts("^cmake@3.19.0", when="@6:11.0.0")

    # Fix lld templates: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=230463
    patch(
        "https://raw.githubusercontent.com/freebsd/freebsd-ports/f8f9333d8e1e5a7a6b28c5ef0ca73785db06136e/devel/llvm50/files/lld/patch-tools_lld_ELF_Symbols.cpp",
        sha256="c81a50c1b6b78d359c0ce3b88914477f4f2a85b8dbfa7ac745b9e7eb4e53931b",
        when="@5+lld%clang@7:",
    )

    # Add missing include directives for the standard headers (the real need for the following
    # patches depends on the implementation of the standard C++ library, the headers, however, must
    # be included according to the standard, therefore, we apply the patches regardless of the
    # compiler and compiler version).
    #
    # fix missing ::size_t in 'llvm@4:5'
    # see comments in the patch file
    patch(
        "xray_buffer_queue-cstddef.patch",
        # we do not cover compiler-rt=runtime because it is not supported when @:5
        when="@4:5 compiler-rt=project",
    )
    #
    # see https://reviews.llvm.org/D64937
    # see https://github.com/spack/spack/issues/24270
    patch(
        "https://github.com/llvm/llvm-project/commit/b288d90b39f4b905c02092a9bfcfd6d78f99b191.patch?full_index=1",
        sha256="2028d52e1a39326bb48fb7463132bbfe7fb4fa18f1adfeea9c3ed0320ed49564",
        when="@8:9.0.0",
    )
    #
    # committed upstream without a review
    # see https://github.com/llvm/llvm-project/commit/b498303066a63a203d24f739b2d2e0e56dca70d1
    # see https://github.com/spack/spack/pull/28547
    patch(
        "https://github.com/llvm/llvm-project/commit/b498303066a63a203d24f739b2d2e0e56dca70d1.patch?full_index=1",
        sha256="514926d661635de47972c7d403c9c4669235aa51e22e56d44676d2a2709179b6",
        when="@8:11",
    )
    #
    # fix compilation against libstdc++13
    patch(
        "https://github.com/llvm/llvm-project/commit/1b4fdf18bc2aaa2d46bf072475dd9cbcd44a9fee.patch?full_index=1",
        sha256="82481418766b4b949ea808d956ff3800b9a241a576370114862428bb0e25ee1f",
        when="@14:15",
    )

    # missing <cstdint> include
    patch(
        "https://github.com/llvm/llvm-project/commit/ff1681ddb303223973653f7f5f3f3435b48a1983.patch?full_index=1",
        sha256="c6ca6b925f150e8644ce756023797b7f94c9619c62507231f979edab1c09af78",
        when="@6:13",
    )
    # fix building of older versions of llvm with newer versions of glibc
    for compiler_rt_as in ["project", "runtime"]:
        with when("compiler-rt={0}".format(compiler_rt_as)):
            # sys/ustat.h has been removed in favour of statfs from glibc-2.28
            # see https://reviews.llvm.org/D47281
            patch(
                "https://github.com/llvm/llvm-project/commit/383fe5c8668f63ef21c646b43f48da9fa41aa100.patch?full_index=1",
                sha256="66f01ac1769a6815aba09d6f4347ac1744f77f82ec9578a1158b24daca7a89e6",
                when="@4:6.0.0",
            )
            # fix sanitizer-common build with glibc 2.31
            # see https://reviews.llvm.org/D70662
            patch("sanitizer-ipc_perm_mode.patch", when="@5:9")
    del compiler_rt_as

    # Backport from llvm upstream gcc ppc const expr long double issue
    # see https://bugs.llvm.org/show_bug.cgi?id=39696
    # This fix was initially committed (3bf63cf3b366) for the 9.0 release
    # but was then broken (0583d9ea8d5e) prior to the 9.0 release and
    # eventually unbroken (d9a42ec98adc) for the 11.0 release.  The first
    # patch backports the original correct fix to previous releases.  The
    # second patch backports the un-breaking of the original fix.
    for libcxx_as in ["project", "runtime"]:
        with when("libcxx={0}".format(libcxx_as)):
            patch(
                "https://github.com/llvm/llvm-project/commit/3bf63cf3b366d3a57cf5cbad4112a6abf6c0c3b1.patch?full_index=1",
                sha256="e56489a4bcf3c3636e206adca366bfcda2722ad81a5fa9a0360faed63933191a",
                when="@6:8",
            )
            patch(
                "https://github.com/llvm/llvm-project/commit/d9a42ec98adcb1ebc0c3837715df4e5a50c7ccc0.patch?full_index=1",
                sha256="50bfc4e82c02bb5b7739990f363d99b1e43d5d11a5104f6aabbc303ebce6fbe3",
                when="@9:10",
            )
    del libcxx_as

    # Backport from llvm to fix issues related to Python 3.7
    # see https://bugs.llvm.org/show_bug.cgi?id=38233
    patch(
        "https://github.com/llvm/llvm-project/commit/5457b426f5e15a29c0acc8af1a476132f8be2a36.patch?full_index=1",
        sha256="7a1e4aa80760167807255c3e3121b1281bfcf532396b2d8fb3dce021f3f18758",
        when="@4:6+python+lldb ^python@3.7:",
    )

    # fix building on SUSE (with panel.h being in /usr/include/ncurses/)
    # see https://reviews.llvm.org/D85219
    # see https://github.com/spack/spack/issues/19625
    patch(
        "https://github.com/llvm/llvm-project/commit/c952ec15d38843b69e22dfd7b0665304a0459f9f.patch?full_index=1",
        sha256="66932ba31b5bf8808ea112e42cfd79b2480a4936e711771c06ce851eac429b2c",
        when="@10:11+lldb",
    )

    # honor Python2_EXECUTABLE and Python3_EXECUTABLE when they are passed to cmake
    # see https://reviews.llvm.org/D91536
    patch(
        "https://github.com/llvm/llvm-project/commit/16de50895e96adbe261a5ce2498366bda7b3fccd.patch?full_index=1",
        sha256="0e121ed460aa6e117f9f5f339d597a96c0fe4f97dc2209aba47b43ffc831ea24",
        # The patch is applicable only starting version 7.0.0 (the older version might require a
        # different patch addressing https://github.com/spack/spack/issues/19908). It looks like
        # the patched function is used only if both compiler-rt and libcxx are enabled but we keep
        # it simple:
        when="@7:11",
    )

    # Workaround for issue https://github.com/spack/spack/issues/18197
    patch("llvm7_intel.patch", when="@7 %intel@18.0.2,19.0.0:19.1.99")

    # Remove cyclades support to build against newer kernel headers
    # https://reviews.llvm.org/D102059
    patch(
        "https://github.com/llvm/llvm-project/commit/68d5235cb58f988c71b403334cd9482d663841ab.patch?full_index=1",
        sha256="742501723642675075e617f3c38339961b2c7b6fd8290dbffc52239ab0783317",
        when="@10:12.0.0",
    )
    # The patch above is not applicable when "@:9" due to the file renaming and reformatting. The
    # following patch is applicable starting at least version 5.0.0, the oldest we try to support.
    patch("no_cyclades9.patch", when="@5:9")

    with when("+libomptarget"):
        # libomptarget makes use of multithreading via the standard C++ library (e.g.
        # std::call_once), which, depending on the platform and the implementation of the standard
        # library, might or might not require linking to libpthread (note that the failure might
        # happen at the linking time as well as at the runtime). In some cases, the required linker
        # flag comes as a transitive dependency (e.g. from the static LLVMSupport component). The
        # following patches enforce linking to the thread library that is relevant for the system,
        # which might lead to overlinking in some cases though.
        # TODO: figure out why we do not use LLVM_PTHREAD_LIB but run find_package(Threads), at
        #  least for newer versions (the solution must work with both openmp=runtime and
        #  openmp=project)
        patch("llvm12-thread.patch", when="@12")
        patch("llvm13-14-thread.patch", when="@13:14")
        patch("llvm15-thread.patch", when="@15")

    # avoid build failed with Fujitsu compiler
    patch("llvm13-fujitsu.patch", when="@13 %fj")

    # avoid build failed with Fujitsu compiler since llvm17
    patch("llvm17-fujitsu.patch", when="@17: %fj")
    patch("llvm17-18-thread.patch", when="@17:18 %fj")

    # patch for missing hwloc.h include for libompd
    # see https://reviews.llvm.org/D123888
    patch(
        "https://github.com/llvm/llvm-project/commit/91ccd8248c85385a5654c63c302a37d97f811bab.patch?full_index=1",
        sha256="b216cff38659c176c5381e9dda3252edbb204e6f6f1f33e843a9ebcc42732e5d",
        when="@14 openmp=runtime",
    )

    # make libflags a list in openmp subproject when openmp=project
    # see https://reviews.llvm.org/D125370
    patch(
        "https://github.com/llvm/llvm-project/commit/e27ce281399dca8b08b6ca593172a1bd5dbdd5c1.patch?full_index=1",
        sha256="6f0cfa55e3ed17ee33346b0a5bca8092adcc1dc75ca712ab83901755fba9767e",
        when="@3.7:14 openmp=project",
    )

    # fix detection of LLDB_PYTHON_EXE_RELATIVE_PATH
    # see https://reviews.llvm.org/D133513
    # TODO: the patch is not applicable after https://reviews.llvm.org/D141042 but it is not clear
    #  yet whether we need a version of it for when="@16:"
    patch("D133513.diff", level=0, when="@14:15+lldb+python")

    # Fix hwloc@:2.3 (Conditionally disable hwloc@2.0 and hwloc@2.4 code)
    patch(
        "https://github.com/llvm/llvm-project/commit/3a362a9f38b95978160377ee408dbc7d14af9aad.patch?full_index=1",
        sha256="25bc503f7855229620e56e76161cf4654945aef0be493a2d8d9e94a088157b7c",
        when="@14:15",
    )

    # Fix false positive detection of a target when building compiler-rt as a runtime
    # https://reviews.llvm.org/D127975
    patch(
        "https://github.com/llvm/llvm-project/commit/9f1d90bf91570efa124c4a86cd033de374d1049a.patch?full_index=1",
        sha256="1f4287465b3e499911e039e6cc2f395b8cb00eb8a0a223fa0db3704ba77f9969",
        when="@13:14 compiler-rt=runtime",
    )

    patch("add-include-for-libelf-llvm-12-14.patch", when="@12:14")
    patch("add-include-for-libelf-llvm-15.patch", when="@15")

    patch("sanitizer-platform-limits-posix-xdr-macos.patch", when="@10:14 platform=darwin")

    @when("@14:17")
    def patch(self):
        # https://github.com/llvm/llvm-project/pull/69458
        filter_file(
            r"${TERMINFO_LIB}",
            r"${Terminfo_LIBRARIES}",
            "lldb/source/Core/CMakeLists.txt",
            string=True,
        )

    compiler_version_regex = (
        # Normal clang compiler versions are left as-is
        r"clang version ([^ )\n]+)-svn[~.\w\d-]*|"
        # Don't include hyphenated patch numbers in the version
        # (see https://github.com/spack/spack/pull/14365 for details)
        r"clang version ([^ )\n]+?)-[~.\w\d-]*|"
        r"clang version ([^ )\n]+)|"
        # LLDB
        r"lldb version ([^ )\n]+)|"
        # LLD
        r"LLD ([^ )\n]+) \(compatible with GNU linkers\)"
    )
    fortran_names = ["flang"]

    @property
    def supported_languages(self):
        languages = []
        if self.spec.satisfies("+clang"):
            languages.extend(["c", "cxx"])
        if self.spec.satisfies("+flang"):
            languages.append("fortran")
        return languages

    @classproperty
    def executables(cls):
        return super().executables + [r"^ld\.lld(-\d+)?$", r"^lldb(-\d+)?$"]

    @classmethod
    def determine_version(cls, exe):
        try:
            compiler = Executable(exe)
            output = compiler(cls.compiler_version_argument, output=str, error=str)
            if "Apple" in output:
                return None
            if "AMD" in output:
                return None
            match = re.search(cls.compiler_version_regex, output)
            if match:
                return match.group(match.lastindex)
        except ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        # Do not need to reuse more general logic from CompilerPackage
        # because LLVM has kindly named compilers
        variants, compilers = ["+clang"], {}
        lld_found, lldb_found = False, False
        for exe in sorted(exes, key=len):
            name = os.path.basename(exe)
            if "clang++" in name:
                compilers.setdefault("cxx", exe)
            elif "clang" in name:
                compilers.setdefault("c", exe)
            elif "flang" in name:
                variants.append("+flang")
                compilers.setdefault("fortran", exe)
            elif "ld.lld" in name:
                lld_found = True
            elif "lldb" in name:
                lldb_found = True

        variants.append("+lld" if lld_found else "~lld")
        variants.append("+lldb" if lldb_found else "~lldb")

        return "".join(variants), {"compilers": compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For LLVM 'compilers' is a mandatory attribute
        msg = 'the extra attribute "compilers" must be set for ' 'the detected spec "{0}"'.format(
            spec
        )
        assert "compilers" in extra_attributes, msg
        compilers = extra_attributes["compilers"]
        for key in ("c", "cxx"):
            msg = "{0} compiler not found for {1}"
            assert key in compilers, msg.format(key, spec)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        result = None
        if self.spec.satisfies("+clang"):
            result = os.path.join(self.spec.prefix.bin, "clang")
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        result = None
        if self.spec.satisfies("+clang"):
            result = os.path.join(self.spec.prefix.bin, "clang++")
        return result

    @property
    def fc(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fc", None)
        result = None
        if self.spec.satisfies("+flang"):
            result = os.path.join(self.spec.prefix.bin, "flang")
        return result

    @property
    def f77(self):
        msg = "cannot retrieve Fortran 77 compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("f77", None)
        result = None
        if self.spec.satisfies("+flang"):
            result = os.path.join(self.spec.prefix.bin, "flang")
        return result

    @property
    def libs(self):
        return LibraryList(self.llvm_config("--libfiles", "all", result="list"))

    @run_before("cmake")
    def codesign_check(self):
        if self.spec.satisfies("+code_signing"):
            codesign = which("codesign")
            mkdir("tmp")
            llvm_check_file = join_path("tmp", "llvm_check")
            copy("/usr/bin/false", llvm_check_file)
            try:
                codesign("-f", "-s", "lldb_codesign", "--dryrun", llvm_check_file)

            except ProcessError:
                # Newer LLVM versions have a simple script that sets up
                # automatically when run with sudo priviliges
                setup = Executable("./lldb/scripts/macos-setup-codesign.sh")
                try:
                    setup()
                except Exception:
                    raise RuntimeError(
                        "spack was unable to either find or set up"
                        "code-signing on your system. Please refer to"
                        "https://lldb.llvm.org/resources/build.html#"
                        "code-signing-on-macos for details on how to"
                        "create this identity."
                    )

    def flag_handler(self, name, flags):
        if name == "ldflags" and self.spec.satisfies("%intel"):
            flags.append("-shared-intel")
            return (None, flags, None)
        return (flags, None, None)

    def setup_build_environment(self, env):
        """When using %clang, add only its ld.lld-$ver and/or ld.lld to our PATH"""
        if self.compiler.name in ["clang", "apple-clang"]:
            for lld in "ld.lld-{0}".format(self.compiler.version.version[0]), "ld.lld":
                bin = os.path.join(os.path.dirname(self.compiler.cc), lld)
                sym = os.path.join(self.stage.path, "ld.lld")
                if os.path.exists(bin) and not os.path.exists(sym):
                    mkdirp(self.stage.path)
                    os.symlink(bin, sym)
            env.prepend_path("PATH", self.stage.path)

        if self.spec.satisfies("platform=darwin"):
            # set the SDKROOT so the bootstrap compiler finds its C++ headers
            env.set("SDKROOT", macos_sdk_path())

    def setup_run_environment(self, env):
        if self.spec.satisfies("+clang"):
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))
        if self.spec.satisfies("+flang"):
            env.set("FC", join_path(self.spec.prefix.bin, "flang"))
            env.set("F77", join_path(self.spec.prefix.bin, "flang"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        cmake_args = [
            define("LLVM_REQUIRES_RTTI", True),
            define("LLVM_ENABLE_RTTI", True),
            define("LLVM_ENABLE_LIBXML2", False),
            define("CLANG_DEFAULT_OPENMP_RUNTIME", "libomp"),
            define("LIBOMP_USE_HWLOC", True),
            define("LIBOMP_HWLOC_INSTALL_DIR", spec["hwloc"].prefix),
            from_variant("LLVM_ENABLE_ZSTD", "zstd"),
        ]

        # Flang does not support exceptions from core llvm.
        # LLVM_ENABLE_EH=True when building flang will soon
        # fail (with changes at the llvm-project level).
        # Only enable exceptions in LLVM if we are *not*
        # building flang.  FYI: LLVM <= 16.x will build flang
        # successfully but the executable will suffer from
        # link errors looking for C++ EH support.
        if "+flang" not in spec:
            cmake_args.append(define("LLVM_ENABLE_EH", True))

        version_suffix = spec.variants["version_suffix"].value
        if version_suffix != "none":
            cmake_args.append(define("LLVM_VERSION_SUFFIX", version_suffix))

        shlib_symbol_version = spec.variants.get("shlib_symbol_version", None)
        if shlib_symbol_version is not None and shlib_symbol_version.value != "none":
            cmake_args.append(define("LLVM_SHLIB_SYMBOL_VERSION", shlib_symbol_version.value))

        projects = []
        runtimes = []

        if spec.satisfies("+cuda"):
            cmake_args.extend(
                [
                    define("CUDA_TOOLKIT_ROOT_DIR", spec["cuda"].prefix),
                    define(
                        "LIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES",
                        ",".join(spec.variants["cuda_arch"].value),
                    ),
                    define(
                        "CLANG_OPENMP_NVPTX_DEFAULT_ARCH",
                        "sm_{0}".format(spec.variants["cuda_arch"].value[-1]),
                    ),
                ]
            )
            if spec.satisfies("openmp=runtime"):
                cmake_args.append(define("LIBOMPTARGET_NVPTX_ENABLE_BCLIB", True))
        else:
            # still build libomptarget but disable cuda
            cmake_args.extend(
                [
                    define("CUDA_TOOLKIT_ROOT_DIR", "IGNORE"),
                    define("CUDA_SDK_ROOT_DIR", "IGNORE"),
                    define("CUDA_NVCC_EXECUTABLE", "IGNORE"),
                    define("LIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES", "IGNORE"),
                ]
            )

        cmake_args.append(from_variant("LIBOMPTARGET_ENABLE_DEBUG", "libomptarget_debug"))

        if spec.satisfies("@14:"):
            # The hsa-rocr-dev package may be pulled in through hwloc, which can lead to cmake
            # finding libhsa and enabling the AMDGPU plugin. Since we don't support this yet,
            # disable explicitly. See commit a05a0c3c2f8eefc80d84b7a87a23a4452d4a3087.
            cmake_args.append(define("LIBOMPTARGET_BUILD_AMDGPU_PLUGIN", False))
            if "python" in spec:  # lit's Python needs to be set with this variable
                cmake_args.append(define("python_executable", spec["python"].command.path))

        if spec.satisfies("+lldb"):
            projects.append("lldb")
            cmake_args.extend(
                [
                    define("LLDB_ENABLE_LIBEDIT", True),
                    define("LLDB_ENABLE_CURSES", True),
                    define("LLDB_ENABLE_LIBXML2", True),
                    from_variant("LLDB_ENABLE_LUA", "lua"),
                    define("LLDB_ENABLE_LZMA", True),
                ]
            )
            if spec.satisfies("@19:"):
                cmake_args.append(define("LLDB_CURSES_LIBS", spec["ncurses"].libs))
            else:
                if spec["ncurses"].satisfies("+termlib"):
                    cmake_args.append(define("LLVM_ENABLE_TERMINFO", True))
                else:
                    cmake_args.append(define("LLVM_ENABLE_TERMINFO", False))
            if spec.version >= Version("10"):
                cmake_args.append(from_variant("LLDB_ENABLE_PYTHON", "python"))
            else:
                cmake_args.append(define("LLDB_DISABLE_PYTHON", spec.satisfies("~python")))
            if spec.satisfies("@5.0.0: +python"):
                cmake_args.append(define("LLDB_USE_SYSTEM_SIX", True))
        elif spec.satisfies("@:19"):
            cmake_args.append(define("LLVM_ENABLE_TERMINFO", False))

        if spec.satisfies("+gold"):
            cmake_args.append(define("LLVM_BINUTILS_INCDIR", spec["binutils"].prefix.include))

        if spec.satisfies("+clang"):
            projects.append("clang")
            projects.append("clang-tools-extra")
            if spec.satisfies("openmp=runtime"):
                runtimes.append("openmp")
            elif spec.satisfies("openmp=project"):
                projects.append("openmp")

            if spec.satisfies("+offload"):
                runtimes.append("offload")

            if spec.satisfies("+libomptarget"):
                cmake_args.append(define("OPENMP_ENABLE_LIBOMPTARGET", True))
            else:
                cmake_args.append(define("OPENMP_ENABLE_LIBOMPTARGET", False))

            if spec.satisfies("@8"):
                cmake_args.append(from_variant("CLANG_ANALYZER_ENABLE_Z3_SOLVER", "z3"))
            elif spec.satisfies("@9:"):
                cmake_args.append(from_variant("LLVM_ENABLE_Z3_SOLVER", "z3"))

        if spec.satisfies("+flang"):
            projects.append("flang")
        if spec.satisfies("+lld"):
            projects.append("lld")
        if spec.satisfies("compiler-rt=runtime"):
            runtimes.append("compiler-rt")
        elif spec.satisfies("compiler-rt=project"):
            projects.append("compiler-rt")
        if spec.satisfies("libcxx=runtime"):
            runtimes.extend(["libcxx", "libcxxabi"])
        elif spec.satisfies("libcxx=project"):
            projects.extend(["libcxx", "libcxxabi"])
        if spec.satisfies("+mlir"):
            projects.append("mlir")
        if spec.satisfies("libunwind=runtime"):
            runtimes.append("libunwind")
        elif spec.satisfies("libunwind=project"):
            projects.append("libunwind")
        if spec.satisfies("+polly"):
            projects.append("polly")
            cmake_args.append(define("LINK_POLLY_INTO_TOOLS", True))

        cmake_args.extend(
            [
                define("BUILD_SHARED_LIBS", False),
                from_variant("LLVM_BUILD_LLVM_DYLIB", "llvm_dylib"),
                from_variant("LLVM_LINK_LLVM_DYLIB", "link_llvm_dylib"),
                from_variant("LLVM_USE_SPLIT_DWARF", "split_dwarf"),
                # By default on Linux, libc++.so is a ldscript. CMake fails to add
                # CMAKE_INSTALL_RPATH to it, which fails. Statically link libc++abi.a
                # into libc++.so, linking with -lc++ or -stdlib=libc++ is enough.
                define("LIBCXX_ENABLE_STATIC_ABI_LIBRARY", True),
                # Make sure that CMake does not pick host-installed tools for the build
                # Until #45535 is merged, prevent CMake from delivering incompatible
                # system tools like python3.12 to older LLVM versions like LLVM-14:
                define("CMAKE_FIND_PACKAGE_PREFER_CONFIG", True),
                define("CMAKE_FIND_USE_PACKAGE_ROOT_PATH", False),
                define("CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY", False),
                define("CMAKE_FIND_USE_PACKAGE_REGISTRY", False),
                define("CMAKE_FIND_USE_SYSTEM_PATH", False),
            ]
        )

        cmake_args.append(define("LLVM_TARGETS_TO_BUILD", get_llvm_targets_to_build(spec)))

        cmake_args.append(from_variant("LIBOMP_TSAN_SUPPORT", "libomp_tsan"))

        # From clang 16 onwards we use a more precise --gcc-install-dir flag in post-install
        # generated config files.
        if self.spec.satisfies("@:15 %gcc"):
            cmake_args.append(define("GCC_INSTALL_PREFIX", self.compiler.prefix))

        if self.spec.satisfies("~code_signing platform=darwin"):
            cmake_args.append(define("LLDB_USE_SYSTEM_DEBUGSERVER", True))

        # LLDB test suite requires libc++
        if spec.satisfies("libcxx=none"):
            cmake_args.append(define("LLDB_INCLUDE_TESTS", False))

        # Enable building with CLT [and not require full Xcode]
        # https://github.com/llvm/llvm-project/issues/57037
        if self.spec.satisfies("@15.0.0: platform=darwin"):
            cmake_args.append(
                define(
                    "BUILTINS_CMAKE_ARGS",
                    ";".join(
                        [f"-DCOMPILER_RT_ENABLE_{os}=OFF" for os in ("IOS", "WATCHOS", "TVOS")]
                    ),
                )
            )

        if self.spec.satisfies("platform=darwin"):
            cmake_args.append(define("LLVM_ENABLE_LIBCXX", True))
            cmake_args.append(define("DEFAULT_SYSROOT", macos_sdk_path()))
            # without this libc++ headers are not fond during compiler-rt build
            cmake_args.append(define("LLVM_BUILD_EXTERNAL_COMPILER_RT", True))

        # Semicolon seperated list of projects to enable
        cmake_args.append(define("LLVM_ENABLE_PROJECTS", projects))

        # Semicolon seperated list of runtimes to enable
        if runtimes:
            # The older versions are not careful enough with the order of the runtimes.
            # Instead of applying
            # https://github.com/llvm/llvm-project/commit/06400a0142af8297b5d39b8f34a7c59db6f9910c,
            # which might be incompatible with the version that we install,
            # we sort the runtimes here according to the same order as
            # in the aforementioned commit:
            if self.spec.satisfies("@:14"):
                runtimes_order = [
                    "libc",
                    "libunwind",
                    "libcxxabi",
                    "libcxx",
                    "compiler-rt",
                    "openmp",
                ]
                runtimes.sort(
                    key=lambda x: (
                        runtimes_order.index(x) if x in runtimes_order else len(runtimes_order)
                    )
                )

            # CMake args passed just to runtimes
            runtime_cmake_args = [define("CMAKE_INSTALL_RPATH_USE_LINK_PATH", True)]

            # When building runtimes, just-built clang has to know where GCC is.
            gcc_install_dir_flag = get_gcc_install_dir_flag(spec, self.compiler)
            if gcc_install_dir_flag:
                runtime_cmake_args.extend(
                    [
                        define("CMAKE_C_FLAGS", gcc_install_dir_flag),
                        define("CMAKE_CXX_FLAGS", gcc_install_dir_flag),
                    ]
                )

            cmake_args.extend(
                [
                    define("LLVM_ENABLE_RUNTIMES", runtimes),
                    define("RUNTIMES_CMAKE_ARGS", runtime_cmake_args),
                ]
            )

        return cmake_args

    @run_after("install")
    def post_install(self):
        spec = self.spec
        define = self.define

        # unnecessary if we build openmp via LLVM_ENABLE_RUNTIMES
        if self.spec.satisfies("+cuda openmp=project"):
            ompdir = "build-bootstrapped-omp"
            prefix_paths = get_cmake_prefix_path(self)
            prefix_paths.append(str(spec.prefix))
            # rebuild libomptarget to get bytecode runtime library files
            with working_dir(ompdir, create=True):
                cmake_args = [
                    "-G",
                    "Ninja",
                    define("CMAKE_BUILD_TYPE", spec.variants["build_type"].value),
                    define("CMAKE_C_COMPILER", spec.prefix.bin + "/clang"),
                    define("CMAKE_CXX_COMPILER", spec.prefix.bin + "/clang++"),
                    define("CMAKE_INSTALL_PREFIX", spec.prefix),
                    define("CMAKE_PREFIX_PATH", prefix_paths),
                ]
                cmake_args.extend(self.cmake_args())
                cmake_args.extend(
                    [
                        define("LIBOMPTARGET_NVPTX_ENABLE_BCLIB", True),
                        self.stage.source_path + "/openmp",
                    ]
                )

                cmake(*cmake_args)
                ninja()
                ninja("install")
        if self.spec.satisfies("+python"):
            if spec.version < Version("17.0.0"):
                # llvm bindings were removed in v17:
                # https://releases.llvm.org/17.0.1/docs/ReleaseNotes.html#changes-to-the-python-bindings
                install_tree("llvm/bindings/python", python_platlib)

            if self.spec.satisfies("+clang"):
                install_tree("clang/bindings/python", python_platlib)

        with working_dir(self.build_directory):
            install_tree("bin", join_path(self.prefix, "libexec", "llvm"))

        cfg_files = []
        if spec.satisfies("+clang"):
            cfg_files.extend(("clang.cfg", "clang++.cfg"))
        if spec.satisfies("@19: +flang"):
            # The config file is `flang.cfg` even though the executable is `flang-new`.
            # `--gcc-install-dir` / `--gcc-toolchain` support was only added in LLVM 19.
            cfg_files.append("flang.cfg")
        gcc_install_dir_flag = get_gcc_install_dir_flag(spec, self.compiler)
        if gcc_install_dir_flag:
            for cfg in cfg_files:
                with open(os.path.join(self.prefix.bin, cfg), "w") as f:
                    print(gcc_install_dir_flag, file=f)

    def llvm_config(self, *args, result=None, **kwargs):
        lc = Executable(self.prefix.bin.join("llvm-config"))
        if not kwargs.get("output"):
            kwargs["output"] = str
        ret = lc(*args, **kwargs)
        if result == "list":
            return ret.split()
        else:
            return ret

    @property
    def unresolved_libraries(self):
        # libomptarget at 14 and older has a hard-coded rpath that lacks hwloc's path
        # https://github.com/llvm/llvm-project/commit/dc52712a063241bd0d3a0473b4e7ed870e41921f
        if self.spec.satisfies("@:14 +libomptarget"):
            return ["*"]

        # TODO: for newer llvm there are still issues with runtimes for omp we
        # have to add rpaths to `bin/llvm-omp-*` and `share/gdb/python/ompd/ompdModule.so`.
        return ["libpython*.so.*", "libomp.so*", "libomptarget*.so*", "libunwind.so.*"]


def get_gcc_install_dir_flag(spec: Spec, compiler) -> Optional[str]:
    """Get the --gcc-install-dir=... flag, so that clang does not do a system scan for GCC."""
    if not spec.satisfies("@16: %gcc"):
        return None
    gcc = Executable(compiler.cc)
    libgcc_path = gcc("-print-file-name=libgcc.a", output=str, fail_on_error=False).strip()
    if not os.path.isabs(libgcc_path):
        return None
    libgcc_dir = os.path.dirname(libgcc_path)
    return f"--gcc-install-dir={libgcc_dir}" if os.path.exists(libgcc_dir) else None


def get_llvm_targets_to_build(spec):
    targets = spec.variants["targets"].value

    # Build everything?
    if "all" in targets:
        return "all"

    # Convert targets variant values to CMake LLVM_TARGETS_TO_BUILD array.
    spack_to_cmake = {
        "aarch64": "AArch64",
        "amdgpu": "AMDGPU",
        "arm": "ARM",
        "avr": "AVR",
        "bpf": "BPF",
        "cppbackend": "CppBackend",
        "hexagon": "Hexagon",
        "lanai": "Lanai",
        "mips": "Mips",
        "msp430": "MSP430",
        "nvptx": "NVPTX",
        "powerpc": "PowerPC",
        "riscv": "RISCV",
        "sparc": "Sparc",
        "systemz": "SystemZ",
        "webassembly": "WebAssembly",
        "x86": "X86",
        "xcore": "XCore",
    }

    if "none" in targets:
        llvm_targets = set()
    else:
        llvm_targets = set(spack_to_cmake[target] for target in targets)

    if spec.target.family in ("x86", "x86_64"):
        llvm_targets.add("X86")
    elif spec.target.family == "arm":
        llvm_targets.add("ARM")
    elif spec.target.family == "aarch64":
        llvm_targets.add("AArch64")
    elif spec.target.family in ("sparc", "sparc64"):
        llvm_targets.add("Sparc")
    elif spec.target.family in ("ppc64", "ppc64le", "ppc", "ppcle"):
        llvm_targets.add("PowerPC")

    return list(llvm_targets)
