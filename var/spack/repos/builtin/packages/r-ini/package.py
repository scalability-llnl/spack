# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIni(RPackage):
    """Parse simple '.ini' configuration files to an structured list. Users can
    manipulate this resulting list with lapply() functions. This same
    structured list can be used to write back to file after modifications."""

    homepage = "https://github.com/dvdscripter/ini"
    url      = "https://cloud.r-project.org/src/contrib/ini_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ini"

    version('0.3.1', sha256='7b191a54019c8c52d6c2211c14878c95564154ec4865f57007953742868cd813')
