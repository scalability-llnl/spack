# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fakechroot(AutotoolsPackage):
    """fakechroot runs a command in an environment were is additional
    possibility to use chroot(8) command without root privileges.This
    is useful for allowing users to create own chrooted environment
    with possibility to install another packages without need for root
    privileges."""

    homepage = "https://github.com/dex4er/fakechroot"
    url = "https://github.com/dex4er/fakechroot/releases/download/2.20.1/fakechroot-2.20.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.20.1", sha256="5abd04323c9ddae06b5dcaa56b2da07728de3fe21007b08bd88a17b2409b32aa")
    version("2.20", sha256="5da99358d2a49ddd3dd54ba2ff401d93a8fa641e3754cd058bdf53adb4b7e100")
    version("2.19", sha256="39ffbbbe3a823be7450928b8e3b99ae4cb339c47213b2f1d8ff903e0246f2e15")

    depends_on("c", type="build")  # generated
