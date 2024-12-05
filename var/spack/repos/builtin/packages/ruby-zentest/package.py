# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyZentest(RubyPackage):
    """ZenTest provides 4 different tools: zentest, unit_diff, autotest, and
    multiruby."""

    homepage = "https://github.com/seattlerb/zentest"
    url = "https://rubygems.org/downloads/ZenTest-4.12.0.gem"

    # Source code available at https://github.com/seattlerb/zentest
    # but I had trouble getting the Rakefile to build

    version(
        "4.12.0",
        sha256="5301757c3ab29dd2222795c1b076dd348f4d92fe0426e97a13ae56fea47a786e",
        expand=False,
    )

    depends_on("ruby@1.8:2", type=("build", "run"))
