# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Umoci(GoPackage):
    """umoci modifies Open Container images, intending to be a
    complete manipulation tool for OCI images."""

    homepage = "https://umo.ci/"
    url = "https://github.com/opencontainers/umoci/archive/v0.4.4.tar.gz"

    license("Apache-2.0", checked_by="wdconinc")

    version("0.4.7", sha256="c01b36de6fdc513eb65add57bc882d72f94fc3b4b65a8f9ef59826fb754af93e")
    version("0.4.4", sha256="bc5c53812e0076d026aa275b197b878857cf7ba7a4f048fd13433de6107b9aed")
    version("0.4.3", sha256="b7d537fec84d4327b1bbfe27118f69df5591143a74a7a1b66cc9904d85c30226")
    version("0.4.2", sha256="fbc397dd39bda2570155dc3b1be0835809a36fccc342e2545b3edb9f0f9dc6f5")
    version("0.4.1", sha256="0d83e01167383f529d726e9fd455660d4837371d5f0d82fad405f3ae6ae52486")
    version("0.4.0", sha256="66997e270dee8abc9796385b162a1e8e32dd2ee2359e5200af4e6671cc1e76a0")

    depends_on("go-md2man", type="build")

    build_directory = "cmd/umoci"

    @property
    def build_args(self):
        args = super().build_args
        args.extend(
            ["-ldflags", f"-s -w -X github.com/opencontainers/umoci.version={self.version}"]
        )
        return args
