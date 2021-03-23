# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

       Note: Orca is licensed software. You will need to create an account
       on the Orca homepage and download Orca yourself. Spack will search
       your current directory for the download file. Alternatively, add this
       file to a mirror so that Spack can find it. For instructions on how to
       set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://cec.mpg.de"
    url      = "file://{0}/orca_4_0_1_2_linux_x86-64_openmpi202.tar.zst".format(os.getcwd())
    manual_download = True

    version('4.2.1', sha256='9bbb3bfdca8220b417ee898b27b2885508d8c82799adfa63dde9e72eab49a6b2',
            expand=False)
    version('4.2.0', sha256='55a5ca5aaad03396ac5ada2f14b61ffa735fdc2d98355e272465e07a6749d399',
            expand=False)
    version('4.0.1.2', sha256='cea442aa99ec0d7ffde65014932196b62343f7a6191b4bfc438bfb38c03942f7',
            expand=False)

    depends_on('zstd', type='build')

    # Map Orca version with the required OpenMPI version
    openmpi_versions = {
        '4.0.1.2': '2.0.2',
        '4.2.0':   '3.1.4',
        '4.2.1':   '3.1.4'
    }
    for orca_version, openmpi_version in openmpi_versions.items():
        depends_on('openmpi@{0}'.format(openmpi_version), type='run',
                   when='@{0}'.format(orca_version))

    def url_for_version(self, version):
        out = "file://{0}/orca_{1}_linux_x86-64_openmpi{2}.tar.zst"
        return out.format(os.getcwd(), version.underscored,
                          self.openmpi_versions[version.string])

    def install(self, spec, prefix):
        # we have to extract the archive ourself
        # fortunately it's just full of a bunch of binaries

        vername = os.path.basename(self.stage.archive_file).split('.')[0]

        zstd = which('zstd')
        zstd('-d', self.stage.archive_file, '-o', vername + '.tar')

        tar = which('tar')
        tar('-xvf', vername + '.tar')

        # there are READMEs in there but they don't hurt anyone
        mkdirp(prefix.bin)
        install_tree(vername, prefix.bin)

        # Check "mpirun" usability when building against OpenMPI
        # with Slurm scheduler and add a "mpirun" wrapper that
        # calls "srun" if need be
        if '^openmpi ~legacylaunchers schedulers=slurm' in self.spec:
            mpirun_srun = join_path(os.path.dirname(__file__),
                                    "mpirun_srun.sh")
            install(mpirun_srun, prefix.bin.mpirun)
