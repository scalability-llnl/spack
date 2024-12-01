# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeeAssetManager(PythonPackage):
    """Google Earth Engine Batch Asset Manager."""

    homepage = "https://github.com/tracek/gee_asset_manager"
    url = "https://github.com/tracek/gee_asset_manager/archive/0.1.tar.gz"
    git = "https://github.com/tracek/gee_asset_manager.git"

    license("Apache-2.0")

    version("master", branch="master")
    version("0.1", sha256="0d3345855352354d8b84188705a09a35c21af2b753cda5c688ffb2e3a454ee23")

    depends_on("py-setuptools", type="build")
    depends_on("py-earthengine-api@0.1.87:", type=("build", "run"))
    depends_on("py-requests@2.10.0:", type=("build", "run"))
    depends_on("py-retrying@1.3.3:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.5.1:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.7.0:", type=("build", "run"))
    depends_on("py-future@0.16.0:", type=("build", "run"))
    depends_on("py-google-cloud-storage@1.1.1:", type=("build", "run"))
