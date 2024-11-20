# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gfal2(CMakePackage):
    """Multi-protocol data management library."""

    homepage = "https://dmc-docs.web.cern.ch/dmc-docs/"
    url = "https://github.com/cern-fts/gfal2/archive/refs/tags/v2.23.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("2.23.0", sha256="e3fc9c2ccb2f54b1d0d460545e1b6c581470d2a2968928a8973045089892e509")

    variant("dcap", default=False, description="Enable dcap plugin")
    variant("file", default=False, description="Enable file plugin")
    variant("gridftp", default=False, description="Enable gridftp plugin")
    variant("http", default=False, description="Enable http plugin")
    variant("sftp", default=False, description="Enable sftp plugin")
    variant("sftp", default=False, description="Enable sftp plugin")
    variant("srm", default=False, description="Enable srm plugin")
    variant("xrootd", default=False, description="Enable xrootd plugin")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("glib")
    depends_on("json-c")
    depends_on("openldap")

    depends_on("dcap", when="+dcap")
    depends_on("zlib", when="+file")
    depends_on("davix +thirdparty", when="+http")
    depends_on("cryptopp", when="+http")
    depends_on("libssh2", when="+sftp")
    depends_on("xrootd", when="+xrootd")

    with when("+gridftp"):
        depends_on("globus-common")
        depends_on("globus-ftp-client")
        depends_on("globus-ftp-control")
        depends_on("globus-gass-copy")
        depends_on("globus-gss-assist")
        depends_on("globus-gssapi-gsi")

    with when("+srm"):
        depends_on("globus-common")
        depends_on("globus-gss-assist")
        depends_on("globus-gssapi-gsi")
        depends_on("srm-ifce")

    depends_on("googletest", type="test")

    def patch(self):
        # FindCryptopp.cmake looks in user-specified ${CRYPTOPP_LOCATION}
        # for both library and headers
        filter_file(
            r"find_library\(CRYPTOPP_LIBRARIES",
            "find_library(CRYPTOPP_LIBRARIES PATH_SUFFIXES lib lib64",
            "cmake/modules/FindCryptopp.cmake",
        )
        filter_file(
            r"find_path\(CRYPTOPP_INCLUDE_DIRS",
            "find_path(CRYPTOPP_INCLUDE_DIRS PATH_SUFFIXES include/cryptopp",
            "cmake/modules/FindCryptopp.cmake",
        )

    def cmake_args(self):
        args = [
            self.define("MAIN_CORE", True),
            self.define("MAIN_TRANSFER", True),
            self.define("SKIP_TESTS", not self.run_tests),
            self.define_from_variant("PLUGIN_DCAP", "dcap"),
            self.define_from_variant("PLUGIN_FILE", "file"),
            self.define_from_variant("PLUGIN_GRIDFTP", "gridftp"),
            self.define_from_variant("PLUGIN_HTTP", "http"),
            self.define_from_variant("PLUGIN_SFTP", "sftp"),
            self.define_from_variant("PLUGIN_SRM", "srm"),
            self.define_from_variant("PLUGIN_XROOTD", "xrootd"),
        ]
        if self.spec.satisfies("+http"):
            args.append(self.define("CRYPTOPP_LOCATION", self.spec["cryptopp"].prefix))
        if self.spec.satisfies("+xrootd"):
            args.append(self.define("XROOTD_LOCATION", self.spec["xrootd"].prefix))
        return args
