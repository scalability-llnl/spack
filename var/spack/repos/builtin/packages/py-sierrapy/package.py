# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySierrapy(PythonPackage):
    """A Client of HIVdb Sierra GraphQL Webservice"""

    homepage = "https://github.com/hivdb/sierra-client/tree/master/python"
    pypi = "sierrapy/sierrapy-0.3.0.tar.gz"

    maintainers("dorton21")

    version("0.3.0", sha256="82474b3815d79d16a480b0cc70b9f7075430ff4990f33306c880b240a3141b6e")

    depends_on("py-setuptools", type="build")
    depends_on("py-certifi@2020.4.5.1", type="build")

    depends_on("py-chardet@3.0.4", type=("build", "run"))
    depends_on("py-click@7.1.2", type=("build", "run"))
    depends_on("py-gql@0.4.0", type=("build", "run"))
    depends_on("py-graphql-core@2.3.2", type=("build", "run"))
    depends_on("py-idna@2.9", type=("build", "run"))
    depends_on("py-rx@1.6.1", type=("build", "run"))
    depends_on("py-promise@2.3", type=("build", "run"))
    depends_on("py-requests@2.23.0", type=("build", "run"))
    depends_on("py-six@1.14.0", type=("build", "run"))
    depends_on("py-tqdm@4.46.0", type=("build", "run"))
    depends_on("py-voluptuous@0.11.7", type=("build", "run"))
    depends_on("py-urllib3@1.25.9", type=("build", "run"))
