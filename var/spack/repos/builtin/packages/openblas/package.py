# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *
from spack.package_test import compare_output_file, compile_c_and_execute


class Openblas(CMakePackage, MakefilePackage):
    """OpenBLAS: An optimized BLAS library"""

    homepage = "https://www.openblas.net"
    url = (
        "https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.2.19/OpenBLAS-0.2.19.tar.gz"
    )
    git = "https://github.com/OpenMathLib/OpenBLAS.git"

    libraries = ["libopenblas", "openblas"]

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("0.3.28", sha256="f1003466ad074e9b0c8d421a204121100b0751c96fc6fcf3d1456bd12f8a00a1")
    version("0.3.27", sha256="aa2d68b1564fe2b13bc292672608e9cdeeeb6dc34995512e65c3b10f4599e897")
    version("0.3.26", sha256="4e6e4f5cb14c209262e33e6816d70221a2fe49eb69eaf0a06f065598ac602c68")
    version("0.3.25", sha256="4c25cb30c4bb23eddca05d7d0a85997b8db6144f5464ba7f8c09ce91e2f35543")
    version("0.3.24", sha256="ceadc5065da97bd92404cac7254da66cc6eb192679cf1002098688978d4d5132")
    version("0.3.23", sha256="5d9491d07168a5d00116cdc068a40022c3455bf9293c7cb86a65b1054d7e5114")
    version("0.3.22", sha256="7fa9685926ba4f27cfe513adbf9af64d6b6b63f9dcabb37baefad6a65ff347a7")
    version("0.3.21", sha256="f36ba3d7a60e7c8bcc54cd9aaa9b1223dd42eaf02c811791c37e8ca707c241ca")
    version("0.3.20", sha256="8495c9affc536253648e942908e88e097f2ec7753ede55aca52e5dead3029e3c")
    version("0.3.19", sha256="947f51bfe50c2a0749304fbe373e00e7637600b0a47b78a51382aeb30ca08562")
    version("0.3.18", sha256="1632c1e8cca62d8bed064b37747e331a1796fc46f688626337362bf0d16aeadb")
    version("0.3.17", sha256="df2934fa33d04fd84d839ca698280df55c690c86a5a1133b3f7266fce1de279f")
    version("0.3.16", sha256="fa19263c5732af46d40d3adeec0b2c77951b67687e670fb6ba52ea3950460d79")
    version("0.3.15", sha256="30a99dec977594b387a17f49904523e6bc8dd88bd247266e83485803759e4bbe")
    version("0.3.14", sha256="d381935d26f9cae8e4bbd7d7f278435adf8e3a90920edf284bb9ad789ee9ad60")
    version("0.3.13", sha256="79197543b17cc314b7e43f7a33148c308b0807cd6381ee77f77e15acf3e6459e")
    version("0.3.12", sha256="65a7d3a4010a4e3bd5c0baa41a234797cd3a1735449a4a5902129152601dc57b")
    version("0.3.11", sha256="bc4617971179e037ae4e8ebcd837e46db88422f7b365325bd7aba31d1921a673")
    version("0.3.10", sha256="0484d275f87e9b8641ff2eecaa9df2830cbe276ac79ad80494822721de6e1693")
    version("0.3.9", sha256="17d4677264dfbc4433e97076220adc79b050e4f8a083ea3f853a53af253bc380")
    version("0.3.8", sha256="8f86ade36f0dbed9ac90eb62575137388359d97d8f93093b38abe166ad7ef3a8")
    version("0.3.7", sha256="bde136122cef3dd6efe2de1c6f65c10955bbb0cc01a520c2342f5287c28f9379")
    version("0.3.6", sha256="e64c8fe083832ffbc1459ab6c72f71d53afd3b36e8497c922a15a06b72e9002f")
    version("0.3.5", sha256="0950c14bd77c90a6427e26210d6dab422271bc86f9fc69126725833ecdaa0e85")
    version("0.3.4", sha256="4b4b4453251e9edb5f57465bf2b3cf67b19d811d50c8588cdf2ea1f201bb834f")
    version("0.3.3", sha256="49d88f4494ae780e3d7fa51769c00d982d7cdb73e696054ac3baa81d42f13bab")
    version("0.3.2", sha256="e8ba64f6b103c511ae13736100347deb7121ba9b41ba82052b1a018a65c0cb15")
    version("0.3.1", sha256="1f5e956f35f3acdd3c74516e955d797a320c2e0135e31d838cbdb3ea94d0eb33")
    version("0.3.0", sha256="cf51543709abe364d8ecfb5c09a2b533d2b725ea1a66f203509b21a8e9d8f1a1")
    version("0.2.20", sha256="5ef38b15d9c652985774869efd548b8e3e972e1e99475c673b25537ed7bcf394")
    version("0.2.19", sha256="9c40b5e4970f27c5f6911cb0a28aa26b6c83f17418b69f8e5a116bb983ca8557")
    version("0.2.18", sha256="7d9f8d4ea4a65ab68088f3bb557f03a7ac9cb5036ef2ba30546c3a28774a4112")
    version("0.2.17", sha256="0fe836dfee219ff4cadcc3567fb2223d9e0da5f60c7382711fb9e2c35ecf0dbf")
    version("0.2.16", sha256="766f350d0a4be614812d535cead8c816fc3ad3b9afcd93167ea5e4df9d61869b")
    version("0.2.15", sha256="73c40ace5978282224e5e122a41c8388c5a19e65a6f2329c2b7c0b61bacc9044")

    variant(
        "fortran",
        default=True,
        when="@0.3.21:",
        description="w/o a Fortran compiler, OpenBLAS will build an f2c-converted LAPACK",
    )

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")
    variant("pic", default=True, description="Build position independent code")
    variant("shared", default=True, description="Build shared libraries")
    variant(
        "dynamic_dispatch",
        default=True,
        description="Enable runtime cpu detection for best kernel selection",
    )
    variant(
        "consistent_fpcsr",
        default=False,
        description="Synchronize FP CSR between threads (x86/x86_64 only)",
    )
    variant(
        "bignuma",
        default=False,
        description="Enable experimental support for up to 1024 CPUs/Cores and 128 numa nodes",
    )
    variant("symbol_suffix", default="none", description="Set a symbol suffix")

    variant("locking", default=True, description="Build with thread safety")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("pthreads", "openmp", "none"),
        multi=False,
    )

    # virtual dependency
    provides("blas", "lapack")
    provides("lapack@3.9.1:", when="@0.3.15:")
    provides("lapack@3.7.0", when="@0.2.20")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("perl", when="@:0.3.20", type="build")

    # https://github.com/OpenMathLib/OpenBLAS/pull/4879
    patch("openblas-0.3.28-thread-buffer.patch", when="@0.3.28")

    # https://github.com/OpenMathLib/OpenBLAS/pull/4328
    patch("xcode15-fortran.patch", when="@0.3.25 %apple-clang@15:")

    # https://github.com/xianyi/OpenBLAS/pull/2519/files
    patch("ifort-msvc.patch", when="%msvc")

    # https://github.com/OpenMathLib/OpenBLAS/pull/3712
    patch("cce.patch", when="@0.3.20 %cce")

    # https://github.com/OpenMathLib/OpenBLAS/pull/3778
    patch("fix-cray-fortran-detection-pr3778.patch", when="@0.3.21")

    # https://github.com/spack/spack/issues/31732
    patch("f_check-oneapi.patch", when="@0.3.20 %oneapi")
    patch("f_check-intel.patch", when="@0.3.21 %intel")

    # OpenBLAS >=3.0 has an official way to disable internal parallel builds
    patch("make.patch", when="@0.2.16:0.2.20")
    #  This patch is in a pull request to OpenBLAS that has not been handled
    #  https://github.com/OpenMathLib/OpenBLAS/pull/915
    #  UPD: the patch has been merged starting version 0.2.20
    patch("openblas_icc.patch", when="@:0.2.19%intel")
    patch("openblas_icc_openmp.patch", when="@:0.2.20%intel@16.0:")
    patch("openblas_icc_fortran.patch", when="@:0.3.14%intel@16.0:")
    patch("openblas_icc_fortran2.patch", when="@:0.3.14%intel@18.0:")
    # See https://github.com/spack/spack/issues/15385
    patch("lapack-0.3.9-xerbl.patch", when="@0.3.8:0.3.9 %intel")

    # Fixes compilation error on POWER8 with GCC 7
    # https://github.com/OpenMathLib/OpenBLAS/pull/1098
    patch("power8.patch", when="@0.2.18:0.2.19 %gcc@7.1.0: target=power8")

    # Change file comments to work around clang 3.9 assembler bug
    # https://github.com/OpenMathLib/OpenBLAS/pull/982
    patch("openblas0.2.19.diff", when="@0.2.19")

    # Fix CMake export symbol error
    # https://github.com/OpenMathLib/OpenBLAS/pull/1703
    patch("openblas-0.3.2-cmake.patch", when="@0.3.1:0.3.2")

    # Disable experimental TLS code that lead to many threading issues
    # https://github.com/OpenMathLib/OpenBLAS/issues/1735#issuecomment-422954465
    # https://github.com/OpenMathLib/OpenBLAS/issues/1761#issuecomment-421039174
    # https://github.com/OpenMathLib/OpenBLAS/pull/1765
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/4d183e5567346f80f2ef97eb98f8601c47f8cb56.patch?full_index=1",
        sha256="9b02860bd78252ed9f09abb65a62fff22c0aeca002757d503f5b643a11b744bf",
        when="@0.3.3",
    )

    # Fix parallel build issues on filesystems
    # with missing sub-second timestamp resolution
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/79ea839b635d1fd84b6ce8a47e086f01d64198e6.patch?full_index=1",
        sha256="1cbadd897d037e6015384aaad70efe0d9eac4382482ee01e3fbe89cde2a1ebea",
        when="@0.3.0:0.3.3",
    )

    # Fix https://github.com/OpenMathLib/OpenBLAS/issues/2431
    # Patch derived from https://github.com/OpenMathLib/OpenBLAS/pull/2424
    patch("openblas-0.3.8-darwin.patch", when="@0.3.8 platform=darwin")
    # Fix ICE in LLVM 9.0.0 https://github.com/OpenMathLib/OpenBLAS/pull/2329
    # Patch as in https://github.com/OpenMathLib/OpenBLAS/pull/2597
    patch("openblas_appleclang11.patch", when="@0.3.8:0.3.9 %apple-clang@11.0.3")
    # There was an error in Reference-LAPACK that is triggeret by Xcode12
    # fixed upstream by https://github.com/OpenMathLib/OpenBLAS/pull/2808 and
    # should be included in post 0.3.10 versions. Application to earlier
    # versions was not tested.
    # See also https://github.com/OpenMathLib/OpenBLAS/issues/2870
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/f42e84d46c52f4ee1e05af8f365cd85de8a77b95.patch?full_index=1",
        sha256="d38396ed602c3b655ad8cfc3d70b72726c567643578bf65466527f3a57bbd495",
        when="@0.3.8:0.3.10 %apple-clang@12.0.0:",
    )

    # Add conditions to f_check to determine the Fujitsu compiler
    # See https://github.com/OpenMathLib/OpenBLAS/pull/3010
    # UPD: the patch has been merged starting version 0.3.13
    patch("openblas_fujitsu.patch", when="@:0.3.10 %fj")
    patch("openblas_fujitsu_v0.3.11.patch", when="@0.3.11:0.3.12 %fj")
    patch("openblas_fujitsu2.patch", when="@0.3.10:0.3.12 %fj")

    # Use /usr/bin/env perl in build scripts
    patch("0001-use-usr-bin-env-perl.patch", when="@:0.3.13")

    # Declare external functions in linktest
    # See <https://github.com/OpenMathLib/OpenBLAS/issues/3760>
    patch("linktest.patch", when="@0.3.20")

    # Fix build on ARM Neoverse N1 when using gcc@:9. The 1st patch is context for the 2nd patch:
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/68277282df4adaafaf9b4a01c2eeb629eed99528.patch?full_index=1",
        sha256="a4c642fbaeafbf4178558368212594e99c74a7b6c2a119fd0627f7b54f1ebfb3",
        when="@0.3.21 %gcc@:9",
    )
    # gcc@:9 doesn't support sve2 and bf16 architecture features, apply upstream fix:
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/c957ad684ed6b8ca64f332221b376f2ad0fdc51a.patch?full_index=1",
        sha256="c20f5188a9145395c37c22ae5c1f72bfc24edfbccbb636cc8f9227345615daa8",
        when="@0.3.21 %gcc@:9",
    )

    # Some installations of clang and libomp have non-standard locations for
    # libomp. OpenBLAS adds the correct linker flags but overwrites the
    # variables in a couple places, causing link-time failures.
    patch("openblas_append_lflags.patch", when="@:0.3.23 threads=openmp")

    # Some builds of libomp on certain systems cause test failures related to
    # forking, so disable the specific test that's failing. This is currently
    # an open issue upstream:
    # https://github.com/llvm/llvm-project/issues/63908
    patch("openblas_libomp_fork.patch", when="%clang@15:")

    # Fix build on A64FX for OpenBLAS v0.3.24
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/90231bfc4e4afc51f67c248328fbef0cecdbd2c2.patch?full_index=1",
        sha256="139e314f3408dc5c080d28887471f382e829d1bd06c8655eb72593e4e7b921cc",
        when="@0.3.24 target=a64fx",
    )

    # Disable -fp-model=fast default on OneAPI (https://github.com/OpenMathLib/OpenBLAS/issues/4713)
    patch(
        "https://github.com/OpenMathLib/OpenBLAS/commit/834e633d796ba94ecb892acb32b6cdcee4e3771d.patch?full_index=1",
        sha256="3e165d8cba4023cb2082b241eee41287dd6cbb66078c5e3cb5d246081b361ff3",
        when="@0.3.27 %oneapi",
    )

    # See https://github.com/spack/spack/issues/19932#issuecomment-733452619
    # Notice: fixed on Amazon Linux GCC 7.3.1 (which is an unofficial version
    # as GCC only has major.minor releases. But the bound :7.3.0 doesn't hurt)
    conflicts("%gcc@7:7.3.0,8:8.2", when="@0.3.11:")

    # See https://github.com/OpenMathLib/OpenBLAS/issues/3074
    conflicts("%gcc@:10.1", when="@0.3.13 target=ppc64le:")

    # See https://github.com/spack/spack/issues/3036
    conflicts("%intel@16", when="@0.2.15:0.2.19")

    conflicts(
        "+consistent_fpcsr",
        when="threads=none",
        msg="FPCSR consistency only applies to multithreading",
    )

    conflicts("threads=pthreads", when="~locking", msg="Pthread support requires +locking")
    conflicts("threads=openmp", when="%apple-clang", msg="Apple's clang does not support OpenMP")
    conflicts(
        "threads=openmp @:0.2.19",
        when="%clang",
        msg="OpenBLAS @:0.2.19 does not support OpenMP with clang!",
    )
    # See https://github.com/OpenMathLib/OpenBLAS/issues/2826#issuecomment-688399162
    conflicts(
        "+dynamic_dispatch",
        when="platform=windows",
        msg="Visual Studio does not support OpenBLAS dynamic dispatch features",
    )

    conflicts("target=x86_64_v4:", when="%intel@2021")

    build_system("makefile", "cmake", default="makefile")

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cflags":
            if spec.satisfies("@0.3.20: %oneapi") or spec.satisfies("@0.3.20: %arm"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    @classmethod
    def determine_version(cls, lib):
        ver = None
        for ext in library_extensions:
            match = re.search(r"lib(\S*?)-r(\d+\.\d+\.\d+)\.%s" % ext, lib)
            if match:
                ver = match.group(2)
        return ver

    @property
    def parallel(self):
        # unclear whether setting `-j N` externally was supported before 0.3
        return self.spec.version >= Version("0.3.0")

    @run_before("edit")
    def check_compilers(self):
        # As of 06/2016 there is no mechanism to specify that packages which
        # depends on Blas/Lapack need C or/and Fortran symbols. For now
        # require both.
        # As of 08/2022 (0.3.21), we can build purely with a C compiler using
        # a f2c translated LAPACK version
        #   https://github.com/xianyi/OpenBLAS/releases/tag/v0.3.21
        if self.compiler.fc is None and "~fortran" not in self.spec:
            raise InstallError(
                self.compiler.cc
                + " has no Fortran compiler added in spack. Add it or use openblas~fortran!"
            )

    @property
    def headers(self):
        # The only public headers for cblas and lapacke in
        # openblas are cblas.h and lapacke.h. The remaining headers are private
        # headers either included in one of these two headers, or included in
        # one of the source files implementing functions declared in these
        # headers.
        return find_headers(["cblas", "lapacke"], self.prefix.include)

    @property
    def libs(self):
        spec = self.spec

        # Look for openblas{symbol_suffix}
        name = ["libopenblas", "openblas"]
        search_shared = bool(spec.variants["shared"].value)
        suffix = spec.variants["symbol_suffix"].value
        if suffix != "none":
            name = [x + suffix for x in name]

        return find_libraries(name, spec.prefix, shared=search_shared, recursive=True)


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    @staticmethod
    def _read_targets(target_file):
        """Parse a list of available targets from the OpenBLAS/TargetList.txt
        file.
        """
        micros = []
        re_target = re.compile(r"^[A-Z0-9_]+$")
        for line in target_file:
            match = re_target.match(line)
            if match is not None:
                micros.append(line.strip().lower())

        return micros

    def _microarch_target_args(self):
        """Given a spack microarchitecture and a list of targets found in
        OpenBLAS' TargetList.txt, determine the best command-line arguments.
        """
        # Read available openblas targets
        targetlist_name = join_path(self.stage.source_path, "TargetList.txt")
        if os.path.exists(targetlist_name):
            with open(targetlist_name) as f:
                available_targets = self._read_targets(f)
        else:
            available_targets = []

        # Get our build microarchitecture
        microarch = self.spec.target

        # We need to detect whether the target supports SVE before the magic for
        # loop below which would change the value of `microarch`.
        has_sve = (
            self.spec.satisfies("@0.3.19:")
            and microarch.family == "aarch64"
            and "sve" in microarch
            # Exclude A64FX, which has its own special handling in OpenBLAS.
            and microarch.name != "a64fx"
        )

        # List of arguments returned by this function
        args = []

        # List of available architectures, and possible aliases
        openblas_arch = set(
            ["alpha", "arm", "ia64", "mips", "mips64", "power", "riscv64", "sparc", "zarch"]
        )
        openblas_arch_map = {
            "amd64": "x86_64",
            "powerpc64": "power",
            "i386": "x86",
            "aarch64": "arm64",
        }
        openblas_arch.update(openblas_arch_map.keys())
        openblas_arch.update(openblas_arch_map.values())

        # Add spack-only microarchitectures to list
        skylake = set(["skylake", "skylake_avx512"])
        available_targets = set(available_targets) | skylake | openblas_arch

        # Find closest ancestor that is known to build in blas
        if microarch.name not in available_targets:
            for microarch in microarch.ancestors:
                if microarch.name in available_targets:
                    break

        if self.spec.version >= Version("0.3"):
            # 'ARCH' argument causes build errors in older OpenBLAS
            # see https://github.com/spack/spack/issues/15385
            arch_name = microarch.family.name
            if arch_name in openblas_arch:
                # Apply possible spack->openblas arch name mapping
                arch_name = openblas_arch_map.get(arch_name, arch_name)
                args.append("ARCH=" + arch_name)

        if has_sve:
            # Check this before testing the value of `microarch`, which may have
            # been altered by the magic for loop above.  If SVE is available
            # (but target isn't A64FX which is treated specially below), use the
            # `ARMV8SVE` OpenBLAS target.
            args.append("TARGET=ARMV8SVE")

        elif microarch.vendor == "generic" and microarch.name != "riscv64":
            # User requested a generic platform, or we couldn't find a good
            # match for the requested one. Allow OpenBLAS to determine
            # an optimized kernel at run time, including older CPUs, while
            # forcing it not to add flags for the current host compiler.
            args.append("DYNAMIC_ARCH=1")
            if self.spec.version >= Version("0.3.12"):
                # These are necessary to prevent OpenBLAS from targeting the
                # host architecture on newer version of OpenBLAS, but they
                # cause build errors on 0.3.5 .
                args.extend(["DYNAMIC_OLDER=1", "TARGET=GENERIC"])

        elif microarch.name in skylake:
            # Special case for renaming skylake family
            args.append("TARGET=SKYLAKEX")
            if microarch.name == "skylake":
                # Special case for disabling avx512 instructions
                args.append("NO_AVX512=1")

        elif microarch.name == "riscv64":
            # Special case for renaming the generic riscv64 uarch to the
            # corresponding OpenBLAS target. riscv64 does not yet support
            # DYNAMIC_ARCH or TARGET=GENERIC. Once it does, this special
            # case can go away.
            args.append("TARGET=" + "RISCV64_GENERIC")

        elif self.spec.satisfies("@0.3.19: target=a64fx"):
            # Special case for Fujitsu's A64FX
            if any(self.spec.satisfies(i) for i in ["%gcc@11:", "%clang", "%fj"]):
                args.append("TARGET=A64FX")
            else:
                # fallback to armv8-a+sve without -mtune=a64fx flag
                args.append("TARGET=ARMV8SVE")

        else:
            args.append("TARGET=" + microarch.name.upper())

        return args

    def setup_build_environment(self, env):
        # When building OpenBLAS with threads=openmp, `make all`
        # runs tests, so we set the max number of threads at runtime
        # accordingly
        if self.spec.satisfies("threads=openmp"):
            env.set("OMP_NUM_THREADS", str(make_jobs))
        elif self.spec.satisfies("threads=pthreads"):
            env.set("OPENBLAS_NUM_THREADS", str(make_jobs))

    @property
    def make_defs(self):
        # Configure fails to pick up fortran from FC=/abs/path/to/fc, but
        # works fine with FC=/abs/path/to/gfortran.
        # When mixing compilers make sure that
        # $SPACK_ROOT/lib/spack/env/<compiler> have symlinks with reasonable
        # names and hack them inside lib/spack/spack/compilers/<compiler>.py
        make_defs = ["CC={0}".format(spack_cc)]
        if "~fortran" not in self.spec:
            make_defs += ["FC={0}".format(spack_fc)]

        # force OpenBLAS to use externally defined parallel build
        if self.spec.version < Version("0.3"):
            make_defs.append("MAKE_NO_J=1")  # flag defined by our make.patch
        else:
            make_defs.append("MAKE_NB_JOBS=0")  # flag provided by OpenBLAS

        # Add target and architecture flags
        make_defs += self._microarch_target_args()

        if self.spec.satisfies("+dynamic_dispatch"):
            make_defs += ["DYNAMIC_ARCH=1"]

        # Fortran-free compilation
        if "~fortran" in self.spec:
            make_defs += ["NOFORTRAN=1"]

        if "~shared" in self.spec:
            if "+pic" in self.spec:
                make_defs.append("CFLAGS={0}".format(self.pkg.compiler.cc_pic_flag))
                if "~fortran" not in self.spec:
                    make_defs.append("FFLAGS={0}".format(self.pkg.compiler.f77_pic_flag))
            make_defs += ["NO_SHARED=1"]
        # fix missing _dggsvd_ and _sggsvd_
        if self.spec.satisfies("@0.2.16"):
            make_defs += ["BUILD_LAPACK_DEPRECATED=1"]

        # serial, but still thread-safe version
        if self.spec.satisfies("@0.3.7:"):
            if "+locking" in self.spec:
                make_defs += ["USE_LOCKING=1"]
            else:
                make_defs += ["USE_LOCKING=0"]

        # Add support for multithreading
        if self.spec.satisfies("threads=openmp"):
            make_defs += ["USE_OPENMP=1", "USE_THREAD=1"]
        elif self.spec.satisfies("threads=pthreads"):
            make_defs += ["USE_OPENMP=0", "USE_THREAD=1"]
        else:
            make_defs += ["USE_OPENMP=0", "USE_THREAD=0"]

        # 64bit ints
        if "+ilp64" in self.spec:
            make_defs += ["INTERFACE64=1"]

        suffix = self.spec.variants["symbol_suffix"].value
        if suffix != "none":
            make_defs += ["SYMBOLSUFFIX={0}".format(suffix)]

        # Synchronize floating-point control and status register (FPCSR)
        # between threads (x86/x86_64 only).
        if "+consistent_fpcsr" in self.spec:
            make_defs += ["CONSISTENT_FPCSR=1"]

        # Flang/f18 does not provide ETIME as an intrinsic.
        # Do not set TIMER variable if fortran is disabled.
        if self.spec.satisfies("+fortran%clang"):
            make_defs.append("TIMER=INT_CPU_TIME")

        # Prevent errors in `as` assembler from newer instructions
        if self.spec.satisfies("%gcc@:4.8.4"):
            make_defs.append("NO_AVX2=1")

        # Fujitsu Compiler dose not add  Fortran runtime in rpath.
        if self.spec.satisfies("%fj"):
            make_defs.append("LDFLAGS=-lfj90i -lfj90f -lfjsrcinfo -lelf")

        # Newer versions of openblas will try to find ranlib in the compiler's
        # prefix, for instance, .../lib/spack/env/gcc/ranlib, which will fail.
        if self.spec.satisfies("@0.3.13:"):
            make_defs.append("RANLIB=ranlib")

        if self.spec.satisfies("+bignuma"):
            make_defs.append("BIGNUMA=1")

        if not self.spec.satisfies("target=x86_64_v4:"):
            make_defs.append("NO_AVX512=1")

        # Avoid that NUM_THREADS gets initialized with the host's number of CPUs.
        if self.spec.satisfies("threads=openmp") or self.spec.satisfies("threads=pthreads"):
            make_defs.append("NUM_THREADS=512")

        return make_defs

    @property
    def build_targets(self):
        return ["-s"] + self.make_defs + ["all"]

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make("tests", *self.make_defs, parallel=False)

    @property
    def install_targets(self):
        make_args = ["install", "PREFIX={0}".format(self.prefix)]
        return make_args + self.make_defs

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        spec = self.spec
        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small
        # test.
        source_file = join_path(os.path.dirname(self.pkg.module.__file__), "test_cblas_dgemm.c")
        blessed_file = join_path(
            os.path.dirname(self.pkg.module.__file__), "test_cblas_dgemm.output"
        )

        include_flags = spec["openblas"].headers.cpp_flags
        link_flags = spec["openblas"].libs.ld_flags
        if self.pkg.compiler.name == "intel":
            link_flags += " -lifcore"
        if self.spec.satisfies("threads=pthreads"):
            link_flags += " -lpthread"
        if spec.satisfies("threads=openmp"):
            link_flags += " -lpthread " + self.pkg.compiler.openmp_flag

        output = compile_c_and_execute(source_file, [include_flags], link_flags.split())
        compare_output_file(output, blessed_file)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        cmake_defs = [
            self.define("TARGET", "GENERIC"),
            # ensure MACOSX_RPATH is set
            self.define("CMAKE_POLICY_DEFAULT_CMP0042", "NEW"),
        ]

        if self.spec.satisfies("+dynamic_dispatch"):
            cmake_defs += [self.define("DYNAMIC_ARCH", "ON")]
        if self.spec.satisfies("platform=windows"):
            cmake_defs += [
                self.define("DYNAMIC_ARCH", "OFF"),
                self.define("BUILD_WITHOUT_LAPACK", "ON"),
            ]

        if "~fortran" in self.spec:
            cmake_defs += [self.define("NOFORTRAN", "ON")]

        if "+shared" in self.spec:
            cmake_defs += [self.define("BUILD_SHARED_LIBS", "ON")]

        if self.spec.satisfies("threads=openmp"):
            cmake_defs += [self.define("USE_OPENMP", "ON"), self.define("USE_THREAD", "ON")]
        elif self.spec.satisfies("threads=pthreads"):
            cmake_defs += [self.define("USE_OPENMP", "OFF"), self.define("USE_THREAD", "ON")]
        else:
            cmake_defs += [self.define("USE_OPENMP", "OFF"), self.define("USE_THREAD", "OFF")]

        return cmake_defs
