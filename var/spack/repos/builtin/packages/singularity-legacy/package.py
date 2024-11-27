# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SingularityLegacy(AutotoolsPackage):
    """Singularity is a container platform focused on supporting 'Mobility of
    Compute'. The software changed the installation method from AutoTools
    to GoLang, so we have two separate package names to support that. The
    legacy package is pre-version 3.0.0
    """

    homepage = "https://sylabs.io/singularity/"
    url = "https://github.com/hpcng/singularity/releases/download/2.5.2/singularity-2.5.2.tar.gz"
    git = "https://github.com/hpcng/singularity.git"

    # Versions before 2.5.2 suffer from a serious security problem.
    # https://nvd.nist.gov/vuln/detail/CVE-2018-12021
    version("2.6-release", branch="vault/2.6-release", deprecated=True)
    version(
        "2.6.1",
        sha256="f38d46a225e8368eb4693137806d2dc96e925a50bdf7f6983662848831041df2",
        deprecated=True,
    )
    version(
        "2.6.0",
        sha256="7c425211a099f6fa6f74037e6e17be58fb5923b0bd11aea745e48ef83c488b49",
        deprecated=True,
    )
    version(
        "2.5.2",
        sha256="eca09dbf4de5e971404a31f24d6c90081aef77075f51be8b3eb15b8715d6805e",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("libarchive", when="@2.5.2:")
    # these are only needed if we're grabbing the unreleased tree
    depends_on("m4", type="build", when="@2.6-release")
    depends_on("autoconf", type="build", when="@2.6-release")
    depends_on("automake", type="build", when="@2.6-release")
    depends_on("libtool", type="build", when="@2.6-release")

    # When installing as root, the copy has to run before chmod runs
    def install(self, spec, prefix):
        make("install", parallel=False)
