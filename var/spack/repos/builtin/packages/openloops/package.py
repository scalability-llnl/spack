# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Openloops(Package):
    """The OpenLoops 2 program is a fully automated implementation of the
       Open Loops algorithm combined with on-the-fly reduction methods,
       which allows for the fast and stable numerical evaluation of tree
       and one-loop matrix elements for any Standard Model process
       at NLO QCD and NLO EW. """

    homepage = "https://openloops.hepforge.org/"
    url      = "https://openloops.hepforge.org/downloads?f=OpenLoops-2.1.1.tar.gz"

    tags = ['hep']

    version('2.1.2', sha256='f52575cae3d70b6b51a5d423e9cd0e076ed5961afcc015eec00987e64529a6ae')
    version('2.1.1', sha256='f1c47ece812227eab584e2c695fef74423d2f212873f762b8658f728685bcb91')

    all_processes = (
        'tbln', 'tbln_ew', 'tbqq', 'tbw', 'pptttt', 'pptttt_ew', 'pptt',
        'pptt_ew', 'ppttbb', 'ppttj', 'ppttj_ew', 'ppttjj', 'pptaj', 'pptajj',
        'pptllj', 'pptlljj', 'pptln', 'pptw', 'pptwj', 'pptzj', 'pptzjj',
        'ppthj', 'ppthjj', 'pptj', 'pptjj', 'ppjj', 'ppjj_ew', 'ppjjj',
        'ppjjj_ew', 'ppjjjj', 'pplllvvv_ew', 'ppatt', 'ppatt_ew', 'ppattj',
        'pplltt', 'pplltt_ew', 'ppllttj', 'ppllttj_ew', 'pplntt', 'pplnttj',
        'ppwtt', 'ppwtt_ew', 'ppwttj', 'ppwttj_ew', 'ppztt', 'ppztt_ew',
        'ppzttj', 'ppaatt', 'ppwwtt', 'ppzatt', 'ppzztt', 'ppvvvv', 'ppllaa',
        'ppllaaj', 'pplllla', 'ppvvv', 'ppvvv_ew', 'ppvvvj', 'ppaajj',
        'ppaajjj', 'pplla', 'pplla_ew', 'ppllaj', 'ppllaj_ew', 'ppllajj',
        'ppllll', 'ppllll_ew', 'ppllllbb', 'ppllllj', 'ppllnnjj_ew',
        'ppllnnjj_vbs', 'pplnaj_ckm', 'pplnajj', 'pplnajj_ckm', 'ppvv',
        'ppvv_ew', 'ppvvj', 'ppvvj_ew', 'ppwajj', 'ppwwjj', 'ppzajj',
        'ppzwj_ew', 'ppzwjj', 'ppzzjj', 'ppajj', 'ppajj_ew', 'ppajjj',
        'ppllj', 'ppllj_ew', 'pplljj', 'pplljj_ew', 'pplljjj', 'pplnj_ckm',
        'pplnjj', 'pplnjj_ckm', 'pplnjj_ew', 'pplnjjj', 'ppnnjj_ew', 'ppnnjjj',
        'ppvj', 'ppvj_ew', 'ppwj_ckm', 'ppwjj', 'ppwjj_ckm', 'ppwjj_ew',
        'ppwjjj', 'ppzjj', 'ppzjj_ew', 'ppzjjj', 'pphtt', 'pphtt_ew', 'pphttj',
        'pphlltt', 'pphll', 'pphll_ew', 'pphllj', 'pphllj_ew', 'pphlljj',
        'pphlljj_top', 'pphlnj_ckm', 'pphlnjj', 'pphv', 'pphv_ew', 'pphwjj',
        'pphzjj', 'pphhtt', 'pphhv', 'heftpphh', 'heftpphhj', 'heftpphhjj',
        'pphhjj_vbf', 'bbhj', 'heftpphj', 'heftpphjj', 'heftpphjjj', 'pphbb',
        'pphbbj', 'pphjj_vbf', 'pphjj_vbf_ew', 'eetttt', 'eettttj', 'eellllbb',
        'eett', 'eett_ew', 'eettj', 'eettjj', 'eevtt', 'eevttj', 'eevttjj',
        'eevvtt', 'eevvttj', 'eellll_ew', 'eevv_ew', 'eevvjj', 'eell_ew',
        'eevjj', 'eehtt', 'eehttj', 'eehll_ew', 'eehvtt', 'eehhtt',
        'heftppllj', 'heftpplljj', 'heftpplljjj')

    variant('compile_extra', default=False,
            description='Compile real radiation tree amplitudes')
    variant('processes', description='Processes to install. See https://' +
                                     'openloops.hepforge.org/process_' +
                                     'library.php?repo=public for details',
            values=disjoint_sets(('all.coll',), ('lhc.coll',), ('lcg.coll',),
                                 all_processes).with_default('lhc.coll'))

    variant('num_jobs', description='Number of parallel jobs to run. '  +
                                    'Set to 1 if compiling a large number' +
                                    'of processes (e.g. lcg.coll)', default=0)
    depends_on('python', type=("build", "run"))

    phases = ['configure', 'build', 'build_processes', 'install']

    def configure(self, spec, prefix):
        spack_env = ('PATH LD_LIBRARY_PATH CPATH C_INCLUDE_PATH' +
                     'CPLUS_INCLUDE_PATH INTEL_LICENSE_FILE').split()
        for k in env.keys():
            if k.startswith('SPACK_'):
                spack_env.append(k)

        spack_env = ' '.join(spack_env)
        is_intel = self.spec.satisfies('%intel')
        njobs = self.spec.variants['num_jobs'].value

        with open('openloops.cfg', 'w') as f:
            f.write('[OpenLoops]\n')
            f.write('import_env={0}\n'.format(spack_env))
            f.write('num_jobs = {0}\n'.format(njobs))
            f.write('process_lib_dir = {0}\n'.format(self.spec.prefix.proclib))
            f.write('cc = {0}\n'.format(env['SPACK_CC']))
            f.write('cxx = {0}\n'.format(env['SPACK_CXX']))
            f.write('fortran_compiler = {0}\n'.format(env['SPACK_FC']))
            if self.spec.satisfies('@1.3.1') and not is_intel:
                f.write('gfortran_f_flags = -ffree-line-length-none\n')
            if self.spec.satisfies('@2.1.1:') and not is_intel:
                f.write('gfortran_f_flags = -ffree-line-length-none ' +
                        '-fdollar-ok ')
                if self.spec.target.family == 'aarch64':
                    f.write('-mcmodel=small\n')
                else:
                    f.write('-mcmodel=medium\n')

        if self.spec.satisfies('@:1.999.999 processes=lcg.coll'):
            copy(join_path(os.path.dirname(__file__), 'sft1.coll'), 'lcg.coll')
        elif self.spec.satisfies('@2:2.1.2 processes=lcg.coll'):
            copy(join_path(os.path.dirname(__file__), 'sft2.coll'), 'lcg.coll')
        elif self.spec.satisfies('@2.1.2:2.99.99 processes=lcg.coll'):
            copy(join_path(os.path.dirname(__file__), 'sft3.coll'), 'lcg.coll')

    def build(self, spec, prefix):
        scons = Executable('./scons')
        scons('generator=1', 'compile=2')

    def build_processes(self, spec, prefix):
        ol = Executable('./openloops')
        processes = self.spec.variants['processes'].value
        if '+compile_extra' in self.spec:
            ce = 'compile_extra=1'
        else:
            ce = ''

        ol('libinstall', ce, *processes)

    def install(self, spec, prefix):
        install_tree(join_path(self.stage.path, 'spack-src'),
                     self.prefix,
                     ignore=lambda x: x in ('process_obj', 'process_src'))
