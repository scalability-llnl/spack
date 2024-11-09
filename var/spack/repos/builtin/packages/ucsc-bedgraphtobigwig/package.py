# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UcscBedgraphtobigwig(Package):
    """Convert a bedGraph file to bigWig format."""

    homepage = "http://hgdownload.cse.ucsc.edu/admin/exe/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v445.src.tgz"
    maintainers("pabloaledo")

    version("449", sha256="b5a86863d6cfe2120f6c796a13b1572ad05b22622f6534b95c9d26ccbede09b7")
    version("445", sha256="c7abb5db6a5e16a79aefcee849d2b59dbc71ee112ca1e41fea0afb25229cf56c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libpng")
    depends_on("uuid")
    depends_on("gmake")
    depends_on("openssl")
    depends_on("zlib-api")
    # This package has known issues installing with the latest MySQL because
    # MySQL removed the type my_bool, while mariadb didn't.
    # https://groups.google.com/a/soe.ucsc.edu/g/genome/c/mIT6fe9l99g
    depends_on("mysql-client")
    conflicts("^mysql@8.0.0:")

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
        with working_dir("kent/src/utils/bedGraphToBigWig"):
            mkdirp(prefix.bin)
            mkdirp("bin")
            make()
            make("install")
            install("bin/bedGraphToBigWig", prefix.bin)
