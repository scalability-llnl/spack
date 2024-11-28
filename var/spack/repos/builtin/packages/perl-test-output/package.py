# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestOutput(PerlPackage):
    """Test::Output - Utilities to test STDOUT and STDERR messages."""

    homepage = "https://github.com/briandfoy/test-output"
    url = "https://github.com/briandfoy/test-output/archive/release-1.033.tar.gz"
    license("Artistic-2.0")

    version("1.034", sha256="cc016f9c89d3a22f461cb88318f53b03645eaec4025d483ae3bd52a166af5f72")
    version("1.033", sha256="35f0a4ef2449fc78886b4c99e1c1d23f432c2fae98538a4489439eb17223bfc2")
    version("1.032", sha256="8b87e16b40199c9d62f07a821e1ff17a2701e42adffb281a649ed631823d5771")
    version("1.031", sha256="1bb5847f26bee90e71b0af2a9d3a5eec4e17a63aacaf18ce5215f350961c5bf7")
    version("1.03", sha256="cac7c9664105764f5845cb48bf7e5b2da806009d33360dab6a615c6dcfe7ca19")
    version("1.02_01", sha256="fd762b929555b93ca7de05bbd02195c09019faf60d63e38cfca3bdf87dfadb56")
    version("1.02", sha256="088a25e5802579e6d3e6669da4228b8897d1372a02998a6bf7435f22688d2e56")
