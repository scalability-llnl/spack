# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGdown(PythonPackage):
    """Google Drive Public File/Folder Downloader."""

    homepage = "https://github.com/wkentaro/gdown"
    pypi = "gdown/gdown-5.2.0.tar.gz"

    license("MIT")

    version("5.2.0", sha256="2145165062d85520a3cd98b356c9ed522c5e7984d408535409fd46f94defc787")

    with default_args(type="build"):
        depends_on("py-hatchling@1.20:")
        depends_on("py-hatch-vcs")
        depends_on("py-hatch-fancy-pypi-readme")

    with default_args(type=("build", "run")):
        depends_on("py-filelock")
        depends_on("py-requests+socks")
        depends_on("py-tqdm")
        depends_on("py-beautifulsoup4")
