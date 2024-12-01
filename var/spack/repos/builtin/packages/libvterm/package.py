# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libvterm(MakefilePackage):
    """An abstract library implementation of a terminal emulator"""

    homepage = "http://www.leonerd.org.uk/code/libvterm/"

    license("MIT")

    maintainers("fthaler")

    version("0.3.3", sha256="09156f43dd2128bd347cbeebe50d9a571d32c64e0cf18d211197946aff7226e0")
    version("0.3.1", sha256="25a8ad9c15485368dfd0a8a9dca1aec8fea5c27da3fa74ec518d5d3787f0c397")
    version("0.3", sha256="61eb0d6628c52bdf02900dfd4468aa86a1a7125228bab8a67328981887483358")
    version("0.2", sha256="4c5150655438cfb8c57e7bd133041140857eb04defd0e544521c0e469258e105")
    version("0.1.4", sha256="bc70349e95559c667672fc8c55b9527d9db9ada0fb80a3beda533418d782d3dd")
    version("0.1.3", sha256="e41724466a4658e0f095e8fc5aeae26026c0726dce98ee71d6920d06f7d78e2b")

    depends_on("c", type="build")  # generated

    depends_on("libtool", type="build")

    def url_for_version(self, version):
        url = "https://launchpad.net/libvterm/trunk/v{0}/+download/libvterm-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        env.set("LIBTOOL", self.spec["libtool"].prefix.bin.join("libtool"))

    def build(self, spec, prefix):
        make("PREFIX=" + prefix)

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
