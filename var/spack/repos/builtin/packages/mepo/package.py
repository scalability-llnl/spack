# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mepo(PythonPackage):
    """Tool to manage (m)ultiple git r(epo)sitories"""

    homepage = "https://github.com/GEOS-ESM/mepo"
    git = "https://github.com/GEOS-ESM/mepo.git"
    pypi = "mepo/mepo-2.0.0.tar.gz"

    maintainers("pchakraborty", "mathomp4")

    license("Apache-2.0", checked_by="mathomp4")

    version("2.1.0", sha256="24f94f7fbc15f740e13ace695e204d6370bf4156eca08c24bcbeacaacb1b6c12")
    version("2.0.0", sha256="8ca4aabd8ca350183db3b8e117b0cd87d9a20277e39931e2799c86bfa910ae71")
    version("2.0.0rc4", sha256="5f6113be565c561c08114355570a259042b25222a9e8e1dc6e6e44448381cd36")
    version("2.0.0rc3", sha256="c0c897a33f5018489e6cc14892961831c8922a3378ac30436496c52bf877aff7")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-colorama@0.4.6:", type=("build", "run"))
    depends_on("py-pyyaml@6.0.1:", type=("build", "run"))

    depends_on("py-hatchling", type="build")
