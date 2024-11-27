# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbytesize(AutotoolsPackage):
    """The goal of this project is to provide a tiny library that would
    facilitate the common operations with sizes in bytes."""

    homepage = "https://github.com/storaged-project/libbytesize"
    url = "https://github.com/storaged-project/libbytesize/releases/download/2.4/libbytesize-2.4.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.4", sha256="25ccb5762bb8c860b63ed1d40e0c5564e3e0084693fbe6554467a8ca1c1d8c7f")
    version("2.3", sha256="3c74113fc8cd1a2fbd8870fa0ed7cef2ef24d60ef91e7145fbc041f9aa144479")
    version("2.2", sha256="b93c54b502880c095c9f5767a42464853e2687db2e5e3084908a615bafe73baa")

    depends_on("c", type="build")  # generated

    extends("python")
    depends_on("pcre2")
    depends_on("gmp")
    depends_on("mpfr")
