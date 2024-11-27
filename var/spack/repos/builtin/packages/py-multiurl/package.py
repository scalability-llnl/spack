# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiurl(PythonPackage):
    """A package to download several URL as one, as well as supporting multi-part URLs."""

    homepage = "https://github.com/ecmwf/multiurl"
    pypi = "multiurl/multiurl-0.2.3.2.tar.gz"

    license("Apache-2.0")

    version("0.2.3.2", sha256="b625892ef3a5b8d4bd323f1dcd4750b6ea7e4e2e2e4574b6e88cdf92e10579e9")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-requests")
        depends_on("py-tqdm")
        depends_on("py-pytz")
        depends_on("py-python-dateutil")
