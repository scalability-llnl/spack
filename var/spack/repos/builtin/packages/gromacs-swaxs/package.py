# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.gromacs import Gromacs


class GromacsSwaxs(Gromacs):
    """Modified Gromacs for small-angle scattering calculations (SAXS/WAXS/SANS)"""

    homepage = 'https://biophys.uni-saarland.de/swaxs.html'
    url = 'https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2019.swaxs-0.1/gromacs-swaxs-release-2019.swaxs-0.1.tar.bz2'
    git = 'https://gitlab.com/cbjh/gromacs-swaxs.git'
    maintainers = ['w8jcik']

    version('2019.6-0.1', sha256='91da09eed80646d6a1c500be78891bef22623a19795a9bc89adf9f2ec4f85635',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2019.swaxs-0.1/gromacs-swaxs-release-2019.swaxs-0.1.tar.bz2')

    version('2018.8-0.2', sha256='f8bf0d363334a9117a2a8deb690dadaa826b73b57a761949c7846a13b84b5af5',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.2/gromacs-swaxs-release-2018.swaxs-0.2.tar.bz2')

    version('2018.8-0.1', sha256='478f45286dfedb8f01c2d5bf0773a391c2de2baf85283ef683e911bc43e24675',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2018.swaxs-0.1/gromacs-swaxs-release-2018.swaxs-0.1.tar.bz2')

    version('2016.6-0.1', sha256='11e8ae6b3141f356bae72b595737a1f253b878d313169703ba33a69ded01a04e',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-2016.swaxs-0.1/gromacs-swaxs-release-2016.swaxs-0.1.tar.bz2')

    version('5.1.5-0.3', sha256='a9e8382eec3cc0d943e1869f13945ea4a971a95a70eb314c1f26a17fa7d03792',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-5-1.swaxs-0.3/gromacs-swaxs-release-5-1.swaxs-0.3.tar.bz2')

    version('5.0.7-0.5', sha256='7f7f69726472a641a5443f1993a6e1fb8cfa9c74aeaf46e8c5d1db37005ece79',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-5-0.swaxs-0.5/gromacs-swaxs-release-5-0.swaxs-0.5.tar.bz2')

    version('4.6.7-0.8', sha256='1cfa34fe9ff543b665cd556f3395a9aa67f916110ba70255c97389eafe8315a2',
            url='https://gitlab.com/cbjh/gromacs-swaxs/-/archive/release-4-6.swaxs-0.8/gromacs-swaxs-release-4-6.swaxs-0.8.tar.bz2')

    conflicts('+plumed')
    conflicts('+opencl')
    conflicts('+sycl')

    def remove_parent_versions(self):
        """
        By inheriting GROMACS package we also inherit versions.
        They are not valid, so we are removing them.
        """

        for version_key in Gromacs.versions.keys():
            if version_key in self.versions:
                del self.versions[version_key]

    def __init__(self, spec):
        super(GromacsSwaxs, self).__init__(spec)

        self.remove_parent_versions()
