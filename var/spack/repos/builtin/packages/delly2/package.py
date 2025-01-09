# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Delly2(MakefilePackage):
    """Delly2 is an integrated structural variant prediction method that can
    discover, genotype and visualize deletions, tandem duplications,
    inversions and translocations at single-nucleotide resolution in
    short-read massively parallel sequencing data.."""

    homepage = "https://github.com/dellytools/delly"
    url = "https://github.com/dellytools/delly/archive/refs/tags/v1.1.6.tar.gz"
    git = "https://github.com/dellytools/delly.git"
    maintainers("snehring")

    license("BSD-3-Clause")

    version("1.2.6", sha256="1a71fcc5f2a55649c2104086f3f7163ed58c5868eaf040a25e45c777b0e1abb7")
    version("1.1.8", sha256="f72a1143dc71449fc277fc8b3e337a4d35b2fe736f3693a14b1986efa8da4889")
    version("1.1.6", sha256="08961e9c81431eb486476fa71eea94941ad24ec1970b71e5a7720623a39bfd2a")
    version("0.9.1", tag="v0.9.1", commit="ef1cd626a85cfd1c1b7acfca2b5fd5957f2a05f1")
    version("2017-08-03", commit="e32a9cd55c7e3df5a6ae4a91f31a0deb354529fc", deprecated=True)

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=False, description="Build with openmp support")

    depends_on("htslib", type=("build", "link"))
    depends_on(
        "boost@:1.78.0+iostreams+filesystem+system+program_options+date_time",
        when="@:0.9.1",
        type=("build", "link"),
    )
    depends_on(
        "boost+iostreams+filesystem+system+program_options+date_time",
        when="@0.9.1:",
        type=("build", "link"),
    )
    depends_on("bcftools", type="run")

    def edit(self, spec, prefix):
        if self.spec.satisfies("+openmp"):
            env["PARALLEL"] = "1"
        # Only want to build delly source, not submodules. Build fails
        # using provided submodules, succeeds with existing spack recipes.
        if self.spec.satisfies("@2017-08-03"):
            makefile = FileFilter("Makefile")
            makefile.filter("HTSLIBSOURCES =", "#HTSLIBSOURCES")
            makefile.filter("BOOSTSOURCES =", "#BOOSTSOURCES")
            makefile.filter("SEQTK_ROOT ?=", "#SEQTK_ROOT")
            makefile.filter("BOOST_ROOT ?=", "#BOOST_ROOT")
            makefile.filter("cd src", "# cd src")
            makefile.filter(".htslib ", "")
            makefile.filter(".bcftools ", "")
            makefile.filter(".boost ", "")
            makefile.filter(".htslib:", "# .htslib:")
            makefile.filter(".bcftools:", "# .bcftools:")
            makefile.filter(".boost:", "# .boost:")
        else:
            env["EBROOTHTSLIB"] = self.spec["htslib"].prefix
            if self.spec.satisfies("@0.9.1"):
                filter_file(
                    "BUILT_PROGRAMS =.*$", "BUILT_PROGRAMS = src/delly src/dpe", "Makefile"
                )
            filter_file("${SUBMODULES}", "", "Makefile", string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("src"):
            install("delly", prefix.bin)
            if self.spec.satisfies("@0.9.1") or self.spec.satisfies("@2017-08-03"):
                install("dpe", prefix.bin)
            if self.spec.satisfies("@2017-08-03"):
                install("cov", prefix.bin)
