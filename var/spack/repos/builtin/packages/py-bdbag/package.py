# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBdbag(PythonPackage):
    """The bdbag utilities are a collection of software programs for working
    with BagIt packages that conform to the BDBag and Bagit/RO profiles.
    """

    homepage = "https://github.com/fair-research/bdbag/"
    pypi = "bdbag/bdbag-1.6.3.tar.gz"

    license("Apache-2.0")

    version("1.6.3", sha256="1ad2e4956045cb3d43a6276391ad919e42a90a2443727dbc5b1ac6eeb6d6e3c9")

    depends_on("python@2.7:2,3.5:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@:5", type=("build", "run"))

    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-tzlocal@2.1", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-requests@2.7:", type=("build", "run"))
    depends_on("py-bagit@1.8.1", type=("build", "run"))
    depends_on("py-bagit-profile@1.3.1", type=("build", "run"))
