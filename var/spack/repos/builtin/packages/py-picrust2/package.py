# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPicrust2(PythonPackage):
    """PICRUSt2 is a software for predicting functional
    abundances based only on marker gene sequences."""

    homepage = "https://github.com/picrust/picrust2"
    url = "https://github.com/picrust/picrust2/archive/v2.3.0-b.tar.gz"

    maintainers("dorton21")

    license("GPL-3.0-only")

    version("2.3.0-b", sha256="ac12c372bc263e750d9101eca0cd0e57de37089b661fa1a13caf5a544d293737")
    version("2.2.0-b", sha256="c41e1f487b33179f4aecede50cfd8b652aa3cef2ea1ae5fd022f531c7d549097")
    version("2.1.4-b", sha256="f781eb323914979b6d3bca088a5152f085f53e6e38f1c3be94b35f99fc1db2d8")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-biom-format", type=("build", "run"))
