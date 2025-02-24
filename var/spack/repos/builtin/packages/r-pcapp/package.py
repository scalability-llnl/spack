# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPcapp(RPackage):
    """Provides functions for robust PCA by projection pursuit.

    Provides functions for robust PCA by projection pursuit. The methods are
    described in Croux et al. (2006) <doi:10.2139/ssrn.968376>, Croux et al.
    (2013) <doi:10.1080/00401706.2012.727746>, Todorov and Filzmoser (2013)
    <doi:10.1007/978-3-642-33042-1_31>."""

    cran = "pcaPP"

    version("2.0-5", sha256="674faed967016a19f9d927506d6b3f4fc7ff2b2ab5679b2368429ee2c61b7c10")
    version("2.0-3", sha256="1aac554f039753bf9d026090e47d66b82bf3f1f75479ed0adefa3f7bbb55d603")
    version("2.0-2", sha256="a18b66974e0bfa5af6505acd777d04fd605b32f06009073488ee2f44280bb54b")
    version("2.0-1", sha256="9690e2f263162452d5a14bd8c52264cb70b317d30907411af4e5b6df4086121a")
    version("1.9-74", sha256="50837b434d67e4b5fcec34c689a9e30c7a9fb94c561b39f24e68a1456ff999b6")
    version("1.9-73", sha256="ca4566b0babfbe83ef9418283b08a12b3420dc362f93c6562f265df7926b53fc")
    version("1.9-72.1", sha256="a9e39ee15a650930c07672092f9f0c431807869b68b5471037eb7290a4d65bd5")
    version("1.9-72", sha256="58bd0bfb5931aecd734801654bac95f28dab6d30fd043c66c5b719b497104844")
    version("1.9-70", sha256="359e2b376b8b7e2de68b0f33f772d99ecbe9a94f8f460574ac2e3c07513c96d5")
    version("1.9-61", sha256="7dc395e159ff1a56135baaf0b1bea40f871c30f6dadd38992f4ccdfc4e88dc29")
    version("1.9-60", sha256="9a4b471957ac39ed7c860e3165bf8e099b5b55cf814654adb58f9d19df2718e7")
    version("1.9-50", sha256="137637314fba6e11883c63b0475d8e50aa7f363e064baa1e70245f7692565b56")

    depends_on("r@3.6.2:", type=("build", "run"), when="@2.0-4:")
    depends_on("r-mvtnorm", type=("build", "run"))
