# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYamlSyck(PerlPackage):
    """Fast, lightweight YAML loader and dumper"""

    homepage = "https://metacpan.org/pod/YAML::Syck"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/YAML-Syck-1.34.tar.gz"

    maintainers("EbiArnie")

    license("MIT")

    version("1.34", sha256="cc9156ccaebda798ebfe2f31b619e806577f860ed1704262f17ffad3c6e34159")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
