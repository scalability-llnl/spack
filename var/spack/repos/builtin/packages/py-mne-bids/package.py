# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMneBids(PythonPackage):
    """MNE-BIDS: Organizing MEG, EEG, and iEEG data according to the BIDS
    specification and facilitating their analysis with MNE-Python."""

    homepage = "https://mne.tools/mne-bids"
    pypi = "mne_bids/mne_bids-0.15.0.tar.gz"
    git = "https://github.com/mne-tools/mne-bids"

    license("BSD-3-Clause")

    version("0.15.0", sha256="8a3ac7fb586ba2be70eb687c67ae060b42693078c56232180b27161124c22f72")

    variant("full", default=False, description="Enable full functionality.")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-mne@1.5:", type=("build", "run"))
    depends_on("py-numpy@1.21.2:", type=("build", "run"))
    depends_on("py-scipy@1.7.1:", type=("build", "run"))
