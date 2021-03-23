# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openrasmol(MakefilePackage):
    """RasMol is a molecular graphics program intended for the
       visualisation of proteins, nucleic acids and small molecules."""

    homepage = "http://www.openrasmol.org/"
    url      = "https://sourceforge.net/projects/openrasmol/files/RasMol/RasMol_2.7.5/RasMol-2.7.5.2.tar.gz"

    version('2.7.5.2', sha256='b975e6e69d5c6b161a81f04840945d2f220ac626245c61bcc6c56181b73a5718')

    depends_on('imake', type='build')
    depends_on('libxext', type='link')
    depends_on('libxi', type='link')

    depends_on('cbflib@0.9.2', type='link')
    depends_on('cqrlib@1.1.2', type='link')
    depends_on('cvector@1.0.3', type='link')
    depends_on('neartree@3.1', type='link')
    depends_on('xforms@1.0.91', type='link')

    patch('rasmol_noqa.patch')
    patch('rasmol_help.patch')

    def edit(self, spec, prefix):
        with working_dir('src'):
            # Imakefile
            bash = which('bash')
            bash('./rasmol_build_options.sh')
            # host.def
            with open('host.def', 'w') as f:
                f.write('#ifdef AfterVendorCF\n')
                f.write('#define CcCmd {0}\n'.format(spack_cc))
                f.write('#endif\n')

    def setup_build_environment(self, env):
        env.set('XFORMSLIB_DIR', self.spec['xforms'].prefix)
        env.set('CBFLIB_DIR', self.spec['cbflib'].prefix)
        env.set('CQRLIB_DIR', self.spec['cqrlib'].prefix)
        env.set('CVECTOR_DIR', self.spec['cvector'].prefix)
        env.set('NEARTREE_DIR', self.spec['neartree'].prefix)

    def build(self, spec, prefix):
        with working_dir('src'):
            bash = which('bash')
            bash('./build_all.sh')

    def install(self, spec, prefix):
        install_tree('./data', prefix.sample)
        install_tree('./doc', prefix.doc)
        with working_dir('src'):
            bash = which('bash')
            bash('./rasmol_install.sh', '--prefix={0}'.format(prefix))

    def test(self):
        testdir = self.test_suite.current_test_data_dir
        opts = []
        opts.append('-insecure')
        opts.append('-script')
        opts.append(join_path(testdir, 'test.rsc'))
        opts.append(join_path(self.prefix.sample, '1crn.pdb'))
        self.run_test('rasmol', options=opts)
