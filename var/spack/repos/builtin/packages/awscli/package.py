##############################################################################
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Awscli(PythonPackage):
    """This package provides a unified command line interface to
    Amazon Web Services"""

    pypi = "awscli/awscli-1.16.308.tar.gz"

    version("1.29.41", sha256="c029edd2c0bd72fb49cefe1a8f83ce2b46ba31ab45769677f7ba0771461078cb")
    version("1.27.84", sha256="a27a7d1f3efa9dd2acf9d8bd72b939337d53da4ac71721cde6d5dff94aa446f7")
    version("1.27.56", sha256="58fd7122547db71646c053c914bd4f9b673356dd8c9520ae6d35560a8aec208b")
    version("1.16.308", sha256="3632fb1db2538128509a7b5e89f2a2c4ea3426bec139944247bddc4d79bf7603")
    version("1.16.179", sha256="6a87114d1325358d000abe22b2103baae7b91f053ff245b9fde33cb0affb5e4f")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", when="@1.25:", type=("build", "run"))

    # py-botocore is pinned to the patch version number
    depends_on("py-botocore@1.31.41", when="@1.29.41", type=("build", "run"))
    depends_on("py-botocore@1.29.84", when="@1.27.84", type=("build", "run"))
    depends_on("py-botocore@1.29.56", when="@1.27.56", type=("build", "run"))
    depends_on("py-botocore@1.13.44", when="@1.16.308", type=("build", "run"))
    depends_on("py-botocore@1.12.169", when="@1.16.179", type=("build", "run"))

    depends_on("py-colorama@0.2.5:0.4.4", when="@1.27:", type=("build", "run"))
    depends_on("py-colorama@0.2.5:0.3.9", when="@1.16", type=("build", "run"))

    depends_on("py-docutils@0.10:0.16", when="@1.27:", type=("build", "run"))
    depends_on("py-docutils@0.10:0.15", when="@1.16", type=("build", "run"))

    depends_on("py-pyyaml@3.10:6.0", when="@1.29", type=("build", "run"))
    depends_on("py-pyyaml@3.10:5.4", when="@1.27", type=("build", "run"))
    depends_on("py-pyyaml@3.10:5.2", when="@1.16", type=("build", "run"))

    depends_on("py-rsa@3.1.2:4.7", when="@1.27:", type=("build", "run"))
    depends_on("py-rsa@3.1.2:3.5.0", when="@1.16", type=("build", "run"))

    depends_on("py-s3transfer@0.6", when="@1.27:", type=("build", "run"))
    depends_on("py-s3transfer@0.2", when="@1.16", type=("build", "run"))
