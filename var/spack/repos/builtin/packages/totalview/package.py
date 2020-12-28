# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Totalview(Package):
    """Totalview parallel debugger.

    Source must be made available to Spack
    externally, either by having the tarballs in the current working directory
    or having the tarballs in a Spack mirror.

    The documentation tarball will
    be used as the primary source and the architecture appropriate tarball will
    be downloaded as a resource."""

    homepage = "https://www.roguewave.com/products-services/totalview"
    maintainers = ['nicholas-sly']
    manual_download = True
    license_required = True
    license_comment = '#'
    license_files = ['licenses/license.dat']
    license_vars = ['TV_LICENSE_FILE']

    # As the install of Totalview is via multiple tarballs, the base install
    # will be the documentation.  The architecture-specific tarballs are added
    # as resources dependent on the specific architecture used.
    version('2019.2.18',
            sha256='09e5c554032af945f8cf147dd548421267e50e906cc9686fb5cd0e8e63fcf650')

    # Distributed with Totalview
    variant('memoryscape', default=True, description='Install memoryscape')

    # Because the actual source tarball is architecture dependent, the main
    # download is the documentation tarball and the source is downloaded as a
    # resource once the target architecture is known.
    resource(
        name='x86_64',
        url='totalview_{0}_linux_x86-64.tar'.format(version),
        destination='.',
        sha256='3b0ab078deff3654ddc912a004d256f1376978aa1c4dd5a8a41fa9fbb474d07c',
        when='@2019.2.18 target=x86_64:')
    resource(
        name='aarch64',
        url='totalview_{0}_linux_arm64.tar'.format(version),
        destination='.',
        sha256='3bbda1aa7c06ce82874c1517bf949c9f6cbd0f4c9ebe283d21f0643f6e724b6b',
        when='@2019.2.18 target=aarch64:')
    resource(
        name='ppcle',
        url='totalview_{0}_linux_powerle.tar'.format(version),
        destination='.',
        sha256='c0e4dbf145312fc7143ad0b7e9474e653933581990e0b9d07237c73dbdff8365',
        when='@2019.2.18 target=ppc64le:')

    def url_for_version(self, version):
        return "file://{0}/totalview.{1}-doc.tar".format(os.getcwd(), version)

    def setup_run_environment(self, env):
        env.prepend_path('PATH',
                         join_path(self.prefix, 'toolworks',
                                   'totalview.{0}'.format(self.version), 'bin')
                         )
        env.prepend_path('TVROOT',
                         join_path(self.prefix, 'toolworks',
                                   'totalview.{0}'.format(self.version)))
        env.prepend_path('TVDSVRLAUNCHCMD', 'ssh')

    def install(self, spec, prefix):
        # Assemble install line
        install_cmd = which('./Install')
        arg_list = ["-agree", "-nosymlink", "-directory", "{0}".format(prefix)]

        # Platform specification.
        if spec.target.family == "x86_64":
            arg_list.extend(["-platform", "linux-x86-64"])
        elif spec.target.family == "x86":
            arg_list.extend(["-platform", "linux-x86"])
        elif spec.target.family == "aarch64":
            arg_list.extend(["-platform", "linux-arm64"])
        elif spec.target.family == "ppc64le":
            arg_list.extend(["-platform", "linux-powerle"])
        elif spec.target.family == "ppc64":
            arg_list.extend(["-platform", "linux-power"])
        else:
            raise InstallError('Architecture {0} not permitted!'
                               .format(spec.target.family))

        # Docs are the 'base' install used with every architecture.
        install_cmd.exe.extend(arg_list)
        install_cmd("-install", "doc-pdf")

        # Run install script for totalview and memoryscape (optional).
        with working_dir("./totalview.{0}".format(self.version)):

            install_cmd = which('./Install')
            arg_list.extend(["-install", "totalview"])
            # If including memoryscape.
            if '+memoryscape' in spec:
                arg_list.append("memoryscape")

            install_cmd.exe.extend(arg_list)
            install_cmd()
