# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""\
Test that Spack's shebang filtering works correctly.
"""
import filecmp
import os
import shutil
import stat
import sys
import tempfile

import pytest

import llnl.util.filesystem as fs

import spack.config
import spack.hooks.sbang as sbang
import spack.store
import spack.util.spack_yaml as syaml
from spack.util.executable import which

if sys.platform != "win32":
    import grp


pytestmark = pytest.mark.not_on_windows("does not run on windows")


too_long = sbang.system_shebang_limit + 1


short_line = "#!/this/is/short/bin/bash\n"
long_line = "#!/this/" + ("x" * too_long) + "/is/long\n"

lua_line = "#!/this/" + ("x" * too_long) + "/is/lua\n"
lua_in_text = ("line\n") * 100 + "lua\n" + ("line\n" * 100)
lua_line_patched = "--!/this/" + ("x" * too_long) + "/is/lua\n"

luajit_line = "#!/this/" + ("x" * too_long) + "/is/luajit\n"
luajit_in_text = ("line\n") * 100 + "lua\n" + ("line\n" * 100)
luajit_line_patched = "--!/this/" + ("x" * too_long) + "/is/luajit\n"

node_line = "#!/this/" + ("x" * too_long) + "/is/node\n"
node_in_text = ("line\n") * 100 + "lua\n" + ("line\n" * 100)
node_line_patched = "//!/this/" + ("x" * too_long) + "/is/node\n"

php_line = "#!/this/" + ("x" * too_long) + "/is/php\n"
php_in_text = ("line\n") * 100 + "php\n" + ("line\n" * 100)
php_line_patched = "<?php #!/this/" + ("x" * too_long) + "/is/php\n"
php_line_patched2 = "?>\n"

last_line = "last!\n"


@pytest.fixture  # type: ignore[no-redef]
def sbang_line():
    yield "#!/bin/sh %s/bin/sbang\n" % spack.store.STORE.layout.root


class ScriptDirectory:
    """Directory full of test scripts to run sbang instrumentation on."""

    def __init__(self, sbang_line):
        self.tempdir = tempfile.mkdtemp()

        self.directory = os.path.join(self.tempdir, "dir")
        fs.mkdirp(self.directory)

        # Script with short shebang
        self.short_shebang = os.path.join(self.tempdir, "short")
        with open(self.short_shebang, "w") as f:
            f.write(short_line)
            f.write(last_line)
        self.make_executable(self.short_shebang)

        # Script with long shebang
        self.long_shebang = os.path.join(self.tempdir, "long")
        with open(self.long_shebang, "w") as f:
            f.write(long_line)
            f.write(last_line)
        self.make_executable(self.long_shebang)

        # Non-executable script with long shebang
        self.nonexec_long_shebang = os.path.join(self.tempdir, "nonexec_long")
        with open(self.nonexec_long_shebang, "w") as f:
            f.write(long_line)
            f.write(last_line)

        # Lua script with long shebang
        self.lua_shebang = os.path.join(self.tempdir, "lua")
        with open(self.lua_shebang, "w") as f:
            f.write(lua_line)
            f.write(last_line)
        self.make_executable(self.lua_shebang)

        # Lua occurring in text, not in shebang
        self.lua_textbang = os.path.join(self.tempdir, "lua_in_text")
        with open(self.lua_textbang, "w") as f:
            f.write(short_line)
            f.write(lua_in_text)
            f.write(last_line)
        self.make_executable(self.lua_textbang)

        # Luajit script with long shebang
        self.luajit_shebang = os.path.join(self.tempdir, "luajit")
        with open(self.luajit_shebang, "w") as f:
            f.write(luajit_line)
            f.write(last_line)
        self.make_executable(self.luajit_shebang)

        # Luajit occuring in text, not in shebang
        self.luajit_textbang = os.path.join(self.tempdir, "luajit_in_text")
        with open(self.luajit_textbang, "w") as f:
            f.write(short_line)
            f.write(luajit_in_text)
            f.write(last_line)
        self.make_executable(self.luajit_textbang)

        # Node script with long shebang
        self.node_shebang = os.path.join(self.tempdir, "node")
        with open(self.node_shebang, "w") as f:
            f.write(node_line)
            f.write(last_line)
        self.make_executable(self.node_shebang)

        # Node occuring in text, not in shebang
        self.node_textbang = os.path.join(self.tempdir, "node_in_text")
        with open(self.node_textbang, "w") as f:
            f.write(short_line)
            f.write(node_in_text)
            f.write(last_line)
        self.make_executable(self.node_textbang)

        # php script with long shebang
        self.php_shebang = os.path.join(self.tempdir, "php")
        with open(self.php_shebang, "w") as f:
            f.write(php_line)
            f.write(last_line)
        self.make_executable(self.php_shebang)

        # php occuring in text, not in shebang
        self.php_textbang = os.path.join(self.tempdir, "php_in_text")
        with open(self.php_textbang, "w") as f:
            f.write(short_line)
            f.write(php_in_text)
            f.write(last_line)
        self.make_executable(self.php_textbang)

        # Script already using sbang.
        self.has_sbang = os.path.join(self.tempdir, "shebang")
        with open(self.has_sbang, "w") as f:
            f.write(sbang_line)
            f.write(long_line)
            f.write(last_line)
        self.make_executable(self.has_sbang)

        # Fake binary file.
        self.binary = os.path.join(self.tempdir, "binary")
        tar = which("tar", required=True)
        tar("czf", self.binary, self.has_sbang)
        self.make_executable(self.binary)

    def destroy(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def make_executable(self, path):
        # make a file executable
        st = os.stat(path)
        executable_mode = st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(path, executable_mode)

        st = os.stat(path)
        assert oct(executable_mode) == oct(st.st_mode & executable_mode)


@pytest.fixture
def script_dir(sbang_line):
    sdir = ScriptDirectory(sbang_line)
    yield sdir
    sdir.destroy()


@pytest.mark.parametrize(
    "shebang,interpreter",
    [
        (b"#!/path/to/interpreter argument\n", b"/path/to/interpreter"),
        (b"#!  /path/to/interpreter truncated-argum", b"/path/to/interpreter"),
        (b"#! \t  \t/path/to/interpreter\t  \targument", b"/path/to/interpreter"),
        (b"#! \t \t /path/to/interpreter", b"/path/to/interpreter"),
        (b"#!/path/to/interpreter\0", b"/path/to/interpreter"),
        (b"#!/path/to/interpreter multiple args\n", b"/path/to/interpreter"),
        (b"#!\0/path/to/interpreter arg\n", None),
        (b"#!\n/path/to/interpreter arg\n", None),
        (b"#!", None),
    ],
)
def test_shebang_interpreter_regex(shebang, interpreter):
    sbang.get_interpreter(shebang) == interpreter


def test_shebang_handling(script_dir, sbang_line):
    sbang.filter_shebangs_in_directory(script_dir.tempdir)

    # Make sure this is untouched
    with open(script_dir.short_shebang, "r") as f:
        assert f.readline() == short_line
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.long_shebang, "r") as f:
        assert f.readline() == sbang_line
        assert f.readline() == long_line
        assert f.readline() == last_line

    # Make sure this is untouched
    with open(script_dir.nonexec_long_shebang, "r") as f:
        assert f.readline() == long_line
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.lua_shebang, "r") as f:
        assert f.readline() == sbang_line
        assert f.readline() == lua_line_patched
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.luajit_shebang, "r") as f:
        assert f.readline() == sbang_line
        assert f.readline() == luajit_line_patched
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.node_shebang, "r") as f:
        assert f.readline() == sbang_line
        assert f.readline() == node_line_patched
        assert f.readline() == last_line

    assert filecmp.cmp(script_dir.lua_textbang, os.path.join(script_dir.tempdir, "lua_in_text"))
    assert filecmp.cmp(
        script_dir.luajit_textbang, os.path.join(script_dir.tempdir, "luajit_in_text")
    )
    assert filecmp.cmp(script_dir.node_textbang, os.path.join(script_dir.tempdir, "node_in_text"))
    assert filecmp.cmp(script_dir.php_textbang, os.path.join(script_dir.tempdir, "php_in_text"))

    # Make sure this is untouched
    with open(script_dir.has_sbang, "r") as f:
        assert f.readline() == sbang_line
        assert f.readline() == long_line
        assert f.readline() == last_line


def test_shebang_handles_non_writable_files(script_dir, sbang_line):
    # make a file non-writable
    st = os.stat(script_dir.long_shebang)
    not_writable_mode = st.st_mode & ~stat.S_IWRITE
    os.chmod(script_dir.long_shebang, not_writable_mode)

    test_shebang_handling(script_dir, sbang_line)

    st = os.stat(script_dir.long_shebang)
    assert oct(not_writable_mode) == oct(st.st_mode)


@pytest.fixture(scope="function")
def configure_group_perms():
    # On systems with remote groups, the primary user group may be remote
    # and grp does not act on remote groups.
    # To ensure we find a group we can operate on, we get take the first group
    # listed which has the current user as a member.
    gid = fs.group_ids(os.getuid())[0]
    group_name = grp.getgrgid(gid).gr_name

    conf = syaml.load_config(
        """\
all:
  permissions:
    read: world
    write: group
    group: {0}
""".format(
            group_name
        )
    )
    spack.config.set("packages", conf, scope="user")

    yield


@pytest.fixture(scope="function")
def configure_user_perms():
    conf = syaml.load_config(
        """\
all:
  permissions:
    read: world
    write: user
"""
    )
    spack.config.set("packages", conf, scope="user")

    yield


def check_sbang_installation(group=False):
    sbang_path = sbang.sbang_install_path()
    sbang_bin_dir = os.path.dirname(sbang_path)
    assert sbang_path.startswith(spack.store.STORE.unpadded_root)

    assert os.path.exists(sbang_path)
    assert fs.is_exe(sbang_path)

    status = os.stat(sbang_bin_dir)
    mode = status.st_mode & 0o777
    if group:
        assert mode == 0o775, "Unexpected {0}".format(oct(mode))
    else:
        assert mode == 0o755, "Unexpected {0}".format(oct(mode))

    status = os.stat(sbang_path)
    mode = status.st_mode & 0o777
    if group:
        assert mode == 0o775, "Unexpected {0}".format(oct(mode))
    else:
        assert mode == 0o755, "Unexpected {0}".format(oct(mode))


def run_test_install_sbang(group):
    sbang_path = sbang.sbang_install_path()
    sbang_bin_dir = os.path.dirname(sbang_path)

    assert sbang_path.startswith(spack.store.STORE.unpadded_root)
    assert not os.path.exists(sbang_bin_dir)

    sbang.install_sbang()
    check_sbang_installation(group)

    # put an invalid file in for sbang
    fs.mkdirp(sbang_bin_dir)
    with open(sbang_path, "w") as f:
        f.write("foo")

    sbang.install_sbang()
    check_sbang_installation(group)

    # install again and make sure sbang is still fine
    sbang.install_sbang()
    check_sbang_installation(group)


def test_install_group_sbang(install_mockery, configure_group_perms):
    run_test_install_sbang(True)


def test_install_user_sbang(install_mockery, configure_user_perms):
    run_test_install_sbang(False)


def test_install_sbang_too_long(tmpdir):
    root = str(tmpdir)
    num_extend = sbang.system_shebang_limit - len(root) - len("/bin/sbang")
    long_path = root
    while num_extend > 1:
        add = min(num_extend, 255)
        long_path = os.path.join(long_path, "e" * add)
        num_extend -= add
    with spack.store.use_store(long_path):
        with pytest.raises(sbang.SbangPathError) as exc_info:
            sbang.sbang_install_path()

    err = str(exc_info.value)
    assert "root is too long" in err
    assert "exceeds limit" in err
    assert "cannot patch" in err


def test_sbang_hook_skips_nonexecutable_blobs(tmpdir):
    # Write a binary blob to non-executable.sh, with a long interpreter "path"
    # consisting of invalid UTF-8. The latter is technically not really necessary for
    # the test, but binary blobs accidentally starting with b'#!' usually do not contain
    # valid UTF-8, so we also ensure that Spack does not attempt to decode as UTF-8.
    contents = b"#!" + b"\x80" * sbang.system_shebang_limit
    file = str(tmpdir.join("non-executable.sh"))
    with open(file, "wb") as f:
        f.write(contents)

    sbang.filter_shebangs_in_directory(str(tmpdir))

    # Make sure there is no sbang shebang.
    with open(file, "rb") as f:
        assert b"sbang" not in f.readline()


def test_sbang_handles_non_utf8_files(tmpdir):
    # We have an executable with a copyright sign as filename
    contents = b"#!" + b"\xa9" * sbang.system_shebang_limit + b"\nand another symbol: \xa9"

    # Make sure it's indeed valid latin1 but invalid utf-8.
    assert contents.decode("latin1")
    with pytest.raises(UnicodeDecodeError):
        contents.decode("utf-8")

    # Put it in an executable file
    file = str(tmpdir.join("latin1.sh"))
    with open(file, "wb") as f:
        f.write(contents)

    # Run sbang
    assert sbang.filter_shebang(file)

    with open(file, "rb") as f:
        new_contents = f.read()

    assert contents in new_contents
    assert b"sbang" in new_contents


@pytest.fixture
def shebang_limits_system_8_spack_16():
    system_limit, sbang.system_shebang_limit = sbang.system_shebang_limit, 8
    spack_limit, sbang.spack_shebang_limit = sbang.spack_shebang_limit, 16
    yield
    sbang.system_shebang_limit = system_limit
    sbang.spack_shebang_limit = spack_limit


def test_shebang_exceeds_spack_shebang_limit(shebang_limits_system_8_spack_16, tmpdir):
    """Tests whether shebangs longer than Spack's limit are skipped"""
    file = str(tmpdir.join("longer_than_spack_limit.sh"))
    with open(file, "wb") as f:
        f.write(b"#!" + b"x" * sbang.spack_shebang_limit)

    # Then Spack shouldn't try to add a shebang
    assert not sbang.filter_shebang(file)

    with open(file, "rb") as f:
        assert b"sbang" not in f.read()


def test_sbang_hook_handles_non_writable_files_preserving_permissions(tmpdir):
    path = str(tmpdir.join("file.sh"))
    with open(path, "w") as f:
        f.write(long_line)
    os.chmod(path, 0o555)
    sbang.filter_shebang(path)
    with open(path, "r") as f:
        assert "sbang" in f.readline()
    assert os.stat(path).st_mode & 0o777 == 0o555
