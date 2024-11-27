# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *


class Libsodium(AutotoolsPackage):
    """Sodium is a modern, easy-to-use software library for encryption,
    decryption, signatures, password hashing and more."""

    homepage = "https://download.libsodium.org/doc/"
    url = "https://github.com/jedisct1/libsodium/releases/download/1.0.19-RELEASE/libsodium-1.0.19.tar.gz"
    git = "https://github.com/jedisct1/libsodium.git"

    license("ISC")

    version("master", branch="master")
    version("stable", branch="stable")
    version("next", branch="next", deprecated=True)

    version("1.0.20", sha256="ebb65ef6ca439333c2bb41a0c1990587288da07f6c7fd07cb3a18cc18d30ce19")
    version("1.0.19", sha256="018d79fe0a045cca07331d37bd0cb57b2e838c51bc48fd837a1472e50068bbea")
    version("1.0.18", sha256="6f504490b342a4f8a4c4a02fc9b866cbef8622d5df4e5452b46be121e46636c1")
    version("1.0.17", sha256="0cc3dae33e642cc187b5ceb467e0ad0e1b51dcba577de1190e9ffa17766ac2b1")
    version("1.0.16", sha256="eeadc7e1e1bcef09680fb4837d448fbdf57224978f865ac1c16745868fbd0533")
    version("1.0.15", sha256="fb6a9e879a2f674592e4328c5d9f79f082405ee4bb05cb6e679b90afe9e178f4")
    version("1.0.13", sha256="9c13accb1a9e59ab3affde0e60ef9a2149ed4d6e8f99c93c7a5b97499ee323fd")
    version("1.0.3", sha256="cbcfc63cc90c05d18a20f229a62c7e7054a73731d0aa858c0517152c549b1288")
    version("1.0.2", sha256="961d8f10047f545ae658bcc73b8ab0bf2c312ac945968dd579d87c768e5baa19")
    version("1.0.1", sha256="c3090887a4ef9e2d63af1c1e77f5d5a0656fadb5105ebb9fb66a302210cb3af5")
    version("1.0.0", sha256="ced1fe3d2066953fea94f307a92f8ae41bf0643739a44309cbe43aa881dbc9a5")
    version("0.7.1", sha256="ef46bbb5bac263ef6d3fc00ccc11d4690aea83643412919fe15369b9870280a7")

    depends_on("c", type="build")

    # https://github.com/jedisct1/libsodium/issues/1372
    conflicts("target=aarch64:", when="@1.0.19")

    def patch(self):
        # Necessary on ppc64le / aarch64, because Spack tries to execute these scripts
        # to check if they work (see lib/spack/spack/build_systems/autotools.py).
        try:
            os.chmod("build-aux/config.guess", 0o755)
            os.chmod("build-aux/config.sub", 0o755)
        except OSError:
            # Old versions of libsodium don't have these files.
            tty.debug("Couldn't chmod config.guess or config.sub: file not found")
            pass
