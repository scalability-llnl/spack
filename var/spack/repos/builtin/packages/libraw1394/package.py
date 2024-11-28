# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libraw1394(AutotoolsPackage):
    """libbraw1394 provides direct access to the IEEE 1394 bus through the
    Linux 1394 subsystem's raw1394 user space interface."""

    homepage = "https://sourceforge.net/projects/libraw1394/"
    url = "https://sourceforge.net/projects/libraw1394/files/libraw1394/1.2.0/libraw1394-1.2.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.2.0", sha256="1fdcfa4c5a0938705b925d06f17da9be6ec3f8f065040bb7f33082ef3fc63fad")

    depends_on("c", type="build")  # generated
