# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gate(CMakePackage):
    """Simulations of Preclinical and Clinical Scans in Emission Tomography,
    Transmission Tomography and Radiation Therapy

    GATE is an advanced opensource software developed by the international
    OpenGATE collaboration and dedicated to numerical simulations in medical
    imaging and radiotherapy. It currently supports simulations of Emission
    Tomography (Positron Emission Tomography - PET and Single Photon Emission
    Computed Tomography - SPECT), Computed Tomography (CT), Optical Imaging
    (Bioluminescence and Fluorescence) and Radiotherapy experiments. Using an
    easy-to-learn macro mechanism to configurate simple or highly sophisticated
    experimental settings, GATE now plays a key role in the design of new
    medical imaging devices, in the optimization of acquisition protocols and
    in the development and assessment of image reconstruction algorithms and
    correction techniques. It can also be used for dose calculation in
    radiotherapy experiments."""

    homepage = "http://opengatecollaboration.org/"
    url      = "https://github.com/OpenGATE/Gate/archive/v9.0.tar.gz"

    maintainers = ['glennpj']

    version('9.0', sha256='8354f392facc0b7ae2ddf0eed61cc43136195b198ba399df25e874886b8b69cb')

    variant('rtk', default=False,
            description='build support for the Reconstruction Toolkit')
    variant('default_platform', default='condor',
            description='select default platform for the cluster tools',
            values=('SGE', 'condor', 'openPBS', 'openmosix', 'slurm', 'xgrid'),
            multi=False)

    depends_on('geant4@:10.6~threads')  # Gate needs a non-threaded geant4
    depends_on('root')
    depends_on('itk+rtk', when='+rtk')

    patch('cluster_tools_filemerger_Makefile.patch')
    patch('cluster_tools_jobsplitter_Makefile.patch')
    patch('cluster_tools_jobsplitter_platform.patch')

    def cmake_args(self):
        args = []

        if '+rtk' in self.spec:
            args.extend([
                '-DGATE_USE_ITK=ON',
                '-DGATE_USE_RTK=ON',
            ])
        else:
            args.extend([
                '-DGATE_USE_ITK=OFF',
                '-DGATE_USE_RTK=OFF',
            ])

        return args

    def setup_build_environment(self, env):
        gc_default_platform = self.spec.variants['default_platform'].value
        env.set('GC_DEFAULT_PLATFORM', gc_default_platform)

    def setup_run_environment(self, env):
        env.set('GC_GATE_EXE_DIR', self.prefix.bin)
        env.set('GC_CONDOR_SCRIPT', join_path(self.prefix, 'share',
                                              'jobsplitter', 'condor.script'))
        env.set('GC_PBS_SCRIPT', join_path(self.prefix, 'share',
                                           'jobsplitter', 'openPBS.script'))
        env.set('GC_SGE_SCRIPT', join_path(self.prefix, 'share',
                                           'jobsplitter', 'SGE.script'))
        env.set('GC_SLURM_SCRIPT', join_path(self.prefix, 'share',
                                             'jobsplitter', 'slurm.script'))

    @run_after('install')
    def cluster_tools(self):
        with working_dir('cluster_tools/filemerger'):
            make()
            make('install', 'PREFIX={0}'.format(self.prefix))

        with working_dir('cluster_tools/jobsplitter'):
            make()
            make('install', 'PREFIX={0}'.format(self.prefix))

        script_path = join_path(self.prefix, 'share', 'jobsplitter')
        mkdirp(script_path)
        install_tree('cluster_tools/jobsplitter/script', script_path)
        install('*.xml', self.prefix.share)
        install('*.db', self.prefix.share)
