# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Redundans(Package):
    """Redundans pipeline assists an assembly of heterozygous genomes."""

    homepage = "https://github.com/Gabaldonlab/redundans"
    url = "https://github.com/Gabaldonlab/redundans/archive/v0.13c.tar.gz"
    git = "https://github.com/Gabaldonlab/redundans.git"

    license("GPL-2.0-or-later")

    version("0.14a", commit="a20215a862aed161cbfc79df9133206156a1e9f0")
    version("0.13c", sha256="26d48f27a32678d94c1d00cb3b8991d74891d6cad64a94569901ff9607a7a736")

    depends_on("python", type=("build", "run"))
    depends_on("py-pyscaf", type=("build", "run"))
    depends_on("py-fastaindex", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("perl", type=("build", "run"))
    depends_on("sspace-standard")
    depends_on("bwa")
    depends_on("last")
    depends_on("gapcloser")
    depends_on("parallel")
    depends_on("snap-berkeley@1.0beta.18:", type=("build", "run"))

    def install(self, spec, prefix):
        sspace_location = join_path(spec["sspace-standard"].prefix, "SSPACE_Standard_v3.0.pl")

        filter_file(
            r"sspacebin = os.path.join(.*)$",
            "sspacebin = '" + sspace_location + "'",
            "redundans.py",
        )

        binfiles = ["redundans.py", "bin/filterReads.py"]

        # new internal dep with 0.14a
        if spec.satisfies("@0.14a:"):
            binfiles.append("bin/denovo.py")

        mkdirp(prefix.bin)
        for f in binfiles:
            install(f, prefix.bin)

        install("bin/fast?2*.py", prefix.bin)
