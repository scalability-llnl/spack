# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SrmIfce(CMakePackage):
    """Client side implementation of the SRMv2 specification."""

    homepage = "https://dmc-docs.web.cern.ch/dmc-docs/srm-ifce.html"
    url = "https://github.com/cern-fts/srm-ifce/archive/refs/tags/v1.24.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("1.24.4", sha256="1a4b937e4ecf04e34106eb4652e18beb3e6fc81ba9c815f6d9b21e07a8a12b1e")

    depends_on("c", type="build")

    depends_on("glib")
    depends_on("gsoap")
    depends_on("cgsi-gsoap")
    depends_on("globus-common")
    depends_on("globus-gsi-cert-utils")
    depends_on("globus-gsi-credential")
    depends_on("globus-gss-assist")
    depends_on("globus-gssapi-gsi")
    depends_on("globus-openssl-module")
    depends_on("openssl")

    def cmake_args(self):
        args = [
            self.define("UNIT_TESTS", self.run_tests),
            self.define("CGSI_GSOAP_LOCATION", self.spec["cgsi-gsoap"].prefix.lib64),
        ]
        return args
