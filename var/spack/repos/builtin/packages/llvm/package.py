# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re
import sys

import llnl.util.tty as tty
import spack.util.executable


class Llvm(CMakePackage, CudaPackage):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = "http://llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    list_url = "http://releases.llvm.org/download.html"
    git = "https://github.com/llvm/llvm-project"
    maintainers = ['trws', 'naromero77']

    family = "compiler"  # Used by lmod

    # fmt: off
    version('master', branch='master')
    version('11.0.0', sha256='8ad4ddbafac4f2c8f2ea523c2c4196f940e8e16f9e635210537582a48622a5d5')
    version('10.0.1', sha256='c7ccb735c37b4ec470f66a6c35fbae4f029c0f88038f6977180b1a8ddc255637')
    version('10.0.0', sha256='b81c96d2f8f40dc61b14a167513d87c0d813aae0251e06e11ae8a4384ca15451')
    version('9.0.1', sha256='be7b034641a5fda51ffca7f5d840b1a768737779f75f7c4fd18fe2d37820289a')
    version('9.0.0', sha256='7807fac25330e24e9955ca46cd855dd34bbc9cc4fdba8322366206654d1036f2')
    version('8.0.0', sha256='d81238b4a69e93e29f74ce56f8107cbfcf0c7d7b40510b7879e98cc031e25167')
    version('7.1.0', sha256='71c93979f20e01f1a1cc839a247945f556fa5e63abf2084e8468b238080fd839')
    version('7.0.1', sha256='f17a6cd401e8fd8f811fbfbb36dcb4f455f898c9d03af4044807ad005df9f3c0')
    version('6.0.1', sha256='aefadceb231f4c195fe6d6cd3b1a010b269c8a22410f339b5a089c2e902aa177')
    version('6.0.0', sha256='1946ec629c88d30122afa072d3c6a89cc5d5e4e2bb28dc63b2f9ebcc7917ee64')
    version('5.0.2', sha256='fe87aa11558c08856739bfd9bd971263a28657663cb0c3a0af01b94f03b0b795')
    version('5.0.1', sha256='84ca454abf262579814a2a2b846569f6e0cb3e16dc33ca3642b4f1dff6fbafd3')
    version('5.0.0', sha256='1f1843315657a4371d8ca37f01265fa9aae17dbcf46d2d0a95c1fdb3c6a4bab6')
    version('4.0.1', sha256='cd664fb3eec3208c08fb61189c00c9118c290b3be5adb3215a97b24255618be5')
    version('4.0.0', sha256='28ca4b2fc434cb1f558e8865386c233c2a6134437249b8b3765ae745ffa56a34')
    version('3.9.1', sha256='f5b6922a5c65f9232f83d89831191f2c3ccf4f41fdd8c63e6645bbf578c4ab92')
    version('3.9.0', sha256='9c6563a72c8b5b79941c773937d997dd2b1b5b3f640136d02719ec19f35e0333')
    version('3.8.1', sha256='69360f0648fde0dc3d3c4b339624613f3bc2a89c4858933bc3871a250ad02826')
    version('3.8.0', sha256='b5cc5974cc2fd4e9e49e1bbd0700f872501a8678bd9694fa2b36c65c026df1d1')
    version('3.7.1', sha256='d2cb0eb9b8eb21e07605bfe5e7a5c6c5f5f8c2efdac01ec1da6ffacaabe4195a')
    version('3.7.0', sha256='dc00bc230be2006fb87b84f6fe4800ca28bc98e6692811a98195da53c9cb28c6')
    version('3.6.2', sha256='f75d703a388ba01d607f9cf96180863a5e4a106827ade17b221d43e6db20778a')
    version('3.5.1', sha256='5d739684170d5b2b304e4fb521532d5c8281492f71e1a8568187bfa38eb5909d')
    # fmt: on

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant(
        "clang",
        default=True,
        description="Build the LLVM C/C++/Objective-C compiler frontend",
    )
    variant(
        "omp_debug",
        default=False,
        description="Include debugging code in OpenMP runtime libraries",
    )
    variant("lldb", default=True, description="Build the LLVM debugger")
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
    variant('code_signing', default=False,
            description="Enable code-signing on macOS")
    variant("python", default=False, description="Install python bindings")

    extends("python", when="+python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on("python@2.7:2.8", when="@:4.999 ~python", type="build")
    depends_on("python", when="@5: ~python", type="build")

    # Universal dependency
    depends_on("python@2.7:2.8", when="@:4.999+python")
    depends_on("python", when="@5:+python")
    depends_on("z3", when="@9:")

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
    depends_on("py-six", when="@5.0.0: +lldb +python")

    # gold support, required for some features
    depends_on("binutils+gold", when="+gold")

    # polly plugin
    depends_on("gmp", when="@:3.6.999 +polly")
    depends_on("isl", when="@:3.6.999 +polly")

    conflicts("+lldb", when="~clang")
    conflicts("+libcxx", when="~clang")
    conflicts("+internal_unwind", when="~clang")
    conflicts("+compiler-rt", when="~clang")

    # LLVM 4 and 5 does not build with GCC 8
    conflicts("%gcc@8:", when="@:5")
    conflicts("%gcc@:5.0.999", when="@8:")

    # OMP TSAN exists in > 5.x
    conflicts("+omp_tsan", when="@:5.99")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    # MLIR exists in > 10.x
    conflicts("+mlir", when="@:9")

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

    # Github issue #4986
    patch("llvm_gcc7.patch", when="@4.0.0:4.0.1+lldb %gcc@7.0:")
    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch("constexpr_longdouble.patch", when="@6:8+libcxx")
    patch("constexpr_longdouble_9.0.patch", when="@9:10.0.0+libcxx")

    # Backport from llvm master; see
    # https://bugs.llvm.org/show_bug.cgi?id=38233
    # for a bug report about this problem in llvm master.
    patch("llvm_py37.patch", when="@4:6 ^python@3.7:")

    # https://bugs.llvm.org/show_bug.cgi?id=39696
    patch("thread-p9.patch", when="@develop+libcxx")

    # https://github.com/spack/spack/issues/19625,
    # merged in llvm-11.0.0_rc2
    patch("lldb_external_ncurses-10.patch", when="@10.0.0:10.99+lldb")

    # The functions and attributes below implement external package
    # detection for LLVM. See:
    #
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
    executables = ['clang', 'ld.lld', 'lldb']

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
            r'clang version ([^ )]+)-svn[~.\w\d-]*|'
            # Don't include hyphenated patch numbers in the version
            # (see https://github.com/spack/spack/pull/14365 for details)
            r'clang version ([^ )]+?)-[~.\w\d-]*|'
            r'clang version ([^ )]+)|'
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

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            "-DLLVM_REQUIRES_RTTI:BOOL=ON",
            "-DLLVM_ENABLE_RTTI:BOOL=ON",
            "-DLLVM_ENABLE_EH:BOOL=ON",
            "-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp",
            "-DPYTHON_EXECUTABLE:PATH={0}".format(spec["python"].command.path),
            "-DLIBOMP_USE_HWLOC:BOOL=ON",
            "-DLIBOMP_HWLOC_INSTALL_DIR={0}".format(spec["hwloc"].prefix),
        ]

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

        if "+python" in spec and "+lldb" in spec and spec.satisfies("@5.0.0:"):
            cmake_args.append("-DLLDB_USE_SYSTEM_SIX:Bool=TRUE")

        if "+lldb" in spec and spec.satisfies("@:9.9.9"):
            cmake_args.append("-DLLDB_DISABLE_PYTHON:Bool={0}".format(
                'ON' if '~python' in spec else 'OFF'))
        if "+lldb" in spec and spec.satisfies("@10.0.0:"):
            cmake_args.append("-DLLDB_ENABLE_PYTHON:Bool={0}".format(
                'ON' if '+python' in spec else 'OFF'))

        if "+gold" in spec:
            cmake_args.append(
                "-DLLVM_BINUTILS_INCDIR=" + spec["binutils"].prefix.include
            )

        if "+clang" in spec:
            projects.append("clang")
            projects.append("clang-tools-extra")
            projects.append("openmp")
        if "+lldb" in spec:
            projects.append("lldb")
        if "+lld" in spec:
            projects.append("lld")
        if "+compiler-rt" in spec:
            projects.append("compiler-rt")
        if "+libcxx" in spec:
            projects.append("libcxx")
            projects.append("libcxxabi")
            if spec.satisfies("@3.9.0:"):
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
        if "+omp_debug" in spec:
            cmake_args.append("-DLIBOMPTARGET_ENABLE_DEBUG:Bool=ON")

        if "+split_dwarf" in spec:
            cmake_args.append("-DLLVM_USE_SPLIT_DWARF:Bool=ON")

        if "+all_targets" not in spec:  # all is default on cmake

            targets = ["NVPTX", "AMDGPU"]
            if spec.version < Version("3.9.0"):
                # Starting in 3.9.0 CppBackend is no longer a target (see
                # LLVM_ALL_TARGETS in llvm's top-level CMakeLists.txt for
                # the complete list of targets)
                targets.append("CppBackend")

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

        if self.compiler.name == "gcc":
            gcc_prefix = ancestor(self.compiler.cc, 2)
            cmake_args.append("-DGCC_INSTALL_PREFIX=" + gcc_prefix)

        if spec.satisfies("@4.0.0:"):
            if spec.satisfies("platform=cray") or spec.satisfies(
                "platform=linux"
            ):
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
            if self.spec.version >= Version("4.0.0"):
                # LLVMDemangle target was added in 4.0.0
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
