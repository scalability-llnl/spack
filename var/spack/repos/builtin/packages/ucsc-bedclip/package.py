# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UcscBedclip(Package):
    """Remove lines from bed file that refer to off-chromosome locations."""

    homepage = "http://hgdownload.cse.ucsc.edu/admin/exe/"
    url = "http://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v449.src.tgz"
    maintainers("pabloaledo")

    version("377", sha256="932f149c19641064a9cd3f2382cbb54b45a9292b8444792872d531346925d676")
    version("449", sha256="b5a86863d6cfe2120f6c796a13b1572ad05b22622f6534b95c9d26ccbede09b7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libpng")
    depends_on("uuid")
    depends_on("gmake")
    depends_on("mysql-connector-c")
    depends_on("openssl")
    depends_on("zlib-api")

    def setup_build_environment(self, env):
        env.set("MYSQLLIBS", "-lmysqlclient")
        env.set("L", "-lssl")
        env.set("BINDIR", "bin")

    def install(self, spec, prefix):
        with working_dir("kent/src/lib"):
            make()
        with working_dir("kent/src/htslib"):
            make()
        with working_dir("kent/src/jkOwnLib"):
            make()
        with working_dir("kent/src/hg/lib"):
            make()
        with working_dir("kent/src/hg/lib"):
            make()
        with working_dir("kent/src/utils/bedClip"):
            mkdirp("bin")
            mkdirp(prefix.bin)
            make()
            make("install")
            install("bin/bedClip", prefix.bin)
