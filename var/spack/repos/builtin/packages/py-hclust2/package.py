# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHclust2(PythonPackage):
    """Hclust2 is a handy tool for plotting heat-maps with several useful
    options to produce high quality figures that can be used in  publication."""

    homepage = "https://github.com/SegataLab/hclust2/"
    pypi = "hclust2/hclust2-1.0.0.tar.gz"

    version("1.0.0", sha256="9667f1d16628940aedd3d1d571b956a6f77795018e3ea4dd83f234419eb0096d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
