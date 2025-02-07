# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    version("2.3.0", sha256="e80d7157553d33382ab0c399fcd5ec43ab5ff642504b07c8aef266165f9095d2")
    version("2.2.1", sha256="b691989bb762dc5944a2f13afd89666602fa7e40816f0cfb0278fe2164b34e30")
    version("2.2.0", sha256="d7cf2456ec2ae9e1724782152b6bf86e06cf071263dbe2eb8ad5b8765b419857")
    version("2.1.0", sha256="24f94f7fbc15f740e13ace695e204d6370bf4156eca08c24bcbeacaacb1b6c12")
    version("2.0.0", sha256="8ca4aabd8ca350183db3b8e117b0cd87d9a20277e39931e2799c86bfa910ae71")
    version("2.0.0rc4", sha256="5f6113be565c561c08114355570a259042b25222a9e8e1dc6e6e44448381cd36")
    version("2.0.0rc3", sha256="c0c897a33f5018489e6cc14892961831c8922a3378ac30436496c52bf877aff7")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-colorama@0.4.6:", type=("build", "run"))
    depends_on("py-pyyaml@6.0.1:", type=("build", "run"))

    depends_on("py-hatchling", type="build")
