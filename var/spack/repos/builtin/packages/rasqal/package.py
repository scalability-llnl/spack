# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rasqal(AutotoolsPackage):
    """Rasqal is a free software / Open Source C library that
    handles Resource Description Framework (RDF) query language
    syntaxes, query construction and execution of queries returning
    results as bindings, boolean, RDF graphs/triples or syntaxes."""

    homepage = "http://librdf.org/"
    url      = "http://download.librdf.org/source/rasqal-0.9.33.tar.gz"

    version('0.9.33', sha256='6924c9ac6570bd241a9669f83b467c728a322470bf34f4b2da4f69492ccfd97c')
    version('0.9.32', sha256='eeba03218e3b7dfa033934d523a1a64671a9a0f64eadc38a01e4b43367be2e8f')
    version('0.9.31', sha256='28d743c9f1b0e5b0486ae4a945fa1e021c8495707e7adbfa0e232244b28b7fee')

    depends_on('raptor2')
