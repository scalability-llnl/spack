# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ripgrep(CargoPackage):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"
    crates_io = "ripgrep"
    git = "https://github.com/BurntSushi/ripgrep.git"

    maintainers = ["AndrewGaspar"]

    version('master', branch='master')
    version('12.1.1', sha256='b955557adc78324dbc2bc663ca85df54b48a579b340876e38dffb39f24882ebf')

    variant(
        "pcre2",
        default=True,
        description="Support for perl-style regex"
    )

    depends_on("pcre2", when="+pcre2")

    variant(
        "simd_accel",
        default=False,
        description="Enable simd acceleration for some dependencies"
    )

    conflicts(
        "+simd_accel", when="^rust@1.0.0:1.999.999",
        msg="The simd_accel feature requires nightly Rust")
    conflicts(
        "+simd_accel", when="^rust@beta",
        msg="The simd_accel feature requires nightly Rust")

    def cargo_features(self):
        features = []
        if "+pcre2" in self.spec:
            features += ["pcre2"]

        if "+simd_accel" in self.spec:
            features += ["simd-accel"]

        return features

    def setup_build_environment(self, env):
        if '+pcre2' in self.spec:
            env.append_flags('PCRE2_SYS_STATIC', '0')
