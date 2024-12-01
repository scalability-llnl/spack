# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import llnl.util.filesystem as fs

import spack.util.executable
import spack.util.gpg
from spack.main import SpackCommand
from spack.paths import mock_gpg_data_path, mock_gpg_keys_path
from spack.util.executable import ProcessError

#: spack command used by tests below
gpg = SpackCommand("gpg")
bootstrap = SpackCommand("bootstrap")
mirror = SpackCommand("mirror")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


# test gpg command detection
@pytest.mark.parametrize(
    "cmd_name,version",
    [
        ("gpg", "undetectable"),  # undetectable version
        ("gpg", "gpg (GnuPG) 1.3.4"),  # insufficient version
        ("gpg", "gpg (GnuPG) 2.2.19"),  # sufficient version
        ("gpg2", "gpg (GnuPG) 2.2.19"),  # gpg2 command
    ],
)
def test_find_gpg(cmd_name, version, tmpdir, mock_gnupghome, monkeypatch):
    TEMPLATE = "#!/bin/sh\n" 'echo "{version}"\n'

    with tmpdir.as_cwd():
        for fname in (cmd_name, "gpgconf"):
            with open(fname, "w") as f:
                f.write(TEMPLATE.format(version=version))
            fs.set_executable(fname)

    monkeypatch.setenv("PATH", str(tmpdir))
    if version == "undetectable" or version.endswith("1.3.4"):
        with pytest.raises(spack.util.gpg.SpackGPGError):
            spack.util.gpg.init(force=True)
    else:
        spack.util.gpg.init(force=True)
        assert spack.util.gpg.GPG is not None
        assert spack.util.gpg.GPGCONF is not None


def test_no_gpg_in_path(tmpdir, mock_gnupghome, monkeypatch, mutable_config):
    monkeypatch.setenv("PATH", str(tmpdir))
    bootstrap("disable")
    with pytest.raises(RuntimeError):
        spack.util.gpg.init(force=True)


@pytest.mark.maybeslow
def test_gpg(tmpdir, mutable_config, mock_gnupghome):
    # Verify a file with an empty keyring.
    with pytest.raises(ProcessError):
        gpg("verify", os.path.join(mock_gpg_data_path, "content.txt"))

    # Import the default key.
    gpg("init", "--from", mock_gpg_keys_path)

    # List the keys.
    # TODO: Test the output here.
    gpg("list", "--trusted")
    gpg("list", "--signing")

    # Verify the file now that the key has been trusted.
    gpg("verify", os.path.join(mock_gpg_data_path, "content.txt"))

    # Untrust the default key.
    gpg("untrust", "Spack testing")

    # Now that the key is untrusted, verification should fail.
    with pytest.raises(ProcessError):
        gpg("verify", os.path.join(mock_gpg_data_path, "content.txt"))

    # Create a file to test signing.
    test_path = tmpdir.join("to-sign.txt")
    with open(str(test_path), "w+") as fout:
        fout.write("Test content for signing.\n")

    # Signing without a private key should fail.
    with pytest.raises(RuntimeError) as exc_info:
        gpg("sign", str(test_path))
    assert exc_info.value.args[0] == "no signing keys are available"

    # Create a key for use in the tests.
    keypath = tmpdir.join("testing-1.key")
    gpg(
        "create",
        "--comment",
        "Spack testing key",
        "--export",
        str(keypath),
        "Spack testing 1",
        "spack@googlegroups.com",
    )
    keyfp = spack.util.gpg.signing_keys()[0]

    # List the keys.
    # TODO: Test the output here.
    gpg("list")
    gpg("list", "--trusted")
    gpg("list", "--signing")

    # Signing with the default (only) key.
    gpg("sign", str(test_path))

    # Verify the file we just verified.
    gpg("verify", str(test_path))

    # Export the key for future use.
    export_path = tmpdir.join("export.testing.key")
    gpg("export", str(export_path))

    # Test exporting the private key
    private_export_path = tmpdir.join("export-secret.testing.key")
    gpg("export", "--secret", str(private_export_path))

    # Ensure we exported the right content!
    with open(str(private_export_path), "r") as fd:
        content = fd.read()
    assert "BEGIN PGP PRIVATE KEY BLOCK" in content

    # and for the public key
    with open(str(export_path), "r") as fd:
        content = fd.read()
    assert "BEGIN PGP PUBLIC KEY BLOCK" in content

    # Create a second key for use in the tests.
    gpg("create", "--comment", "Spack testing key", "Spack testing 2", "spack@googlegroups.com")

    # List the keys.
    # TODO: Test the output here.
    gpg("list", "--trusted")
    gpg("list", "--signing")

    test_path = tmpdir.join("to-sign-2.txt")
    with open(str(test_path), "w+") as fout:
        fout.write("Test content for signing.\n")

    # Signing with multiple signing keys is ambiguous.
    with pytest.raises(RuntimeError) as exc_info:
        gpg("sign", str(test_path))
    assert exc_info.value.args[0] == "multiple signing keys are available; please choose one"

    # Signing with a specified key.
    gpg("sign", "--key", keyfp, str(test_path))

    # Untrusting signing keys needs a flag.
    with pytest.raises(ProcessError):
        gpg("untrust", "Spack testing 1")

    # Untrust the key we created.
    gpg("untrust", "--signing", keyfp)

    # Verification should now fail.
    with pytest.raises(ProcessError):
        gpg("verify", str(test_path))

    # Trust the exported key.
    gpg("trust", str(export_path))

    # Verification should now succeed again.
    gpg("verify", str(test_path))

    # Publish the keys using a directory path
    test_path = tmpdir.join("dir_cache")
    os.makedirs("%s" % test_path)
    gpg("publish", "--rebuild-index", "-d", str(test_path))
    assert os.path.exists("%s/build_cache/_pgp/index.json" % test_path)

    # Publish the keys using a mirror url
    test_path = tmpdir.join("url_cache")
    os.makedirs("%s" % test_path)
    test_url = "file://%s" % test_path
    gpg("publish", "--rebuild-index", "--mirror-url", test_url)
    assert os.path.exists("%s/build_cache/_pgp/index.json" % test_path)

    # Publish the keys using a mirror name
    test_path = tmpdir.join("named_cache")
    os.makedirs("%s" % test_path)
    mirror_url = "file://%s" % test_path
    mirror("add", "gpg", mirror_url)
    gpg("publish", "--rebuild-index", "-m", "gpg")
    assert os.path.exists("%s/build_cache/_pgp/index.json" % test_path)
