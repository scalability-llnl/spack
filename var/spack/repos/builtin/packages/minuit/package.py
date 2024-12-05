# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minuit(AutotoolsPackage):
    """MINUIT is a physics analysis tool for function minimization."""

    homepage = "https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/home.html"
    url = "http://www.cern.ch/mathlibs/sw/5_34_14/Minuit2/Minuit2-5.34.14.tar.gz"
    list_url = "https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/release/download.html"

    version("5.34.14", sha256="2ca9a283bbc315064c0a322bc4cb74c7e8fd51f9494f7856e5159d0a0aa8c356")
    version("5.28.00", sha256="c3d380b021f4f8e21cde9b73f7019a2aa94c4fcaf5af3f30151ef5f7bfcb23cb")
    version("5.27.02", sha256="262e2a014f17dd54535b71efc69d1ee6318e6109a57dbe376b416247a031ad5e")
    version("5.24.00", sha256="2e4df8de85eab97484424d1c10128c489948f0dbab4779c36195aa1a42d4b2c2")
    version("5.22.00", sha256="9a64698e8c38a1ac88c98a023f423611f3a157fd9f63bf13671211d3c7a9d7c4")
    version("5.21.06", sha256="4c12b35993c8ecf644043d3d876afb5537a702eb24771f57dbe55d5ea6f49d92")
    version("5.20.00", sha256="c5afbfcf25cb4fb95f773f6611a46ec4f293ad2f3c3a3cd75f79ea5e226f62e4")
    version("5.18.00", sha256="57f0a6079677d45f89ac7d1105bbcb28fe6f22609856f3225c582ff5209ada7e")
    version("5.16.00", sha256="db840e4983de0cea9fa1e861cd3c373c5effd969ad88849b1dd0894f80a02717")
    version("5.14.00", sha256="d38fc8477124b07ebf38fa3fe9f16e7fa070aefe700fce15454b2e749f89db8d")
    version("5.12.00", sha256="c206033a723888a0a079fd0de05027460d99dca1d2b4eeb0ad0e7b60cea86236")
    version("5.10.00", sha256="4f51eb73b0eed527cc2c6f860cc6e2a5d86bb84f37f3c6d8ca469ce6c1ae96c4")
    version("5.08.00", sha256="cf5f2858f40933928738b4d204651dfdfdca8431111bb8b7300b3b43b9b5fa30")
    version("1.7.9", sha256="a7b7fdf89267fe272ae336725c9f4b98e5ccc67ab666e34284a64ec977ee0e07")
    version("1.7.6", sha256="1141e885eec53a0fa859581c160dee522876c65fc7396255ab9a0388622aedd8")
    version("1.7.1", sha256="fe7255974969a7e329dd3ed2b934f502c80a6f74ffb85a311ea56a325cd7ca06")
    version("1.6.3", sha256="17851717cd7e99c705bf3546641572064ef9485653c5741698ff760d34af7271")
    version("1.6.0", sha256="d12259f53ed9957215c3cef11e2d0dce755f627bb3506172f25dcd7ce9950a24")
    version("1.5.2", sha256="b0ed8d7d0071b1e8daa5a5dc4c05d522731617a5430a288b932edc331869c063")
    version("1.5.0", sha256="b5fffdc1d06a2b4ffd6dad5fdd30d127ea354a789aaa9f25f33cf7c539898b7f")

    def url_for_version(self, version):
        if version > Version("5.0.0"):
            url = "http://www.cern.ch/mathlibs/sw/{0}/Minuit2/Minuit2-{1}.tar.gz"
            return url.format(version.underscored, version)
        else:
            url = "http://seal.web.cern.ch/seal/minuit/releases/Minuit-{0}.tar.gz"
            return url.format(version.underscored)

    patch("sprintf.cxx.patch", when="@5.08.00:5.18.00")
    patch("sprintf.patch", when="@:1.7.9")
    patch("LASymMatrix.h.patch", when="@:1.7.6")
