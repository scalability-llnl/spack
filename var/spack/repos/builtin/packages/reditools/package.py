# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Reditools(PythonPackage):
    """REDItools: python scripts for RNA editing detection by RNA-Seq data.

    REDItools are simple python scripts conceived to facilitate the
    investigation of RNA editing at large-scale and devoted to research groups
    that would to explore such phenomenon in own data but don't have sufficient
    bioinformatics skills. They work on main operating systems (although
    unix/linux-based OS are preferred), can handle reads from whatever platform
    in the standard BAM format and implement a variety of filters."""

    homepage = "https://github.com/BioinfoUNIBA/REDItools"
    git = "https://github.com/BioinfoUNIBA/REDItools.git"

    license("MIT")

    version("1.3_2020-08-03", commit="2dc71277a25e667797c363d1fca22726249774a3")
    version("1.3_2020-03-20", commit="cf47f3d54f324aeb9650bcf8bfacf5a967762a55")

    variant(
        "nature_protocol",
        default=False,
        description="Install the Nature Protocol scripts and files",
    )

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-reindent", type="build")
    depends_on("blat", type="run")
    depends_on("py-fisher", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pysam", type="run")
    depends_on("py-scipy", type="run")
    depends_on("tabix", type="run")

    # Nature Protocol
    depends_on("bcftools", type="run", when="+nature_protocol")
    depends_on("bedtools2", type="run", when="+nature_protocol")
    depends_on("bwa", type="run", when="+nature_protocol")
    depends_on("bzip2", type="run", when="+nature_protocol")
    depends_on("fastp", type="run", when="+nature_protocol")
    depends_on("fastqc", type="run", when="+nature_protocol")
    depends_on("git", type="run", when="+nature_protocol")
    depends_on("gmap-gsnap", type="run", when="+nature_protocol")
    depends_on("htslib", type="run", when="+nature_protocol")
    depends_on("libdeflate", type="run", when="+nature_protocol")
    depends_on("py-bx-python", type="run", when="+nature_protocol")
    depends_on("py-rseqc", type="run", when="+nature_protocol")
    depends_on("samtools", type="run", when="+nature_protocol")
    depends_on("star", type="run", when="+nature_protocol")
    depends_on("wget", type="run", when="+nature_protocol")

    patch("interpreter.patch")
    patch("setup.py.patch")
    patch("batch_sort.patch", when="^python@3:")

    @run_before("install")
    def p2_to_p3(self):
        if "^python@3:" in self.spec:
            # clean up space/tab mixing
            reindent = which("reindent")
            reindent("--nobackup", "--recurse", ".")

            # convert to be python3 compatible
            p2_to_p3 = which("2to3")
            p2_to_p3("--nobackups", "--write", ".")

    @run_after("install")
    def nature_protocol(self):
        if "+nature_protocol" in self.spec:
            mkdirp(prefix.NPfiles)
            install_tree("NPfiles", prefix.NPfiles)

            ignore_files = [
                "conda_pckg_installer_docker.py",
                "conda_pckgs_installer.py",
                "download-prepare-data-NP_docker.py",
            ]
            docker_conda = lambda p: p in ignore_files
            install_tree("NPscripts", prefix.bin, ignore=docker_conda)
