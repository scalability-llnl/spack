# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRrcov(RPackage):
    """Scalable Robust Estimators with High Breakdown Point.

    Robust Location and Scatter Estimation and Robust Multivariate Analysis
    with High Breakdown Point: principal component analysis (Filzmoser and
    Todorov (2013), <doi:10.1016/j.ins.2012.10.017>), linear and quadratic
    discriminant analysis (Todorov and Pires (2007)), multivariate tests
    (Todorov and Filzmoser (2010) <doi:10.1016/j.csda.2009.08.015>), outlier
    detection (Todorov et al. (2010) <doi:10.1007/s11634-010-0075-2>). See also
    Todorov and Filzmoser (2009) <ISBN-13:978-3838108148>, Todorov and
    Filzmoser (2010) <doi:10.18637/jss.v032.i03> and Boudt et al. (2019)
    <doi:10.1007/s11222-019-09869-x>."""

    cran = "rrcov"

    license("GPL-3.0-or-later")

    version("1.7-6", sha256="b8a2c07c42e4e76e9f90cb016cb72a40f6d2ce1f10d1753c06e3344f38e148de")
    version("1.7-2", sha256="0f01ed07cbc9e55dfcba27040a3f72237fb2fb86eda899472c2f96500220ecae")
    version("1.7-1", sha256="e115a09997b46c7eed33017f748632c7d50a95ad621f1f452f22dfc714c9a4e5")
    version("1.7-0", sha256="cbcca84a82d63fa50556aa8db29312b9bb588a638eb306ce4a81c271529228fd")
    version("1.6-1", sha256="9f3b500f2bdac375d0374cd1b120806c785b1981101d7d018fc1fcc73e305d90")
    version("1.6-0", sha256="795f3a49b3e17c9c6e0fdd865e81a0402cefda970032c8299bcf2056ca7ec944")
    version("1.5-5", sha256="1f7f07558e347e7d1f1adff68631764670bc672777a7d990901c4fa94cc0e629")
    version("1.4-7", sha256="cbd08ccce8b583a2f88946a3267c8fc494ee2b44ba749b9296a6e3d818f6f293")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-robustbase@0.92.1:", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-pcapp", type=("build", "run"))

    depends_on("r-cluster", type=("build", "run"), when="@:1.4-7")
