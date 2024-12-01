# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RevocapCoupler(AutotoolsPackage):
    """Large Scale Assembly, Structural Correspondence,
    Multi Dynamics Simulator.In this program,
    a part of functions of ADVENTURE_Solid ver.1.1 module"""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/dl/index.php"
    url = "file://{0}/REVOCAP_Coupler-2.1.tar.gz".format(os.getcwd())
    manual_download = True

    version("2.1", sha256="9e7612d5c508ccdce23bff9ccbf62aeb635877bc2276cdc05c109de40f609f49")

    depends_on("mpi")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-mpicc=%s" % spec["mpi"].mpicc,
            "--with-fortran=%s" % spec["mpi"].mpif77,
            "--with-mpif90=%s" % spec["mpi"].mpifc,
        ]
        return args
