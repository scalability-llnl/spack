# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Atompaw(AutotoolsPackage):
    """A Projector Augmented Wave (PAW) code for generating
    atom-centered functions.

    Official website: http://pwpaw.wfu.edu

    User's guide: ~/doc/atompaw-usersguide.pdf
    """

    homepage = "https://users.wfu.edu/natalie/papers/pwpaw/man.html"
    url = "https://users.wfu.edu/natalie/papers/pwpaw/atompaw-4.0.0.13.tar.gz"

    license("GPL-3.0-only")

    version("4.2.0.3", sha256="9fd4f9b60e793eee10aead4296e89f0bd6e8612b729a15e2401bbd90e4e9dd2d")
    version("4.2.0.2", sha256="c16648611f5798b8e1781fb2229854c54fa63f085bd11440fdc4ecacbf0ad93e")
    version("4.2.0.1", sha256="d3476a5aa5f80f9430b81f28273c2c2a9b6e7d9c3d08c65544247bb76cd5a114")
    version("4.2.0.0", sha256="9ab4f4ab78a720fbcd95bbbc1403e8ff348d15570e7c694932a56be15985e93d")
    version("4.1.1.0", sha256="b1ee2b53720066655d98523ef337e54850cb1e68b3a2da04ff5a1576d3893891")
    version("4.0.0.13", sha256="cbd73f11f3e9cc3ff2e5f3ec87498aeaf439555903d0b95a72f3b0a021902020")
    version("3.1.0.3", sha256="15fe9a0369bdcc366370a0ecaa67e803ae54534b479ad63c4c7494a04fa3ea78")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("lapack")
    depends_on("blas")

    # libxc
    depends_on("libxc")
    depends_on("libxc@:2", when="@:4.0")

    patch("atompaw-4.1.1.0-fix-ifort.patch", when="@4.1.1.0:4.2.0.0")
    patch("atompaw-4.1.1.0-fix-fujitsu.patch", when="@4.1.1.0 %fj")

    parallel = False

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%fj") and name == "fflags":
            opt_flag_found = any(f in self.compiler.opt_flags for f in flags)
            if not opt_flag_found:
                flags.append("-Kfast")
        return (flags, None, None)

    def configure_args(self):
        spec = self.spec
        linalg = spec["lapack"].libs + spec["blas"].libs
        return [
            f"--with-linalg-libs={linalg.ld_flags}",
            "--enable-libxc",
            f"--with-libxc-incs=-I{spec['libxc'].prefix.include}",
            f"--with-libxc-libs=-L{spec['libxc'].prefix.lib} -lxcf90 -lxc",
        ]
