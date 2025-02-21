# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Verdict(CMakePackage):
    """Verdict mesh quality library for evaluating the geometric qualities of regions of space."""

    homepage = "https://github.com/sandialabs/verdict"
    url = "https://github.com/sandialabs/verdict/archive/refs/tags/1.4.2.tar.gz"
    git = "https://github.com/sandialabs/verdict.git"

    maintainers("rblake-llnl")

    license("BSD-3-Clause", checked_by="rblake-llnl")

    version("1.4.2", sha256="225c8c5318f4b02e7215cefa61b5dc3f99e05147ad3fefe6ee5a3ee5b828964b")
    version("1.4.1", sha256="26fa583265cb2ced2e9b30ed26260f6c9f89c3296221d96ccd5e7bfeec219de7")

    variant("doc", default=False, description="install documentation with library")
    variant(
        "mangle",
        default=False,
        description="Mangle verdict names for inclusion in a larger library",
    )
    variant("test", default=False, description="enable testing from cmake")

    depends_on("cxx", type="build")

    depends_on("googletest", type="test", when="+test")

    def cmake_args(self):
        args = [
            self.define_from_variant("VERDICT_BUILD_DOCS", "doc"),
            self.define_from_variant("VERDICT_MANGLE", "mangle"),
            self.define_from_variant("VERDICT_ENABLE_TESTING", "test"),
        ]
        return args
