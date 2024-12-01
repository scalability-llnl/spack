# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trimgalore(Package):
    """Trim Galore! is a wrapper around Cutadapt and FastQC to consistently
    apply adapter and quality trimming to FastQ files, with extra
    functionality for RRBS data."""

    homepage = "https://github.com/FelixKrueger/TrimGalore"
    url = "https://github.com/FelixKrueger/TrimGalore/archive/0.4.4.tar.gz"

    license("GPL-3.0-or-later")

    version("0.6.10", sha256="3a4e414fc658d6eb4356f1572351204e8475a9d7dc79f6798270b57d35bda017")
    version("0.6.9", sha256="d50ce6106f979c316c89c7e7bcb44e5f841935d88bc4f756ccf0bc4cbab4e6f5")
    version("0.6.6", sha256="b8db8ffd131d9d9e7c8532a5a1f1caee656c0c58d3eafd460fee3c39b9fcab5e")
    version("0.6.4", sha256="eb57e18203d8a1dce1397b930a348a9969eebaa758b8a7304d04c22f216cea2d")
    version("0.6.3", sha256="c85104452dbb5cfa8c9307920e804fb53baaad355ce656b111f5243e5eb92db4")
    version("0.6.2", sha256="c50b841bdc294a6cdc6a27fb7bfbed1973541d20a68a4708584b817c58b3f376")
    version("0.6.1", sha256="658578c29d007fe66f9ab49608442be703a6fcf535db06eb82659c7edccb62b0")
    version("0.6.0", sha256="f374dfa4c94e2ad50c63276dda0f341fd95b29cb1d5a0e2ad56e8b0168b758ec")
    version("0.4.5", sha256="a6b97e554944ddc6ecd50e78df486521f17225d415aad84e9911163faafe1f3c")
    version("0.4.4", sha256="485a1357e08eadeb5862bbb796022a25a6ace642c4bc13bbaf453b7dc7cff8e2")

    variant("pigz", default=False, description="Use pigz for compression", when="@0.6.0:")
    variant("igzip", default=False, description="Use igzip for compression", when="@0.6.8:")

    # general dependencies
    depends_on("perl", type=("build", "run"))
    depends_on("py-cutadapt", type=("build", "run"))
    depends_on("fastqc")
    # variant dependencies
    depends_on("pigz", type="run", when="+pigz")
    depends_on("libisal", type="run", when="+igzip")

    def install(self, spec, prefix):
        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "trim_galore")

        mkdirp(prefix.bin)
        install("trim_galore", prefix.bin)
