# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibgpgError(AutotoolsPackage):
    """Common error values for all GnuPG components."""

    homepage = "https://www.gnupg.org/related_software/libgpg-error/index.en.html"
    url = "https://gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.37.tar.bz2"

    maintainers("alalazo")

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("1.50", sha256="69405349e0a633e444a28c5b35ce8f14484684518a508dc48a089992fe93e20a")
    version("1.49", sha256="8b79d54639dbf4abc08b5406fb2f37e669a2dec091dd024fb87dd367131c63a9")
    version("1.48", sha256="89ce1ae893e122924b858de84dc4f67aae29ffa610ebf668d5aa539045663d6f")
    version("1.47", sha256="9e3c670966b96ecc746c28c2c419541e3bcb787d1a73930f5e5f5e1bcbbb9bdb")
    version("1.46", sha256="b7e11a64246bbe5ef37748de43b245abd72cfcd53c9ae5e7fc5ca59f1c81268d")
    version("1.45", sha256="570f8ee4fb4bff7b7495cff920c275002aea2147e9a1d220c068213267f80a26")
    version("1.44", sha256="8e3d2da7a8b9a104dd8e9212ebe8e0daf86aa838cc1314ba6bc4de8f2d8a1ff9")
    version("1.43", sha256="a9ab83ca7acc442a5bd846a75b920285ff79bdb4e3d34aa382be88ed2c3aebaf")
    version("1.42", sha256="fc07e70f6c615f8c4f590a8e37a9b8dd2e2ca1e9408f8e60459c67452b925e23")
    version("1.41", sha256="64b078b45ac3c3003d7e352a5e05318880a5778c42331ce1ef33d1a0d9922742")
    version("1.40", sha256="e6b0392e852a8ad069242265c513c946b492b00816f3967a97d297886939623a")
    version("1.37", sha256="b32d6ff72a73cf79797f7f2d039e95e9c6f92f0c1450215410840ab62aea9763")
    version("1.36", sha256="babd98437208c163175c29453f8681094bcaf92968a15cafb1a276076b33c97c")
    version("1.27", sha256="4f93aac6fecb7da2b92871bb9ee33032be6a87b174f54abf8ddf0911a22d29d2")
    version("1.21", sha256="b7dbdb3cad63a740e9f0c632a1da32d4afdb694ec86c8625c98ea0691713b84d")
    version("1.18", sha256="9ff1d6e61d4cef7c1d0607ceef6d40dc33f3da7a3094170c3718c00153d80810")

    depends_on("c", type="build")  # generated

    depends_on("awk", type="build")
    # Patch for using gawk@5, c.f. https://dev.gnupg.org/T4459
    patch("awk-5.patch", when="@1.36^gawk@5:")
    # See https://github.com/macports/macports-ports/pull/24601 and https://dev.gnupg.org/T7169
    patch(
        "https://raw.githubusercontent.com/ryandesign/macports-ports/290e77cca6ce054768ddefee2b51222d72780ac9/devel/libgpg-error/files/patch-src-spawn-posix.c.diff",
        sha256="0b2a0ffab81b2b0b40d6ab59016c92fcebbe80710a3e0adba570f73f7a931d16",
        level=0,
        when="@1.50",
    )

    def configure_args(self):
        args = [
            "--enable-static",
            "--enable-shared",
            "--enable-tests" if self.run_tests else "--disable-tests",
        ]
        if self.spec.satisfies("@1.46:"):
            args.append("--enable-install-gpg-error-config")
        return args
