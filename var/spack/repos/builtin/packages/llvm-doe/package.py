# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import re
import sys

import llnl.util.tty as tty

import spack.util.executable
from spack.build_systems.cmake import get_cmake_prefix_path
from spack.package import *


class LlvmDoe(CMakePackage, CudaPackage):
    """This package provides a collection of the experimental LLVM projects done
    by the US DOE research and development teams.
    """

    homepage = "https://github.com/llvm-doe-org"
    url = "https://github.com/llvm-doe-org/llvm-project/archive/llvmorg-10.0.0.zip"
    git = "https://github.com/llvm-doe-org/llvm-project"
    maintainers("vlkale")

    tags = ["e4s"]

    generator("ninja")

    version("doe", branch="doe", preferred=True)
    version("upstream", branch="llvm.org/main")
    version("bolt", branch="bolt/main")
    version("develop.clacc", branch="clacc/main")
    version("pragma-clang-loop", branch="sollve/pragma-clang-loop")
    version("pragma-omp-tile", branch="sollve/pragma-omp-tile")
    version("13.0.0", branch="llvm.org/llvmorg-13.0.0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant(
        "clang", default=True, description="Build the LLVM C/C++/Objective-C compiler frontend"
    )
    variant("flang", default=False, description="Build the LLVM Fortran compiler frontend")
    variant(
        "omp_debug",
        default=False,
        description="Include debugging code in OpenMP runtime libraries",
    )
    variant("lldb", default=False, description="Build the LLVM debugger")
    variant("lld", default=True, description="Build the LLVM linker")
    variant("mlir", default=False, description="Build with MLIR support")
    variant("internal_unwind", default=True, description="Build the libcxxabi libunwind")
    variant(
        "polly",
        default=True,
        description="Build the LLVM polyhedral optimization plugin, " "only builds for 3.7.0+",
    )
    variant("libcxx", default=True, description="Build the LLVM C++ standard library")
    variant(
        "compiler-rt",
        default=True,
        description="Build LLVM compiler runtime, including sanitizers",
    )
    variant(
        "gold",
        default=(sys.platform != "darwin"),
        description="Add support for LTO with the gold linker plugin",
    )
    variant("split_dwarf", default=False, description="Build with split dwarf information")
    variant(
        "llvm_dylib",
        default=False,
        description="Build LLVM shared library, containing all "
        "components in a single shared library",
    )
    variant(
        "link_llvm_dylib",
        default=False,
        description="Link LLVM tools against the LLVM shared library",
    )
    variant(
        "all_targets",
        default=False,
        description="Build all supported targets, default targets "
        "<current arch>,NVPTX,AMDGPU,CppBackend",
    )
    variant("omp_tsan", default=False, description="Build with OpenMP capable thread sanitizer")
    variant(
        "omp_as_runtime",
        default=True,
        description="Build OpenMP runtime via ENABLE_RUNTIME by just-built Clang",
    )
    variant(
        "argobots",
        default=False,
        description="Build BOLT/OpenMP with Argobots. Effective when @bolt",
    )
    variant("code_signing", default=False, description="Enable code-signing on macOS")
    variant("python", default=False, description="Install python bindings")

    variant("version_suffix", default="none", description="Add a symbol suffix")
    variant("z3", default=False, description="Use Z3 for the clang static analyzer")

    extends("python", when="+python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on("cmake@3.13.4:", type="build", when="@12:")
    depends_on("python", when="~python", type="build")
    depends_on("pkgconfig", type="build")

    # Universal dependency
    depends_on("python", when="+python")
    depends_on("z3", when="+clang+z3")

    # openmp dependencies
    depends_on("perl-data-dumper", type=("build"))
    depends_on("hwloc")
    depends_on("libelf", when="+cuda")  # libomptarget
    depends_on("libffi", when="+cuda")  # libomptarget

    # ncurses dependency
    depends_on("ncurses+termlib")

    # lldb dependencies
    depends_on("swig", when="+lldb")
    depends_on("libedit", when="+lldb")
    depends_on("py-six", when="+lldb +python")

    # gold support, required for some features
    depends_on("binutils+gold+ld+plugins", when="+gold")

    conflicts("+link_llvm_dylib", when="~llvm_dylib")
    conflicts("+lldb", when="~clang")
    conflicts("+libcxx", when="~clang")
    conflicts("+internal_unwind", when="~clang")
    conflicts("+compiler-rt", when="~clang")
    conflicts("+flang", when="~clang")

    conflicts("~mlir", when="+flang", msg="Flang requires MLIR")

    # Older LLVM do not build with newer compilers, and vice versa
    conflicts("%gcc@8:", when="@:5")
    conflicts("%gcc@:5.0", when="@8:")
    # clang/lib: a lambda parameter cannot shadow an explicitly captured entity
    conflicts("%clang@8:", when="@:4")

    # When these versions are concretized, but not explicitly with +libcxx, these
    # conflicts will enable clingo to set ~libcxx, making the build successful:

    # libc++ of LLVM13, see https://libcxx.llvm.org/#platform-and-compiler-support
    # @13 does not support %gcc@:10 https://bugs.llvm.org/show_bug.cgi?id=51359#c1
    # GCC    11     - latest stable release per GCC release page
    # Clang: 11, 12 - latest two stable releases per LLVM release page
    # AppleClang 12 - latest stable release per Xcode release page
    conflicts("%gcc@:10", when="@13:+libcxx")
    conflicts("%clang@:10", when="@13:+libcxx")
    conflicts("%apple-clang@:11", when="@13:+libcxx")

    # libcxx-4 and compiler-rt-4 fail to build with "newer" clang and gcc versions:
    conflicts("%gcc@7:", when="@:4+libcxx")
    conflicts("%clang@6:", when="@:4+libcxx")
    conflicts("%apple-clang@6:", when="@:4+libcxx")
    conflicts("%gcc@7:", when="@:4+compiler-rt")
    conflicts("%clang@6:", when="@:4+compiler-rt")
    conflicts("%apple-clang@6:", when="@:4+compiler-rt")

    # OMP TSAN exists in > 5.x
    conflicts("+omp_tsan", when="@:5")

    # OpenMP via ENABLE_RUNTIME restrictions
    conflicts("+omp_as_runtime", when="~clang", msg="omp_as_runtime requires clang being built.")
    conflicts("+omp_as_runtime", when="@:11.1", msg="omp_as_runtime works since LLVM 12.")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    # MLIR exists in > 10.x
    conflicts("+mlir", when="@:9")

    # code signing is only necessary on macOS",
    conflicts("+code_signing", when="platform=linux")

    conflicts(
        "+code_signing",
        when="~lldb platform=darwin",
        msg="code signing is only necessary for building the "
        "in-tree debug server on macOS. Turning this variant "
        "off enables a build of llvm with lldb that uses the "
        "system debug server",
    )

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts("^cmake@3.19.0", when="@:11.0.0")

    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch("constexpr_longdouble_9.0.patch", when="@9:10.0.0+libcxx")

    # https://github.com/spack/spack/issues/19625,
    # merged in llvm-11.0.0_rc2
    patch("lldb_external_ncurses-10.patch", when="@10.0.0:10+lldb")

    # https://github.com/spack/spack/issues/19908
    # merged in llvm main prior to 12.0.0
    patch("llvm_python_path.patch", when="@11.0.0")

    # The functions and attributes below implement external package
    # detection for LLVM. See:
    #
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
    executables = ["clang", "flang", "ld.lld", "lldb"]

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # Executables like lldb-vscode-X are daemon listening
            # on some port and would hang Spack during detection.
            # clang-cl and clang-cpp are dev tools that we don't
            # need to test
            if any(x in exe for x in ("vscode", "cpp", "-cl", "-gpu")):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(
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
        try:
            compiler = Executable(exe)
            output = compiler("--version", output=str, error=str)
            if "Apple" in output:
                return None
            if "AMD" in output:
                return None
            match = version_regex.search(output)
            if match:
                return match.group(match.lastindex)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants, compilers = ["+clang"], {}
        lld_found, lldb_found = False, False
        for exe in exes:
            if "clang++" in exe:
                compilers["cxx"] = exe
            elif "clang" in exe:
                compilers["c"] = exe
            elif "flang" in exe:
                variants.append("+flang")
                compilers["fc"] = exe
                compilers["f77"] = exe
            elif "ld.lld" in exe:
                lld_found = True
                compilers["ld"] = exe
            elif "lldb" in exe:
                lldb_found = True
                compilers["lldb"] = exe

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
        if name == "cxxflags":
            flags.append(self.compiler.cxx11_flag)
            return (None, flags, None)
        elif name == "ldflags" and self.spec.satisfies("%intel"):
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
            define("LLVM_ENABLE_EH", True),
            define("CLANG_DEFAULT_OPENMP_RUNTIME", "libomp"),
            define("LIBOMP_USE_HWLOC", True),
            define("LIBOMP_HWLOC_INSTALL_DIR", spec["hwloc"].prefix),
        ]

        version_suffix = spec.variants["version_suffix"].value
        if version_suffix != "none":
            cmake_args.append(define("LLVM_VERSION_SUFFIX", version_suffix))

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
            if spec.satisfies("+omp_as_runtime"):
                cmake_args.extend(
                    [
                        define("LIBOMPTARGET_NVPTX_ENABLE_BCLIB", True),
                        # work around bad libelf detection in libomptarget
                        define(
                            "LIBOMPTARGET_DEP_LIBELF_INCLUDE_DIR", spec["libelf"].prefix.include
                        ),
                    ]
                )
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

        cmake_args.append(from_variant("LIBOMPTARGET_ENABLE_DEBUG", "omp_debug"))

        if spec.satisfies("+lldb"):
            if spec.version >= Version("10"):
                cmake_args.append(from_variant("LLDB_ENABLE_PYTHON", "python"))
            else:
                cmake_args.append(define("LLDB_DISABLE_PYTHON", spec.satisfies("~python")))
            if spec.satisfies("@5.0.0: +python"):
                cmake_args.append(define("LLDB_USE_SYSTEM_SIX", True))

        if spec.satisfies("+gold"):
            cmake_args.append(define("LLVM_BINUTILS_INCDIR", spec["binutils"].prefix.include))

        if spec.satisfies("+clang"):
            projects.append("clang")
            projects.append("clang-tools-extra")
            if spec.satisfies("+omp_as_runtime"):
                runtimes.append("openmp")
            else:
                projects.append("openmp")

            if self.spec.satisfies("@8"):
                cmake_args.append(
                    define("CLANG_ANALYZER_ENABLE_Z3_SOLVER", self.spec.satisfies("@8+z3"))
                )
            if self.spec.satisfies("@9:"):
                cmake_args.append(define("LLVM_ENABLE_Z3_SOLVER", self.spec.satisfies("@9:+z3")))

        if spec.satisfies("+flang"):
            projects.append("flang")
        if spec.satisfies("+lldb"):
            projects.append("lldb")
        if spec.satisfies("+lld"):
            projects.append("lld")
        if spec.satisfies("+compiler-rt"):
            projects.append("compiler-rt")
        if spec.satisfies("+libcxx"):
            projects.append("libcxx")
            projects.append("libcxxabi")
        if spec.satisfies("+mlir"):
            projects.append("mlir")
        if spec.satisfies("+internal_unwind"):
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
            ]
        )

        if "+all_targets" not in spec:  # all is default on cmake
            targets = ["NVPTX", "AMDGPU"]
            if spec.version < Version("3.9.0"):
                # Starting in 3.9.0 CppBackend is no longer a target (see
                # LLVM_ALL_TARGETS in llvm's top-level CMakeLists.txt for
                # the complete list of targets)
                targets.append("CppBackend")

            if spec.target.family in ("x86", "x86_64"):
                targets.append("X86")
            elif spec.target.family == "arm":
                targets.append("ARM")
            elif spec.target.family == "aarch64":
                targets.append("AArch64")
            elif spec.target.family in ("sparc", "sparc64"):
                targets.append("Sparc")
            elif spec.target.family in ("ppc64", "ppc64le", "ppc", "ppcle"):
                targets.append("PowerPC")

            cmake_args.append(define("LLVM_TARGETS_TO_BUILD", targets))

        cmake_args.append(from_variant("LIBOMP_TSAN_SUPPORT", "omp_tsan"))

        if spec.satisfies("@bolt"):
            projects.remove("openmp")
            projects.append("bolt")
            cmake_args.append("-DLIBOMP_USE_BOLT_DEFAULT=ON")
            if spec.satisfies("+argobots") and spec.satisfies("@bolt"):
                cmake_args.append("-DLIBOMP_USE_ARGOBOTS=ON")

        if self.compiler.name == "gcc":
            cmake_args.append(define("GCC_INSTALL_PREFIX", self.compiler.prefix))

        # if spec.satisfies("platform=linux"):
        #     cmake_args.append("-DCMAKE_BUILD_WITH_INSTALL_RPATH=1")

        if self.spec.satisfies("~code_signing platform=darwin"):
            cmake_args.append(define("LLDB_USE_SYSTEM_DEBUGSERVER", True))

        # Semicolon seperated list of projects to enable
        cmake_args.append(define("LLVM_ENABLE_PROJECTS", projects))

        # Semicolon seperated list of runtimes to enable
        if runtimes:
            cmake_args.append(define("LLVM_ENABLE_RUNTIMES", runtimes))

        return cmake_args

    @run_after("install")
    def post_install(self):
        spec = self.spec
        define = self.define

        # unnecessary if we build openmp via LLVM_ENABLE_RUNTIMES
        if self.spec.satisfies("+cuda ~omp_as_runtime"):
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
                        define(
                            "LIBOMPTARGET_DEP_LIBELF_INCLUDE_DIR", spec["libelf"].prefix.include
                        ),
                        self.stage.source_path + "/openmp",
                    ]
                )

                cmake(*cmake_args)
                ninja()
                ninja("install")
        if self.spec.satisfies("+python"):
            install_tree("llvm/bindings/python", python_platlib)

            if self.spec.satisfies("+clang"):
                install_tree("clang/bindings/python", python_platlib)

        with working_dir(self.build_directory):
            install_tree("bin", join_path(self.prefix, "libexec", "llvm"))
