# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataValidator(PythonPackage):
    """Validation schema and code for HEPdata submissions."""

    homepage = "https://github.com/hepdata/hepdata-validator"
    pypi = "hepdata_validator/hepdata_validator-0.1.16.tar.gz"

    tags = ["hep"]

    version("0.3.3", sha256="dccdf2ba58bac78e879145a2ff31d299e7b20bd7f28b575ab9d07b950ab723ae")
    version("0.3.0", sha256="d603ddf908ce3838bac09bf7334184db4b35f03e2b215572c67b5e1fabbf0d9b")
    version("0.2.3", sha256="314e75eae7d4a134bfc8291440259839d82aabefdd720f237c0bf8ea5c9be4dc")
    version("0.1.16", sha256="3d7f725328ecdbb66826bff2e48a40a1d9234249859c8092ca0e92be7fb78111")
    version("0.1.15", sha256="1030654b1a1cfc387c2759f8613f033da467c8182dc027e181227aeb52854bb2")
    version("0.1.14", sha256="d1596741fb26be234c2adb6972306908f09b049dc670d8312cf2636f1a615a52")
    version("0.1.8", sha256="08686563e0130c5dd6d9fb8d5c7bf5a2617a637b105a42f7106b96a31eaffa61")

    depends_on("python@3.6:", when="@0.3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click", when="@0.3.3:", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-packaging", when="@0.3.3:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyyaml@5.4.1:", when="@0.3.3:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
