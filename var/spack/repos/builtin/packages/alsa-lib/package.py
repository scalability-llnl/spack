# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AlsaLib(AutotoolsPackage):
    """The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
    functionality to the Linux operating system. alsa-lib contains the user
    space library that developers compile ALSA applications against."""

    homepage = "https://www.alsa-project.org"
    url = "ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.2.3.2.tar.bz2"

    license("LGPL-2.1-or-later")

    version("1.2.3.2", sha256="e81fc5b7afcaee8c9fd7f64a1e3043e88d62e9ad2c4cff55f578df6b0a9abe15")
    version("1.2.2", sha256="d8e853d8805574777bbe40937812ad1419c9ea7210e176f0def3e6ed255ab3ec")
    version("1.1.4.1", sha256="91bb870c14d1c7c269213285eeed874fa3d28112077db061a3af8010d0885b76")

    depends_on("c", type="build")  # generated

    variant("python", default=False, description="enable python")

    patch("python.patch", when="@1.1.4:1.1.5 +python")

    depends_on("python", type=("link", "run"), when="+python")

    conflicts("platform=darwin", msg="ALSA only works for Linux")

    def configure_args(self):
        spec = self.spec
        args = []
        if spec.satisfies("+python"):
            args.append(f"--with-pythonlibs={spec['python'].libs.ld_flags}")
            args.append(f"--with-pythonincludes={spec['python'].headers.include_flags}")
        else:
            args.append("--disable-python")
        return args
