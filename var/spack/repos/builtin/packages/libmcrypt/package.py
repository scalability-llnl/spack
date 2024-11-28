# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmcrypt(AutotoolsPackage):
    """Libmcrypt is a thread-safe library providing a uniform
    interface to access several block and stream encryption
    algorithms."""

    homepage = "https://sourceforge.net/projects/mcrypt/files/Libmcrypt/"
    url = "https://sourceforge.net/projects/mcrypt/files/Libmcrypt/2.5.8/libmcrypt-2.5.8.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.5.8", sha256="e4eb6c074bbab168ac47b947c195ff8cef9d51a211cdd18ca9c9ef34d27a373e")

    depends_on("c", type="build")  # generated
