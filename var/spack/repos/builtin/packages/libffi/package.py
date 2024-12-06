# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libffi(AutotoolsPackage):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""

    homepage = "https://sourceware.org/libffi/"
    url = "https://github.com/libffi/libffi/releases/download/v3.4.2/libffi-3.4.2.tar.gz"

    license("MIT")

    version("3.4.6", sha256="b0dea9df23c863a7a50e825440f3ebffabd65df1497108e5d437747843895a4e")
    version("3.4.5", sha256="96fff4e589e3b239d888d9aa44b3ff30693c2ba1617f953925a70ddebcc102b2")
    version("3.4.4", sha256="d66c56ad259a82cf2a9dfc408b32bf5da52371500b84745f7fb8b645712df676")
    version("3.4.3", sha256="4416dd92b6ae8fcb5b10421e711c4d3cb31203d77521a77d85d0102311e6c3b8")
    version("3.4.2", sha256="540fb721619a6aba3bdeef7d940d8e9e0e6d2c193595bc243241b77ff9e93620")
    version(
        "3.3",
        url="https://sourceware.org/pub/libffi/libffi-3.3.tar.gz",
        sha256="72fba7922703ddfa7a028d513ac15a85c8d54c8d67f55fa5a4802885dc652056",
    )
    version(
        "3.2.1",
        url="https://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz",
        sha256="d06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("clang-powerpc-3.2.1.patch", when="@3.2.1%clang platform=linux")
    # ref.: https://github.com/libffi/libffi/pull/561
    patch("powerpc-3.3.patch", when="@3.3")
    patch(
        "https://github.com/libffi/libffi/commit/ce077e5565366171aa1b4438749b0922fce887a4.patch?full_index=1",
        sha256="070b1f3aa87f2b56f83aff38afc42157e1692bfaa580276ecdbad2048b818ed7",
        when="@3.4.3:3.4.4",
    )

    @property
    def headers(self):
        # The headers are probably in self.prefix.lib but we search everywhere
        return find_headers("ffi", self.prefix, recursive=True)

    def flag_handler(self, name, flags):
        if name == "cflags":
            if (
                self.spec.satisfies("%oneapi@2023:")
                or self.spec.satisfies("%arm@23.04:")
                or self.spec.satisfies("%clang@16:")
            ):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def configure_args(self):
        args = ["--with-pic"]
        if self.spec.version >= Version("3.3"):
            # Spack adds its own target flags, so tell libffi not to
            # second-guess us
            args.append("--without-gcc-arch")
        # At the moment, build scripts accept 'aarch64-apple-darwin'
        # but not 'arm64-apple-darwin'.
        # See: https://github.com/libffi/libffi/issues/571
        if self.spec.satisfies("platform=darwin target=aarch64:"):
            args.append("--build=aarch64-apple-darwin")
        return args
