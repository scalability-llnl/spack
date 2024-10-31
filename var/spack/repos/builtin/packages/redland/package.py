# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Redland(AutotoolsPackage):
    """Redland RDF Library - librdf providing the RDF API and triple stores"""

    homepage = "https://librdf.org/"
    url = "https://download.librdf.org/source/redland-1.0.17.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.0.17", sha256="de1847f7b59021c16bdc72abb4d8e2d9187cd6124d69156f3326dd34ee043681")
    version("1.0.16", sha256="d9a274fc086e61119d5c9beafb8d05527e040ec86f4c0961276ca8de0a049dbd")
    version("1.0.15", sha256="0e1f5825b6357c9b490da866c95ae1d895dbb5f445013d2511c37df822ee9ec6")

    depends_on("c", type="build")  # generated

    depends_on("raptor2")
    depends_on("rasqal")
