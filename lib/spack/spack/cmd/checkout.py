# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.environment as ev
import spack.paths
import spack.repo
from spack.util.executable import which

_SPACK_UPSTREAM = 'https://github.com/spack/spack'

description = "update the spack prefix or subcomponent to a git ref"
section = "admin"
level = "long"

git = None


def setup_parser(subparser):
    subparser.add_argument(
        '-r', '--remote', action='store', default='origin',
        help="name of the git remote from which to fetch")
    subparser.add_argument(
        '--url', action='store', default=None,
        help="url to use if the remote does not already exist")

    subrepo_subparser = subparser.add_mutually_exclusive_group()
    subrepo_subparser.add_argument(
        '--env', action='store', default=None,
        help="checkout an environment instead of the Spack source")
    subrepo_subparser.add_argument(
        '--repo', action='store', default=None,
        help="checkout a Spack repo instead of the Spack source")

    subparser.add_argument(
        'ref', help="git reference to checkout")


def fetch_remote(remote, url):
    # Ensure we have the appropriate remote configured
    remotes = git('remote', output=str, errror=str).split('\n')
    if remote in remotes:
        remote_url = git('remote', 'get-url', remote, output=str, error=str)
        remote_url = remote_url.strip('\n')
        if url and remote_url != url:
            msg = "Git url %s does not match given url %s" % (remote_url, url)
            msg += " for remote '%s'. Either use the git url or" % remote
            msg += " specify a new remote name for the new url."
            tty.die(msg)
    elif not url:
        msg = "Spack requires url to checkout from unknown remote %s" % remote
        tty.die(msg)
    else:
        git('remote', 'add', remote, url)
    git('fetch', remote)


def known_commit_or_tag(ref):
    # No need to fetch for tags and commits if we have the ref already
    # Fetch on other types rather than failing here because a tree ref could
    # be ambiguous with a commit ref after fetching
    ref_type = git('cat-file', '-t', ref,
                   output=str, error=str, fail_on_error=False).strip('\n ')
    return ref_type in ('commit', 'tag')


def checkout(parser, args):
    remote = args.remote or 'origin'
    url = args.url
    ref = args.ref

    global git  # make git available to called methods
    git = which('git', required=True)

    work_dir = spack.paths.prefix

    # Set the appropriate workdir if we are modifying an environment or repo
    # instead of Spack itself
    if args.env:
        if ev.exists(args.env):
            work_dir = ev.read(args.env).path
        elif ev.is_env_dir(args.env):
            work_dir = ev.Environment(args.env)
        else:
            raise ValueError("'%s' is not a valid Spack environment." %
                             args.env)
    elif args.repo:
        if args.repo in spack.repo.path.by_namespace:
            work_dir = spack.repo.path.by_namespace[args.repo]
        else:
            raise ValueError("'%s' is not a valid Spack repo namespace." %
                             args.repo)

    with fs.working_dir(work_dir):
        # Always fetch branches
        # branches includes emptry string; since ref cannot be empty string,
        # this does not cause a bug and fixing it reduces code legibility
        branches = map(lambda b: b.strip('* '),
                       git('branch', output=str, error=str).split('\n'))
        if ref in branches or not known_commit_or_tag(ref):
            fetch_remote(remote, url)

        # For branches, ensure we're getting the version from the correct remote
        full_ref = '%s/%s' % (remote, ref) if ref in branches else ref
        git('checkout', full_ref)
