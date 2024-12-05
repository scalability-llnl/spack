# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTermreadkey(PerlPackage):
    """Term::ReadKey is a compiled perl module dedicated to providing simple
    control over terminal driver modes (cbreak, raw, cooked, etc.,) support
    for non-blocking reads, if the architecture allows, and some generalized
    handy functions for working with terminals. One of the main goals is to
    have the functions as portable as possible, so you can just plug in
    "use Term::ReadKey" on any architecture and have a good likelihood of it
    working."""

    homepage = "https://metacpan.org/pod/Term::ReadKey"
    url = "https://www.cpan.org/authors/id/J/JS/JSTOWE/TermReadKey-2.37.tar.gz"

    version("2.38", sha256="5a645878dc570ac33661581fbb090ff24ebce17d43ea53fd22e105a856a47290")
    version("2.37", sha256="4a9383cf2e0e0194668fe2bd546e894ffad41d556b41d2f2f577c8db682db241")
