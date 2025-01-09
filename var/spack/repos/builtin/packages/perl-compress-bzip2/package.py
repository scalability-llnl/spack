# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCompressBzip2(PerlPackage):
    """Interface to Bzip2 compression library"""

    homepage = "https://metacpan.org/pod/Compress::Bzip2"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Compress-Bzip2-2.28.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.28", sha256="859f835c3f5c998810d8b2a6f9e282ff99d6cb66ccfa55cae7e66dafb035116e")

    depends_on("c", type="build")
    depends_on("bzip2", type=("build", "test", "run"))

    def setup_build_environment(self, env):
        env.set("BZLIB_INCLUDE", self.spec["bzip2"].prefix.include)
        env.set("BZLIB_LIB", self.spec["bzip2"].prefix.lib)
        env.set("BZLIB_BIN", self.spec["bzip2"].prefix.bin)

    def test_use(self):
        """Test 'use module'"""
        options = ["-we", 'use strict; use Compress::Bzip2; print("OK\n")']

        perl = self.spec["perl"].command
        out = perl(*options, output=str.split, error=str.split)
        assert "OK" in out
