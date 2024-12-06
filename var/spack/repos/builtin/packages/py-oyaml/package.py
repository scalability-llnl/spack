# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOyaml(PythonPackage):
    """Ordered YAML: a drop-in replacement for PyYAML which preserves dict ordering."""

    homepage = "https://github.com/wimglenn/oyaml"
    pypi = "oyaml/oyaml-1.0.tar.gz"

    license("MIT")

    version("1.0", sha256="ed8fc096811f4763e1907dce29c35895d6d5936c4d0400fe843a91133d4744ed")

    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml", type=("build", "run"))
