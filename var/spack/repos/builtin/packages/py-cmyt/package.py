# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmyt(PythonPackage):
    """Matplotlib colormaps from the yt project !"""

    homepage = "https://yt-project.org"
    pypi = "cmyt/cmyt-1.0.4.tar.gz"
    git = "https://github.com/yt-project/cmyt.git"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version("main", branch="main")

    version("1.1.2", sha256="7027514a89331ee5cd672999e34c15feae218c8ed9b127832b6618c6771a869e")

    # https://github.com/yt-project/cmyt/blob/v1.1.2/pyproject.toml#L2
    depends_on("py-setuptools@40.9:", type="build")

    # https://github.com/yt-project/cmyt/blob/v1.1.2/setup.cfg#40
    depends_on("python@3.8:", type=("build", "run"))

    # https://github.com/yt-project/cmyt/blob/v1.1.2/setup.cfg#35
    depends_on("py-colorspacious@1.1.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.2:", type=("build", "run"))
    depends_on("py-more-itertools@8.4:", type=("build", "run"))
    depends_on("py-numpy@1.17.4:", type=("build", "run"))
