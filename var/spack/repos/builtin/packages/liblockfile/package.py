# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblockfile(AutotoolsPackage):
    """NFS-safe locking library"""

    homepage = "https://github.com/miquels/liblockfile"
    url = "https://github.com/miquels/liblockfile/archive/v1.14.tar.gz"

    license("LGPL-2.0-or-later AND GPL-2.0-or-later")

    version("1.14", sha256="be85dba347889d9b65cbd361a611e6b88e044fdca9c98e5139d5fbc9ba37ccc8")

    depends_on("c", type="build")  # generated

    patch("install_as_nonroot.patch")

    def configure_args(self):
        args = ["--enable-shared"]
        return args
