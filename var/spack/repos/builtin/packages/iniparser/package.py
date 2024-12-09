# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Iniparser(MakefilePackage):
    """This modules offers parsing of ini files from the C level."""

    homepage = "http://ndevilla.free.fr/iniparser/"
    url = "https://github.com/ndevilla/iniparser/archive/v4.1.tar.gz"

    license("MIT")

    version("4.2", sha256="dbcbaf3aedb4f88a9fc0df4b315737ddd10e6c37918e3d89f0ecc475333bde4d")
    version("4.1", sha256="960daa800dd31d70ba1bacf3ea2d22e8ddfc2906534bf328319495966443f3ae")
    version("4.0", sha256="e0bbd664bb3f0d64c21ac2d67a843b1c7a3a9710e96393344d170ab8b33e92ba")
    version("3.2", sha256="4a60b8e29d33d24b458749404e1ff2bcbfedd53ad800757daeed7955599fdce4")
    version("3.1", sha256="73b88632dc16c2839f5d9ac7e6ec7a41415a68e590f75d0580b302af4a5d821d")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        install("src/*.h", prefix.include)
        install("libiniparser.*", prefix.lib)
