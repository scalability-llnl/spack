# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import platform
import re
from datetime import datetime
from glob import glob

import llnl.util.tty as tty
import spack.architecture as architecture
import spack.config
import spack.paths
import spack.store
from llnl.util.filesystem import working_dir
from spack.main import get_version
from spack.util.executable import which

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='debug_command')
    sp.add_parser('create-db-tarball',
                  help="create a tarball of Spack's installation metadata")
    sp.add_parser('report', help='print information useful for bug reports')


def _debug_tarball_suffix():
    now = datetime.now()
    suffix = now.strftime('%Y-%m-%d-%H%M%S')

    git = which('git')
    if not git:
        return 'nobranch-nogit-%s' % suffix

    with working_dir(spack.paths.prefix):
        if not os.path.isdir('.git'):
            return 'nobranch.nogit.%s' % suffix

        # Get symbolic branch name and strip any special chars (mainly '/')
        symbolic = git(
            'rev-parse', '--abbrev-ref', '--short', 'HEAD', output=str).strip()
        symbolic = re.sub(r'[^\w.-]', '-', symbolic)

        # Get the commit hash too.
        commit = git(
            'rev-parse', '--short', 'HEAD', output=str).strip()

        if symbolic == commit:
            return "nobranch.%s.%s" % (commit, suffix)
        else:
            return "%s.%s.%s" % (symbolic, commit, suffix)


def create_db_tarball(args):
    tar = which('tar')
    tarball_name = "spack-db.%s.tar.gz" % _debug_tarball_suffix()
    tarball_path = os.path.abspath(tarball_name)

    store = spack.store.store
    base = os.path.basename(str(store.root))
    transform_args = []
    if 'GNU' in tar('--version', output=str):
        transform_args = ['--transform', 's/^%s/%s/' % (base, tarball_name)]
    else:
        transform_args = ['-s', '/^%s/%s/' % (base, tarball_name)]

    wd = os.path.dirname(str(store.root))
    with working_dir(wd):
        files = [store.db._index_path]
        files += glob('%s/*/*/*/.spack/spec.yaml' % base)
        files = [os.path.relpath(f) for f in files]

        args = ['-czf', tarball_path]
        args += transform_args
        args += files
        tar(*args)

    tty.msg('Created %s' % tarball_name)


def report(args):
    print('* **Spack:**', get_version())
    print('* **Python:**', platform.python_version())
    print('* **Platform:**', architecture.Arch(
        architecture.platform(), 'frontend', 'frontend'))
    print('* **Concretizer:**', spack.config.get('config:concretizer'))


def debug(parser, args):
    action = {
        'create-db-tarball': create_db_tarball,
        'report': report,
    }
    action[args.debug_command](args)
