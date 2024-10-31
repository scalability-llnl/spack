# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralSoftware(CMakePackage):
    """SPIRAL is a program generation system for linear transforms and other
    mathematical functions that produces very high performance code for a wide
    spectrum of hardware platforms."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-software/archive/refs/tags/8.5.1.tar.gz"
    git = "https://github.com/spiral-software/spiral-software.git"

    maintainers("spiralgen")

    license("BSD-2-Clause-FreeBSD")

    version("develop", branch="develop")
    version("master", branch="master")
    version("8.5.1", sha256="845630a69c93c915435100fcb4c800e9f0b181a44bb1debbf8e3a68993ce7797")
    version("8.5.0", sha256="829345b8ca3ab0069a1a6e230f60ab03257060a8f05c021cee022e294eef592d")
    version("8.4.0", sha256="d0c58de65c678130eeee6b8b8b48061bbe463468990f66d9b452225ce46dee19")
    version("8.3.0", sha256="41cf0e7f14f9497e98353baa1ef4ca6204ce5ca525db8093f5bb44e89992abdf")

    depends_on("c", type="build")  # generated

    extendable = True

    # No dependencies.  Spiral pacakges are listed here as variants.  If a
    # variant (i.e., spiral-package) is enabled then spiral-software depends
    # on the package, so dependencies may be added during the install process.

    variant("fftx", default=False, description="Install Spiral package FFTX.")
    variant(
        "simt",
        default=False,
        description="Install Spiral package for Single Instruction, Multiple Threads"
        " (SIMT) to generate code for GPUs.",
    )
    variant(
        "mpi",
        default=False,
        description="Install Spiral package for Message Passing Interface (MPI).",
    )
    variant(
        "jit",
        default=False,
        description="Install Spiral supporting Just-In-Time (aka RTC) Compilation.",
    )
    variant(
        "hcol",
        default=False,
        description="Install Spiral package for the Hybrid Control Operator Language (HCOL).",
    )

    # Dependencies
    for pkg in ["fftx", "simt", "mpi", "jit", "hcol"]:
        depends_on(f"spiral-package-{pkg}", when=f"+{pkg}")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("all")
            make("install")

    def spiral_package_install(self, spec, prefix, pkg):
        pkg_name = "spiral-package-" + pkg
        pkg_prefix = spec[pkg_name].prefix
        dest = join_path(prefix, "namespaces", "packages", pkg)
        src = join_path(pkg_prefix, "namespaces", "packages", pkg)
        install_tree(src, dest)

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("%oneapi"):
            flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            files = ("LICENSE", "README.md", "ReleaseNotes.md", "Contributing.md")
            for fil in files:
                install(fil, prefix)

        mkdirp(prefix.gap.bin)
        mkdirp(prefix.gap.lib)
        mkdirp(prefix.gap.grp)
        mkdirp(prefix.namespaces)
        mkdirp(prefix.profiler)
        mkdirp(prefix.tests)
        mkdirp(prefix.bin)
        mkdirp(prefix.config)

        print("self.stage.source_path = " + self.stage.source_path)
        with working_dir(self.stage.source_path):
            install_tree("namespaces", prefix.namespaces)
            install_tree("profiler", prefix.profiler)
            install_tree("tests", prefix.tests)
            install_tree("bin", prefix.bin)
            install_tree("config", prefix.config)

        with working_dir(join_path(self.stage.source_path, "gap")):
            install_tree("lib", prefix.gap.lib)
            install_tree("grp", prefix.gap.grp)
            install_tree("bin", prefix.gap.bin)

        for pkg in ["fftx", "simt", "mpi", "jit", "hcol"]:
            if f"+{pkg}" in spec:
                self.spiral_package_install(spec, prefix, pkg)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("SPIRAL_HOME", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("SPIRAL_HOME", self.prefix)

    def setup_run_environment(self, env):
        env.set("SPIRAL_HOME", self.prefix)
