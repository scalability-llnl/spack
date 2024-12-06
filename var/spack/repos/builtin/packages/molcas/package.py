# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Molcas(CMakePackage):
    """Molcas is an ab initio quantum chemistry software package
    developed by scientists to be used by scientists.
    Please set the path to licence file with the following command
    export MOLCAS_LICENSE=/path/to/molcas/license/"""

    homepage = "https://www.molcas.org/"
    url = "file://{0}/molcas8.2.tar.gz".format(os.getcwd())
    manual_download = True

    version("8.2", md5="25b5fb8e1338b458a3eaea0b3d3b5e58")

    # Licensing
    license_required = True
    license_vars = ["MOLCAS_LICENSE"]

    depends_on("openmpi")
    depends_on("openblas")
    depends_on("hdf5")

    patch("install_driver.patch")
