# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ck(MavenPackage):
    """CK calculates class-level and metric-level code metrics in Java
    projects by means of static analysis (i.e. no need for compiled code)."""

    homepage = "https://github.com/mauricioaniche/ck"
    url = "https://github.com/mauricioaniche/ck/archive/ck-0.6.2.tar.gz"

    license("BSD-2-Clause AND Apache-2.0")

    version("0.6.2", sha256="ee16d209f05852230504dea1af39cdb1cfc8e9b56f4708ed1afcd5ce44af76eb")
    version("0.6.1", sha256="1db1fef7111bb485d5554d5927611761a102133a41b88e8fb20cd44494411ac4")
    version("0.6.0", sha256="8a1affad047fbefda5d2dad1a795204ffd06c50e2fba830f87cf6c7518423137")
    version("0.5.2", sha256="35f610f5d97ca31a62903ba368be7e0b74764daccd95afa3eb9ff04e0326a7ca")
    version("0.5.1", sha256="732849ae7b26d01ee082283396a6fdd7823282c368ae6fd05966acb4598ccebe")
    version("0.5.0", sha256="3923d25ff4941a6207d644fd1ba3115b5ad303ef953285610e836bc59a4cbcb7")
