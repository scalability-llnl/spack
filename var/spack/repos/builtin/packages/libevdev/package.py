# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libevdev(AutotoolsPackage):
    """libevdev is a wrapper library for evdev devices. it moves the common
    tasks when dealing with evdev devices into a library and provides a
    library interface to the callers, thus avoiding erroneous ioctls, etc."""

    homepage = "https://cgit.freedesktop.org/libevdev"
    url = "https://github.com/whot/libevdev/archive/libevdev-1.5.4.tar.gz"

    license("MIT")

    version("1.5.4", sha256="11ef3510970c049b0e30985be3149d27b4b36b7cbe14ca678746aac1ca86744d")
    version("1.5.3", sha256="14575ecac843af1f05dd90099a3163086da5b7a888da9d14263036b7b93894eb")
    version("1.5.2", sha256="75780467d76ee93ecaf62cfd0fa6020629231289230548dae04638936af1e1c8")
    version("1.5.1", sha256="a9a789abf2f047d2449f09458bb754a9dd53f550ea537654d59492acad787ce6")
    version("1.5.0", sha256="ae1b64f26f4b6b55d78bf6e8de87eeb8c58e964b1d457ffa8060e4a889dcb31f")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
