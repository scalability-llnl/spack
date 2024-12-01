# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bind9(AutotoolsPackage):
    """
    BIND 9 has evolved to be a very flexible, full-featured DNS system.
    """

    homepage = "https://www.isc.org"
    url = "https://downloads.isc.org/isc/bind9/9.18.28/bind-9.18.28.tar.xz"
    list_url = "https://downloads.isc.org/isc/bind9/"
    git = "https://gitlab.isc.org/isc-projects/bind9"

    license("MPL-2.0", checked_by="wdconinc")

    # Only even minor releases are stable
    version("9.20.0", sha256="cc580998017b51f273964058e8cb3aa5482bc785243dea71e5556ec565a13347")
    version("9.18.28", sha256="e7cce9a165f7b619eefc4832f0a8dc16b005d29e3890aed6008c506ea286a5e7")

    depends_on("pkgconfig", type="build")

    depends_on("libuv@1.34,1.37:", type="link")
    depends_on("openssl@1.1.1:", type="link")
    depends_on("libcap", type="link")
    depends_on("liburcu@0.14:", type="link", when="@9.20:")

    def configure_args(self):
        args = ["--without-python", "--disable-doh"]
        return args
