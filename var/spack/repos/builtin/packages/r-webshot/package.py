# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RWebshot(RPackage):
    """Take Screenshots of Web Pages

    Takes screenshots of web pages, including Shiny applications and R Markdown
    documents."""

    homepage = "https://github.com/wch/webshot/"
    url      = "https://cloud.r-project.org/src/contrib/webshot_0.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/webshot/"

    version('0.5.2', sha256='f183dc970157075b51ac543550a7a48fa3428b9c6838abb72fe987c21982043f')
    version('0.5.1', sha256='b9750d206c6fa0f1f16cc212b0a34f4f4bfa916962d2c877f0ee9a33620f4b23')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-callr', type=('build', 'run'))
    depends_on('imagemagick', type='run')

    # need a phantomjs package to make this actually work.
