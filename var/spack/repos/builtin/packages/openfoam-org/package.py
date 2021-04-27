# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Original Author: Mark Olesen <mark.olesen@esi-group.com>
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Notes
# - The openfoam-org package is a modified version of the openfoam package.
#   If changes are needed here, consider if they should also be applied there.
#
# - mpi handling: WM_MPLIB=SYSTEMMPI and populate prefs.{csh,sh} with values
#   from spack.
#
# - Building with boost/cgal is not included, since some of the logic is not
#   entirely clear and thus untested.
# - Resolution of flex, zlib needs more attention (within OpenFOAM)
#
# Known issues
# - Combining +zoltan with +int64 has not been tested, but probably won't work.
# - Combining +mgridgen with +int64 or +float32 probably won't work.
#
##############################################################################
import glob
import re
import os

import llnl.util.tty as tty

from spack import *
from spack.pkg.builtin.openfoam import add_extra_files
from spack.pkg.builtin.openfoam import write_environ
from spack.pkg.builtin.openfoam import rewrite_environ_files
from spack.pkg.builtin.openfoam import mplib_content
from spack.pkg.builtin.openfoam import OpenfoamArch
from spack.util.environment import EnvironmentModifications


class OpenfoamOrg(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    The openfoam.org release is managed by the OpenFOAM Foundation Ltd as
    a licensee of the OPENFOAM trademark.
    This offering is not approved or endorsed by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    """

    homepage = "http://www.openfoam.org/"
    baseurl  = "https://github.com/OpenFOAM"
    url      = "https://github.com/OpenFOAM/OpenFOAM-4.x/archive/version-4.1.tar.gz"
    git      = "https://github.com/OpenFOAM/OpenFOAM-dev.git"

    version('develop', branch='master')
    version('8', sha256='94ba11cbaaa12fbb5b356e01758df403ac8832d69da309a5d79f76f42eb008fc',
            url=baseurl + '/OpenFOAM-8/archive/version-8.tar.gz')
    version('7', sha256='12389cf092dc032372617785822a597aee434a50a62db2a520ab35ba5a7548b5',
            url=baseurl + '/OpenFOAM-7/archive/version-7.tar.gz')
    version('6', sha256='32a6af4120e691ca2df29c5b9bd7bc7a3e11208947f9bccf6087cfff5492f025',
            url=baseurl + '/OpenFOAM-6/archive/version-6.tar.gz')
    version('5.0', sha256='9057d6a8bb9fa18802881feba215215699065e0b3c5cdd0c0e84cb29c9916c89',
            url=baseurl + '/OpenFOAM-5.x/archive/version-5.0.tar.gz')
    version('4.1', sha256='2de18de64e7abdb1b649ad8e9d2d58b77a2b188fb5bcb6f7c2a038282081fd31',
            url=baseurl + '/OpenFOAM-4.x/archive/version-4.1.tar.gz')
    version('2.4.0', sha256='9529aa7441b64210c400c019dcb2e0410fcfd62a6f62d23b6c5994c4753c4465',
            url=baseurl + '/OpenFOAM-2.4.x/archive/version-2.4.0.tar.gz')
    version('2.3.1', sha256='2bbcf4d5932397c2087a9b6d7eeee6d2b1350c8ea4f455415f05e7cd94d9e5ba',
            url='http://downloads.sourceforge.net/foam/OpenFOAM-2.3.1.tgz')

    variant('int64', default=False,
            description='Compile with 64-bit label')
    variant('float32', default=False,
            description='Compile with 32-bit scalar (single-precision)')
    variant('source', default=True,
            description='Install library/application sources and tutorials')
    variant('metis', default=False,
            description='With metis decomposition')

    depends_on('mpi')
    depends_on('zlib')
    depends_on('flex')
    depends_on('cmake', type='build')

    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    depends_on('scotch~metis+mpi~int64', when='~int64')
    depends_on('scotch~metis+mpi+int64', when='+int64')

    depends_on('metis@5:', when='+metis')
    depends_on('metis+int64', when='+metis+int64')

    # General patches - foamEtcFile as per openfoam.com (robuster)
    common = ['spack-Allwmake', 'README-spack']
    assets = ['bin/foamEtcFile']

    # Version-specific patches
    patch('https://github.com/OpenFOAM/OpenFOAM-7/commit/ef33cf38ac9b811072a8970c71fbda35a90f6641.patch',
          sha256='73103e6b1bdbf3b1e0d517cbbd11562e98c6e9464df5f43e5125e9a5b457d1c5', when='@7')
    patch('50-etc.patch', when='@5.0:5.9')
    patch('41-etc.patch', when='@4.1')
    patch('41-site.patch', when='@4.1:')
    patch('240-etc.patch', when='@:2.4.0')
    patch('isnan.patch', when='@:2.4.0')
    # Add support for SYSTEMMPI
    patch('https://github.com/OpenFOAM/OpenFOAM-2.3.x/commit/ae9a670c99472787f3a5446ac2b522bf3519b796.patch',
          sha256='6c4c535baca3ce64035d512265c4ce8effd39de7602c923c5e19985db68b632a', when='@:2.3.1')

    # The openfoam architecture, compiler information etc
    _foam_arch = None

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}

    phases = ['configure', 'build', 'install']
    build_script = './spack-Allwmake'  # <- Added by patch() method.

    #
    # - End of definitions / setup -
    #

    # Some user config settings
    @property
    def config(self):
        settings = {
            # Use SYSTEMMPI since openfoam-org doesn't have USERMPI
            'mplib': 'SYSTEMMPI',

            # Add links into bin/, lib/ (eg, for other applications)
            'link': False,
        }
        # OpenFOAM v2.4 and earlier lacks WM_LABEL_OPTION
        if self.spec.satisfies('@:2.4'):
            settings['label-size'] = False
        return settings

    def setup_run_environment(self, env):
        bashrc = self.prefix.etc.bashrc
        try:
            env.extend(EnvironmentModifications.from_sourcing_file(
                bashrc, clean=True
            ))
        except Exception as e:
            msg = 'unexpected error when sourcing OpenFOAM bashrc [{0}]'
            tty.warn(msg.format(str(e)))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Location of the OpenFOAM project directory.
        This is identical to the WM_PROJECT_DIR value, but we avoid that
        variable since it would mask the normal OpenFOAM cleanup of
        previous versions.
        """
        env.set('FOAM_PROJECT_DIR', self.projectdir)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Location of the OpenFOAM project directory.
        This is identical to the WM_PROJECT_DIR value, but we avoid that
        variable since it would mask the normal OpenFOAM cleanup of
        previous versions.
        """
        env.set('FOAM_PROJECT_DIR', self.projectdir)

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return self.prefix  # <- install directly under prefix

    @property
    def foam_arch(self):
        if not self._foam_arch:
            self._foam_arch = OpenfoamOrgArch(self.spec, **self.config)
        return self._foam_arch

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        return join_path('platforms', self.foam_arch, 'bin')

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path('platforms', self.foam_arch, 'lib')

    def rename_source(self):
        """This is fairly horrible.
        The github tarfiles have weird names that do not correspond to the
        canonical name. We need to rename these, but leave a symlink for
        spack to work with.
        """
        # Note that this particular OpenFOAM requires absolute directories
        # to build correctly!
        parent   = os.path.dirname(self.stage.source_path)
        original = os.path.basename(self.stage.source_path)
        target   = 'OpenFOAM-{0}'.format(self.version)
        # Could also grep through etc/bashrc for WM_PROJECT_VERSION
        with working_dir(parent):
            if original != target and not os.path.lexists(target):
                os.rename(original, target)
                os.symlink(target, original)
                tty.info('renamed {0} -> {1}'.format(original, target))

    def patch(self):
        """Adjust OpenFOAM build for spack.
           Where needed, apply filter as an alternative to normal patching."""
        self.rename_source()
        add_extra_files(self, self.common, self.assets)

        # Avoid WM_PROJECT_INST_DIR for ThirdParty, site or jobControl.
        # Use openfoam-site.patch to handle jobControl, site.
        #
        # Filtering: bashrc,cshrc (using a patch is less flexible)
        edits = {
            'WM_THIRD_PARTY_DIR':
            r'$WM_PROJECT_DIR/ThirdParty #SPACK: No separate third-party',
            'WM_VERSION': str(self.version),  # consistency
            'FOAMY_HEX_MESH': '',  # This is horrible (unset variable?)
        }
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

    def configure(self, spec, prefix):
        """Make adjustments to the OpenFOAM configuration files in their various
        locations: etc/bashrc, etc/config.sh/FEATURE and customizations that
        don't properly fit get placed in the etc/prefs.sh file (similiarly for
        csh).
        """
        # Filtering bashrc, cshrc
        edits = {}
        edits.update(self.foam_arch.foam_dict())
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

        # MPI content, with absolute paths
        user_mpi = mplib_content(spec)

        # Content for etc/prefs.{csh,sh}
        self.etc_prefs = {
            r'MPI_ROOT': spec['mpi'].prefix,  # Absolute
            r'MPI_ARCH_FLAGS': '"%s"' % user_mpi['FLAGS'],
            r'MPI_ARCH_INC':   '"%s"' % user_mpi['PINC'],
            r'MPI_ARCH_LIBS':  '"%s"' % user_mpi['PLIBS'],
        }

        # Content for etc/config.{csh,sh}/ files
        self.etc_config = {
            'CGAL': {},
            'scotch': {},
            'metis': {},
            'paraview': [],
            'gperftools': [],  # Currently unused
        }

        if True:
            self.etc_config['scotch'] = {
                'SCOTCH_ARCH_PATH': spec['scotch'].prefix,
                # For src/parallel/decompose/Allwmake
                'SCOTCH_VERSION': 'scotch-{0}'.format(spec['scotch'].version),
            }

        if '+metis' in spec:
            self.etc_config['metis'] = {
                'METIS_ARCH_PATH': spec['metis'].prefix,
            }

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        if self.etc_prefs:
            write_environ(
                self.etc_prefs,
                posix=join_path('etc', 'prefs.sh'),
                cshell=join_path('etc', 'prefs.csh'))

        # Adjust components to use SPACK variants
        for component, subdict in self.etc_config.items():
            # Versions up to 3.0 used an etc/config/component.sh naming
            # convention instead of etc/config.sh/component
            if spec.satisfies('@:3.0'):
                write_environ(
                    subdict,
                    posix=join_path('etc', 'config',  component) + '.sh',
                    cshell=join_path('etc', 'config', component) + '.csh')
            else:
                write_environ(
                    subdict,
                    posix=join_path('etc', 'config.sh',  component),
                    cshell=join_path('etc', 'config.csh', component))

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        Only build if the compiler is known to be supported.
        """
        self.foam_arch.has_rule(self.stage.source_path)
        self.foam_arch.create_rules(self.stage.source_path, self)

        args = []
        if self.parallel:  # Build in parallel? - pass via the environment
            os.environ['WM_NCOMPPROCS'] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir"""
        mkdirp(self.projectdir)
        projdir = os.path.basename(self.projectdir)
        # Filtering: bashrc, cshrc
        edits = {
            'WM_PROJECT_INST_DIR': os.path.dirname(self.projectdir),
            'WM_PROJECT_DIR': join_path('$WM_PROJECT_INST_DIR', projdir),
        }

        # All top-level files, except spack build info and possibly Allwmake
        if '+source' in spec:
            ignored = re.compile(r'^spack-.*')
        else:
            ignored = re.compile(r'^(Allwmake|spack-).*')

        files = [
            f for f in glob.glob("*")
            if os.path.isfile(f) and not ignored.search(f)
        ]
        for f in files:
            install(f, self.projectdir)

        # Having wmake and ~source is actually somewhat pointless...
        # Install 'etc' before 'bin' (for symlinks)
        # META-INFO for 1812 and later (or backported)
        dirs = ['META-INFO', 'etc', 'bin', 'wmake']
        if '+source' in spec:
            dirs.extend(['applications', 'src', 'tutorials'])

        for d in dirs:
            if os.path.isdir(d):
                install_tree(
                    d,
                    join_path(self.projectdir, d),
                    symlinks=True)

        dirs = ['platforms']
        if '+source' in spec:
            dirs.extend(['doc'])

        # Install platforms (and doc) skipping intermediate targets
        relative_ignore_paths = ['src', 'applications', 'html', 'Guides']
        ignore = lambda p: p in relative_ignore_paths
        for d in dirs:
            install_tree(
                d,
                join_path(self.projectdir, d),
                ignore=ignore,
                symlinks=True)

        etc_dir = join_path(self.projectdir, 'etc')
        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            edits,
            posix=join_path(etc_dir, 'bashrc'),
            cshell=join_path(etc_dir, 'cshrc'))
        self.install_links()

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        # Make build log visible - it contains OpenFOAM-specific information
        with working_dir(self.projectdir):
            os.symlink(
                join_path(os.path.relpath(self.install_log_path)),
                join_path('log.' + str(self.foam_arch)))

        if not self.config['link']:
            return

        # ln -s platforms/linux64GccXXX/lib lib
        with working_dir(self.projectdir):
            if os.path.isdir(self.archlib):
                os.symlink(self.archlib, 'lib')

        # (cd bin && ln -s ../platforms/linux64GccXXX/bin/* .)
        with working_dir(join_path(self.projectdir, 'bin')):
            for f in [
                f for f in glob.glob(join_path('..', self.archbin, "*"))
                if os.path.isfile(f)
            ]:
                os.symlink(f, os.path.basename(f))


# -----------------------------------------------------------------------------

class OpenfoamOrgArch(OpenfoamArch):
    """An openfoam-org variant of OpenfoamArch
    """
    def update_arch(self, spec):
        """Handle differences in WM_ARCH naming
        """
        OpenfoamArch.update_arch(self, spec)

        # ARM64 (openfoam) -> Arm64 (openfoam-org)
        self.arch = self.arch.replace("ARM64", "Arm64")
