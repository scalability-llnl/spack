# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re
import shutil

import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty
import llnl.util.tty.colify as colify
import spack.extensions
import spack.config
import spack.util.executable as executable

description = "manage custom extensions to Spack"
section = "commands"
level = "short"

# FIXME: generalize this mechanism
extensions_root = os.path.expanduser('~/.spack/extensions')

#: This is the git executable, wrapped into a lazy loader
git = lang.Singleton(lambda: executable.which('git', required=True))


def checkout_tag_or_branch(repository_dir, tag_or_branch):
    """Moves to a repository and checks out a given branch or tag

    Args:
        repository_dir (str): directory of the repository
        checkout_name (str): name of the branch or tag to checkout
        checkout_type (str): type of the checkout
    """
    with fs.working_dir(repository_dir):
        git('fetch', '--all', '--tags', output=os.devnull, error=os.devnull)
        git('checkout', tag_or_branch, output=os.devnull, error=os.devnull)
        git('pull', output=os.devnull, error=os.devnull)


def clone_repository(folder, url, branch_or_tag):
    """Clones a repository at a branch or tag in a given folder.

    Args:
        folder (str): root folder where the clone is performed
        url (str): url of the repository
        branch_or_tag (str): branch or tag to checkout
    """
    msg = 'Cloning custom extension from : {0}@{1}'
    tty.msg(msg.format(url, branch_or_tag))
    with fs.working_dir(folder, create=True):
        git('clone', '-q', '--branch', branch_or_tag, url)


def remote_url(repository_dir):
    """Returns the first remote url of a repository.

    Args:
        repository_dir (str): directory where the repository resides
    """
    with fs.working_dir(repository_dir):
        remote = git('remote', output=str).split().pop(0)
        url = git('remote', 'get-url', remote, output=str).strip()
    return url


def verify_user_url(url):
    """Verifies that the user url has the form we expect.

    Currently only urls from github.com are supported.

    Args:
        url: url as prompted on the cli by the user

    Returns:
        Return the user or organization, name of the extension and version

    Raises:
        ValueError: if the url is not valid
    """
    # TODO: Allow for different provenance than github.com
    github_regexp = r'github\.com/([\w]+)/(spack-[\w-]+)@?(.*)'
    m = re.match(github_regexp, url)
    if not m:
        msg = 'the url "{0}" does not match the required format r"{1}"'
        raise ValueError(msg.format(url, github_regexp))

    return m.group(1, 2, 3)


def analyze_repository(url):
    """Returns the branches and tags in a remote repository.

    Args:
        url (str): url of the repository to be analyzed

    Returns:
        The list of branches and tags
    """
    output = git('ls-remote', url, output=str)
    output = output.split()
    refs = output[1::2]
    tags = [x.replace('refs/tags/', '') for x in refs if 'refs/tags/' in x]
    branches = [
        x.replace('refs/heads/', '') for x in refs if 'refs/heads/' in x
    ]
    return branches, tags


def ensure_url_and_version(ext):
    """Ensures an extension has url and version set.

    Args:
        ext: extension to be checked

    Returns:
        True if the extension has been modified, False otherwise
    """
    updated = False
    folder = os.path.join(ext['root'], ext['name'])
    if not ext['url']:
        updated = True
        ext['url'] = remote_url(folder)
    if not ext['version']['value']:
        msg = 'Adding a version to the "{0}" extension'
        tty.msg(msg.format(ext['name']))
        updated = True
        ext['version'] = {
            'type': 'branch',
            'value': 'master'
        }
        checkout_tag_or_branch(folder, ext['version']['value'])
    return updated


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')

    # spack command-extensions get github.com/alalazo/spack-container@develop
    get_parser = sp.add_parser(
        'get', help='gets a custom extension from a URL'
    )
    get_parser.add_argument('url', help='the url of the custom extension')

    # spack command-extensions remove spack-container
    remove_parser = sp.add_parser(
        'remove', help='removes a currently installed extension'
    )
    remove_parser.add_argument(
        '--delete', action='store_true',
        help='deletes the extension source code'
    )
    remove_parser.add_argument('name', help='the name of the custom extension')

    # spack command extensions update spack-container
    # spack command extensions update spack-container@develop
    # spack command extensions update spack-container@v0.1.0
    # spack command extensions update spack-container@<hash>
    # spack command extensions update --all
    update_parser = sp.add_parser(
        'update', help='ensure a custom extension is up to date'
    )
    update_parser.add_argument(
        'url', help='the name of the custom extension', nargs='*'
    )

    # spack command extensions list
    sp.add_parser(
        'list', help='list all available custom extensions'
    )

    # spack command-extensions inspect
    inspect_parser = sp.add_parser(
        'inspect', help='returns information on a given extension'
    )
    inspect_parser.add_argument(
        'name', help='the name of the custom extension'
    )


def command_extensions_get(args):
    user_or_org, name, version = verify_user_url(args.url)
    extensions = spack.extensions.from_config()
    if any(e['name'] == name for e in extensions):
        msg = 'The extension "{0}" is already installed. If you want to ' \
              'modify it use the "spack command-extensions update" command '
        tty.msg(msg.format(name))
        return

    # Extract version information
    protocol = 'https://'
    full_url = protocol + '/'.join(['github.com', user_or_org, name]) + '.git'
    version = version or 'master'
    branches, tags = analyze_repository(full_url)
    version_type = None
    if version in branches:
        version_type = 'branch'
    elif version in tags:
        version_type = 'tag'
    if version_type is None:
        msg = 'cannot find branch or tag "{0}" in the repository at {1}'
        raise ValueError(msg.format(version, full_url))

    # Check if the repository is already on disk
    extension_dir = os.path.join(extensions_root, name)
    if not os.path.exists(extension_dir):
        clone_repository(extensions_root, full_url, version)
    else:
        # If it's not the same url and the extension was not
        # registered before wipe out what's there and clone again
        url = remote_url(extension_dir)
        if full_url != url:
            shutil.rmtree(extension_dir)
            clone_repository(extensions_root, full_url, version)
        else:
            # Else checkout the branch and pull
            msg = 'Repository {0} already present at {1}, checking-out "{2}"'
            tty.msg(msg.format(full_url, extension_dir, version))
            checkout_tag_or_branch(extension_dir, version)

    config_scope = spack.config.default_modify_scope()
    current_extensions = spack.extensions.from_config(scope=config_scope)
    current_extensions.append({
        'name': name,
        'version': {
            'type': version_type,
            'value': version
        },
        'root': extensions_root,
        'url': args.url
    })
    spack.config.set(
        'config:extensions', current_extensions, scope=config_scope
    )

    msg = 'Extension "{0}" has been installed and it is ready to be used'
    tty.msg(msg.format(name))


def command_extensions_remove(args):
    found = False
    for scope in spack.config.scopes():
        extensions = spack.extensions.from_config(scope=scope)
        if any(e['name'] == args.name for e in extensions):
            found = True
            updated = [x for x in extensions if x['name'] != args.name]
            spack.config.set('config:extensions', updated, scope=scope)
            msg = 'Extension "{0}" removed from "{1}" scope'
            tty.msg(msg.format(args.name, scope))
            if args.delete:
                to_delete = [x for x in extensions if x['name'] == args.name]
                for x in to_delete:
                    folder = os.path.join(x['root'], x['name'])
                    shutil.rmtree(folder)
                    msg = 'Removing folder {0}'
                    tty.debug(msg.format(folder))

    if not found:
        msg = 'Extension "{0}" is not installed'
        tty.msg(msg.format(args.name))


def command_extensions_update(args):
    for scope in spack.config.scopes():
        # Skip default scopes when updating as those are meant to be red-only
        if 'defaults' in scope:
            continue

        # If there are no extensions in this scope, skip it
        extensions = spack.extensions.from_config(scope=scope)
        if not extensions:
            continue

        # Construct a map name->version based on user input
        ext2ver = {}
        for x in args.url:
            name, _, version = x.partition('@')
            ext2ver[name] = version

        # Make sure the extensions fields are all assigned
        # (they could not be there if the extension comes
        # from the old format)
        updated = False
        for ext in extensions:
            # If the user specified a list of extensions, look
            # only for what matches
            name = ext['name']
            repository_dir = os.path.join(ext['root'], name)
            if ext2ver and name not in ext2ver:
                continue

            updated = True
            # The call below is needed to deal with the old string format
            ensure_url_and_version(ext)

            # Check if we have a specific version to check out
            version = ext2ver.get(ext['name'], None)
            if version:
                msg = 'Updating extension "{0}" in the "{1}" scope [@{2}]'
                tty.msg(msg.format(name, scope, version))
                checkout_tag_or_branch(repository_dir, version)
            else:
                msg = 'Updating extension "{0}" in the "{1}" scope'
                tty.msg(msg.format(name, scope, version))
                with fs.working_dir(repository_dir):
                    git('pull', output=os.devnull, error=os.devnull)

        if updated:
            spack.config.set('config:extensions', extensions, scope=scope)
            msg = 'Finished updating the "{0}" scope'
            tty.msg(msg.format(scope))


def command_extensions_list(args):
    found = False
    for scope in spack.config.scopes():
        extensions = spack.extensions.from_config(scope=scope)
        if extensions:
            found = True
            print('---- "{0}" scope ----'.format(scope))
            colify.colify([x['name'] for x in extensions], indent=4)
            print('')

    if not found:
        tty.msg('No extensions found')


def command_extensions_inspect(args):
    extensions = spack.extensions.from_config()
    try:
        selected = next(filter(lambda x: x['name'] == args.name, extensions))
    except StopIteration:
        tty.msg('Extension "{0}" not found'.format(args.name))
        return

    print('NAME:             {0}'.format(selected['name']))
    print('VERSION:          {0}'.format(selected['version']['value']))
    repository_dir = os.path.join(selected['root'], selected['name'])
    print('LOCAL REPOSITORY: {0}'.format(repository_dir))
    name = spack.extensions.extension_name(repository_dir)
    cmd_dir = os.path.join(repository_dir, name, 'cmd')
    commands = [f[:-3] for f in os.listdir(cmd_dir) if f.endswith('.py')]
    print('COMMANDS:         {0}'.format(', '.join(commands)))


def command_extensions(parser, args):
    subcommands = {
        'get': command_extensions_get,
        'remove': command_extensions_remove,
        'update': command_extensions_update,
        'list': command_extensions_list,
        'inspect': command_extensions_inspect
    }
    subcommands[args.subcommand](args)
