# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os.path
import platform
import re
import shutil

import llnl.util.filesystem
import pytest
import spack.architecture
import spack.concretize
import spack.hooks.sbang as sbang
import spack.paths
import spack.relocate
import spack.spec
import spack.store
import spack.tengine
import spack.util.executable


def rpaths_for(new_binary):
    """Return the RPATHs or RUNPATHs of a binary."""
    patchelf = spack.util.executable.which('patchelf')
    output = patchelf('--print-rpath', str(new_binary), output=str)
    return output.strip()


def text_in_bin(text, binary):
    with open(str(binary), "rb") as f:
        data = f.read()
        f.seek(0)
        pat = re.compile(text.encode('utf-8'))
        if not pat.search(data):
            return False
        return True


@pytest.fixture(params=[True, False])
def is_relocatable(request):
    return request.param


@pytest.fixture()
def source_file(tmpdir, is_relocatable):
    """Returns the path to a source file of a relocatable executable."""
    if is_relocatable:
        template_src = os.path.join(
            spack.paths.test_path, 'data', 'templates', 'relocatable.c'
        )
        src = tmpdir.join('relocatable.c')
        shutil.copy(template_src, str(src))
    else:
        template_dirs = [
            os.path.join(spack.paths.test_path, 'data', 'templates')
        ]
        env = spack.tengine.make_environment(template_dirs)
        template = env.get_template('non_relocatable.c')
        text = template.render({'prefix': spack.store.layout.root})

        src = tmpdir.join('non_relocatable.c')
        src.write(text)

    return src


@pytest.fixture(params=['which_found', 'installed', 'to_be_installed'])
def expected_patchelf_path(request, mutable_database, monkeypatch):
    """Prepare the stage to tests different cases that can occur
    when searching for patchelf.
    """
    case = request.param

    # Mock the which function
    which_fn = {
        'which_found': lambda x: collections.namedtuple(
            '_', ['path']
        )('/usr/bin/patchelf')
    }
    monkeypatch.setattr(
        spack.util.executable, 'which',
        which_fn.setdefault(case, lambda x: None)
    )
    if case == 'which_found':
        return '/usr/bin/patchelf'

    # TODO: Mock a case for Darwin architecture

    spec = spack.spec.Spec('patchelf')
    spec.concretize()

    patchelf_cls = type(spec.package)
    do_install = patchelf_cls.do_install
    expected_path = os.path.join(spec.prefix.bin, 'patchelf')

    def do_install_mock(self, **kwargs):
        do_install(self, fake=True)
        with open(expected_path):
            pass

    monkeypatch.setattr(patchelf_cls, 'do_install', do_install_mock)
    if case == 'installed':
        spec.package.do_install()

    return expected_path


@pytest.fixture()
def mock_patchelf(tmpdir, mock_executable):
    def _factory(output):
        return mock_executable('patchelf', output=output)
    return _factory


@pytest.fixture()
def hello_world(tmpdir):
    """Factory fixture that compiles an ELF binary setting its RPATH. Relative
    paths are encoded with `$ORIGIN` prepended.
    """
    def _factory(rpaths, message="Hello world!"):
        source = tmpdir.join('main.c')
        source.write("""
        #include <stdio.h>
        int main(){{
            printf("{0}");
        }}
        """.format(message))
        gcc = spack.util.executable.which('gcc')
        executable = source.dirpath('main.x')
        # Encode relative RPATHs using `$ORIGIN` as the root prefix
        rpaths = [x if os.path.isabs(x) else os.path.join('$ORIGIN', x)
                  for x in rpaths]
        rpath_str = ':'.join(rpaths)
        opts = [
            '-Wl,--disable-new-dtags',
            '-Wl,-rpath={0}'.format(rpath_str),
            str(source), '-o', str(executable)
        ]
        gcc(*opts)
        return executable

    return _factory


@pytest.fixture()
def copy_binary():
    """Returns a function that copies a binary somewhere and
    returns the new location.
    """
    def _copy_somewhere(orig_binary):
        new_root = orig_binary.mkdtemp()
        new_binary = new_root.join('main.x')
        shutil.copy(str(orig_binary), str(new_binary))
        return new_binary
    return _copy_somewhere


@pytest.mark.requires_executables(
    '/usr/bin/gcc', 'patchelf', 'strings', 'file'
)
def test_file_is_relocatable(source_file, is_relocatable):
    compiler = spack.util.executable.Executable('/usr/bin/gcc')
    executable = str(source_file).replace('.c', '.x')
    compiler_env = {
        'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    }
    compiler(str(source_file), '-o', executable, env=compiler_env)

    assert spack.relocate.is_binary(executable)
    assert spack.relocate.file_is_relocatable(executable) is is_relocatable


@pytest.mark.requires_executables('patchelf', 'strings', 'file')
def test_patchelf_is_relocatable():
    patchelf = spack.relocate._patchelf()
    assert llnl.util.filesystem.is_exe(patchelf)
    assert spack.relocate.file_is_relocatable(patchelf)


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_file_is_relocatable_errors(tmpdir):
    # The file passed in as argument must exist...
    with pytest.raises(ValueError) as exc_info:
        spack.relocate.file_is_relocatable('/usr/bin/does_not_exist')
    assert 'does not exist' in str(exc_info.value)

    # ...and the argument must be an absolute path to it
    file = tmpdir.join('delete.me')
    file.write('foo')

    with llnl.util.filesystem.working_dir(str(tmpdir)):
        with pytest.raises(ValueError) as exc_info:
            spack.relocate.file_is_relocatable('delete.me')
        assert 'is not an absolute path' in str(exc_info.value)


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_search_patchelf(expected_patchelf_path):
    current = spack.relocate._patchelf()
    assert current == expected_patchelf_path


@pytest.mark.parametrize('patchelf_behavior,expected', [
    ('echo ', []),
    ('echo /opt/foo/lib:/opt/foo/lib64', ['/opt/foo/lib', '/opt/foo/lib64']),
    ('exit 1', [])
])
def test_existing_rpaths(patchelf_behavior, expected, mock_patchelf):
    # Here we are mocking an executable that is always called "patchelf"
    # because that will skip the part where we try to build patchelf
    # by ourselves. The executable will output some rpaths like
    # `patchelf --print-rpath` would.
    path = mock_patchelf(patchelf_behavior)
    rpaths = spack.relocate._elf_rpaths_for(path)
    assert rpaths == expected


@pytest.mark.parametrize('start_path,path_root,paths,expected', [
    ('/usr/bin/test', '/usr', ['/usr/lib', '/usr/lib64', '/opt/local/lib'],
     ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib'])
])
def test_make_relative_paths(start_path, path_root, paths, expected):
    relatives = spack.relocate._make_relative(start_path, path_root, paths)
    assert relatives == expected


@pytest.mark.parametrize('start_path,relative_paths,expected', [
    # $ORIGIN will be replaced with os.path.dirname('usr/bin/test')
    # and then normalized
    ('/usr/bin/test',
     ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib'],
     ['/usr/lib', '/usr/lib64', '/opt/local/lib']),
    # Relative path without $ORIGIN
    ('/usr/bin/test', ['../local/lib'], ['../local/lib']),
])
def test_normalize_relative_paths(start_path, relative_paths, expected):
    normalized = spack.relocate._normalize_relative_paths(
        start_path, relative_paths
    )
    assert normalized == expected


def test_set_elf_rpaths(mock_patchelf):
    # Try to relocate a mock version of patchelf and check
    # the call made to patchelf itself
    patchelf = mock_patchelf('echo $@')
    rpaths = ['/usr/lib', '/usr/lib64', '/opt/local/lib']
    output = spack.relocate._set_elf_rpaths(patchelf, rpaths)

    # Assert that the arguments of the call to patchelf are as expected
    assert '--force-rpath' in output
    assert '--set-rpath ' + ':'.join(rpaths) in output
    assert patchelf in output


def test_set_elf_rpaths_warning(mock_patchelf):
    # Mock a failing patchelf command and ensure it warns users
    patchelf = mock_patchelf('exit 1')
    rpaths = ['/usr/lib', '/usr/lib64', '/opt/local/lib']
    # To avoid using capfd in order to check if the warning was triggered
    # here we just check that output is not set
    output = spack.relocate._set_elf_rpaths(patchelf, rpaths)
    assert output is None


@pytest.mark.requires_executables('patchelf', 'strings', 'file', 'gcc')
@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_replace_prefix_bin(hello_world):
    # Compile an "Hello world!" executable and set RPATHs
    executable = hello_world(rpaths=['/usr/lib', '/usr/lib64'])

    # Relocate the RPATHs
    spack.relocate._replace_prefix_bin(str(executable), '/usr', '/foo')

    # Some compilers add rpaths so ensure changes included in final result
    assert '/foo/lib:/foo/lib64' in rpaths_for(executable)


@pytest.mark.requires_executables('patchelf', 'strings', 'file', 'gcc')
@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_relocate_elf_binaries_absolute_paths(
        hello_world, copy_binary, tmpdir
):
    # Create an executable, set some RPATHs, copy it to another location
    orig_binary = hello_world(rpaths=[str(tmpdir.mkdir('lib')), '/usr/lib64'])
    new_binary = copy_binary(orig_binary)

    spack.relocate.relocate_elf_binaries(
        binaries=[str(new_binary)],
        orig_root=str(orig_binary.dirpath()),
        new_root=None,  # Not needed when relocating absolute paths
        new_prefixes={
            str(tmpdir): '/foo'
        },
        rel=False,
        # Not needed when relocating absolute paths
        orig_prefix=None, new_prefix=None
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert '/foo/lib:/usr/lib64' in rpaths_for(new_binary)


@pytest.mark.requires_executables('patchelf', 'strings', 'file', 'gcc')
@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_relocate_elf_binaries_relative_paths(hello_world, copy_binary):
    # Create an executable, set some RPATHs, copy it to another location
    orig_binary = hello_world(rpaths=['lib', 'lib64', '/opt/local/lib'])
    new_binary = copy_binary(orig_binary)

    spack.relocate.relocate_elf_binaries(
        binaries=[str(new_binary)],
        orig_root=str(orig_binary.dirpath()),
        new_root=str(new_binary.dirpath()),
        new_prefixes={str(orig_binary.dirpath()): '/foo'},
        rel=True,
        orig_prefix=str(orig_binary.dirpath()),
        new_prefix=str(new_binary.dirpath())
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert '/foo/lib:/foo/lib64:/opt/local/lib' in rpaths_for(new_binary)


@pytest.mark.requires_executables('patchelf', 'strings', 'file', 'gcc')
@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_make_elf_binaries_relative(hello_world, copy_binary, tmpdir):
    orig_binary = hello_world(rpaths=[
        str(tmpdir.mkdir('lib')), str(tmpdir.mkdir('lib64')), '/opt/local/lib'
    ])
    new_binary = copy_binary(orig_binary)

    spack.relocate.make_elf_binaries_relative(
        [str(new_binary)], [str(orig_binary)], str(orig_binary.dirpath())
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert '$ORIGIN/lib:$ORIGIN/lib64:/opt/local/lib' in rpaths_for(new_binary)


def test_raise_if_not_relocatable(monkeypatch):
    monkeypatch.setattr(spack.relocate, 'file_is_relocatable', lambda x: False)
    with pytest.raises(spack.relocate.InstallRootStringError):
        spack.relocate.raise_if_not_relocatable(
            ['an_executable'], allow_root=False
        )


@pytest.mark.requires_executables('patchelf', 'strings', 'file', 'gcc')
@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_relocate_text_bin(hello_world, copy_binary, tmpdir):
    orig_binary = hello_world(rpaths=[
        str(tmpdir.mkdir('lib')), str(tmpdir.mkdir('lib64')), '/opt/local/lib'
    ], message=str(tmpdir))
    new_binary = copy_binary(orig_binary)

    # Check original directory is in the executabel and the new one is not
    assert text_in_bin(str(tmpdir), new_binary)
    assert not text_in_bin(str(new_binary.dirpath()), new_binary)

    # Check this call succeed
    spack.relocate.relocate_text_bin(
        [str(new_binary)],
        str(orig_binary.dirpath()), str(new_binary.dirpath()),
        spack.paths.spack_root, spack.paths.spack_root,
        {str(orig_binary.dirpath()): str(new_binary.dirpath())}
    )

    # Check original directory is not there anymore and it was
    # substituted with the new one
    assert not text_in_bin(str(tmpdir), new_binary)
    assert text_in_bin(str(new_binary.dirpath()), new_binary)


def test_relocate_text_bin_raise_if_new_prefix_is_longer():
    short_prefix = '/short'
    long_prefix = '/much/longer'
    with pytest.raises(spack.relocate.BinaryTextReplaceError):
        spack.relocate.relocate_text_bin(
            ['item'], short_prefix, long_prefix, None, None, None
        )


@pytest.mark.parametrize("sbang_line", [
    "#!/bin/bash /path/to/orig/spack/bin/sbang",
    "#!/bin/sh /orig/layout/root/bin/sbang"
])
def test_relocate_text_old_sbang(tmpdir, sbang_line):
    """Ensure that old and new sbang styles are relocated."""

    old_install_prefix = "/orig/layout/root/orig/install/prefix"
    new_install_prefix = os.path.join(
        spack.store.layout.root, "new", "install", "prefix"
    )

    # input file with an sbang line
    original = """\
{0}
#!/usr/bin/env python

/orig/layout/root/orig/install/prefix
""".format(sbang_line)

    # expected relocation
    expected = """\
{0}
#!/usr/bin/env python

{1}
""".format(sbang.sbang_shebang_line(), new_install_prefix)

    path = tmpdir.ensure("path", "to", "file")
    with path.open("w") as f:
        f.write(original)

    spack.relocate.relocate_text(
        [str(path)],
        "/orig/layout/root",   spack.store.layout.root,
        old_install_prefix,    new_install_prefix,
        "/path/to/orig/spack", spack.paths.spack_root,
        {
            old_install_prefix: new_install_prefix
        }
    )

    assert expected == open(str(path)).read()
