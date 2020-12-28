# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRio(RPackage):
    """Streamlined data import and export by making assumptions that the user
    is probably willing to make: 'import()' and 'export()' determine the data
    structure from the file extension, reasonable defaults are used for data
    import and export (e.g., 'stringsAsFactors=FALSE'), web-based import is
    natively supported (including from SSL/HTTPS), compressed files can be read
    directly without explicit decompression, and fast import packages are used
    where appropriate. An additional convenience function, 'convert()',
    provides a simple method for converting between file types."""

    homepage = "https://github.com/leeper/rio"
    url      = "https://cloud.r-project.org/src/contrib/rio_0.5.16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rio"

    version('0.5.16', sha256='d3eb8d5a11e0a3d26169bb9d08f834a51a6516a349854250629072d59c29d465')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-foreign', type=('build', 'run'))
    depends_on('r-haven@1.1.0:', type=('build', 'run'))
    depends_on('r-curl@0.6:', type=('build', 'run'))
    depends_on('r-data-table@1.9.8:', type=('build', 'run'))
    depends_on('r-readxl@0.1.1:', type=('build', 'run'))
    depends_on('r-openxlsx', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
