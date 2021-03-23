# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re
import sys

import llnl.util.tty as tty
import spack.util.executable


class LlvmDoe(CMakePackage, CudaPackage):
    """This package provides a collection of the experimental LLVM projects done
    by the US DOE research and development teams.
    """

    homepage = "https://github.com/llvm-doe-org"
    url = "https://github.com/llvm-doe-org/llvm-project/archive/llvmorg-10.0.0.zip"
    git = "https://github.com/llvm-doe-org/llvm-project"
    maintainers = ['shintaro-iwasaki']

    version('doe', branch='doe', preferred=True)
    version('upstream', branch='llvm.org/main')
    version('bolt', branch='bolt/main')
    version('clacc', branch='clacc/master')
    version('pragma-clang-loop', branch='sollve/pragma-clang-loop')
    version('pragma-omp-tile', branch='sollve/pragma-omp-tile')

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant(
        "clang",
        default=True,
        description="Build the LLVM C/C++/Objective-C compiler frontend",
    )
    variant(
        "flang",
        default=False,
        description="Build the LLVM Fortran compiler frontend",
    )
    variant(
        "omp_debug",
        default=False,
        description="Include debugging code in OpenMP runtime libraries",
    )
    variant("lldb", default=False, description="Build the LLVM debugger")
    variant("lld", default=True, description="Build the LLVM linker")
    variant("mlir", default=False, description="Build with MLIR support")
    variant(
        "internal_unwind",
        default=True,
        description="Build the libcxxabi libunwind",
    )
    variant(
        "polly",
        default=True,
        description="Build the LLVM polyhedral optimization plugin, "
        "only builds for 3.7.0+",
    )
    variant(
        "libcxx",
        default=True,
        description="Build the LLVM C++ standard library",
    )
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
    variant(
        "split_dwarf",
        default=False,
        description="Build with split dwarf information",
    )
    variant(
        "shared_libs",
        default=False,
        description="Build all components as shared libraries, faster, "
        "less memory to build, less stable",
    )
    variant(
        "llvm_dylib",
        default=False,
        description="Build LLVM shared library, containing all "
        "components in a single shared library",
    )
    variant(
        "all_targets",
        default=False,
        description="Build all supported targets, default targets "
        "<current arch>,NVPTX,AMDGPU,CppBackend",
    )
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant(
        "omp_tsan",
        default=False,
        description="Build with OpenMP capable thread sanitizer",
    )
    variant(
        "argobots",
        default=False,
        description="Build BOLT/OpenMP with Argobots. Effective when @bolt",
    )
    variant('code_signing', default=False,
            description="Enable code-signing on macOS")
    variant("python", default=False, description="Install python bindings")

    extends("python", when="+python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on("python", when="~python", type="build")
    depends_on("pkgconfig", type="build")

    # Universal dependency
    depends_on("python", when="+python")
    depends_on("z3")

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
    depends_on("binutils+gold", when="+gold")

    conflicts("+llvm_dylib", when="+shared_libs")
    conflicts("+lldb", when="~clang")
    conflicts("+libcxx", when="~clang")
    conflicts("+internal_unwind", when="~clang")
    conflicts("+compiler-rt", when="~clang")

    conflicts("%gcc@:5.0.999")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    conflicts("+mlir")

    conflicts("+flang", when="~clang")

    # code signing is only necessary on macOS",
    conflicts('+code_signing', when='platform=linux')
    conflicts('+code_signing', when='platform=cray')

    conflicts(
        '+code_signing',
        when='~lldb platform=darwin',
        msg="code signing is only necessary for building the "
            "in-tree debug server on macOS. Turning this variant "
            "off enables a build of llvm with lldb that uses the "
            "system debug server",
    )

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts('^cmake@3.19.0', when='@:11.0.0')

    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch("constexpr_longdouble_9.0.patch", when="@9:10.0.0+libcxx")

    # https://github.com/spack/spack/issues/19625,
    # merged in llvm-11.0.0_rc2
    patch("lldb_external_ncurses-10.patch", when="@10.0.0:10.99+lldb")

    # https://github.com/spack/spack/issues/19908
    # merged in llvm main prior to 12.0.0
    patch("llvm_python_path.patch", when="@11.0.0")

    # The functions and attributes below implement external package
    # detection for LLVM. See:
    #
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
    executables = ['clang', 'flang', 'ld.lld', 'lldb']

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # Executables like lldb-vscode-X are daemon listening
            # on some port and would hang Spack during detection.
            # clang-cl and clang-cpp are dev tools that we don't
            # need to test
            if any(x in exe for x in ('vscode', 'cpp', '-cl', '-gpu')):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(
            # Normal clang compiler versions are left as-is
            r'clang version ([^ )\n]+)-svn[~.\w\d-]*|'
            # Don't include hyphenated patch numbers in the version
            # (see https://github.com/spack/spack/pull/14365 for details)
            r'clang version ([^ )\n]+?)-[~.\w\d-]*|'
            r'clang version ([^ )\n]+)|'
            # LLDB
            r'lldb version ([^ )\n]+)|'
            # LLD
            r'LLD ([^ )\n]+) \(compatible with GNU linkers\)'
        )
        try:
            compiler = Executable(exe)
            output = compiler('--version', output=str, error=str)
            if 'Apple' in output:
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
        variants, compilers = ['+clang'], {}
        lld_found, lldb_found = False, False
        for exe in exes:
            if 'clang++' in exe:
                compilers['cxx'] = exe
            elif 'clang' in exe:
                compilers['c'] = exe
            elif 'flang' in exe:
                variants.append('+flang')
                compiler['fc'] = exe
                compilers['f77'] = exe
            elif 'ld.lld' in exe:
                lld_found = True
                compilers['ld'] = exe
            elif 'lldb' in exe:
                lldb_found = True
                compilers['lldb'] = exe

        variants.append('+lld' if lld_found else '~lld')
        variants.append('+lldb' if lldb_found else '~lldb')

        return ''.join(variants), {'compilers': compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For LLVM 'compilers' is a mandatory attribute
        msg = ('the extra attribute "compilers" must be set for '
               'the detected spec "{0}"'.format(spec))
        assert 'compilers' in extra_attributes, msg
        compilers = extra_attributes['compilers']
        for key in ('c', 'cxx'):
            msg = '{0} compiler not found for {1}'
            assert key in compilers, msg.format(key, spec)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        result = None
        if '+clang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'clang')
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        result = None
        if '+clang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'clang++')
        return result

    @property
    def fc(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('fc', None)
        result = None
        if '+flang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'flang')
        return result

    @property
    def f77(self):
        msg = "cannot retrieve Fortran 77 compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('f77', None)
        result = None
        if '+flang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'flang')
        return result

    @run_before('cmake')
    def codesign_check(self):
        if self.spec.satisfies("+code_signing"):
            codesign = which('codesign')
            mkdir('tmp')
            llvm_check_file = join_path('tmp', 'llvm_check')
            copy('/usr/bin/false', llvm_check_file)
            try:
                codesign('-f', '-s', 'lldb_codesign', '--dryrun',
                         llvm_check_file)

            except ProcessError:
                # Newer LLVM versions have a simple script that sets up
                # automatically when run with sudo priviliges
                setup = Executable("./lldb/scripts/macos-setup-codesign.sh")
                try:
                    setup()
                except Exception:
                    raise RuntimeError(
                        'spack was unable to either find or set up'
                        'code-signing on your system. Please refer to'
                        'https://lldb.llvm.org/resources/build.html#'
                        'code-signing-on-macos for details on how to'
                        'create this identity.'
                    )

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", self.compiler.cxx11_flag)

    def setup_run_environment(self, env):
        if "+clang" in self.spec:
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))
        if "+flang" in self.spec:
            env.set("FC", join_path(self.spec.prefix.bin, "flang"))
            env.set("F77", join_path(self.spec.prefix.bin, "flang"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        python = spec['python']
        cmake_args = [
            "-DLLVM_REQUIRES_RTTI:BOOL=ON",
            "-DLLVM_ENABLE_RTTI:BOOL=ON",
            "-DLLVM_ENABLE_EH:BOOL=ON",
            "-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp",
            "-DPYTHON_EXECUTABLE:PATH={0}".format(python.command.path),
            "-DLIBOMP_USE_HWLOC:BOOL=ON",
            "-DLIBOMP_HWLOC_INSTALL_DIR={0}".format(spec["hwloc"].prefix),
        ]

        if python.version >= Version("3.0.0"):
            cmake_args.append("-DPython3_EXECUTABLE={0}".format(
                              python.command.path))
        else:
            cmake_args.append("-DPython2_EXECUTABLE={0}".format(
                              python.command.path))

        projects = []

        if "+cuda" in spec:
            cmake_args.extend(
                [
                    "-DCUDA_TOOLKIT_ROOT_DIR:PATH=" + spec["cuda"].prefix,
                    "-DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES={0}".format(
                        ",".join(spec.variants["cuda_arch"].value)
                    ),
                    "-DCLANG_OPENMP_NVPTX_DEFAULT_ARCH=sm_{0}".format(
                        spec.variants["cuda_arch"].value[-1]
                    ),
                ]
            )
        else:
            # still build libomptarget but disable cuda
            cmake_args.extend(
                [
                    "-DCUDA_TOOLKIT_ROOT_DIR:PATH=IGNORE",
                    "-DCUDA_SDK_ROOT_DIR:PATH=IGNORE",
                    "-DCUDA_NVCC_EXECUTABLE:FILEPATH=IGNORE",
                    "-DLIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES:STRING=IGNORE",
                ]
            )

        if "+omp_debug" in spec:
            cmake_args.append("-DLIBOMPTARGET_ENABLE_DEBUG:Bool=ON")

        if "+python" in spec and "+lldb" in spec:
            cmake_args.append("-DLLDB_USE_SYSTEM_SIX:Bool=TRUE")

        if "+lldb" in spec and spec.satisfies("@10.0.0:,doe"):
            cmake_args.append("-DLLDB_ENABLE_PYTHON:Bool={0}".format(
                'ON' if '+python' in spec else 'OFF'))
        if "+lldb" in spec and spec.satisfies("@:9.9.9"):
            cmake_args.append("-DLLDB_DISABLE_PYTHON:Bool={0}".format(
                'ON' if '~python' in spec else 'OFF'))

        if "+gold" in spec:
            cmake_args.append(
                "-DLLVM_BINUTILS_INCDIR=" + spec["binutils"].prefix.include
            )

        if "+clang" in spec:
            projects.append("clang")
            projects.append("clang-tools-extra")
            projects.append("openmp")
        if "+flang" in spec:
            projects.append("flang")
        if "+lldb" in spec:
            projects.append("lldb")
        if "+lld" in spec:
            projects.append("lld")
        if "+compiler-rt" in spec:
            projects.append("compiler-rt")
        if "+libcxx" in spec:
            projects.append("libcxx")
            projects.append("libcxxabi")
            cmake_args.append("-DCLANG_DEFAULT_CXX_STDLIB=libc++")
        if "+mlir" in spec:
            projects.append("mlir")
        if "+internal_unwind" in spec:
            projects.append("libunwind")
        if "+polly" in spec:
            projects.append("polly")
            cmake_args.append("-DLINK_POLLY_INTO_TOOLS:Bool=ON")

        if "+shared_libs" in spec:
            cmake_args.append("-DBUILD_SHARED_LIBS:Bool=ON")
        if "+llvm_dylib" in spec:
            cmake_args.append("-DLLVM_BUILD_LLVM_DYLIB:Bool=ON")
        if "+omp_debug" in spec:
            cmake_args.append("-DLIBOMPTARGET_ENABLE_DEBUG:Bool=ON")

        if "+split_dwarf" in spec:
            cmake_args.append("-DLLVM_USE_SPLIT_DWARF:Bool=ON")

        if "+all_targets" not in spec:  # all is default on cmake

            targets = ["NVPTX", "AMDGPU"]
            if spec.target.family == "x86" or spec.target.family == "x86_64":
                targets.append("X86")
            elif spec.target.family == "arm":
                targets.append("ARM")
            elif spec.target.family == "aarch64":
                targets.append("AArch64")
            elif (
                spec.target.family == "sparc"
                or spec.target.family == "sparc64"
            ):
                targets.append("Sparc")
            elif (
                spec.target.family == "ppc64"
                or spec.target.family == "ppc64le"
                or spec.target.family == "ppc"
                or spec.target.family == "ppcle"
            ):
                targets.append("PowerPC")

            cmake_args.append(
                "-DLLVM_TARGETS_TO_BUILD:STRING=" + ";".join(targets)
            )

        if "+omp_tsan" in spec:
            cmake_args.append("-DLIBOMP_TSAN_SUPPORT=ON")

        if spec.satisfies("@bolt"):
            projects.remove("openmp")
            projects.append("bolt")
            cmake_args.append("-DLIBOMP_USE_BOLT_DEFAULT=ON")
            if "+argobots" in spec and spec.satisfies("@bolt"):
                cmake_args.append("-DLIBOMP_USE_ARGOBOTS=ON")

        if self.compiler.name == "gcc":
            gcc_prefix = ancestor(self.compiler.cc, 2)
            cmake_args.append("-DGCC_INSTALL_PREFIX=" + gcc_prefix)

        if spec.satisfies("platform=cray") or spec.satisfies("platform=linux"):
            cmake_args.append("-DCMAKE_BUILD_WITH_INSTALL_RPATH=1")

        if self.spec.satisfies("~code_signing platform=darwin"):
            cmake_args.append('-DLLDB_USE_SYSTEM_DEBUGSERVER=ON')

        # Semicolon seperated list of projects to enable
        cmake_args.append(
            "-DLLVM_ENABLE_PROJECTS:STRING={0}".format(";".join(projects))
        )

        return cmake_args

    @run_before("build")
    def pre_install(self):
        with working_dir(self.build_directory):
            # When building shared libraries these need to be installed first
            make("install-LLVMTableGen")
            make("install-LLVMDemangle")
            make("install-LLVMSupport")

    @run_after("install")
    def post_install(self):
        spec = self.spec

        # unnecessary if we get bootstrap builds in here
        if "+cuda" in self.spec:
            ompdir = "build-bootstrapped-omp"
            # rebuild libomptarget to get bytecode runtime library files
            with working_dir(ompdir, create=True):
                cmake_args = [
                    self.stage.source_path + "/openmp",
                    "-DCMAKE_C_COMPILER:PATH={0}".format(
                        spec.prefix.bin + "/clang"
                    ),
                    "-DCMAKE_CXX_COMPILER:PATH={0}".format(
                        spec.prefix.bin + "/clang++"
                    ),
                    "-DCMAKE_INSTALL_PREFIX:PATH={0}".format(spec.prefix),
                ]
                cmake_args.extend(self.cmake_args())
                cmake_args.append(
                    "-DLIBOMPTARGET_NVPTX_ENABLE_BCLIB:BOOL=TRUE"
                )

                # work around bad libelf detection in libomptarget
                cmake_args.append(
                    "-DLIBOMPTARGET_DEP_LIBELF_INCLUDE_DIR:String={0}".format(
                        spec["libelf"].prefix.include
                    )
                )

                cmake(*cmake_args)
                make()
                make("install")
        if "+python" in self.spec:
            install_tree("llvm/bindings/python", site_packages_dir)

            if "+clang" in self.spec:
                install_tree("clang/bindings/python", site_packages_dir)

        with working_dir(self.build_directory):
            install_tree("bin", join_path(self.prefix, "libexec", "llvm"))
