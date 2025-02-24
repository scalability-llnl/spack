# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Time(AutotoolsPackage, GNUMirrorPackage):
    """The time command runs another program, then displays
    information about the resources used by that program."""

    homepage = "https://www.gnu.org/software/time/"
    gnu_mirror_path = "time/time-1.9.tar.gz"

    license("GPL-3.0-only")

    version("1.9", sha256="fbacf0c81e62429df3e33bda4cee38756604f18e01d977338e23306a3e3b521e")

    depends_on("c", type="build")  # generated

    build_directory = "spack-build"
