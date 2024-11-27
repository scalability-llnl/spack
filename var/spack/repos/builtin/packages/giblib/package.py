# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Giblib(AutotoolsPackage):
    """Giblib is a simple library which wraps imlib2's context
    API, avoiding all the context_get/set calls, adds
    fontstyles to the truetype renderer and supplies a generic
    doubly-linked list and some string functions."""

    homepage = "https://web.archive.org/web/20071002210842/http://linuxbrit.co.uk/giblib/"
    url = "https://mirror.amdmi3.ru/distfiles/giblib-1.2.4.tar.gz"

    license("MIT")

    version("1.2.4", sha256="176611c4d88d742ea4013991ad54c2f9d2feefbc97a28434c0f48922ebaa8bac")

    depends_on("imlib2")
