# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

_os_map_before_23 = {
    "ubuntu18.04": "Ubuntu-18.04",
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-20.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rocky8": "RHEL-8",
    "amzn2": "RHEL-7",
    "amzn2023": "RHEL-7",
}

_os_map = {
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-22.04",
    "debian12": "Ubuntu-22.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rhel9": "RHEL-9",
    "rocky8": "RHEL-8",
    "rocky9": "RHEL-9",
    "amzn2": "AmazonLinux-2",
    "amzn2023": "AmazonLinux-2023",
}

_versions = {
    "24.04": {
        "RHEL-7": (
            "064c3ecfd71cba3d8bf639448e899388f58eb7faef4b38f3c1aace625ace8b1e",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "38f46a3549667d0fbccd947653d3a1a56b630d3bbb1251888c674c463f00dac3",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_RHEL-8_aarch64.tar",
        ),
        "RHEL-9": (
            "d335db82c8310e1d79c96dc09a19e4d509c5ab17eb6027214bb79cfc75d8229e",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_RHEL-9_aarch64.tar",
        ),
        "SLES-15": (
            "6f2e090efcd8da2cbeaf63272fac5917f637713f1e86d73cde2ad7268e3a05a2",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_SLES-15_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "0d782e6a69a11f90bf3b392313c885a2376c5761f227bf2f68e34e9848ec8e97",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_Ubuntu-20.04_aarch64.tar",
        ),
        "Ubuntu-22.04": (
            "0bab2e89f0a2359746f89a01251dca763305c5b0dee95cf47b0968dd1cb5f6f6",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_Ubuntu-22.04_aarch64.tar",
        ),
        "AmazonLinux-2": (
            "cf0bebe2d7123749c919a5f4e36100ad21f08ffbad3b53e477205c08ae973a2d",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_AmazonLinux-2_aarch64.tar",
        ),
        "AmazonLinux-2023": (
            "035dae8c41a1ac86c8885837978cb712306aa75dc5d26d17aca843b84eaee9f4",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/24-04/arm-compiler-for-linux_24.04_AmazonLinux-2023_aarch64.tar",
        ),
    },
    "23.10": {
        "RHEL-7": (
            "c3bd4df3e5f6c97369237b0067e0a421dceb9c167d73f22f3da87f5025258314",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "2aea8890a0c0f60bbcc5ddb043d13bd7cd10501218b04cbeb19129449e7d7053",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_RHEL-8_aarch64.tar",
        ),
        "RHEL-9": (
            "6c5c63c701875da7e87c6362be189bcbfaad678c08b81ec91e1e0252a321fae7",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_RHEL-9_aarch64.tar",
        ),
        "SLES-15": (
            "e1e62544210bae495cd2503ef280a748fda637c373f1eb76f5ff30c9ec92c4c1",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_SLES-15_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "83dce8ea03de3b9b937ecfc611961a8e4d15eba4c267a4e47e22a876e403da96",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_Ubuntu-20.04_aarch64.tar",
        ),
        "Ubuntu-22.04": (
            "3354f0ab73856a8a5cd99364cbec7a6b22621701790cb36c3e5f756b363e6d43",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_Ubuntu-22.04_aarch64.tar",
        ),
        "AmazonLinux-2": (
            "ee4fa47246f16323d05d91135ef70a8c355ff60209307754b8532b5744d9cfe9",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_AmazonLinux-2_aarch64.tar",
        ),
        "AmazonLinux-2023": (
            "640487dfc7ab6eca48b448264013c9aa972b84af9f0c6fc8734fa5e8dc008e43",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_AmazonLinux-2023_aarch64.tar",
        ),
    },
    "23.04.1": {
        "RHEL-7": (
            "5e84daaf0510f73c235723112f9241bbd744ed89eb4f70f089bac05cf2aad2c4",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "6ec1f2c7338ea8a2831a7ff353ab44f87804f56716d1f3686576fb950c2f730f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_RHEL-8_aarch64.tar",
        ),
        "RHEL-9": (
            "dbd6493ea762b9b4c6cb54a76ad42e2223360882165ee3c223c1b7d1ebe927e2",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_RHEL-9_aarch64.tar",
        ),
        "SLES-15": (
            "74c29890d47556114922c77e5a9797b055f8fe49f0c8665d17102465fca766b4",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_SLES-15_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "78015ff5a246facfe45219a03a3774221b2f3b58db6fa3d9840d2574d103310c",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_Ubuntu-20.04_aarch64.tar",
        ),
        "Ubuntu-22.04": (
            "19213db67aa11de44b617255e9e32efd294f930c6b6145192acf9ee331452ea6",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_Ubuntu-22.04_aarch64.tar",
        ),
        "AmazonLinux-2": (
            "31ba559302a2889e5f0897f1c07563b20a5a8eaa671e623bef406b6490d1f4f2",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_AmazonLinux-2_aarch64.tar",
        ),
        "AmazonLinux-2023": (
            "fa38f3d79775e9a537c59c8ba39c3b10505e895a3602bbd93c09445170db571f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04-1/arm-compiler-for-linux_23.04.1_AmazonLinux-2023_aarch64.tar",
        ),
    },
    "22.1": {
        "RHEL-7": (
            "367b9a60fa13b5fcf2fa787122c12d4bfb14d6f3e3e7b0460efc7627484a56a4",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "f03ad3381a74df73a4c25baf5f1c15bd466cfd6286498c38b37ddeaa85c9965e",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "8a1c5bd570bd195982c342da8dafb7075f8f6b373b44539d4c810e69e8157c1f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "4628599d389efcee07d0986cc3e791931e6a37eddb6e4b93c7846e17efe2148f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "20d950d16e6bb0b3a4c4f3c8ad393aae2356d4c998303b319da9e9833d4a6d12",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_Ubuntu-20.04_aarch64.tar",
        ),
    },
    "22.0.2": {
        "RHEL-7": (
            "e4dec577ed2d33124a556ba05584fad45a9acf6e13dccadb37b521d1bad5a826",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "3064bec6e0e3d4da9ea2bcdcb4590a8fc1f7e0e97092e24e2245c7f1745ef4f3",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "82dea469dc567b848bcaa6cbaed3eb3faaf45ceb9ec7071bdfef8a383e929ef8",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "355f548e86b9fa90d72684480d13ec60e6bec6b2bd837df42ac84d5a8fdebc48",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "a2a752dce089a34b91dc89c0d1dd8b58a4104bf7c9ba3affd71fd1fd593e3732",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_Ubuntu-20.04_aarch64.tar",
        ),
    },
    "22.0.1": {
        "RHEL-7": (
            "6b0ab76dce3fd44aab1e679baef01367c86f6bbd3544e04f9642b6685482cd76",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "41e5bffc52701b1e8a606f8db09c3c02e35ae39eae0ebeed5fbb41a13e61f057",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "b578ff517dec7fa23c4b7353a1a7c958f28cc9c9447f71f7c4e83de2e2c5538f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "becc6826ce0f6e696092e79a40f758d7cd0302227f6cfc7c2215f6483ade9748",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "dea136238fc2855c41b8a8154bf279b7df5df8dba48d8f29121fa26f343e7cdb",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-20.04_aarch64.tar",
        ),
    },
}


def get_os(ver):
    spack_os = spack.platforms.host().default_os
    if ver.startswith("22."):
        return _os_map_before_23.get(spack_os, "")
    else:
        return _os_map.get(spack_os, "RHEL-7")


def get_armpl_version_to_3(spec):
    """Return version string with 3 numbers"""
    version_len = len(spec.version)
    assert version_len == 2 or version_len == 3
    if version_len == 2:
        return spec.version.string + ".0"
    elif version_len == 3:
        return spec.version.string


def get_armpl_prefix(spec):
    ver = get_armpl_version_to_3(spec)
    os = get_os(spec.version.string)
    if spec.version.string.startswith("22."):
        return join_path(spec.prefix, f"armpl-{ver}_AArch64_{os}_arm-linux-compiler_aarch64-linux")
    else:
        return join_path(spec.prefix, f"armpl-{ver}_{os}_arm-linux-compiler")


def get_acfl_prefix(spec):
    os = get_os(spec.version.string)
    if spec.version.string.startswith("22."):
        return join_path(
            spec.prefix, f"arm-linux-compiler-{spec.version}_Generic-AArch64_{os}_aarch64-linux"
        )
    else:
        return join_path(spec.prefix, f"arm-linux-compiler-{spec.version}_{os}")


def get_armpl_suffix(spec):
    suffix = ""
    if spec.satisfies("@24:"):
        suffix += "_ilp64" if spec.satisfies("+ilp64") else "_lp64"
    else:
        suffix += "_ilp64" if spec.satisfies("+ilp64") else ""
    suffix += "_mp" if spec.satisfies("threads=openmp") else ""
    return suffix


class Acfl(Package, CompilerPackage):
    """Arm Compiler combines the optimized tools and libraries from Arm
    with a modern LLVM-based compiler framework.
    """

    homepage = "https://developer.arm.com/Tools%20and%20Software/Arm%20Compiler%20for%20Linux"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-10/arm-compiler-for-linux_23.10_Ubuntu-22.04_aarch64.tar"

    maintainers("paolotricerri")

    # Build Versions
    for ver, packages in _versions.items():
        acfl_os = get_os(ver)
        pkg = packages.get(acfl_os)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    # Only install for Aarch64
    conflicts("target=x86_64:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    executables = [r"armclang", r"armclang\+\+", r"armflang"]

    variant("ilp64", default=False, description="use ilp64 specific Armpl library")
    variant("shared", default=True, description="enable shared libs")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    provides("blas")
    provides("lapack")
    provides("fftw-api@3")

    # Licensing - Not required from 22.0.1 on.

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        exe = Executable(
            f"./arm-compiler-for-linux_{spec.version}_{get_os(spec.version.string)}.sh"
        )
        exe("--accept", "--force", "--install-to", prefix)

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["armclang"]
    cxx_names = ["armclang++"]
    fortran_names = ["armflang"]

    compiler_version_argument = "--version"
    compiler_version_regex = (
        r"Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) \(build number \d+\) "
    )

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armclang")

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armclang++")

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armflang")

    @property
    def lib_suffix(self):
        return get_armpl_suffix(self.spec)

    @property
    def blas_libs(self):
        armpl_prefix = get_armpl_prefix(self.spec)

        libname = "libarmpl" + self.lib_suffix

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, "libamath", "libastring"],
            root=armpl_prefix,
            shared=self.spec.satisfies("+shared"),
            recursive=True,
        )

        armpl_libs += find_system_libraries(["libm"])

        return armpl_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    @property
    def headers(self):
        armpl_dir = get_armpl_prefix(self.spec)

        if self.spec.satisfies("@24:"):
            suffix = "include"
        else:
            suffix = "include" + self.lib_suffix

        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        arm_dir = get_acfl_prefix(self.spec)
        armpl_dir = get_armpl_prefix(self.spec)

        env.set("ARM_LINUX_COMPILER_DIR", arm_dir)
        env.set("ARM_LINUX_COMPILER_INCLUDES", join_path(arm_dir, "includes"))
        env.append_path("ARM_LINUX_COMPILER_LIBRARIES", join_path(arm_dir, "lib"))
        env.prepend_path("PATH", join_path(arm_dir, "bin"))
        env.prepend_path("CPATH", join_path(arm_dir, "include"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(arm_dir, "lib"))
        env.append_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
        env.prepend_path("LIBRARY_PATH", join_path(arm_dir, "lib"))
        env.prepend_path("MANPATH", join_path(arm_dir, "share", "man"))

    @run_after("install")
    def check_install(self):
        arm_dir = get_acfl_prefix(self.spec)
        armpl_dir = get_armpl_prefix(self.spec)
        suffix = get_armpl_suffix(self.spec)
        armpl_example_dir = join_path(armpl_dir, f"examples{suffix}")
        # run example makefile
        make(
            "-C",
            armpl_example_dir,
            "CC=" + self.cc,
            "F90=" + self.fortran,
            "CPATH=" + join_path(arm_dir, "include"),
            "ARMPL_DIR=" + armpl_dir,
        )
        # clean up
        make("-C", armpl_example_dir, "clean")
