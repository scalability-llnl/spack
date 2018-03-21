##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import collections
import copy
import os
import shutil
import re

import spack.util.ordereddict

import py
import pytest

from llnl.util.filesystem import remove_linked_tree

import spack
import spack.architecture
import spack.database
import spack.directory_layout
import spack.platforms.test
import spack.repository
import spack.stage
import spack.util.executable
import spack.util.pattern
from spack.dependency import Dependency
from spack.package import PackageBase
from spack.fetch_strategy import FetchStrategyComposite, URLFetchStrategy
from spack.fetch_strategy import FetchError
from spack.spec import Spec
from spack.version import Version


#
# These fixtures are applied to all tests
#
@pytest.fixture(scope='function', autouse=True)
def no_chdir():
    """Ensure that no test changes Spack's working dirctory.

    This prevents Spack tests (and therefore Spack commands) from
    changing the working directory and causing other tests to fail
    mysteriously. Tests should use ``working_dir`` or ``py.path``'s
    ``.as_cwd()`` instead of ``os.chdir`` to avoid failing this check.

    We assert that the working directory hasn't changed, unless the
    original wd somehow ceased to exist.

    """
    original_wd = os.getcwd()
    yield
    if os.path.isdir(original_wd):
        assert os.getcwd() == original_wd


@pytest.fixture(scope='session', autouse=True)
def mock_stage(tmpdir_factory):
    """Mocks up a fake stage directory for use by tests."""
    stage_path = spack.stage_path
    new_stage = str(tmpdir_factory.mktemp('mock_stage'))
    spack.stage_path = new_stage
    yield new_stage
    spack.stage_path = stage_path


@pytest.fixture(scope='session')
def _ignore_stage_files():
    """Session-scoped helper for check_for_leftover_stage_files.

    Used to track which leftover files in the stage have been seen.
    """
    # to start with, ignore the .lock file at the stage root.
    return set(['.lock'])


def remove_whatever_it_is(path):
    """Type-agnostic remove."""
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.islink(path):
        remove_linked_tree(path)
    else:
        shutil.rmtree(path)


@pytest.fixture(scope='function', autouse=True)
def check_for_leftover_stage_files(request, mock_stage, _ignore_stage_files):
    """Ensure that each test leaves a clean stage when done.

    This can be disabled for tests that are expected to dirty the stage
    by adding::

        @pytest.mark.disable_clean_stage_check

    to tests that need it.
    """
    yield

    files_in_stage = set()
    if os.path.exists(spack.stage_path):
        files_in_stage = set(
            os.listdir(spack.stage_path)) - _ignore_stage_files

    if 'disable_clean_stage_check' in request.keywords:
        # clean up after tests that are expected to be dirty
        for f in files_in_stage:
            path = os.path.join(spack.stage_path, f)
            remove_whatever_it_is(path)
    else:
        _ignore_stage_files |= files_in_stage
        assert not files_in_stage


@pytest.fixture(autouse=True)
def mock_fetch_cache(monkeypatch):
    """Substitutes spack.fetch_cache with a mock object that does nothing
    and raises on fetch.
    """
    class MockCache(object):
        def store(self, copyCmd, relativeDst):
            pass

        def fetcher(self, targetPath, digest, **kwargs):
            return MockCacheFetcher()

    class MockCacheFetcher(object):
        def set_stage(self, stage):
            pass

        def fetch(self):
            raise FetchError('Mock cache always fails for tests')

        def __str__(self):
            return "[mock fetch cache]"

    monkeypatch.setattr(spack, 'fetch_cache', MockCache())


# FIXME: The lines below should better be added to a fixture with
# FIXME: session-scope. Anyhow doing it is not easy, as it seems
# FIXME: there's some weird interaction with compilers during concretization.
spack.architecture.real_platform = spack.architecture.platform
spack.architecture.platform = lambda: spack.platforms.test.Test()

##########
# Test-specific fixtures
##########


@pytest.fixture(scope='session')
def repo_path():
    """Session scoped RepoPath object pointing to the mock repository"""
    return spack.repository.RepoPath(spack.mock_packages_path)


@pytest.fixture(scope='module')
def builtin_mock(repo_path):
    """Uses the 'builtin.mock' repository instead of 'builtin'"""
    mock_repo = copy.deepcopy(repo_path)
    spack.repo.swap(mock_repo)
    BuiltinMock = collections.namedtuple('BuiltinMock', ['real', 'mock'])
    # Confusing, but we swapped above
    yield BuiltinMock(real=mock_repo, mock=spack.repo)
    spack.repo.swap(mock_repo)


@pytest.fixture()
def refresh_builtin_mock(builtin_mock, repo_path):
    """Refreshes the state of spack.repo"""
    # Get back the real repository
    mock_repo = copy.deepcopy(repo_path)
    spack.repo.swap(mock_repo)
    return builtin_mock


@pytest.fixture(scope='session')
def linux_os():
    """Returns a named tuple with attributes 'name' and 'version'
    representing the OS.
    """
    platform = spack.architecture.platform()
    name, version = 'debian', '6'
    if platform.name == 'linux':
        platform = spack.architecture.platform()
        current_os = platform.operating_system('default_os')
        name, version = current_os.name, current_os.version
    LinuxOS = collections.namedtuple('LinuxOS', ['name', 'version'])
    return LinuxOS(name=name, version=version)


@pytest.fixture(scope='session')
def configuration_dir(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory. Returns the
    directory path.
    """
    tmpdir = tmpdir_factory.mktemp('configurations')
    # Name of the yaml files in the test/data folder
    test_path = py.path.local(spack.test_path)
    compilers_yaml = test_path.join('data', 'compilers.yaml')
    packages_yaml = test_path.join('data', 'packages.yaml')
    config_yaml = test_path.join('data', 'config.yaml')
    # Create temporary 'site' and 'user' folders
    tmpdir.ensure('site', dir=True)
    tmpdir.ensure('user', dir=True)
    # Copy the configurations that don't need further work
    packages_yaml.copy(tmpdir.join('site', 'packages.yaml'))
    config_yaml.copy(tmpdir.join('site', 'config.yaml'))
    # Write the one that needs modifications
    content = ''.join(compilers_yaml.read()).format(linux_os)
    t = tmpdir.join('site', 'compilers.yaml')
    t.write(content)
    return tmpdir


@pytest.fixture(scope='module')
def config(configuration_dir):
    """Hooks the mock configuration files into spack.config"""
    # Set up a mock config scope
    spack.package_prefs.PackagePrefs.clear_caches()
    spack.config.clear_config_caches()
    real_scope = spack.config.config_scopes
    spack.config.config_scopes = spack.util.ordereddict.OrderedDict()
    spack.config.ConfigScope('site', str(configuration_dir.join('site')))
    spack.config.ConfigScope('system', str(configuration_dir.join('system')))
    spack.config.ConfigScope('user', str(configuration_dir.join('user')))
    Config = collections.namedtuple('Config', ['real', 'mock'])

    yield Config(real=real_scope, mock=spack.config.config_scopes)

    spack.config.config_scopes = real_scope
    spack.config.clear_config_caches()
    spack.package_prefs.PackagePrefs.clear_caches()


@pytest.fixture(scope='module')
def database(tmpdir_factory, builtin_mock, config):
    """Creates a mock database with some packages installed note that
    the ref count for dyninst here will be 3, as it's recycled
    across each install.
    """

    # Here is what the mock DB looks like:
    #
    # o  mpileaks     o  mpileaks'    o  mpileaks''
    # |\              |\              |\
    # | o  callpath   | o  callpath'  | o  callpath''
    # |/|             |/|             |/|
    # o |  mpich      o |  mpich2     o |  zmpi
    #   |               |             o |  fake
    #   |               |               |
    #   |               |______________/
    #   | .____________/
    #   |/
    #   o  dyninst
    #   |\
    #   | o  libdwarf
    #   |/
    #   o  libelf

    # Make a fake install directory
    install_path = tmpdir_factory.mktemp('install_for_database')
    spack_install_path = spack.store.root

    spack.store.root = str(install_path)
    install_layout = spack.directory_layout.YamlDirectoryLayout(
        str(install_path))
    spack_install_layout = spack.store.layout
    spack.store.layout = install_layout

    # Make fake database and fake install directory.
    install_db = spack.database.Database(str(install_path))
    spack_install_db = spack.store.db
    spack.store.db = install_db

    Entry = collections.namedtuple('Entry', ['path', 'layout', 'db'])
    Database = collections.namedtuple(
        'Database', ['real', 'mock', 'install', 'uninstall', 'refresh'])

    real = Entry(
        path=spack_install_path,
        layout=spack_install_layout,
        db=spack_install_db)
    mock = Entry(path=install_path, layout=install_layout, db=install_db)

    def _install(spec):
        s = spack.spec.Spec(spec)
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.do_install(fake=True)

    def _uninstall(spec):
        spec.package.do_uninstall(spec)

    def _refresh():
        with spack.store.db.write_transaction():
            for spec in spack.store.db.query():
                _uninstall(spec)
            _install('mpileaks ^mpich')
            _install('mpileaks ^mpich2')
            _install('mpileaks ^zmpi')
            _install('externaltest')

    t = Database(
        real=real,
        mock=mock,
        install=_install,
        uninstall=_uninstall,
        refresh=_refresh)

    # Transaction used to avoid repeated writes.
    with spack.store.db.write_transaction():
        t.install('mpileaks ^mpich')
        t.install('mpileaks ^mpich2')
        t.install('mpileaks ^zmpi')
        t.install('externaltest')

    yield t

    with spack.store.db.write_transaction():
        for spec in spack.store.db.query():
            if spec.package.installed:
                t.uninstall(spec)
            else:
                spack.store.db.remove(spec)

    install_path.remove(rec=1)
    spack.store.root = spack_install_path
    spack.store.layout = spack_install_layout
    spack.store.db = spack_install_db


@pytest.fixture()
def refresh_db_on_exit(database):
    """"Restores the state of the database after a test."""
    yield
    database.refresh()


@pytest.fixture()
def install_mockery(tmpdir, config, builtin_mock):
    """Hooks a fake install directory, DB, and stage directory into Spack."""
    layout = spack.store.layout
    extensions = spack.store.extensions
    db = spack.store.db
    new_opt = str(tmpdir.join('opt'))

    # Use a fake install directory to avoid conflicts bt/w
    # installed pkgs and mock packages.
    spack.store.layout = spack.directory_layout.YamlDirectoryLayout(new_opt)
    spack.store.extensions = spack.directory_layout.YamlExtensionsLayout(
        new_opt, spack.store.layout)
    spack.store.db = spack.database.Database(new_opt)

    # We use a fake package, so skip the checksum.
    spack.do_checksum = False
    yield
    # Turn checksumming back on
    spack.do_checksum = True
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.extensions = extensions
    spack.store.db = db


@pytest.fixture()
def mock_fetch(mock_archive):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(mock_archive.url))

    @property
    def fake_fn(self):
        return fetcher

    orig_fn = PackageBase.fetcher
    PackageBase.fetcher = fake_fn
    yield
    PackageBase.fetcher = orig_fn


##########
# Fake archives and repositories
##########


@pytest.fixture(scope='session')
def mock_archive(tmpdir_factory):
    """Creates a very simple archive directory with a configure script and a
    makefile that installs to a prefix. Tars it up into an archive.
    """
    tar = spack.util.executable.which('tar', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-archive-dir')
    repo_name = 'mock-archive-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)

    # Create the configure script
    configure_path = str(tmpdir.join(repo_name, 'configure'))
    with open(configure_path, 'w') as f:
        f.write(
            "#!/bin/sh\n"
            "prefix=$(echo $1 | sed 's/--prefix=//')\n"
            "cat > Makefile <<EOF\n"
            "all:\n"
            "\techo Building...\n\n"
            "install:\n"
            "\tmkdir -p $prefix\n"
            "\ttouch $prefix/dummy_file\n"
            "EOF\n"
        )
    os.chmod(configure_path, 0o755)

    # Archive it
    with tmpdir.as_cwd():
        archive_name = '{0}.tar.gz'.format(repo_name)
        tar('-czf', archive_name, repo_name)

    Archive = collections.namedtuple('Archive',
                                     ['url', 'path', 'archive_file'])
    archive_file = str(tmpdir.join(archive_name))

    # Return the url
    yield Archive(
        url=('file://' + archive_file),
        archive_file=archive_file,
        path=str(repodir))


@pytest.fixture(scope='session')
def mock_git_repository(tmpdir_factory):
    """Creates a very simple git repository with two branches and
    two commits.
    """
    git = spack.util.executable.which('git', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-git-repo-dir')
    repo_name = 'mock-git-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)

    # Initialize the repository
    with repodir.as_cwd():
        git('init')
        git('config', 'user.name', 'Spack')
        git('config', 'user.email', 'spack@spack.io')
        url = 'file://' + str(repodir)

        # r0 is just the first commit
        r0_file = 'r0_file'
        repodir.ensure(r0_file)
        git('add', r0_file)
        git('commit', '-m', 'mock-git-repo r0')

        branch = 'test-branch'
        branch_file = 'branch_file'
        git('branch', branch)

        tag_branch = 'tag-branch'
        tag_file = 'tag_file'
        git('branch', tag_branch)

        # Check out first branch
        git('checkout', branch)
        repodir.ensure(branch_file)
        git('add', branch_file)
        git('commit', '-m' 'r1 test branch')

        # Check out a second branch and tag it
        git('checkout', tag_branch)
        repodir.ensure(tag_file)
        git('add', tag_file)
        git('commit', '-m' 'tag test branch')

        tag = 'test-tag'
        git('tag', tag)

        git('checkout', 'master')

        # R1 test is the same as test for branch
        rev_hash = lambda x: git('rev-parse', x, output=str).strip()
        r1 = rev_hash(branch)
        r1_file = branch_file

    Bunch = spack.util.pattern.Bunch
    checks = {
        'master': Bunch(
            revision='master', file=r0_file, args={'git': str(repodir)}
        ),
        'branch': Bunch(
            revision=branch, file=branch_file, args={
                'git': str(repodir), 'branch': branch
            }
        ),
        'tag': Bunch(
            revision=tag, file=tag_file, args={'git': str(repodir), 'tag': tag}
        ),
        'commit': Bunch(
            revision=r1, file=r1_file, args={'git': str(repodir), 'commit': r1}
        )
    }

    t = Bunch(checks=checks, url=url, hash=rev_hash, path=str(repodir))
    yield t


@pytest.fixture(scope='session')
def mock_hg_repository(tmpdir_factory):
    """Creates a very simple hg repository with two commits."""
    hg = spack.util.executable.which('hg', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-hg-repo-dir')
    repo_name = 'mock-hg-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)

    get_rev = lambda: hg('id', '-i', output=str).strip()

    # Initialize the repository
    with repodir.as_cwd():
        url = 'file://' + str(repodir)
        hg('init')

        # Commit file r0
        r0_file = 'r0_file'
        repodir.ensure(r0_file)
        hg('add', r0_file)
        hg('commit', '-m', 'revision 0', '-u', 'test')
        r0 = get_rev()

        # Commit file r1
        r1_file = 'r1_file'
        repodir.ensure(r1_file)
        hg('add', r1_file)
        hg('commit', '-m' 'revision 1', '-u', 'test')
        r1 = get_rev()

    Bunch = spack.util.pattern.Bunch
    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'hg': str(repodir)}
        ),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'hg': str(repodir), 'revision': r0
            }
        )
    }
    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


@pytest.fixture(scope='session')
def mock_svn_repository(tmpdir_factory):
    """Creates a very simple svn repository with two commits."""
    svn = spack.util.executable.which('svn', required=True)
    svnadmin = spack.util.executable.which('svnadmin', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-svn-stage')
    repo_name = 'mock-svn-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)
    url = 'file://' + str(repodir)

    # Initialize the repository
    with repodir.as_cwd():
        # NOTE: Adding --pre-1.5-compatible works for NERSC
        # Unknown if this is also an issue at other sites.
        svnadmin('create', '--pre-1.5-compatible', str(repodir))

        # Import a structure (first commit)
        r0_file = 'r0_file'
        tmpdir.ensure('tmp-path', r0_file)
        tmp_path = tmpdir.join('tmp-path')
        svn('import',
            str(tmp_path),
            url,
            '-m',
            'Initial import r0')
        tmp_path.remove()

        # Second commit
        r1_file = 'r1_file'
        svn('checkout', url, str(tmp_path))
        tmpdir.ensure('tmp-path', r1_file)

        with tmp_path.as_cwd():
            svn('add', str(tmpdir.ensure('tmp-path', r1_file)))
            svn('ci', '-m', 'second revision r1')

        tmp_path.remove()
        r0 = '1'
        r1 = '2'

    Bunch = spack.util.pattern.Bunch
    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'svn': url}),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'svn': url, 'revision': r0})
    }

    def get_rev():
        output = svn('info', output=str)
        assert "Revision" in output
        for line in output.split('\n'):
            match = re.match(r'Revision: (\d+)', line)
            if match:
                return match.group(1)

    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


##########
# Mock packages
##########


class MockPackage(object):
    def __init__(self, name, dependencies, dependency_types, conditions=None,
                 versions=None):
        self.name = name
        self.spec = None
        self.dependencies = spack.util.ordereddict.OrderedDict()

        assert len(dependencies) == len(dependency_types)
        for dep, dtype in zip(dependencies, dependency_types):
            d = Dependency(self, Spec(dep.name), type=dtype)
            if not conditions or dep.name not in conditions:
                self.dependencies[dep.name] = {Spec(name): d}
            else:
                dep_conditions = conditions[dep.name]
                dep_conditions = dict(
                    (Spec(x), Dependency(self, Spec(y), type=dtype))
                    for x, y in dep_conditions.items())
                self.dependencies[dep.name] = dep_conditions

        if versions:
            self.versions = versions
        else:
            versions = list(Version(x) for x in [1, 2, 3])
            self.versions = dict((x, {'preferred': False}) for x in versions)

        self.variants = {}
        self.provided = {}
        self.conflicts = {}
        self.patches = {}


class MockPackageMultiRepo(object):
    def __init__(self, packages):
        self.spec_to_pkg = dict((x.name, x) for x in packages)
        self.spec_to_pkg.update(
            dict(('mockrepo.' + x.name, x) for x in packages))

    def get(self, spec):
        if not isinstance(spec, spack.spec.Spec):
            spec = Spec(spec)
        return self.spec_to_pkg[spec.name]

    def get_pkg_class(self, name):
        return self.spec_to_pkg[name]

    def exists(self, name):
        return name in self.spec_to_pkg

    def is_virtual(self, name):
        return False

    def repo_for_pkg(self, name):
        import collections
        Repo = collections.namedtuple('Repo', ['namespace'])
        return Repo('mockrepo')

##########
# Specs of various kind
##########


@pytest.fixture(
    params=[
        'conflict%clang',
        'conflict%clang+foo',
        'conflict-parent%clang',
        'conflict-parent@0.9^conflict~foo'
    ]
)
def conflict_spec(request):
    """Specs which violate constraints specified with the "conflicts"
    directive in the "conflict" package.
    """
    return request.param
