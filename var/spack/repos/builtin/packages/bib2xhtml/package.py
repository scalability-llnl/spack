# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bib2xhtml(Package):
    """bib2xhtml is a program that converts BibTeX files into HTML."""

    homepage = "https://www.spinellis.gr/sw/textproc/bib2xhtml/"
    url = "https://www.spinellis.gr/sw/textproc/bib2xhtml/bib2xhtml-v3.0-79-ge935.tar.gz"

    license("GPL-2.0-only")

    version(
        "3.0-79-ge935", sha256="4a2d2d89dd2f3fed1c735055b806809b5cc1cde32dee1aa5987097ec5bf2181f"
    )

    depends_on("texlive", type="run")

    def install(self, spec, prefix):
        # Add the bst include files to the install directory
        bst_include = join_path(prefix.share, "bib2xhtml")
        mkdirp(bst_include)
        install("html-*bst", bst_include)

        # Install the script and point it at the user's favorite perl
        # and the bst include directory.
        mkdirp(prefix.bin)
        install("bib2xhtml", prefix.bin)
        filter_file(
            r"#!/usr/bin/perl",
            "#!/usr/bin/env BSTINPUTS=%s perl" % bst_include,
            join_path(prefix.bin, "bib2xhtml"),
        )
