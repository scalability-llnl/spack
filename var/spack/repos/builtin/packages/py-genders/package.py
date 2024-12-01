# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenders(Package):
    """Genders is a static cluster configuration database used for cluster
    configuration management. It is used by a variety of tools and scripts
    for management of large clusters."""

    homepage = "https://github.com/chaos/genders"
    url = "https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.22",
        sha256="0ff292825a29201106239c4d47d9ce4c6bda3f51c78c0463eb2634ecc337b774",
        url="https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    extends("python")

    # FIXME: Missing a dependency on genders
    # #include <genders.h>
    depends_on("bison", type="build")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make(parallel=False)
        make("install")
