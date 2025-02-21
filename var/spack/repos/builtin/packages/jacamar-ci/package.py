# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class JacamarCi(GoPackage):
    """Jacamar CI is a HPC focused CI/CD driver for the GitLab custom executor."""

    homepage = "https://gitlab.com/ecp-ci/jacamar-ci"
    url = "https://gitlab.com/ecp-ci/jacamar-ci/-/archive/v0.24.0/jacamar-ci-v0.24.0.tar.gz"
    git = "https://gitlab.com/ecp-ci/jacamar-ci.git"

    maintainers("paulbry")

    license("Apache-2.0 OR MIT")

    version("develop", branch="develop")
    version("0.24.2", sha256="d2b8be464b88a92df0ad2ba1e846226b993c4162779432cb8366fb9bca5c40db")
    version("0.24.1", sha256="fe1036fee2e97e38457212bf1246895803eeb6e1a6aa1ecd24eba1d3ea994029")
    version("0.23.0", sha256="796679e13ece5f88dd7d4a4f40a27a87a6f3273085bb07043b258a612a4b43d3")

    conflicts("platform=darwin", msg="Jacamar CI does not support MacOS")

    depends_on("go@1.22.7:", type="build", when="@0.23.0:")
    depends_on("gmake", type="build")
    depends_on("libc", type="link")
    depends_on("libseccomp", type="link")

    executables = ["^jacamar$", "^jacamar-auth$"]
    phases = ["build", "install"]

    def url_for_version(self, version):
        return f"https://gitlab.com/ecp-ci/jacamar-ci/-/archive/v{version}/jacamar-ci-v{version}.tar.gz"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"Version:\s*(\S+)", output)
        return match.group(1) if match else None

    def build(self, spec, prefix):
        make("VERSION={0}".format(spec.version), "build")

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
