# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeeadd(PythonPackage):
    """Google Earth Engine Batch Assets Manager with Addons."""

    homepage = "https://github.com/samapriya/gee_asset_manager_addon"
    pypi = "geeadd/geeadd-0.3.0.tar.gz"

    license("Apache-2.0")

    version("0.3.0", sha256="591e6ff2847122598ed5b0452a892a76e332ce227d4ba75e4d03eca2c7a4beea")

    depends_on("py-setuptools", type="build")
    depends_on("py-earthengine-api@0.1.87:", type=("build", "run"))
    depends_on("py-requests@2.10.0:", type=("build", "run"))
    depends_on("py-poster@0.8.1:", type=("build", "run"))
    depends_on("py-retrying@1.3.3:", type=("build", "run"))
    depends_on("py-clipboard@0.0.4:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.5.1:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.7.0:", type=("build", "run"))
    depends_on("py-future@0.16.0:", type=("build", "run"))
    depends_on("py-google-cloud-storage@1.1.1:", type=("build", "run"))
    depends_on("py-oauth2client@4.1.3:", type=("build", "run"))
