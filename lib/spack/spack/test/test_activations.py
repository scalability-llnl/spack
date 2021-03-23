# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This includes tests for customized activation logic for specific packages
   (e.g. python and perl).
"""

import os
import pytest

import spack.spec
import spack.package
from llnl.util.link_tree import MergeConflictError
from spack.directory_layout import YamlDirectoryLayout
from spack.filesystem_view import YamlFilesystemView
from spack.repo import RepoPath


def create_ext_pkg(name, prefix, extendee_spec, monkeypatch):
    ext_spec = spack.spec.Spec(name)
    ext_spec._concrete = True

    ext_spec.package.spec.prefix = prefix
    ext_pkg = ext_spec.package

    # temporarily override extendee_spec property on the package
    monkeypatch.setattr(ext_pkg.__class__, "extendee_spec", extendee_spec)

    return ext_pkg


def create_python_ext_pkg(name, prefix, python_spec, monkeypatch,
                          namespace=None):
    ext_pkg = create_ext_pkg(name, prefix, python_spec, monkeypatch)
    ext_pkg.py_namespace = namespace
    return ext_pkg


def create_dir_structure(tmpdir, dir_structure):
    for fname, children in dir_structure.items():
        tmpdir.ensure(fname, dir=fname.endswith('/'))
        if children:
            create_dir_structure(tmpdir.join(fname), children)


@pytest.fixture()
def builtin_and_mock_packages():
    # These tests use mock_repo packages to test functionality of builtin
    # packages for python and perl. To test this we put the mock repo at lower
    # precedence than the builtin repo, so we test builtin.perl against
    # builtin.mock.perl-extension.
    repo_dirs = [spack.paths.packages_path, spack.paths.mock_packages_path]
    path = RepoPath(*repo_dirs)

    with spack.repo.use_repositories(path):
        yield


@pytest.fixture()
def python_and_extension_dirs(tmpdir, builtin_and_mock_packages):
    python_dirs = {
        'bin/': {
            'python': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': None
            }
        }
    }

    python_name = 'python'
    python_prefix = tmpdir.join(python_name)
    create_dir_structure(python_prefix, python_dirs)

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec.prefix = str(python_prefix)

    ext_dirs = {
        'bin/': {
            'py-ext-tool': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'py-extension1/': {
                        'sample.py': None
                    }
                }
            }
        }
    }

    ext_name = 'py-extension1'
    ext_prefix = tmpdir.join(ext_name)
    create_dir_structure(ext_prefix, ext_dirs)

    easy_install_location = 'lib/python2.7/site-packages/easy-install.pth'
    with open(str(ext_prefix.join(easy_install_location)), 'w') as f:
        f.write("""path/to/ext1.egg
path/to/setuptools.egg""")

    return str(python_prefix), str(ext_prefix)


@pytest.fixture()
def namespace_extensions(tmpdir, builtin_and_mock_packages):
    ext1_dirs = {
        'bin/': {
            'py-ext-tool1': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'examplenamespace/': {
                        '__init__.py': None,
                        'ext1_sample.py': None
                    }
                }
            }
        }
    }

    ext2_dirs = {
        'bin/': {
            'py-ext-tool2': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'examplenamespace/': {
                        '__init__.py': None,
                        'ext2_sample.py': None
                    }
                }
            }
        }
    }

    ext1_name = 'py-extension1'
    ext1_prefix = tmpdir.join(ext1_name)
    create_dir_structure(ext1_prefix, ext1_dirs)

    ext2_name = 'py-extension2'
    ext2_prefix = tmpdir.join(ext2_name)
    create_dir_structure(ext2_prefix, ext2_dirs)

    return str(ext1_prefix), str(ext2_prefix), 'examplenamespace'


def test_python_activation_with_files(tmpdir, python_and_extension_dirs,
                                      monkeypatch, builtin_and_mock_packages):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec.prefix = python_prefix

    ext_pkg = create_python_ext_pkg(
        'py-extension1', ext_prefix, python_spec, monkeypatch)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg, python_pkg.view())

    assert os.path.exists(os.path.join(python_prefix, 'bin/py-ext-tool'))

    easy_install_location = 'lib/python2.7/site-packages/easy-install.pth'
    with open(os.path.join(python_prefix, easy_install_location), 'r') as f:
        easy_install_contents = f.read()

    assert 'ext1.egg' in easy_install_contents
    assert 'setuptools.egg' not in easy_install_contents


def test_python_activation_view(tmpdir, python_and_extension_dirs,
                                builtin_and_mock_packages, monkeypatch):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec.prefix = python_prefix

    ext_pkg = create_python_ext_pkg('py-extension1', ext_prefix, python_spec,
                                    monkeypatch)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg, view)

    assert not os.path.exists(os.path.join(python_prefix, 'bin/py-ext-tool'))

    assert os.path.exists(os.path.join(view_dir, 'bin/py-ext-tool'))


def test_python_ignore_namespace_init_conflict(
        tmpdir, namespace_extensions, builtin_and_mock_packages, monkeypatch):
    """Test the view update logic in PythonPackage ignores conflicting
       instances of __init__ for packages which are in the same namespace.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = create_python_ext_pkg('py-extension1', ext1_prefix, python_spec,
                                     monkeypatch, py_namespace)
    ext2_pkg = create_python_ext_pkg('py-extension2', ext2_prefix, python_spec,
                                     monkeypatch, py_namespace)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    # Normally handled by Package.do_activate, but here we activate directly
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    python_pkg.activate(ext2_pkg, view)

    f1 = 'lib/python2.7/site-packages/examplenamespace/ext1_sample.py'
    f2 = 'lib/python2.7/site-packages/examplenamespace/ext2_sample.py'
    init_file = 'lib/python2.7/site-packages/examplenamespace/__init__.py'

    assert os.path.exists(os.path.join(view_dir, f1))
    assert os.path.exists(os.path.join(view_dir, f2))
    assert os.path.exists(os.path.join(view_dir, init_file))


def test_python_keep_namespace_init(
        tmpdir, namespace_extensions, builtin_and_mock_packages, monkeypatch):
    """Test the view update logic in PythonPackage keeps the namespace
       __init__ file as long as one package in the namespace still
       exists.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = create_python_ext_pkg('py-extension1', ext1_prefix, python_spec,
                                     monkeypatch, py_namespace)
    ext2_pkg = create_python_ext_pkg('py-extension2', ext2_prefix, python_spec,
                                     monkeypatch, py_namespace)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    # Normally handled by Package.do_activate, but here we activate directly
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    python_pkg.activate(ext2_pkg, view)
    view.extensions_layout.add_extension(python_spec, ext2_pkg.spec)

    f1 = 'lib/python2.7/site-packages/examplenamespace/ext1_sample.py'
    init_file = 'lib/python2.7/site-packages/examplenamespace/__init__.py'

    python_pkg.deactivate(ext1_pkg, view)
    view.extensions_layout.remove_extension(python_spec, ext1_pkg.spec)

    assert not os.path.exists(os.path.join(view_dir, f1))
    assert os.path.exists(os.path.join(view_dir, init_file))

    python_pkg.deactivate(ext2_pkg, view)
    view.extensions_layout.remove_extension(python_spec, ext2_pkg.spec)

    assert not os.path.exists(os.path.join(view_dir, init_file))


def test_python_namespace_conflict(tmpdir, namespace_extensions,
                                   monkeypatch, builtin_and_mock_packages):
    """Test the view update logic in PythonPackage reports an error when two
       python extensions with different namespaces have a conflicting __init__
       file.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions
    other_namespace = py_namespace + 'other'

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = create_python_ext_pkg('py-extension1', ext1_prefix, python_spec,
                                     monkeypatch, py_namespace)
    ext2_pkg = create_python_ext_pkg('py-extension2', ext2_prefix, python_spec,
                                     monkeypatch, other_namespace)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    with pytest.raises(MergeConflictError):
        python_pkg.activate(ext2_pkg, view)


@pytest.fixture()
def perl_and_extension_dirs(tmpdir, builtin_and_mock_packages):
    perl_dirs = {
        'bin/': {
            'perl': None
        },
        'lib/': {
            'site_perl/': {
                '5.24.1/': {
                    'x86_64-linux/': None
                }
            }
        }
    }

    perl_name = 'perl'
    perl_prefix = tmpdir.join(perl_name)
    create_dir_structure(perl_prefix, perl_dirs)

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = str(perl_prefix)

    ext_dirs = {
        'bin/': {
            'perl-ext-tool': None
        },
        'lib/': {
            'site_perl/': {
                '5.24.1/': {
                    'x86_64-linux/': {
                        'TestExt/': {
                        }
                    }
                }
            }
        }
    }

    ext_name = 'perl-extension'
    ext_prefix = tmpdir.join(ext_name)
    create_dir_structure(ext_prefix, ext_dirs)

    return str(perl_prefix), str(ext_prefix)


def test_perl_activation(tmpdir, builtin_and_mock_packages, monkeypatch):
    # Note the lib directory is based partly on the perl version
    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True

    perl_name = 'perl'
    tmpdir.ensure(perl_name, dir=True)

    perl_prefix = str(tmpdir.join(perl_name))
    # Set the prefix on the package's spec reference because that is a copy of
    # the original spec
    perl_spec.package.spec.prefix = perl_prefix

    ext_name = 'perl-extension'
    tmpdir.ensure(ext_name, dir=True)
    ext_pkg = create_ext_pkg(
        ext_name, str(tmpdir.join(ext_name)), perl_spec, monkeypatch)

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, perl_pkg.view())


def test_perl_activation_with_files(tmpdir, perl_and_extension_dirs,
                                    monkeypatch, builtin_and_mock_packages):
    perl_prefix, ext_prefix = perl_and_extension_dirs

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = perl_prefix

    ext_pkg = create_ext_pkg(
        'perl-extension', ext_prefix, perl_spec, monkeypatch)

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, perl_pkg.view())

    assert os.path.exists(os.path.join(perl_prefix, 'bin/perl-ext-tool'))


def test_perl_activation_view(tmpdir, perl_and_extension_dirs,
                              monkeypatch, builtin_and_mock_packages):
    perl_prefix, ext_prefix = perl_and_extension_dirs

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = perl_prefix

    ext_pkg = create_ext_pkg(
        'perl-extension', ext_prefix, perl_spec, monkeypatch)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, view)

    assert not os.path.exists(os.path.join(perl_prefix, 'bin/perl-ext-tool'))

    assert os.path.exists(os.path.join(view_dir, 'bin/perl-ext-tool'))


def test_is_activated_upstream_extendee(tmpdir, builtin_and_mock_packages,
                                        monkeypatch):
    """When an extendee is installed upstream, make sure that the extension
    spec is never considered to be globally activated for it.
    """
    extendee_spec = spack.spec.Spec('python')
    extendee_spec._concrete = True

    python_name = 'python'
    tmpdir.ensure(python_name, dir=True)

    python_prefix = str(tmpdir.join(python_name))
    # Set the prefix on the package's spec reference because that is a copy of
    # the original spec
    extendee_spec.package.spec.prefix = python_prefix
    monkeypatch.setattr(extendee_spec.package.__class__,
                        'installed_upstream', True)

    ext_name = 'py-extension1'
    tmpdir.ensure(ext_name, dir=True)
    ext_pkg = create_ext_pkg(
        ext_name, str(tmpdir.join(ext_name)), extendee_spec, monkeypatch)

    # The view should not be checked at all if the extendee is installed
    # upstream, so use 'None' here
    mock_view = None
    assert not ext_pkg.is_activated(mock_view)
