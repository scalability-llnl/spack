# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
import spack.bootstrap
import spack.relocate
import spack.binary_distribution
import os


def on_install_success(spec):
    """
    After successful install, use debugedit to change DW_TAG_comp_dir paths.
    """
    # Don't run in CI
    if os.environ.get("CI"):
        return

    tty.debug("Running post_install debugedit for %s" % spec)

    # create info for later relocation
    workdir = str(spec.prefix)
    spack.binary_distribution.write_buildinfo_file(spec, workdir)

    # read in the buildinfo file to get stage and install prefix
    buildinfo = spack.binary_distribution.read_buildinfo_file(workdir)

    # Derive list of binaries, old prefix (staging) and new prefix (install)
    old_prefix = os.path.join(buildinfo['stage_path'], 'spack-src')
    new_prefix = buildinfo['install_prefix']
    binaries = [os.path.join(buildinfo['install_prefix'], x)
                for x in buildinfo['relocate_binaries']]

    # Change the stage directory to install for DW_AT_comp_dir with debugedit
    spack.relocate.run_debugedit(binaries, new_prefix, comp_dirs=[old_prefix])
