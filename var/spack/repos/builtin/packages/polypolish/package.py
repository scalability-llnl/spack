# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Polypolish(Package):
    """Polypolish is a tool for polishing genome assemblies with short reads.
    Unlike other tools in this category, Polypolish uses SAM files where each
    read has been aligned to all possible locations (not just a single best
    location). This allows it to repair errors in repeat regions that other
    alignment-based polishers cannot fix."""

    homepage = "https://github.com/rrwick/Polypolish"
    url = "https://github.com/rrwick/Polypolish/archive/refs/tags/v0.5.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.5.0", sha256="183156093c03094290951f140010b3aef6222a672bf538e9136914178775fb1f")

    depends_on("rust")
    depends_on("python@3.6:", type="run")
    depends_on("bwa", type="run")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
        install("scripts/polypolish_insert_filter.py", prefix.bin)
