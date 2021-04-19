# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from six import StringIO

import pytest

import llnl.util.filesystem as fs

import spack.hash_types as ht
import spack.modules
import spack.environment as ev

from spack.cmd.env import _env_create
from spack.spec import Spec
from spack.main import SpackCommand, SpackCommandError
from spack.stage import stage_prefix

from spack.util.mock_package import MockPackageMultiRepo
import spack.util.spack_json as sjson
from spack.util.path import substitute_path_variables


# everything here uses the mock_env_path
pytestmark = [
    pytest.mark.usefixtures('mutable_mock_env_path', 'config', 'mutable_mock_repo'),
    pytest.mark.maybeslow
]

env        = SpackCommand('env')
install    = SpackCommand('install')
add        = SpackCommand('add')
remove     = SpackCommand('remove')
concretize = SpackCommand('concretize')
stage      = SpackCommand('stage')
uninstall  = SpackCommand('uninstall')
find       = SpackCommand('find')


def check_mpileaks_and_deps_in_view(viewdir):
    """Check that the expected install directories exist."""
    assert os.path.exists(str(viewdir.join('.spack', 'mpileaks')))
    assert os.path.exists(str(viewdir.join('.spack', 'libdwarf')))


def check_viewdir_removal(viewdir):
    """Check that the uninstall/removal worked."""
    assert (not os.path.exists(str(viewdir.join('.spack'))) or
            os.listdir(str(viewdir.join('.spack'))) == ['projections.yaml'])


@pytest.fixture()
def env_deactivate():
    yield
    spack.environment._active_environment = None
    os.environ.pop('SPACK_ENV', None)


def test_add():
    e = ev.create('test')
    e.add('mpileaks')
    assert Spec('mpileaks') in e.user_specs


def test_env_add_virtual():
    env('create', 'test')

    e = ev.read('test')
    e.add('mpi')
    e.concretize()

    hashes = e.concretized_order
    assert len(hashes) == 1
    spec = e.specs_by_hash[hashes[0]]
    assert spec.satisfies('mpi')


def test_env_add_nonexistant_fails():
    env('create', 'test')

    e = ev.read('test')
    with pytest.raises(ev.SpackEnvironmentError, match=r'no such package'):
        e.add('thispackagedoesnotexist')


def test_env_list(mutable_mock_env_path):
    env('create', 'foo')
    env('create', 'bar')
    env('create', 'baz')

    out = env('list')

    assert 'foo' in out
    assert 'bar' in out
    assert 'baz' in out

    # make sure `spack env list` skips invalid things in var/spack/env
    mutable_mock_env_path.join('.DS_Store').ensure(file=True)
    out = env('list')

    assert 'foo' in out
    assert 'bar' in out
    assert 'baz' in out
    assert '.DS_Store' not in out


def test_env_remove(capfd):
    env('create', 'foo')
    env('create', 'bar')

    out = env('list')
    assert 'foo' in out
    assert 'bar' in out

    foo = ev.read('foo')
    with foo:
        with pytest.raises(spack.main.SpackCommandError):
            with capfd.disabled():
                env('remove', '-y', 'foo')
        assert 'foo' in env('list')

    env('remove', '-y', 'foo')
    out = env('list')
    assert 'foo' not in out
    assert 'bar' in out

    env('remove', '-y', 'bar')
    out = env('list')
    assert 'foo' not in out
    assert 'bar' not in out


def test_concretize():
    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()
    env_specs = e._get_environment_specs()
    assert any(x.name == 'mpileaks' for x in env_specs)


def test_env_uninstalled_specs(install_mockery, mock_fetch):
    e = ev.create('test')
    e.add('cmake-client')
    e.concretize()
    assert any(s.name == 'cmake-client' for s in e.uninstalled_specs())
    e.install_all()
    assert not any(s.name == 'cmake-client' for s in e.uninstalled_specs())
    e.add('mpileaks')
    e.concretize()
    assert not any(s.name == 'cmake-client' for s in e.uninstalled_specs())
    assert any(s.name == 'mpileaks' for s in e.uninstalled_specs())


def test_env_install_all(install_mockery, mock_fetch):
    e = ev.create('test')
    e.add('cmake-client')
    e.concretize()
    e.install_all()
    env_specs = e._get_environment_specs()
    spec = next(x for x in env_specs if x.name == 'cmake-client')
    assert spec.package.installed


def test_env_install_single_spec(install_mockery, mock_fetch):
    env('create', 'test')
    install = SpackCommand('install')

    e = ev.read('test')
    with e:
        install('cmake-client')

    e = ev.read('test')
    assert e.user_specs[0].name == 'cmake-client'
    assert e.concretized_user_specs[0].name == 'cmake-client'
    assert e.specs_by_hash[e.concretized_order[0]].name == 'cmake-client'


def test_env_modifications_error_on_activate(
        install_mockery, mock_fetch, monkeypatch, capfd):
    env('create', 'test')
    install = SpackCommand('install')

    e = ev.read('test')
    with e:
        install('cmake-client')

    def setup_error(pkg, env):
        raise RuntimeError("cmake-client had issues!")

    pkg = spack.repo.path.get_pkg_class("cmake-client")
    monkeypatch.setattr(pkg, "setup_run_environment", setup_error)
    with e:
        pass

    _, err = capfd.readouterr()
    assert "cmake-client had issues!" in err
    assert "Warning: couldn't get environment settings" in err


def test_env_install_same_spec_twice(install_mockery, mock_fetch):
    env('create', 'test')

    e = ev.read('test')
    with e:
        # The first installation outputs the package prefix, updates the view
        out = install('cmake-client')
        assert 'Updating view at' in out

        # The second installation reports all packages already installed
        out = install('cmake-client')
        assert 'already installed' in out


def test_env_install_two_specs_same_dep(
        install_mockery, mock_fetch, tmpdir, capsys):
    """Test installation of two packages that share a dependency with no
    connection and the second specifying the dependency as a 'build'
    dependency.
    """
    path = tmpdir.join('spack.yaml')

    with tmpdir.as_cwd():
        with open(str(path), 'w') as f:
            f.write("""\
env:
  specs:
  - a
  - depb
""")

        env('create', 'test', 'spack.yaml')

    with ev.read('test'):
        with capsys.disabled():
            out = install()

    # Ensure both packages reach install phase processing and are installed
    out = str(out)
    assert 'depb: Executing phase:' in out
    assert 'a: Executing phase:' in out

    depb = spack.repo.path.get_pkg_class('depb')
    assert depb.installed, 'Expected depb to be installed'

    a = spack.repo.path.get_pkg_class('a')
    assert a.installed, 'Expected a to be installed'


def test_remove_after_concretize():
    e = ev.create('test')

    e.add('mpileaks')
    e.concretize()

    e.add('python')
    e.concretize()

    e.remove('mpileaks')
    assert Spec('mpileaks') not in e.user_specs
    env_specs = e._get_environment_specs()
    assert any(s.name == 'mpileaks' for s in env_specs)

    e.add('mpileaks')
    assert any(s.name == 'mpileaks' for s in e.user_specs)

    e.remove('mpileaks', force=True)
    assert Spec('mpileaks') not in e.user_specs
    env_specs = e._get_environment_specs()
    assert not any(s.name == 'mpileaks' for s in env_specs)


def test_remove_command():
    env('create', 'test')
    assert 'test' in env('list')

    with ev.read('test'):
        add('mpileaks')
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        remove('mpileaks')
        assert 'mpileaks' not in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        add('mpileaks')
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        concretize()
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' in find('--show-concretized')

    with ev.read('test'):
        remove('mpileaks')
        assert 'mpileaks' not in find()
        # removed but still in last concretized specs
        assert 'mpileaks@' in find('--show-concretized')

    with ev.read('test'):
        concretize()
        assert 'mpileaks' not in find()
        assert 'mpileaks@' not in find()
        # now the lockfile is regenerated and it's gone.
        assert 'mpileaks@' not in find('--show-concretized')


def test_environment_status(capsys, tmpdir):
    with tmpdir.as_cwd():
        with capsys.disabled():
            assert 'No active environment' in env('status')

        with ev.create('test'):
            with capsys.disabled():
                assert 'In environment test' in env('status')

        with ev.Environment('local_dir'):
            with capsys.disabled():
                assert os.path.join(os.getcwd(), 'local_dir') in env('status')

            e = ev.Environment('myproject')
            e.write()
            with tmpdir.join('myproject').as_cwd():
                with e:
                    with capsys.disabled():
                        assert 'in current directory' in env('status')


def test_env_status_broken_view(
    mutable_mock_env_path, mock_archive, mock_fetch, mock_packages,
    install_mockery
):
    with ev.create('test'):
        install('trivial-install-test-package')

        # switch to a new repo that doesn't include the installed package
        # test that Spack detects the missing package and warns the user
        new_repo = MockPackageMultiRepo()
        with spack.repo.use_repositories(new_repo):
            output = env('status')
            assert 'In environment test' in output
            assert 'Environment test includes out of date' in output

        # Test that the warning goes away when it's fixed
        output = env('status')
        assert 'In environment test' in output
        assert 'Environment test includes out of date' not in output


def test_env_activate_broken_view(
    mutable_mock_env_path, mock_archive, mock_fetch, mock_packages,
    install_mockery
):
    with ev.create('test'):
        install('trivial-install-test-package')

    # switch to a new repo that doesn't include the installed package
    # test that Spack detects the missing package and fails gracefully
    new_repo = MockPackageMultiRepo()
    with spack.repo.use_repositories(new_repo):
        with pytest.raises(SpackCommandError):
            env('activate', '--sh', 'test')

    # test replacing repo fixes it
    env('activate', '--sh', 'test')


def test_to_lockfile_dict():
    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()
    context_dict = e._to_lockfile_dict()

    e_copy = ev.create('test_copy')

    e_copy._read_lockfile_dict(context_dict)
    assert e.specs_by_hash == e_copy.specs_by_hash


def test_env_repo():
    e = ev.create('test')
    e.add('mpileaks')
    e.write()

    with ev.read('test'):
        concretize()

    package = e.repo.get('mpileaks')
    assert package.name == 'mpileaks'
    assert package.namespace == 'builtin.mock'


def test_user_removed_spec():
    """Ensure a user can remove from any position in the spack.yaml file."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")

    before = ev.create('test', initial_yaml)
    before.concretize()
    before.write()

    # user modifies yaml externally to spack and removes hypre
    with open(before.manifest_path, 'w') as f:
        f.write("""\
env:
  specs:
  - mpileaks
  - libelf
""")

    after = ev.read('test')
    after.concretize()
    after.write()

    env_specs = after._get_environment_specs()
    read = ev.read('test')
    env_specs = read._get_environment_specs()

    assert not any(x.name == 'hypre' for x in env_specs)


def test_init_from_lockfile(tmpdir):
    """Test that an environment can be instantiated from a lockfile."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")
    e1 = ev.create('test', initial_yaml)
    e1.concretize()
    e1.write()

    e2 = ev.Environment(str(tmpdir), e1.lock_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    for h1, h2 in zip(e1.concretized_order, e2.concretized_order):
        assert h1 == h2
        assert e1.specs_by_hash[h1] == e2.specs_by_hash[h2]

    for s1, s2 in zip(e1.concretized_user_specs, e2.concretized_user_specs):
        assert s1 == s2


def test_init_from_yaml(tmpdir):
    """Test that an environment can be instantiated from a lockfile."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")
    e1 = ev.create('test', initial_yaml)
    e1.concretize()
    e1.write()

    e2 = ev.Environment(str(tmpdir), e1.manifest_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    assert not e2.concretized_order
    assert not e2.concretized_user_specs
    assert not e2.specs_by_hash


@pytest.mark.usefixtures('config')
def test_env_view_external_prefix(
        tmpdir_factory, mutable_database, mock_packages
):
    fake_prefix = tmpdir_factory.mktemp('a-prefix')
    fake_bin = fake_prefix.join('bin')
    fake_bin.ensure(dir=True)

    initial_yaml = StringIO("""\
env:
  specs:
  - a
  view: true
""")

    external_config = StringIO("""\
packages:
  a:
    externals:
    - spec: a@2.0
      prefix: {a_prefix}
    buildable: false
""".format(a_prefix=str(fake_prefix)))
    external_config_dict = spack.util.spack_yaml.load_config(external_config)

    test_scope = spack.config.InternalConfigScope(
        'env-external-test', data=external_config_dict)
    with spack.config.override(test_scope):

        e = ev.create('test', initial_yaml)
        e.concretize()
        # Note: normally installing specs in a test environment requires doing
        # a fake install, but not for external specs since no actions are
        # taken to install them. The installation commands also include
        # post-installation functions like DB-registration, so are important
        # to do (otherwise the package is not considered installed).
        e.install_all()
        e.write()

        env_modifications = e.add_default_view_to_shell('sh')
        individual_modifications = env_modifications.split('\n')

        def path_includes_fake_prefix(cmd):
            return 'export PATH' in cmd and str(fake_bin) in cmd

        assert any(
            path_includes_fake_prefix(cmd) for cmd in individual_modifications
        )


def test_init_with_file_and_remove(tmpdir):
    """Ensure a user can remove from any position in the spack.yaml file."""
    path = tmpdir.join('spack.yaml')

    with tmpdir.as_cwd():
        with open(str(path), 'w') as f:
            f.write("""\
env:
  specs:
  - mpileaks
""")

        env('create', 'test', 'spack.yaml')

    out = env('list')
    assert 'test' in out

    with ev.read('test'):
        assert 'mpileaks' in find()

    env('remove', '-y', 'test')

    out = env('list')
    assert 'test' not in out


def test_env_with_config():
    test_config = """\
env:
  specs:
  - mpileaks
  packages:
    mpileaks:
      version: [2.2]
"""
    _env_create('test', StringIO(test_config))

    e = ev.read('test')
    with e:
        e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_with_config_bad_include(env_deactivate, capfd):
    env_name = 'test_bad_include'
    test_config = """\
spack:
  include:
  - /no/such/directory
  - no/such/file.yaml
"""
    _env_create(env_name, StringIO(test_config))

    e = ev.read(env_name)
    with pytest.raises(SystemExit):
        with e:
            e.concretize()

    out, err = capfd.readouterr()

    assert 'missing include' in err
    assert '/no/such/directory' in err
    assert 'no/such/file.yaml' in err


def test_env_with_include_config_files_same_basename():
    test_config = """\
        env:
            include:
                - ./path/to/included-config.yaml
                - ./second/path/to/include-config.yaml
            specs:
                [libelf, mpileaks]
            """

    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    fs.mkdirp(os.path.join(e.path, 'path', 'to'))
    with open(os.path.join(
            e.path,
            './path/to/included-config.yaml'), 'w') as f:
        f.write("""\
        packages:
          libelf:
              version: [0.8.10]
        """)

    fs.mkdirp(os.path.join(e.path, 'second', 'path', 'to'))
    with open(os.path.join(
            e.path,
            './second/path/to/include-config.yaml'), 'w') as f:
        f.write("""\
        packages:
          mpileaks:
              version: [2.2]
        """)

    with e:
        e.concretize()

    environment_specs = e._get_environment_specs(False)

    assert(environment_specs[0].satisfies('libelf@0.8.10'))
    assert(environment_specs[1].satisfies('mpileaks@2.2'))


def test_env_with_included_config_file():
    test_config = """\
env:
  include:
  - ./included-config.yaml
  specs:
  - mpileaks
"""
    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'included-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    with e:
        e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_with_included_config_scope():
    config_scope_path = os.path.join(ev.root('test'), 'config')
    test_config = """\
env:
  include:
  - %s
  specs:
  - mpileaks
""" % config_scope_path

    _env_create('test', StringIO(test_config))

    e = ev.read('test')

    fs.mkdirp(config_scope_path)
    with open(os.path.join(config_scope_path, 'packages.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    with e:
        e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_with_included_config_var_path():
    config_var_path = os.path.join('$tempdir', 'included-config.yaml')
    test_config = """\
env:
  include:
  - %s
  specs:
  - mpileaks
""" % config_var_path

    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    config_real_path = substitute_path_variables(config_var_path)
    fs.mkdirp(os.path.dirname(config_real_path))
    with open(config_real_path, 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    with e:
        e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_config_precedence():
    test_config = """\
env:
  packages:
    libelf:
      version: [0.8.12]
  include:
  - ./included-config.yaml
  specs:
  - mpileaks
"""
    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'included-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
  libelf:
    version: [0.8.11]
""")

    with e:
        e.concretize()

    # ensure included scope took effect
    assert any(
        x.satisfies('mpileaks@2.2') for x in e._get_environment_specs())

    # ensure env file takes precedence
    assert any(
        x.satisfies('libelf@0.8.12') for x in e._get_environment_specs())


def test_included_config_precedence():
    test_config = """\
env:
  include:
  - ./high-config.yaml  # this one should take precedence
  - ./low-config.yaml
  specs:
  - mpileaks
"""
    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'high-config.yaml'), 'w') as f:
        f.write("""\
packages:
  libelf:
    version: [0.8.10]  # this should override libelf version below
""")

    with open(os.path.join(e.path, 'low-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
  libelf:
    version: [0.8.12]
""")

    with e:
        e.concretize()

    assert any(
        x.satisfies('mpileaks@2.2') for x in e._get_environment_specs())

    assert any(
        [x.satisfies('libelf@0.8.10') for x in e._get_environment_specs()])


def test_bad_env_yaml_format(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  spacks:
    - mpileaks
""")

    with tmpdir.as_cwd():
        with pytest.raises(spack.config.ConfigFormatError) as e:
            env('create', 'test', './spack.yaml')
        assert './spack.yaml:2' in str(e)
        assert "'spacks' was unexpected" in str(e)


def test_env_loads(install_mockery, mock_fetch):
    env('create', 'test')

    with ev.read('test'):
        add('mpileaks')
        concretize()
        install('--fake')

    with ev.read('test'):
        env('loads', 'test')

    e = ev.read('test')

    loads_file = os.path.join(e.path, 'loads')
    assert os.path.exists(loads_file)

    with open(loads_file) as f:
        contents = f.read()
        assert 'module load mpileaks' in contents


@pytest.mark.disable_clean_stage_check
def test_stage(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        add('zmpi')
        concretize()
        stage()

    root = str(mock_stage)

    def check_stage(spec):
        spec = Spec(spec).concretized()
        for dep in spec.traverse():
            stage_name = "{0}{1}-{2}-{3}".format(stage_prefix, dep.name,
                                                 dep.version, dep.dag_hash())
            assert os.path.isdir(os.path.join(root, stage_name))

    check_stage('mpileaks')
    check_stage('zmpi')


def test_env_commands_die_with_no_env_arg():
    # these fail in argparse when given no arg
    with pytest.raises(SystemExit):
        env('create')
    with pytest.raises(SystemExit):
        env('remove')

    # these have an optional env arg and raise errors via tty.die
    with pytest.raises(spack.main.SpackCommandError):
        env('loads')

    # This should NOT raise an error with no environment
    # it just tells the user there isn't an environment
    env('status')


def test_env_blocks_uninstall(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        install('--fake')

    out = uninstall('mpileaks', fail_on_error=False)
    assert uninstall.returncode == 1
    assert 'used by the following environments' in out


def test_roots_display_with_variants():
    env('create', 'test')
    with ev.read('test'):
        add('boost+shared')

    with ev.read('test'):
        out = find(output=str)

    assert "boost +shared" in out


def test_uninstall_removes_from_env(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        add('libelf')
        install('--fake')

    test = ev.read('test')
    assert any(s.name == 'mpileaks' for s in test.specs_by_hash.values())
    assert any(s.name == 'libelf' for s in test.specs_by_hash.values())

    with ev.read('test'):
        uninstall('-ya')

    test = ev.read('test')
    assert not test.specs_by_hash
    assert not test.concretized_order
    assert not test.user_specs


def create_v1_lockfile_dict(roots, all_specs):
    test_lockfile_dict = {
        "_meta": {
            "lockfile-version": 1,
            "file-type": "spack-lockfile"
        },
        "roots": list(
            {
                "hash": s.dag_hash(),
                "spec": s.name
            } for s in roots
        ),
        # Version one lockfiles use the dag hash without build deps as keys,
        # but they write out the full node dict (including build deps)
        "concrete_specs": dict(
            (s.dag_hash(), s.to_node_dict(hash=ht.build_hash))
            for s in all_specs
        )
    }
    return test_lockfile_dict


@pytest.mark.usefixtures('config')
def test_read_old_lock_and_write_new(tmpdir):
    build_only = ('build',)

    mock_repo = MockPackageMultiRepo()
    y = mock_repo.add_package('y', [], [])
    mock_repo.add_package('x', [y], [build_only])

    with spack.repo.use_repositories(mock_repo):
        x = Spec('x')
        x.concretize()

        y = x['y']

        test_lockfile_dict = create_v1_lockfile_dict([x], [x, y])

        test_lockfile_path = str(tmpdir.join('test.lock'))
        with open(test_lockfile_path, 'w') as f:
            sjson.dump(test_lockfile_dict, stream=f)

        _env_create('test', test_lockfile_path, with_view=False)

        e = ev.read('test')
        hashes = set(e._to_lockfile_dict()['concrete_specs'])
        # When the lockfile is rewritten, it should adopt the new hash scheme
        # which accounts for all dependencies, including build dependencies
        assert hashes == set([
            x.build_hash(),
            y.build_hash()])


@pytest.mark.usefixtures('config')
def test_read_old_lock_creates_backup(tmpdir):
    """When reading a version-1 lockfile, make sure that a backup of that file
    is created.
    """
    mock_repo = MockPackageMultiRepo()
    y = mock_repo.add_package('y', [], [])

    with spack.repo.use_repositories(mock_repo):
        y = Spec('y')
        y.concretize()

        test_lockfile_dict = create_v1_lockfile_dict([y], [y])

        env_root = tmpdir.mkdir('test-root')
        test_lockfile_path = str(env_root.join(ev.lockfile_name))
        with open(test_lockfile_path, 'w') as f:
            sjson.dump(test_lockfile_dict, stream=f)

        e = ev.Environment(str(env_root))
        assert os.path.exists(e._lock_backup_v1_path)
        with open(e._lock_backup_v1_path, 'r') as backup_v1_file:
            lockfile_dict_v1 = sjson.load(backup_v1_file)
        # Make sure that the backup file follows the v1 hash scheme
        assert y.dag_hash() in lockfile_dict_v1['concrete_specs']


@pytest.mark.usefixtures('config')
def test_indirect_build_dep():
    """Simple case of X->Y->Z where Y is a build/link dep and Z is a
    build-only dep. Make sure this concrete DAG is preserved when writing the
    environment out and reading it back.
    """
    default = ('build', 'link')
    build_only = ('build',)

    mock_repo = MockPackageMultiRepo()
    z = mock_repo.add_package('z', [], [])
    y = mock_repo.add_package('y', [z], [build_only])
    mock_repo.add_package('x', [y], [default])

    def noop(*args):
        pass
    setattr(mock_repo, 'dump_provenance', noop)

    with spack.repo.use_repositories(mock_repo):
        x_spec = Spec('x')
        x_concretized = x_spec.concretized()

        _env_create('test', with_view=False)
        e = ev.read('test')
        e.add(x_spec)
        e.concretize()
        e.write()

        e_read = ev.read('test')
        x_env_hash, = e_read.concretized_order

        x_env_spec = e_read.specs_by_hash[x_env_hash]
        assert x_env_spec == x_concretized


@pytest.mark.usefixtures('config')
def test_store_different_build_deps():
    r"""Ensure that an environment can store two instances of a build-only
    dependency::

              x       y
             /| (l)   | (b)
        (b) | y       z2
             \| (b)
              z1

    """
    default = ('build', 'link')
    build_only = ('build',)

    mock_repo = MockPackageMultiRepo()
    z = mock_repo.add_package('z', [], [])
    y = mock_repo.add_package('y', [z], [build_only])
    mock_repo.add_package('x', [y, z], [default, build_only])

    def noop(*args):
        pass
    setattr(mock_repo, 'dump_provenance', noop)

    with spack.repo.use_repositories(mock_repo):
        y_spec = Spec('y ^z@3')
        y_concretized = y_spec.concretized()

        x_spec = Spec('x ^z@2')
        x_concretized = x_spec.concretized()

        # Even though x chose a different 'z', it should choose the same y
        # according to the DAG hash (since build deps are excluded from
        # comparison by default). Although the dag hashes are equal, the specs
        # are not considered equal because they compare build deps.
        assert x_concretized['y'].dag_hash() == y_concretized.dag_hash()

        _env_create('test', with_view=False)
        e = ev.read('test')
        e.add(y_spec)
        e.add(x_spec)
        e.concretize()
        e.write()

        e_read = ev.read('test')
        y_env_hash, x_env_hash = e_read.concretized_order

        y_read = e_read.specs_by_hash[y_env_hash]
        x_read = e_read.specs_by_hash[x_env_hash]

        assert x_read['z'] != y_read['z']


def test_env_updates_view_install(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    with ev.read('test'):
        add('mpileaks')
        install('--fake')

    check_mpileaks_and_deps_in_view(view_dir)


def test_env_view_fails(
        tmpdir, mock_packages, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    with ev.read('test'):
        add('libelf')
        add('libelf cflags=-g')
        with pytest.raises(RuntimeError, match='merge blocked by file'):
            install('--fake')


def test_env_without_view_install(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    # Test enabling a view after installing specs
    env('create', '--without-view', 'test')

    test_env = ev.read('test')
    with pytest.raises(spack.environment.SpackEnvironmentError):
        test_env.default_view

    view_dir = tmpdir.mkdir('view')

    with ev.read('test'):
        add('mpileaks')
        install('--fake')

        env('view', 'enable', str(view_dir))

    # After enabling the view, the specs should be linked into the environment
    # view dir
    check_mpileaks_and_deps_in_view(view_dir)


def test_env_config_view_default(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    # This config doesn't mention whether a view is enabled
    test_config = """\
env:
  specs:
  - mpileaks
"""

    _env_create('test', StringIO(test_config))

    with ev.read('test'):
        install('--fake')

    e = ev.read('test')
    # Try retrieving the view object
    view = e.default_view.view()
    assert view.get_spec('mpileaks')


def test_env_updates_view_install_package(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    with ev.read('test'):
        install('--fake', 'mpileaks')

    assert os.path.exists(str(view_dir.join('.spack/mpileaks')))


def test_env_updates_view_add_concretize(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    install('--fake', 'mpileaks')
    with ev.read('test'):
        add('mpileaks')
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)


def test_env_updates_view_uninstall(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    with ev.read('test'):
        install('--fake', 'mpileaks')

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read('test'):
        uninstall('-ay')

    check_viewdir_removal(view_dir)


def test_env_updates_view_uninstall_referenced_elsewhere(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    install('--fake', 'mpileaks')
    with ev.read('test'):
        add('mpileaks')
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read('test'):
        uninstall('-ay')

    check_viewdir_removal(view_dir)


def test_env_updates_view_remove_concretize(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    install('--fake', 'mpileaks')
    with ev.read('test'):
        add('mpileaks')
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read('test'):
        remove('mpileaks')
        concretize()

    check_viewdir_removal(view_dir)


def test_env_updates_view_force_remove(
        tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.mkdir('view')
    env('create', '--with-view=%s' % view_dir, 'test')
    with ev.read('test'):
        install('--fake', 'mpileaks')

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read('test'):
        remove('-f', 'mpileaks')

    check_viewdir_removal(view_dir)


def test_env_activate_view_fails(
        tmpdir, mock_stage, mock_fetch, install_mockery, env_deactivate):
    """Sanity check on env activate to make sure it requires shell support"""
    out = env('activate', 'test')
    assert "To set up shell support" in out


def test_stack_yaml_definitions(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        test = ev.read('test')

        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_yaml_definitions_as_constraints(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - mpis: [mpich, openmpi]
  specs:
    - matrix:
      - [$packages]
      - [$^mpis]
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        test = ev.read('test')

        assert Spec('mpileaks^mpich') in test.user_specs
        assert Spec('callpath^mpich') in test.user_specs
        assert Spec('mpileaks^openmpi') in test.user_specs
        assert Spec('callpath^openmpi') in test.user_specs


def test_stack_yaml_definitions_as_constraints_on_matrix(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - mpis:
      - matrix:
        - [mpich]
        - ['@3.0.4', '@3.0.3']
  specs:
    - matrix:
      - [$packages]
      - [$^mpis]
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        test = ev.read('test')

        assert Spec('mpileaks^mpich@3.0.4') in test.user_specs
        assert Spec('callpath^mpich@3.0.4') in test.user_specs
        assert Spec('mpileaks^mpich@3.0.3') in test.user_specs
        assert Spec('callpath^mpich@3.0.3') in test.user_specs


@pytest.mark.regression('12095')
def test_stack_yaml_definitions_write_reference(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - indirect: [$packages]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        with ev.read('test'):
            concretize()
        test = ev.read('test')

        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_yaml_add_to_list(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            add('-l', 'packages', 'libelf')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_yaml_remove_from_list(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            remove('-l', 'packages', 'mpileaks')

        test = ev.read('test')

        assert Spec('mpileaks') not in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_yaml_remove_from_list_force(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - matrix:
        - [$packages]
        - [^mpich, ^zmpi]
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            concretize()
            remove('-f', '-l', 'packages', 'mpileaks')
            find_output = find('-c')

        assert 'mpileaks' not in find_output

        test = ev.read('test')
        assert len(test.user_specs) == 2
        assert Spec('callpath ^zmpi') in test.user_specs
        assert Spec('callpath ^mpich') in test.user_specs


def test_stack_yaml_remove_from_matrix_no_effect(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages:
        - matrix:
            - [mpileaks, callpath]
            - [target=be]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test') as e:
            before = e.user_specs.specs
            remove('-l', 'packages', 'mpileaks')
            after = e.user_specs.specs

            assert before == after


def test_stack_yaml_force_remove_from_matrix(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages:
        - matrix:
            - [mpileaks, callpath]
            - [target=be]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test') as e:
            concretize()

            before_user = e.user_specs.specs
            before_conc = e.concretized_user_specs

            remove('-f', '-l', 'packages', 'mpileaks')

            after_user = e.user_specs.specs
            after_conc = e.concretized_user_specs

            assert before_user == after_user

            mpileaks_spec = Spec('mpileaks target=be')
            assert mpileaks_spec in before_conc
            assert mpileaks_spec not in after_conc


def test_stack_concretize_extraneous_deps(tmpdir, config, mock_packages):
    # FIXME: The new concretizer doesn't handle yet soft
    # FIXME: constraints for stacks
    if spack.config.get('config:concretizer') == 'clingo':
        pytest.skip('Clingo concretizer does not support soft constraints')

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['^zmpi', '^mpich']
  specs:
    - $install
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            concretize()

        test = ev.read('test')

        for user, concrete in test.concretized_specs():
            assert concrete.concrete
            assert not user.concrete
            if user.name == 'libelf':
                assert not concrete.satisfies('^mpi', strict=True)
            elif user.name == 'mpileaks':
                assert concrete.satisfies('^mpi', strict=True)


def test_stack_concretize_extraneous_variants(tmpdir, config, mock_packages):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['~shared', '+shared']
  specs:
    - $install
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            concretize()

        test = ev.read('test')

        for user, concrete in test.concretized_specs():
            assert concrete.concrete
            assert not user.concrete
            if user.name == 'libelf':
                assert 'shared' not in concrete.variants
            if user.name  == 'mpileaks':
                assert (concrete.variants['shared'].value ==
                        user.variants['shared'].value)


def test_stack_concretize_extraneous_variants_with_dash(tmpdir, config,
                                                        mock_packages):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['shared=False', '+shared-libs']
  specs:
    - $install
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            concretize()

        ev.read('test')

        # Regression test for handling of variants with dashes in them
        # will fail before this point if code regresses
        assert True


def test_stack_definition_extension(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_definition_conditional_false(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: 'False'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') not in test.user_specs


def test_stack_definition_conditional_true(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: 'True'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_definition_conditional_with_variable(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: platform == 'test'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_definition_conditional_with_satisfaction(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
      when: arch.satisfies('platform=foo')  # will be "test" when testing
    - packages: [callpath]
      when: arch.satisfies('platform=test')
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') not in test.user_specs
        assert Spec('mpileaks') not in test.user_specs
        assert Spec('callpath') in test.user_specs


def test_stack_definition_complex_conditional(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: re.search(r'foo', hostname) and env['test'] == 'THISSHOULDBEFALSE'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')

        test = ev.read('test')

        assert Spec('libelf') in test.user_specs
        assert Spec('mpileaks') in test.user_specs
        assert Spec('callpath') not in test.user_specs


def test_stack_definition_conditional_invalid_variable(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: bad_variable == 'test'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        with pytest.raises(NameError):
            env('create', 'test', './spack.yaml')


def test_stack_definition_conditional_add_write(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: platform == 'test'
  specs:
    - $packages
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            add('-l', 'packages', 'zmpi')

        test = ev.read('test')

        packages_lists = list(filter(lambda x: 'packages' in x,
                                     test.yaml['env']['definitions']))

        assert len(packages_lists) == 2
        assert 'callpath' not in packages_lists[0]['packages']
        assert 'callpath' in packages_lists[1]['packages']
        assert 'zmpi' in packages_lists[0]['packages']
        assert 'zmpi' not in packages_lists[1]['packages']


def test_stack_combinatorial_view(tmpdir, mock_fetch, mock_packages,
                                  mock_archive, install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            assert os.path.exists(
                os.path.join(viewdir, spec.name, '%s-%s' %
                             (spec.version, spec.compiler.name)))


def test_stack_view_select(tmpdir, mock_fetch, mock_packages,
                           mock_archive, install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if spec.satisfies('%gcc'):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_stack_view_exclude(tmpdir, mock_fetch, mock_packages,
                            mock_archive, install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      exclude: [callpath]
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if not spec.satisfies('callpath'):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_stack_view_select_and_exclude(tmpdir, mock_fetch, mock_packages,
                                       mock_archive, install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if spec.satisfies('%gcc') and not spec.satisfies('callpath'):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_view_link_roots(tmpdir, mock_fetch, mock_packages, mock_archive,
                         install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      link: 'roots'
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if spec in test.roots() and (spec.satisfies('%gcc') and
                                         not spec.satisfies('callpath')):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_view_link_all(tmpdir, mock_fetch, mock_packages, mock_archive,
                       install_mockery):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      link: 'all'
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if spec.satisfies('%gcc') and not spec.satisfies('callpath'):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_stack_view_activate_from_default(tmpdir, mock_fetch, mock_packages,
                                          mock_archive, install_mockery,
                                          env_deactivate):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    default:
      root: %s
      select: ['%%gcc']""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        shell = env('activate', '--sh', 'test')

        assert 'PATH' in shell
        assert os.path.join(viewdir, 'bin') in shell
        assert 'FOOBAR=mpileaks' in shell


def test_stack_view_no_activate_without_default(tmpdir, mock_fetch,
                                                mock_packages, mock_archive,
                                                install_mockery,
                                                env_deactivate):
    filename = str(tmpdir.join('spack.yaml'))
    viewdir = str(tmpdir.join('view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    not-default:
      root: %s
      select: ['%%gcc']""" % viewdir)
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        shell = env('activate', '--sh', 'test')
        assert 'PATH' not in shell
        assert viewdir not in shell


def test_stack_view_multiple_views(tmpdir, mock_fetch, mock_packages,
                                   mock_archive, install_mockery,
                                   env_deactivate):
    filename = str(tmpdir.join('spack.yaml'))
    default_viewdir = str(tmpdir.join('default-view'))
    combin_viewdir = str(tmpdir.join('combinatorial-view'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    default:
      root: %s
      select: ['%%gcc']
    combinatorial:
      root: %s
      exclude: [callpath %%gcc]
      projections:
        'all': '{name}/{version}-{compiler.name}'""" % (default_viewdir,
                                                        combin_viewdir))
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        with ev.read('test'):
            install()

        shell = env('activate', '--sh', 'test')
        assert 'PATH' in shell
        assert os.path.join(default_viewdir, 'bin') in shell

        test = ev.read('test')
        for spec in test._get_environment_specs():
            if not spec.satisfies('callpath%gcc'):
                assert os.path.exists(
                    os.path.join(combin_viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))
            else:
                assert not os.path.exists(
                    os.path.join(combin_viewdir, spec.name, '%s-%s' %
                                 (spec.version, spec.compiler.name)))


def test_env_activate_sh_prints_shell_output(
        tmpdir, mock_stage, mock_fetch, install_mockery, env_deactivate
):
    """Check the shell commands output by ``spack env activate --sh``.

    This is a cursory check; ``share/spack/qa/setup-env-test.sh`` checks
    for correctness.
    """
    env('create', 'test', add_view=True)

    out = env('activate', '--sh', 'test')
    assert "export SPACK_ENV=" in out
    assert "export PS1=" not in out
    assert "alias despacktivate=" in out

    out = env('activate', '--sh', '--prompt', 'test')
    assert "export SPACK_ENV=" in out
    assert "export PS1=" in out
    assert "alias despacktivate=" in out


def test_env_activate_csh_prints_shell_output(
        tmpdir, mock_stage, mock_fetch, install_mockery, env_deactivate
):
    """Check the shell commands output by ``spack env activate --csh``."""
    env('create', 'test', add_view=True)

    out = env('activate', '--csh', 'test')
    assert "setenv SPACK_ENV" in out
    assert "setenv set prompt" not in out
    assert "alias despacktivate" in out

    out = env('activate', '--csh', '--prompt', 'test')
    assert "setenv SPACK_ENV" in out
    assert "set prompt=" in out
    assert "alias despacktivate" in out


@pytest.mark.regression('12719')
def test_env_activate_default_view_root_unconditional(env_deactivate,
                                                      mutable_mock_env_path):
    """Check that the root of the default view in the environment is added
    to the shell unconditionally."""
    env('create', 'test', add_view=True)

    with ev.read('test') as e:
        viewdir = e.default_view.root

    out = env('activate', '--sh', 'test')
    viewdir_bin = os.path.join(viewdir, 'bin')

    assert "export PATH={0}".format(viewdir_bin) in out or \
           "export PATH='{0}".format(viewdir_bin) in out or \
           'export PATH="{0}'.format(viewdir_bin) in out


def test_concretize_user_specs_together():
    e = ev.create('coconcretization')
    e.concretization = 'together'

    # Concretize a first time using 'mpich' as the MPI provider
    e.add('mpileaks')
    e.add('mpich')
    e.concretize()

    assert all('mpich' in spec for _, spec in e.concretized_specs())
    assert all('mpich2' not in spec for _, spec in e.concretized_specs())

    # Concretize a second time using 'mpich2' as the MPI provider
    e.remove('mpich')
    e.add('mpich2')
    e.concretize()

    assert all('mpich2' in spec for _, spec in e.concretized_specs())
    assert all('mpich' not in spec for _, spec in e.concretized_specs())

    # Concretize again without changing anything, check everything
    # stays the same
    e.concretize()

    assert all('mpich2' in spec for _, spec in e.concretized_specs())
    assert all('mpich' not in spec for _, spec in e.concretized_specs())


def test_cant_install_single_spec_when_concretizing_together():
    e = ev.create('coconcretization')
    e.concretization = 'together'

    with pytest.raises(ev.SpackEnvironmentError, match=r'cannot install'):
        e.concretize_and_add('zlib')
        e.install_all()


def test_duplicate_packages_raise_when_concretizing_together():
    e = ev.create('coconcretization')
    e.concretization = 'together'

    e.add('mpileaks+opt')
    e.add('mpileaks~opt')
    e.add('mpich')

    with pytest.raises(ev.SpackEnvironmentError, match=r'cannot contain more'):
        e.concretize()


def test_env_write_only_non_default():
    env('create', 'test')

    e = ev.read('test')
    with open(e.manifest_path, 'r') as f:
        yaml = f.read()

    assert yaml == ev.default_manifest_yaml


@pytest.mark.regression('20526')
def test_env_write_only_non_default_nested(tmpdir):
    # setup an environment file
    # the environment includes configuration because nested configs proved the
    # most difficult to avoid writing.
    filename = 'spack.yaml'
    filepath = str(tmpdir.join(filename))
    contents = """\
env:
  specs:
  - matrix:
    - [mpileaks]
  packages:
    mpileaks:
      compiler: [gcc]
  view: true
"""

    # create environment with some structure
    with open(filepath, 'w') as f:
        f.write(contents)
    env('create', 'test', filepath)

    # concretize
    with ev.read('test') as e:
        concretize()
        e.write()

        with open(e.manifest_path, 'r') as f:
            manifest = f.read()

    assert manifest == contents


@pytest.fixture
def packages_yaml_v015(tmpdir):
    """Return the path to an existing manifest in the v0.15.x format
    and the path to a non yet existing backup file.
    """
    raw_yaml = """
spack:
  specs:
  - mpich
  packages:
    cmake:
      paths:
        cmake@3.17.3: /usr
"""
    manifest = tmpdir.ensure('spack.yaml')
    backup_file = tmpdir.join('spack.yaml.bkp')
    manifest.write(raw_yaml)
    return manifest, backup_file


def test_update_anonymous_env(packages_yaml_v015):
    manifest, backup_file = packages_yaml_v015
    env('update', '-y', str(manifest.dirname))

    # The environment is now at the latest format
    assert ev.is_latest_format(str(manifest))
    # A backup file has been created and it's not at the latest format
    assert os.path.exists(str(backup_file))
    assert not ev.is_latest_format(str(backup_file))


def test_double_update(packages_yaml_v015):
    manifest, backup_file = packages_yaml_v015

    # Update the environment
    env('update', '-y', str(manifest.dirname))
    # Try to read the environment (it should not error)
    ev.create('test', str(manifest))
    # Updating again does nothing since the manifest is up-to-date
    env('update', '-y', str(manifest.dirname))

    # The environment is at the latest format
    assert ev.is_latest_format(str(manifest))
    # A backup file has been created and it's not at the latest format
    assert os.path.exists(str(backup_file))
    assert not ev.is_latest_format(str(backup_file))


def test_update_and_revert(packages_yaml_v015):
    manifest, backup_file = packages_yaml_v015

    # Update the environment
    env('update', '-y', str(manifest.dirname))
    assert os.path.exists(str(backup_file))
    assert not ev.is_latest_format(str(backup_file))
    assert ev.is_latest_format(str(manifest))

    # Revert to previous state
    env('revert', '-y', str(manifest.dirname))
    assert not os.path.exists(str(backup_file))
    assert not ev.is_latest_format(str(manifest))


def test_old_format_cant_be_updated_implicitly(packages_yaml_v015):
    manifest, backup_file = packages_yaml_v015
    env('activate', str(manifest.dirname))
    with pytest.raises(spack.main.SpackCommandError):
        add('hdf5')


@pytest.mark.regression('18147')
def test_can_update_attributes_with_override(tmpdir):
    spack_yaml = """
spack:
  mirrors::
    test: /foo/bar
  packages:
    cmake:
      paths:
        cmake@3.18.1: /usr
  specs:
  - hdf5
"""
    abspath = tmpdir.join('spack.yaml')
    abspath.write(spack_yaml)

    # Check that an update does not raise
    env('update', '-y', str(abspath.dirname))


@pytest.mark.regression('18338')
def test_newline_in_commented_sequence_is_not_an_issue(tmpdir):
    spack_yaml = """
spack:
  specs:
  - dyninst
  packages:
    libelf:
      externals:
      - spec: libelf@0.8.13
        modules:
        - libelf/3.18.1

  concretization: together
"""
    abspath = tmpdir.join('spack.yaml')
    abspath.write(spack_yaml)

    def extract_build_hash(environment):
        _, dyninst = next(iter(environment.specs_by_hash.items()))
        return dyninst['libelf'].build_hash()

    # Concretize a first time and create a lockfile
    with ev.Environment(str(tmpdir)) as e:
        concretize()
        libelf_first_hash = extract_build_hash(e)

    # Check that a second run won't error
    with ev.Environment(str(tmpdir)) as e:
        concretize()
        libelf_second_hash = extract_build_hash(e)

    assert libelf_first_hash == libelf_second_hash


@pytest.mark.regression('18441')
def test_lockfile_not_deleted_on_write_error(tmpdir, monkeypatch):
    raw_yaml = """
spack:
  specs:
  - dyninst
  packages:
    libelf:
      externals:
      - spec: libelf@0.8.13
        prefix: /usr
"""
    spack_yaml = tmpdir.join('spack.yaml')
    spack_yaml.write(raw_yaml)
    spack_lock = tmpdir.join('spack.lock')

    # Concretize a first time and create a lockfile
    with ev.Environment(str(tmpdir)):
        concretize()
    assert os.path.exists(str(spack_lock))

    # If I run concretize again and there's an error during write,
    # the spack.lock file shouldn't disappear from disk
    def _write_helper_raise(self, x, y):
        raise RuntimeError('some error')

    monkeypatch.setattr(
        ev.Environment, '_update_and_write_manifest', _write_helper_raise
    )
    with ev.Environment(str(tmpdir)) as e:
        e.concretize(force=True)
        with pytest.raises(RuntimeError):
            e.clear()
            e.write()
    assert os.path.exists(str(spack_lock))


def _setup_develop_packages(tmpdir):
    """Sets up a structure ./init_env/spack.yaml, ./build_folder, ./dest_env
       where spack.yaml has a relative develop path to build_folder"""
    init_env = tmpdir.join('init_env')
    build_folder = tmpdir.join('build_folder')
    dest_env = tmpdir.join('dest_env')

    fs.mkdirp(str(init_env))
    fs.mkdirp(str(build_folder))
    fs.mkdirp(str(dest_env))

    raw_yaml = """
spack:
  specs: ['mypkg1', 'mypkg2']
  develop:
  - path: ../build_folder
    spec: mypkg1@main
  - path: /some/other/path
    spec: mypkg2@main
"""
    spack_yaml = init_env.join('spack.yaml')
    spack_yaml.write(raw_yaml)

    return init_env, build_folder, dest_env, spack_yaml


def test_rewrite_rel_dev_path_new_dir(tmpdir):
    """Relative develop paths should be rewritten for new environments in
       a different directory from the original manifest file"""
    _, build_folder, dest_env, spack_yaml = _setup_develop_packages(tmpdir)

    env('create', '-d', str(dest_env), str(spack_yaml))
    with ev.Environment(str(dest_env)) as e:
        assert e.dev_specs[0]['path'] == str(build_folder)
        assert e.dev_specs[1]['path'] == '/some/other/path'


def test_rewrite_rel_dev_path_named_env(tmpdir):
    """Relative develop paths should by default be rewritten for new named
       environment"""
    _, build_folder, _, spack_yaml = _setup_develop_packages(tmpdir)
    env('create', 'named_env', str(spack_yaml))
    with ev.read('named_env') as e:
        assert e.dev_specs[0]['path'] == str(build_folder)
        assert e.dev_specs[1]['path'] == '/some/other/path'


def test_rewrite_rel_dev_path_original_dir(tmpdir):
    """Relative devevelop paths should not be rewritten when initializing an
       environment with root path set to the same directory"""
    init_env, _, _, spack_yaml = _setup_develop_packages(tmpdir)
    with ev.Environment(str(init_env), str(spack_yaml)) as e:
        assert e.dev_specs[0]['path'] == '../build_folder'
        assert e.dev_specs[1]['path'] == '/some/other/path'


def test_rewrite_rel_dev_path_create_original_dir(tmpdir):
    """Relative develop paths should not be rewritten when creating an
       environment in the original directory"""
    init_env, _, _, spack_yaml = _setup_develop_packages(tmpdir)
    env('create', '-d', str(init_env), str(spack_yaml))
    with ev.Environment(str(init_env)) as e:
        assert e.dev_specs[0]['path'] == '../build_folder'
        assert e.dev_specs[1]['path'] == '/some/other/path'


def test_does_not_rewrite_rel_dev_path_when_keep_relative_is_set(tmpdir):
    """Relative develop paths should not be rewritten when --keep-relative is
       passed to create"""
    _, _, _, spack_yaml = _setup_develop_packages(tmpdir)
    env('create', '--keep-relative', 'named_env', str(spack_yaml))
    with ev.read('named_env') as e:
        print(e.dev_specs)
        assert e.dev_specs[0]['path'] == '../build_folder'
        assert e.dev_specs[1]['path'] == '/some/other/path'
