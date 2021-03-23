# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Mathematica(Package):
    """Mathematica: high-powered computation with thousands of Wolfram Language
       functions, natural language input, real-world data, mobile support.

       Note: A manual download is required for Mathematica.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.wolfram.com/mathematica/"
    url = 'file://{0}/Mathematica_12.0.0_LINUX.sh'.format(os.getcwd())
    manual_download = True

    version('12.1.1',
            sha256='ad47b886be4a9864d70f523f792615a051d4ebc987d9a0f654b645b4eb43b30a',
            expand=False)
    version('12.0.0',
            sha256='b9fb71e1afcc1d72c200196ffa434512d208fa2920e207878433f504e58ae9d7',
            expand=False)

    # Licensing
    license_required = True
    license_comment  = '#'
    license_files    = ['Configuration/Licensing/mathpass']
    license_url      = 'https://reference.wolfram.com/language/tutorial/RegistrationAndPasswords.html#857035062'

    def install(self, spec, prefix):
        # Backup .spack because Mathematica moves it but never restores it
        copy_tree(join_path(prefix, '.spack'),
                  join_path(self.stage.path, '.spack'))

        sh = which('sh')
        sh(self.stage.archive_file, '--', '-auto', '-verbose',
           '-targetdir={0}'.format(prefix),
           '-execdir={0}'.format(prefix.bin),
           '-selinux=y')
        # This is what most people would use on a cluster but the installer
        # does not symlink it
        ws_link_path = os.path.join(prefix.bin, 'wolframscript')
        if not os.path.exists(ws_link_path):
            ln = which('ln')
            ws_path = os.path.join(prefix, 'Executables', 'wolframscript')
            ln('-s', ws_path, ws_link_path)

        # Move back .spack where it belongs
        copy_tree(join_path(self.stage.path, '.spack'),
                  join_path(prefix, '.spack'))
