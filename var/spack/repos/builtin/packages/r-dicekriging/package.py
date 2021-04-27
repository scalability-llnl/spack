# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RDicekriging(RPackage):
    """Kriging Methods for Computer Experiments

    Estimation, validation and prediction of kriging models. Important
    functions : km, print.km, plot.km, predict.km."""

    homepage = "http://dice.emse.fr/"
    url      = "https://cloud.r-project.org/src/contrib/DiceKriging_1.5.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DiceKriging"

    version('1.5.8', sha256='11d02b894cb509dbb8887ae27b6d08ba25aa52ac3ece134c3759c2b3b1bf4d77')
    version('1.5.6', sha256='25466d2db9f17083d1c7b9545e5ec88f630be934f9373c2f7b36c38de4e64e92')
    version('1.5.5', sha256='55fe161f867a0c3772023c3047041b877aa54d29cb474ec87293ec31cc5cb30c')
