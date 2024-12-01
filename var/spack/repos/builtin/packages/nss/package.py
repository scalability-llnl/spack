# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nss(MakefilePackage):
    """Network Security Services (NSS) is a set of libraries designed to
    support cross-platform development of security-enabled client and server
    applications. Applications built with NSS can support SSL v3, TLS, PKCS #5,
    PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3 certificates, and other
    security standards."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS"
    url = "https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_67_RTM/src/nss-3.67.tar.gz"

    license("MPL-2.0")

    version("3.87", sha256="68a1894496d3d158babc75f8a5dda3f55b7c1560573936e3b101a10fa4ac152d")
    version("3.75", sha256="fd571507827284644f4dd522a032acda2286835f6683ed22a1c2d3878cc58582")
    version("3.73", sha256="566d3a68da9b10d7da9ef84eb4fe182f8f04e20d85c55d1bf360bb2c0096d8e5")
    # Everything before 3.73 is vulnerable (CVE-2021-43527)
    version(
        "3.67",
        sha256="f6549a9148cd27b394b40c77fa73111d5ea23cdb51d796665de1b7458f88ce7f",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("nspr@4.24:")
    depends_on("sqlite")
    depends_on("zlib-api")

    parallel = False

    build_directory = "nss"

    def url_for_version(self, version):
        url = "https://ftp.mozilla.org/pub/security/nss/releases/NSS_{0}_RTM/src/nss-{1}.tar.gz"

        return url.format(version.underscored, version)

    @property
    def build_targets(self):
        # We cannot use nss_build_all because this will try to build nspr.
        targets = ["all", "latest"]

        targets.extend(
            [
                "CCC={}".format(spack_cxx),
                "USE_64=1",
                "BUILD_OPT=1",
                "NSS_USE_SYSTEM_SQLITE=1",
                "NSS_ENABLE_WERROR=0",
                "NSS_DISABLE_GTESTS=1",
            ]
        )

        for var in ("DIST", "SOURCE_PREFIX", "SOURCE_MD_DIR"):
            targets.append("{0}={1}".format(var, join_path(self.stage.source_path, "dist")))

        return targets

    def install(self, spec, prefix):
        install_tree("dist/bin", prefix.bin, symlinks=False)
        install_tree("dist/public/nss", prefix.include.nss, symlinks=False)
        install_tree("dist/lib", prefix.lib, symlinks=False)

    @run_after("install")
    def install_pkgconfig(self):
        pkg_path = join_path(self.prefix.lib, "pkgconfig")
        mkdirp(pkg_path)

        with open(join_path(pkg_path, "nss.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}\n")
            f.write("libdir={0}\n".format(self.prefix.lib))
            f.write("includedir={0}\n".format(self.prefix.include.nss))
            f.write("\n")
            f.write("Name: NSS\n")
            f.write("Description: Network Security Services\n")
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Requires: nspr\n")
            f.write("Cflags: -I${includedir}\n")
            f.write("Libs: -L${libdir} -lssl3 -lsmime3 -lnss3 -lnssutil3\n")
