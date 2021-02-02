# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os

import llnl.util.tty as tty
import spack.cmd.common.deployment as deployment
import spack.config
import spack.repo
import spack.util.path

description = "manage package source repositories"
section = "config"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='repo_command')
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Create
    create_parser = sp.add_parser('create', help=repo_create.__doc__)
    create_parser.add_argument(
        'directory', help="directory to create the repo in")
    create_parser.add_argument(
        'namespace', help="namespace to identify packages in the repository. "
        "defaults to the directory name", nargs='?')

    # List
    list_parser = sp.add_parser('list', help=repo_list.__doc__)
    list_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from")

    # Add
    add_parser = sp.add_parser('add', help=repo_add.__doc__)
    add_parser.add_argument(
        'path', help="path to a Spack package repository directory")
    add_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser(
        'remove', help=repo_remove.__doc__, aliases=['rm'])
    remove_parser.add_argument(
        'namespace_or_path',
        help="namespace or path of a Spack package repository")
    remove_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")


def repo_create(args):
    """Create a new package repository."""
    full_path, namespace = spack.repo.create_repo(
        args.directory, args.namespace
    )
    tty.msg("Created repo with namespace '%s'." % namespace)
    tty.msg("To register it with spack, run this command:",
            'spack repo add %s' % full_path)


def repo_add(args):
    """Add a package source to Spack's configuration."""
    deployment.die_if_deployment('repo add')

    path = args.path

    # real_path is absolute and handles substitution.
    canon_path = spack.util.path.canonicalize_path(path)

    # check if the path exists
    if not os.path.exists(canon_path):
        tty.die("No such file or directory: %s" % path)

    # Make sure the path is a directory.
    if not os.path.isdir(canon_path):
        tty.die("Not a Spack repository: %s" % path)

    # Make sure it's actually a spack repository by constructing it.
    repo = spack.repo.Repo(canon_path)

    # If that succeeds, finally add it to the configuration.
    repos = spack.config.get('repos', scope=args.scope)
    if not repos:
        repos = []

    if repo.root in repos or path in repos:
        tty.die("Repository is already registered with Spack: %s" % path)

    repos.insert(0, canon_path)
    spack.config.set('repos', repos, args.scope)
    tty.msg("Added repo with namespace '%s'." % repo.namespace)


def repo_remove(args):
    """Remove a repository from Spack's configuration."""
    deployment.die_if_deployment('repo remove')

    repos = spack.config.get('repos', scope=args.scope)
    namespace_or_path = args.namespace_or_path

    # If the argument is a path, remove that repository from config.
    canon_path = spack.util.path.canonicalize_path(namespace_or_path)
    for repo_path in repos:
        repo_canon_path = spack.util.path.canonicalize_path(repo_path)
        if canon_path == repo_canon_path:
            repos.remove(repo_path)
            spack.config.set('repos', repos, args.scope)
            tty.msg("Removed repository %s" % repo_path)
            return

    # If it is a namespace, remove corresponding repo
    for path in repos:
        try:
            repo = spack.repo.Repo(path)
            if repo.namespace == namespace_or_path:
                repos.remove(path)
                spack.config.set('repos', repos, args.scope)
                tty.msg("Removed repository %s with namespace '%s'."
                        % (repo.root, repo.namespace))
                return
        except spack.repo.RepoError:
            continue

    tty.die("No repository with path or namespace: %s"
            % namespace_or_path)


def repo_list(args):
    """Show registered repositories and their namespaces."""
    roots = spack.config.get('repos', scope=args.scope)
    repos = []
    for r in roots:
        try:
            repos.append(spack.repo.Repo(r))
        except spack.repo.RepoError:
            continue

    msg = "%d package repositor" % len(repos)
    msg += "y." if len(repos) == 1 else "ies."
    tty.msg(msg)

    if not repos:
        return

    max_ns_len = max(len(r.namespace) for r in repos)
    for repo in repos:
        fmt = "%%-%ds%%s" % (max_ns_len + 4)
        print(fmt % (repo.namespace, repo.root))


def repo(parser, args):
    action = {'create': repo_create,
              'list': repo_list,
              'add': repo_add,
              'remove': repo_remove,
              'rm': repo_remove}
    action[args.repo_command](args)
