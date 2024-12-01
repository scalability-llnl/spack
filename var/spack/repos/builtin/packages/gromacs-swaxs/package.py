# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.gromacs import CMakeBuilder as GromacsCMakeBuilder
from spack.pkg.builtin.gromacs import Gromacs


class GromacsSwaxs(Gromacs):
    """Modified Gromacs for small-angle scattering calculations (SAXS/WAXS/SANS)"""

    homepage = "https://biophys.uni-saarland.de/swaxs.html"
    url = "https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.5/gromacs-swaxs-release-2021.swaxs-0.5.tar.bz2"
    git = "https://gitlab.com/cbjh/gromacs-swaxs.git"
    maintainers("w8jcik")

    version(
        "2021.5-0.5",
        sha256="7207f107dc6c4009a04a533e18545666d4f58c172b2b24d04442bb1a0f43ff44",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.5/gromacs-swaxs-release-2021.swaxs-0.5.tar.bz2",
    )

    version(
        "2021.5-0.4",
        sha256="9f8ed6d448a04789d45e847cbbc706a07130377f578388220a9d5357fae9d1c3",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.4/gromacs-swaxs-release-2021.swaxs-0.4.tar.bz2",
    )

    version(
        "2021.5-0.3",
        sha256="e05ea76610657e52e8293abff53ee9f16f4cffa508074e1e10132ed5fba97881",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.3/gromacs-swaxs-release-2021.swaxs-0.3.tar.bz2",
    )

    version(
        "2021.4-0.2",
        sha256="ea0dbe868d20e05c8fca337e0dddc16116a83fa7a6ac3a924942e9d00952ed62",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.2/gromacs-swaxs-release-2021.swaxs-0.2.tar.bz2",
    )

    version(
        "2021.4-0.1",
        sha256="eda1c8a7aae6001ef40480addf9fff9cdccc7e2b80480e36d069f50d6f2be26e",
        deprecated=True,
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2021.swaxs-0.1/gromacs-swaxs-release-2021.swaxs-0.1.tar.bz2",
    )

    version(
        "2020.7-0.4",
        sha256="3eb0975ec92a89f6a3be548896307376974805ac685a9f776b0131a449a6b8a4",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2020.swaxs-0.4/gromacs-swaxs-release-2020.swaxs-0.4.tar.bz2",
    )

    version(
        "2020.7-0.3",
        sha256="eb5902df079b8f86c56b62be695c0d17307c195b2cdd7cefb7e117466be83211",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2020.swaxs-0.3/gromacs-swaxs-release-2020.swaxs-0.3.tar.bz2",
    )

    version(
        "2020.6-0.2",
        sha256="c22a7c6a0ee54eee1b3e224530f65e6f976a7aca5dc0f5ea22b2935a5a4357e9",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2020.swaxs-0.2/gromacs-swaxs-release-2020.swaxs-0.2.tar.bz2",
    )

    version(
        "2020.6-0.1",
        sha256="3d8360a3cc9144772786bddaa11e3dbc37d6a466b99f3314bf3928261c2fddcf",
        deprecated=True,
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2020.swaxs-0.1/gromacs-swaxs-release-2020.swaxs-0.1.tar.bz2",
    )

    version(
        "2019.6-0.3",
        sha256="1cf81592813333954bb1051321543f211d81f120a821a0c9386081e4cd367e84",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2019.swaxs-0.3/gromacs-swaxs-release-2019.swaxs-0.3.tar.bz2",
    )

    version(
        "2019.6-0.2",
        sha256="a45eeee3983a4443d3a40ea417770f3abd93f43eb80e021fd9d6830e414565cb",
        deprecated=True,
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2019.swaxs-0.2/gromacs-swaxs-release-2019.swaxs-0.2.tar.bz2",
    )

    version(
        "2019.6-0.1",
        sha256="91da09eed80646d6a1c500be78891bef22623a19795a9bc89adf9f2ec4f85635",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2019.swaxs-0.1/gromacs-swaxs-release-2019.swaxs-0.1.tar.bz2",
    )

    version(
        "2018.8-0.4",
        sha256="465bbd234b6805209cf39c6bfa4f482c367b947742bb2b9a3d535d362f254dcb",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.4/gromacs-swaxs-release-2018.swaxs-0.4.tar.bz2",
    )

    version(
        "2018.8-0.3",
        sha256="5e94d636fda28e81ff1f3cff2c9f6e7f458bf496f4d1ed7bc10e911bd98b303c",
        deprecated=True,
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.3/gromacs-swaxs-release-2018.swaxs-0.3.tar.bz2",
    )

    version(
        "2018.8-0.2",
        sha256="f8bf0d363334a9117a2a8deb690dadaa826b73b57a761949c7846a13b84b5af5",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.2/gromacs-swaxs-release-2018.swaxs-0.2.tar.bz2",
    )

    version(
        "2018.8-0.1",
        sha256="478f45286dfedb8f01c2d5bf0773a391c2de2baf85283ef683e911bc43e24675",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.1/gromacs-swaxs-release-2018.swaxs-0.1.tar.bz2",
    )

    version(
        "2016.6-0.1",
        sha256="11e8ae6b3141f356bae72b595737a1f253b878d313169703ba33a69ded01a04e",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2016.swaxs-0.1/gromacs-swaxs-release-2016.swaxs-0.1.tar.bz2",
    )

    version(
        "5.1.5-0.3",
        sha256="a9e8382eec3cc0d943e1869f13945ea4a971a95a70eb314c1f26a17fa7d03792",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-5-1.swaxs-0.3/gromacs-swaxs-release-5-1.swaxs-0.3.tar.bz2",
    )

    version(
        "5.0.7-0.5",
        sha256="7f7f69726472a641a5443f1993a6e1fb8cfa9c74aeaf46e8c5d1db37005ece79",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-5-0.swaxs-0.5/gromacs-swaxs-release-5-0.swaxs-0.5.tar.bz2",
    )

    version(
        "4.6.7-0.8",
        sha256="1cfa34fe9ff543b665cd556f3395a9aa67f916110ba70255c97389eafe8315a2",
        url="https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-4-6.swaxs-0.8/gromacs-swaxs-release-4-6.swaxs-0.8.tar.bz2",
    )

    conflicts("+plumed")
    conflicts("+opencl")
    conflicts("+sycl")

    def remove_parent_versions(self):
        """
        By inheriting GROMACS package we also inherit versions.
        They are not valid, so we are removing them.
        """

        for version_key in Gromacs.versions.keys():
            if version_key in self.versions:
                del self.versions[version_key]

    def __init__(self, spec):
        super().__init__(spec)

        self.remove_parent_versions()


class CMakeBuilder(GromacsCMakeBuilder):
    pass
