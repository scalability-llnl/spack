# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hama(Package):
    """
    Apache Hama is a framework for Big Data analytics which uses the Bulk
    Synchronous Parallel (BSP) computing model, which was established in
    2012 as a Top-Level Project of The Apache Software Foundation.
    """

    homepage = "https://www-eu.apache.org"
    url = "https://www-eu.apache.org/dist/hama/hama-0.7.1/hama-dist-0.7.1.tar.gz"

    license("Apache-2.0")

    version("0.7.1", sha256="c7466c2a70a949609a501e868f6a288b7142725c407e24649ea6f7121632bc89")

    def install(self, spec, prefix):
        install_tree(".", prefix)
