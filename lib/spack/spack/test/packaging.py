# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks the binary packaging infrastructure
"""
import os
import stat
import shutil
import pytest
import re
import platform

from llnl.util.filesystem import mkdirp

import spack.main
import spack.repo
import spack.store
import spack.binary_distribution as bindist
import spack.util.gpg
from spack.spec import Spec
from spack.paths import mock_gpg_keys_path
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.relocate import needs_binary_relocation, needs_text_relocation
from spack.relocate import relocate_text, relocate_links
from spack.relocate import macho_make_paths_relative
from spack.relocate import macho_make_paths_normal
from spack.relocate import _placeholder, macho_find_paths
from spack.relocate import file_is_relocatable


buildcache_cmd = spack.main.SpackCommand('buildcache')


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.skipif(not spack.util.gpg.has_gpg(),
                    reason='This test requires gpg')
@pytest.mark.usefixtures('install_mockery', 'mock_gnupghome')
def test_buildcache(mock_archive, tmpdir):
    # tweak patchelf to only do a download
    pspec = Spec("patchelf")
    pspec.concretize()
    pkg = spack.repo.get(pspec)
    fake_fetchify(pkg.fetcher, pkg)
    mkdirp(os.path.join(pkg.prefix, "bin"))
    patchelfscr = os.path.join(pkg.prefix, "bin", "patchelf")
    f = open(patchelfscr, 'w')
    body = """#!/bin/bash
echo $PATH"""
    f.write(body)
    f.close()
    st = os.stat(patchelfscr)
    os.chmod(patchelfscr, st.st_mode | stat.S_IEXEC)

    # Install the test package
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    fake_fetchify(mock_archive.url, pkg)
    pkg.do_install()
    pkghash = '/' + str(spec.dag_hash(7))

    # Put some non-relocatable file in there
    filename = os.path.join(spec.prefix, "dummy.txt")
    with open(filename, "w") as script:
        script.write(spec.prefix)

    # Create an absolute symlink
    linkname = os.path.join(spec.prefix, "link_to_dummy.txt")
    os.symlink(filename, linkname)

    # Create the build cache  and
    # put it directly into the mirror
    mirror_path = os.path.join(str(tmpdir), 'test-mirror')
    spack.mirror.create(mirror_path, specs=[])

    # register mirror with spack config
    mirrors = {'spack-mirror-test': 'file://' + mirror_path}
    spack.config.set('mirrors', mirrors)

    stage = spack.stage.Stage(
        mirrors['spack-mirror-test'], name="build_cache", keep=True)
    stage.create()

    create_args = ['create', '-a', '-f', '-d', mirror_path, pkghash]
    # Create a private key to sign package with if gpg2 available
    spack.util.gpg.create(name='test key 1', expires='0',
                          email='spack@googlegroups.com',
                          comment='Spack test key')

    create_args.insert(create_args.index('-a'), '--rebuild-index')

    create_tuple = tuple(create_args)
    buildcache_cmd(*create_tuple)
    # trigger overwrite warning
    buildcache_cmd(*create_tuple)

    # Reread the contents of the mirror so we can install it.
    bindist.binary_index.refresh_mirrors()

    # Uninstall the package
    pkg.do_uninstall(force=True)

    install_args = ['install', '-a', '-f', pkghash]
    install_tuple = tuple(install_args)
    # Test install
    buildcache_cmd(*install_tuple)

    files = os.listdir(spec.prefix)

    assert 'link_to_dummy.txt' in files
    assert 'dummy.txt' in files

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec.prefix)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])
    assert(buildinfo['relocate_links'] == ['link_to_dummy.txt'])

    # create build cache with relative path
    create_args.insert(create_args.index('-a'), '-f')
    create_args.insert(create_args.index('-a'), '-r')
    create_tuple = tuple(create_args)
    buildcache_cmd(*create_tuple)

    # Uninstall the package
    pkg.do_uninstall(force=True)

    buildcache_cmd(*install_tuple)

    # test overwrite install
    install_args.insert(install_args.index('-a'), '-f')
    install_tuple = tuple(install_args)
    buildcache_cmd(*install_tuple)

    files = os.listdir(spec.prefix)
    assert 'link_to_dummy.txt' in files
    assert 'dummy.txt' in files

    buildcache_cmd('keys')

    buildcache_cmd('list')

    buildcache_cmd('list')

    buildcache_cmd('list', 'trivial')

    # Copy a key to the mirror to have something to download
    shutil.copyfile(mock_gpg_keys_path + '/external.key',
                    mirror_path + '/external.key')

    buildcache_cmd('keys')

    buildcache_cmd('keys', '-f')

    buildcache_cmd('keys', '-i', '-t')

    # unregister mirror with spack config
    mirrors = {}
    spack.config.set('mirrors', mirrors)
    shutil.rmtree(mirror_path)
    stage.destroy()

    # Remove cached binary specs since we deleted the mirror
    bindist._cached_specs = set()


@pytest.mark.usefixtures('install_mockery')
def test_relocate_text(tmpdir):
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    with tmpdir.as_cwd():
        # Validate the text path replacement
        old_dir = '/home/spack/opt/spack'
        filename = 'dummy.txt'
        with open(filename, "w") as script:
            script.write(old_dir)
            script.close()
        filenames = [filename]
        new_dir = '/opt/rh/devtoolset/'
        # Singleton dict doesn't matter if Ordered
        relocate_text(filenames, {old_dir: new_dir})
        with open(filename, "r")as script:
            for line in script:
                assert(new_dir in line)
        assert(file_is_relocatable(os.path.realpath(filename)))
    # Remove cached binary specs since we deleted the mirror
    bindist._cached_specs = set()


def test_relocate_links(tmpdir):
    with tmpdir.as_cwd():
        old_layout_root = os.path.join(
            '%s' % tmpdir, 'home', 'spack', 'opt', 'spack')
        old_install_prefix = os.path.join(
            '%s' % old_layout_root, 'debian6', 'test')
        old_binname = os.path.join(old_install_prefix, 'binfile')
        placeholder = _placeholder(old_layout_root)
        re.sub(old_layout_root, placeholder, old_binname)
        filenames = ['link.ln', 'outsideprefix.ln']
        new_layout_root = os.path.join(
            '%s' % tmpdir, 'opt', 'rh', 'devtoolset')
        new_install_prefix = os.path.join(
            '%s' % new_layout_root, 'test', 'debian6')
        new_linkname = os.path.join(new_install_prefix, 'link.ln')
        new_linkname2 = os.path.join(new_install_prefix, 'outsideprefix.ln')
        new_binname = os.path.join(new_install_prefix, 'binfile')
        mkdirp(new_install_prefix)
        with open(new_binname, 'w') as f:
            f.write('\n')
        os.utime(new_binname, None)
        os.symlink(old_binname, new_linkname)
        os.symlink('/usr/lib/libc.so', new_linkname2)
        relocate_links(filenames, old_layout_root,
                       old_install_prefix, new_install_prefix)
        assert os.readlink(new_linkname) == new_binname
        assert os.readlink(new_linkname2) == '/usr/lib/libc.so'


def test_needs_relocation():

    assert needs_binary_relocation('application', 'x-sharedlib')
    assert needs_binary_relocation('application', 'x-executable')
    assert not needs_binary_relocation('application', 'x-octet-stream')
    assert not needs_binary_relocation('text', 'x-')
    assert needs_text_relocation('text', 'x-')
    assert not needs_text_relocation('symbolic link to', 'x-')

    assert needs_binary_relocation('application', 'x-mach-binary')


def test_replace_paths(tmpdir):
    with tmpdir.as_cwd():
        suffix = 'dylib' if platform.system().lower() == 'darwin' else 'so'
        hash_a = '53moz6jwnw3xpiztxwhc4us26klribws'
        hash_b = 'tk62dzu62kd4oh3h3heelyw23hw2sfee'
        hash_c = 'hdkhduizmaddpog6ewdradpobnbjwsjl'
        hash_d = 'hukkosc7ahff7o65h6cdhvcoxm57d4bw'
        hash_loco = 'zy4oigsc4eovn5yhr2lk4aukwzoespob'

        prefix2hash = dict()

        old_spack_dir = os.path.join('%s' % tmpdir,
                                     'Users', 'developer', 'spack')
        mkdirp(old_spack_dir)

        oldprefix_a = os.path.join('%s' % old_spack_dir, 'pkgA-%s' % hash_a)
        oldlibdir_a = os.path.join('%s' % oldprefix_a, 'lib')
        mkdirp(oldlibdir_a)
        prefix2hash[str(oldprefix_a)] = hash_a

        oldprefix_b = os.path.join('%s' % old_spack_dir, 'pkgB-%s' % hash_b)
        oldlibdir_b = os.path.join('%s' % oldprefix_b, 'lib')
        mkdirp(oldlibdir_b)
        prefix2hash[str(oldprefix_b)] = hash_b

        oldprefix_c = os.path.join('%s' % old_spack_dir, 'pkgC-%s' % hash_c)
        oldlibdir_c = os.path.join('%s' % oldprefix_c, 'lib')
        oldlibdir_cc = os.path.join('%s' % oldlibdir_c, 'C')
        mkdirp(oldlibdir_c)
        prefix2hash[str(oldprefix_c)] = hash_c

        oldprefix_d = os.path.join('%s' % old_spack_dir, 'pkgD-%s' % hash_d)
        oldlibdir_d = os.path.join('%s' % oldprefix_d, 'lib')
        mkdirp(oldlibdir_d)
        prefix2hash[str(oldprefix_d)] = hash_d

        oldprefix_local = os.path.join('%s' % tmpdir, 'usr', 'local')
        oldlibdir_local = os.path.join('%s' % oldprefix_local, 'lib')
        mkdirp(oldlibdir_local)
        prefix2hash[str(oldprefix_local)] = hash_loco
        libfile_a = 'libA.%s' % suffix
        libfile_b = 'libB.%s' % suffix
        libfile_c = 'libC.%s' % suffix
        libfile_d = 'libD.%s' % suffix
        libfile_loco = 'libloco.%s' % suffix
        old_libnames  = [os.path.join(oldlibdir_a, libfile_a),
                         os.path.join(oldlibdir_b, libfile_b),
                         os.path.join(oldlibdir_c, libfile_c),
                         os.path.join(oldlibdir_d, libfile_d),
                         os.path.join(oldlibdir_local, libfile_loco)]

        for old_libname in old_libnames:
            with open(old_libname, 'a'):
                os.utime(old_libname, None)

        hash2prefix = dict()

        new_spack_dir = os.path.join('%s' % tmpdir, 'Users', 'Shared',
                                     'spack')
        mkdirp(new_spack_dir)

        prefix_a = os.path.join(new_spack_dir, 'pkgA-%s' % hash_a)
        libdir_a = os.path.join(prefix_a, 'lib')
        mkdirp(libdir_a)
        hash2prefix[hash_a] = str(prefix_a)

        prefix_b = os.path.join(new_spack_dir, 'pkgB-%s' % hash_b)
        libdir_b = os.path.join(prefix_b, 'lib')
        mkdirp(libdir_b)
        hash2prefix[hash_b] = str(prefix_b)

        prefix_c = os.path.join(new_spack_dir, 'pkgC-%s' % hash_c)
        libdir_c = os.path.join(prefix_c, 'lib')
        libdir_cc = os.path.join(libdir_c, 'C')
        mkdirp(libdir_cc)
        hash2prefix[hash_c] = str(prefix_c)

        prefix_d = os.path.join(new_spack_dir, 'pkgD-%s' % hash_d)
        libdir_d = os.path.join(prefix_d, 'lib')
        mkdirp(libdir_d)
        hash2prefix[hash_d] = str(prefix_d)

        prefix_local = os.path.join('%s' % tmpdir, 'usr', 'local')
        libdir_local = os.path.join(prefix_local, 'lib')
        mkdirp(libdir_local)
        hash2prefix[hash_loco] = str(prefix_local)

        new_libnames  = [os.path.join(libdir_a, libfile_a),
                         os.path.join(libdir_b, libfile_b),
                         os.path.join(libdir_cc, libfile_c),
                         os.path.join(libdir_d, libfile_d),
                         os.path.join(libdir_local, libfile_loco)]

        for new_libname in new_libnames:
            with open(new_libname, 'a'):
                os.utime(new_libname, None)

        prefix2prefix = dict()
        for prefix, hash in prefix2hash.items():
            prefix2prefix[prefix] = hash2prefix[hash]

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c,
                                     oldlibdir_cc, oldlibdir_local],
                                    [os.path.join(oldlibdir_a,
                                                  libfile_a),
                                     os.path.join(oldlibdir_b,
                                                  libfile_b),
                                     os.path.join(oldlibdir_local,
                                                  libfile_loco)],
                                    os.path.join(oldlibdir_cc,
                                                 libfile_c),
                                    old_spack_dir,
                                    prefix2prefix
                                    )
        assert out_dict == {oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            os.path.join(oldlibdir_a, libfile_a):
                            os.path.join(libdir_a, libfile_a),
                            os.path.join(oldlibdir_b, libfile_b):
                            os.path.join(libdir_b, libfile_b),
                            os.path.join(oldlibdir_local, libfile_loco):
                            os.path.join(libdir_local, libfile_loco),
                            os.path.join(oldlibdir_cc, libfile_c):
                            os.path.join(libdir_cc, libfile_c)}

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c,
                                     oldlibdir_cc,
                                     oldlibdir_local],
                                    [os.path.join(oldlibdir_a,
                                                  libfile_a),
                                     os.path.join(oldlibdir_b,
                                                  libfile_b),
                                     os.path.join(oldlibdir_cc,
                                                  libfile_c),
                                     os.path.join(oldlibdir_local,
                                                  libfile_loco)],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix
                                    )
        assert out_dict == {oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            os.path.join(oldlibdir_a, libfile_a):
                            os.path.join(libdir_a, libfile_a),
                            os.path.join(oldlibdir_b, libfile_b):
                            os.path.join(libdir_b, libfile_b),
                            os.path.join(oldlibdir_local, libfile_loco):
                            os.path.join(libdir_local, libfile_loco),
                            os.path.join(oldlibdir_cc, libfile_c):
                            os.path.join(libdir_cc, libfile_c)}

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c, oldlibdir_cc,
                                     oldlibdir_local],
                                    ['@rpath/%s' % libfile_a,
                                     '@rpath/%s' % libfile_b,
                                     '@rpath/%s' % libfile_c,
                                     '@rpath/%s' % libfile_loco],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix
                                    )

        assert out_dict == {'@rpath/%s' % libfile_a:
                            '@rpath/%s' % libfile_a,
                            '@rpath/%s' % libfile_b:
                            '@rpath/%s' % libfile_b,
                            '@rpath/%s' % libfile_c:
                            '@rpath/%s' % libfile_c,
                            '@rpath/%s' % libfile_loco:
                            '@rpath/%s' % libfile_loco,
                            oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            }

        out_dict = macho_find_paths([oldlibdir_a,
                                     oldlibdir_b,
                                     oldlibdir_d,
                                     oldlibdir_local],
                                    ['@rpath/%s' % libfile_a,
                                     '@rpath/%s' % libfile_b,
                                     '@rpath/%s' % libfile_loco],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix)
        assert out_dict == {'@rpath/%s' % libfile_a:
                            '@rpath/%s' % libfile_a,
                            '@rpath/%s' % libfile_b:
                            '@rpath/%s' % libfile_b,
                            '@rpath/%s' % libfile_loco:
                            '@rpath/%s' % libfile_loco,
                            oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_d: libdir_d,
                            libdir_local: libdir_local,
                            }


def test_macho_make_paths():
    out = macho_make_paths_relative('/Users/Shared/spack/pkgC/lib/libC.dylib',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'),
                                    '/Users/Shared/spack/pkgC/lib/libC.dylib')
    assert out == {'/Users/Shared/spack/pkgA/lib':
                   '@loader_path/../../pkgA/lib',
                   '/Users/Shared/spack/pkgB/lib':
                   '@loader_path/../../pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '/Users/Shared/spack/pkgA/libA.dylib':
                   '@loader_path/../../pkgA/libA.dylib',
                   '/Users/Shared/spack/pkgB/libB.dylib':
                   '@loader_path/../../pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib',
                   '/Users/Shared/spack/pkgC/lib/libC.dylib':
                   '@rpath/libC.dylib'}

    out = macho_make_paths_normal('/Users/Shared/spack/pkgC/lib/libC.dylib',
                                  ('@loader_path/../../pkgA/lib',
                                   '@loader_path/../../pkgB/lib',
                                   '/usr/local/lib'),
                                  ('@loader_path/../../pkgA/libA.dylib',
                                   '@loader_path/../../pkgB/libB.dylib',
                                   '/usr/local/lib/libloco.dylib'),
                                  '@rpath/libC.dylib')

    assert out == {'@rpath/libC.dylib':
                   '/Users/Shared/spack/pkgC/lib/libC.dylib',
                   '@loader_path/../../pkgA/lib':
                   '/Users/Shared/spack/pkgA/lib',
                   '@loader_path/../../pkgB/lib':
                   '/Users/Shared/spack/pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '@loader_path/../../pkgA/libA.dylib':
                   '/Users/Shared/spack/pkgA/libA.dylib',
                   '@loader_path/../../pkgB/libB.dylib':
                   '/Users/Shared/spack/pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'
                   }

    out = macho_make_paths_relative('/Users/Shared/spack/pkgC/bin/exeC',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'), None)

    assert out == {'/Users/Shared/spack/pkgA/lib':
                   '@loader_path/../../pkgA/lib',
                   '/Users/Shared/spack/pkgB/lib':
                   '@loader_path/../../pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '/Users/Shared/spack/pkgA/libA.dylib':
                   '@loader_path/../../pkgA/libA.dylib',
                   '/Users/Shared/spack/pkgB/libB.dylib':
                   '@loader_path/../../pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'}

    out = macho_make_paths_normal('/Users/Shared/spack/pkgC/bin/exeC',
                                  ('@loader_path/../../pkgA/lib',
                                   '@loader_path/../../pkgB/lib',
                                   '/usr/local/lib'),
                                  ('@loader_path/../../pkgA/libA.dylib',
                                      '@loader_path/../../pkgB/libB.dylib',
                                      '/usr/local/lib/libloco.dylib'),
                                  None)

    assert out == {'@loader_path/../../pkgA/lib':
                   '/Users/Shared/spack/pkgA/lib',
                   '@loader_path/../../pkgB/lib':
                   '/Users/Shared/spack/pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '@loader_path/../../pkgA/libA.dylib':
                   '/Users/Shared/spack/pkgA/libA.dylib',
                   '@loader_path/../../pkgB/libB.dylib':
                   '/Users/Shared/spack/pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'}


@pytest.fixture()
def mock_download():
    """Mock a failing download strategy."""
    class FailedDownloadStrategy(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                "<non-existent URL>", "This FetchStrategy always fails")

    fetcher = FetchStrategyComposite()
    fetcher.append(FailedDownloadStrategy())

    @property
    def fake_fn(self):
        return fetcher

    orig_fn = spack.package.PackageBase.fetcher
    spack.package.PackageBase.fetcher = fake_fn
    yield
    spack.package.PackageBase.fetcher = orig_fn


@pytest.mark.parametrize("manual,instr", [(False, False), (False, True),
                                          (True, False), (True, True)])
@pytest.mark.disable_clean_stage_check
def test_manual_download(install_mockery, mock_download, monkeypatch, manual,
                         instr):
    """
    Ensure expected fetcher fail message based on manual download and instr.
    """
    @property
    def _instr(pkg):
        return 'Download instructions for {0}'.format(pkg.spec.name)

    spec = Spec('a').concretized()
    pkg = spec.package

    pkg.manual_download = manual
    if instr:
        monkeypatch.setattr(spack.package.PackageBase, 'download_instr',
                            _instr)

    expected = pkg.download_instr if manual else 'All fetchers failed'
    with pytest.raises(spack.fetch_strategy.FetchError, match=expected):
        pkg.do_fetch()
