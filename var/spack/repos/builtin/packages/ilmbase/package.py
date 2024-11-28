# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ilmbase(AutotoolsPackage):
    """OpenEXR ILM Base libraries (high dynamic-range image file format)"""

    homepage = "https://www.openexr.com/"
    url = "https://github.com/openexr/openexr/releases/download/v2.3.0/ilmbase-2.3.0.tar.gz"

    version("2.3.0", sha256="456978d1a978a5f823c7c675f3f36b0ae14dba36638aeaa3c4b0e784f12a3862")

    version(
        "2.2.0",
        sha256="ecf815b60695555c1fbc73679e84c7c9902f4e8faa6e8000d2f905b8b86cedc7",
        url="http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.2.0.tar.gz",
    )
    version(
        "2.0.1",
        sha256="19b03975fea4461f2eff91f5df138b301b3ea9709eccbda98447f372bf09735f",
        url="http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.0.1.tar.gz",
    )
    version(
        "1.0.2",
        sha256="2e5cda799ffdfca9b1a16bb120d49c74a39af1457ef22f968918c6200ba62e44",
        url="http://download.savannah.nongnu.org/releases/openexr/ilmbase-1.0.2.tar.gz",
    )
    version(
        "0.9.0",
        sha256="c134e47206d0e22ff0be96fa95391a13b635b6ad42668673e293f835fbd176b1",
        url="http://download.savannah.nongnu.org/releases/openexr/ilmbase-0.9.0.tar.gz",
    )

    depends_on("cxx", type="build")  # generated
