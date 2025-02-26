# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yarn(Package):
    """Fast, reliable, and secure dependency management."""

    homepage = "https://yarnpkg.com"
    url = "https://github.com/yarnpkg/berry/archive/refs/tags/@yarnpkg/cli/4.6.0.tar.gz"

    maintainers("cosmicexplorer")

    depends_on("node-js@18.12.0:", type="run", when="@4:")
    depends_on("node-js@4.8.0:4.9.1,6.2.2:6.17.1,8:", type="run", when="@1.22.22")
    depends_on("node-js@4.0:", type="run")

    license("BSD-2-Clause")

    version("4.6.0", sha256="c3a318af0deb9d284d7c46bf97a28f9d70b156142dcab8ec985481d5818dc651")
    version("1.22.22", sha256="88268464199d1611fcf73ce9c0a6c4d44c7d5363682720d8506f6508addf36a0")
    version("1.22.4", sha256="bc5316aa110b2f564a71a3d6e235be55b98714660870c5b6b2d2d3f12587fb58")
    version("1.22.2", sha256="de4cff575ae7151f8189bf1d747f026695d768d0563e2860df407ab79c70693d")
    version("1.22.1", sha256="3af905904932078faa8f485d97c928416b30a86dd09dcd76e746a55c7f533b72")
    version("1.22.0", sha256="de8871c4e2822cba80d58c2e72366fb78567ec56e873493c9ca0cca76c60f9a5")
    version("1.21.1", sha256="d1d9f4a0f16f5ed484e814afeb98f39b82d4728c6c8beaafb5abc99c02db6674")

    def url_for_version(self, version):
        if version < Version("2.0.0"):
            return f"https://github.com/yarnpkg/yarn/releases/download/v{version}/yarn-v{version}.tar.gz"
        else:
            return (
                f"https://github.com/yarnpkg/berry/archive/refs/tags/@yarnpkg/cli/{version}.tar.gz"
            )

    def install(self, spec, prefix):
        if spec.version < Version("2.0.0"):
            install_tree(".", prefix)
        else:
            mkdirp(prefix.bin)
            install("packages/yarnpkg-cli/bin/yarn.js", prefix.bin.yarn)
