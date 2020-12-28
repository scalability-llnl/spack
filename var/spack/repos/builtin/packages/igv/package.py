# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Igv(Package):
    """The Integrative Genomics Viewer (IGV) is a high-performance visualization
    tool for interactive exploration of large, integrated genomic datasets.
    It supports a wide variety of data types, including array-based and
    next-generation sequence data, and genomic annotations."""

    homepage = "https://software.broadinstitute.org/software/igv/home"
    url      = "https://data.broadinstitute.org/igv/projects/downloads/2.8/IGV_Linux_2.8.0.zip"

    maintainers = ['snehring']

    version('2.8.0', sha256='897f683645b02c4da55424110b885071c2b9dd51bc180174e2a9b10788bf3257')

    # They ship with 11, out of an abundance of caution I'm going to restrict
    # it to just 11.

    depends_on('java@11:11.99', type='run')

    def install(self, spec, prefix):
        # Binary dist, just copy what we need, which should be the lib
        # directory, the two script, and the arg file
        install_tree('lib', prefix.lib)
        mkdirp(prefix.bin)
        filter_file('^prefix=.*$', 'prefix=' + prefix,
                    'igv.sh', 'igv_hidpi.sh')
        install('igv.sh', prefix.bin)
        install('igv_hidpi.sh', prefix.bin)
        install('igv.args', prefix)
