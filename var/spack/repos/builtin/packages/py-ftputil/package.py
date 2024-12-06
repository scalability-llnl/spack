# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFtputil(PythonPackage):
    """High-level FTP client for Python."""

    homepage = "https://ftputil.sschwarzer.net"
    pypi = "ftputil/ftputil-5.0.4.tar.gz"
    maintainers("charmoniumQ")

    license("AFL-2.1")

    version("5.0.4", sha256="6889db8649dd20d9b6d40a6c5f0f84ccf340a7dac1e0bfc0f0024090fc2afb33")

    # https://git.sr.ht/~sschwarzer/ftputil/tree/v5.0.4/item/setup.py
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # https://git.sr.ht/~sschwarzer/ftputil/tree/v5.0.4/item/requirements.txt
    # Note that the requirements in `requirements.txt` are only necessary for a dev environment.
    # They are not included in `setup.py`
