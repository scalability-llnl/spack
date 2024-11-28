# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ddt(Package):
    """Arm DDT is the number one debugger in research, industry, and academia
    for software engineers and scientists developing C++, C, Fortran parallel
    and threaded applications on CPUs, GPUs, Intel and Arm. Arm DDT is trusted
    as a powerful tool for automatic detection of memory bugs and divergent
    behavior to achieve lightning-fast performance at all scales."""

    homepage = "https://arm.com"
    url = "https://downloads.linaroforge.com/22.1.3/linaro-forge-22.1.3-linux-x86_64.tar"
    list_url = "https://www.linaroforge.com/download-documentation"

    maintainers("robgics")

    license_required = True
    license_files = ["./licences/ddt.lic"]

    with default_args(deprecated=True):
        # All versions are deprecated; the package linaro-forge is preferred
        version(
            "24.0.3", sha256="1796559fb86220d5e17777215d3820f4b04aba271782276b81601d5065284526"
        )
        version(
            "23.1.2", sha256="675d2d8e4510afefa0405eecb46ac8bf440ff35a5a40d5507dc12d29678a22bf"
        )
        version(
            "23.0.4", sha256="41a81840a273ea9a232efb4f031149867c5eff7a6381d787e18195f1171caac4"
        )
        version(
            "22.1.3", sha256="4f8a8b1df6ad712e89c82eedf4bd85b93b57b3c8d5b37d13480ff058fa8f4467"
        )
        version(
            "22.0.2", sha256="3db0c3993d1db617f850c48d25c9239f06a018c895ea305786a7ad836a44496d"
        )
        # Versions before 22.0 have a security vulnerability. Do not install them.

    def url_for_version(self, version):
        if version <= Version("22.1.3"):
            return (
                f"https://downloads.linaroforge.com/{version}/arm-forge-{version}-linux-x86_64.tar"
            )
        else:
            return f"https://downloads.linaroforge.com/{version}/linaro-forge-{version}-linux-x86_64.tar"

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "bin"))

    def install(self, spec, prefix):
        install_shell = which("sh")
        args = ["./textinstall.sh", "--accept-license", prefix]
        install_shell(*args)
