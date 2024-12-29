# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Umoci(MakefilePackage):
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

    depends_on("go")
    depends_on("go-md2man", type="build")

    def build(self, spec, prefix):
        provider = "github.com"
        project = "opencontainers"
        repo = "umoci"

        mkdirp(join_path(self.stage.source_path, "src", provider, project))

        ln = which("ln")
        ln("-s", self.stage.source_path, join_path("src", provider, project, repo))

        make("GOPATH={0}".format(self.stage.source_path))

    def install(self, spec, prefix):
        make("PREFIX=", "DESTDIR={0}".format(prefix), "install")
