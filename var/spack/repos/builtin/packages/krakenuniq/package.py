# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Krakenuniq(Package):
    """Metagenomics classifier with unique k-mer counting for more specific results."""

    homepage = "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1568-0"
    url = "https://github.com/fbreitwieser/krakenuniq/archive/refs/tags/v0.7.3.tar.gz"

    license("GPL-3.0-only")

    version("1.0.4", sha256="5e2ef21878c1c4ce92be9925e47b9ccae0ecb59a79d71cc4cbb53d057e0de9ec")
    version("0.7.3", sha256="140dccbabec00153c8231ac3c92eb8aecc0277c8947055d4d41abe949ae658c3")
    version("0.7.2", sha256="e6b4c04dbe8276c44fa9e2613cca78429439d75d59e22303094e6577ba333627")
    version("0.7.1", sha256="7f3da1efa1377f8615ad3587c4028fa462e7d802fa3f676b9c4e05d15215fad4")
    version("0.6", sha256="8b058bd36a584ea7318fc19cd858cd55bde7fd4434ef5d37f2da6f28cb5ce036")
    version("0.5.8", sha256="f6363683c826c6d39ac5e43efdc8316328783a9cb4d29995520e9ca6913621ed")
    version("0.5.7", sha256="58a6d615f7d2f30e8a3e3e95b84a1331e8994572b34b46bd32f032407b0b8246")
    version("0.5.6", sha256="57eeab0ed2f408126318533150e4b70028c6e6787c483ba4ed29f1433c6e6e0a")
    version("0.5.5", sha256="645f4387a59638526dededacd5104abc1b325c020d5e4c136b902f1167fc4fd5")
    version("0.5.3", sha256="bc57fd4d5f50363aef640d61b2b111d9bef84a32e9a4eebfb977812cb8dc0250")

    depends_on("cxx", type="build")  # generated

    variant("jellyfish", default=False, description="Install jellyfish v1.1.")

    depends_on("bzip2")
    depends_on("zlib-api")
    depends_on("wget", when="+jellyfish")

    def install(self, spec, prefix):
        local_script = which("./install_krakenuniq.sh")
        if self.spec.satisfies("+jellyfish"):
            local_script("-j", prefix.bin)
        else:
            local_script(prefix.bin)
