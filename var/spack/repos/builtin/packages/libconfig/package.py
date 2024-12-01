# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libconfig(AutotoolsPackage):
    """C/C++ Configuration File Library"""

    homepage = "https://www.hyperrealm.com/libconfig/"
    url = "https://github.com/hyperrealm/libconfig/archive/v1.5.tar.gz"

    force_autoreconf = True

    license("LGPL-2.1-or-later")

    version("1.7.3", sha256="68757e37c567fd026330c8a8449aa5f9cac08a642f213f2687186b903bd7e94e")
    version("1.7.2", sha256="f67ac44099916ae260a6c9e290a90809e7d782d96cdd462cac656ebc5b685726")
    version("1.7.1", sha256="d288e6ae817f4ef78df43cdb2647f768dc97899ee82fcc41f857e8eb9fd7fbdb")
    version("1.5", sha256="cae5c02361d8a9b2bb26946c64f089d2e5e599972f386203fbc48975c0d885c8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("m4", type=("build"))
    depends_on("autoconf", type=("build"))
    depends_on("automake", type=("build"))
    depends_on("libtool", type=("build"))
    depends_on("texinfo", type="build")
