# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PkgConfig(AutotoolsPackage):
    """pkg-config is a helper tool used when compiling applications
    and libraries"""

    homepage = "https://www.freedesktop.org/wiki/Software/pkg-config/"
    # URL must remain http:// so Spack can bootstrap curl
    url = "https://pkgconfig.freedesktop.org/releases/pkg-config-0.29.2.tar.gz"

    license("GPL-2.0-only")

    version("0.29.2", sha256="6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591")
    version("0.29.1", sha256="beb43c9e064555469bd4390dcfd8030b1536e0aa103f08d7abf7ae8cac0cb001")
    version("0.28", sha256="6b6eb31c6ec4421174578652c7e141fdaae2dabad1021f420d8713206ac1f845")

    depends_on("c", type="build")  # generated

    provides("pkgconfig")

    variant("internal_glib", default=True, description="Builds with internal glib")

    # The following patch is needed for gcc-6.1
    patch("g_date_strftime.patch", when="@:0.29.1")

    # https://github.com/spack/spack/issues/3525
    conflicts("%pgi")

    parallel = False

    tags = ["build-tools"]

    executables = ["^pkg-config$"]

    @classmethod
    def determine_version(cls, exe):
        exe = Executable(exe)

        # Make sure this is actually pkg-config, not pkgconf
        if "usage: pkgconf" in exe("--help", output=str, error=str):
            return None

        version = exe("--version", output=str, error=str).rstrip()

        return version

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        env.append_path("ACLOCAL_PATH", self.prefix.share.aclocal)

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-shared"]

        if spec.satisfies("+internal_glib"):
            # There's a bootstrapping problem here;
            # glib uses pkg-config as well, so break
            # the cycle by using the internal glib.
            config_args.append("--with-internal-glib")

        for strict_compiler in ("%oneapi", "%cce", "%apple-clang@15:", "%clang@15:"):
            if spec.satisfies(strict_compiler):
                config_args.append("CFLAGS=-Wno-error=int-conversion")
                break

        return config_args
