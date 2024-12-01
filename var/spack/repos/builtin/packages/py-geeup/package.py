# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeeup(PythonPackage):
    """Simple Client for Earth Engine Uploads with Selenium Support."""

    homepage = "https://github.com/samapriya/geeup"
    pypi = "geeup/geeup-0.2.4.tar.gz"

    license("Apache-2.0")

    version("0.2.4", sha256="20f62306ea900d7fa28a97cc92204716212dc030c50a6ac8214772a61a1a83fe")

    depends_on("py-setuptools@38.3.0:", type="build")
    depends_on("py-earthengine-api@0.1.87:", type=("build", "run"))
    depends_on("py-requests@2.10.0:", type=("build", "run"))
    depends_on("py-retrying@1.3.3:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.5.1:", type=("build", "run"))
    depends_on("py-pandas@0.23.0:", type=("build", "run"))
    depends_on("py-psutil@5.4.5:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.7.0:", type=("build", "run"))
    depends_on("py-pytest@3.0.0:", type=("build", "run"))
    depends_on("py-future@0.16.0:", type=("build", "run"))
    depends_on("py-google-cloud-storage@1.1.1:", type=("build", "run"))
    depends_on("py-selenium@3.13.0:", type=("build", "run"))
    depends_on("py-pysmartdl", type=("build", "run"))
    depends_on("py-pysmartdl@1.3.1:", type=("build", "run"))
    depends_on("py-lxml@4.1.1:", type=("build", "run"))
    depends_on("py-oauth2client@4.1.3:", type=("build", "run"))
