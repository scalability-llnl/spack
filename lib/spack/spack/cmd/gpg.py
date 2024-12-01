# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import tempfile

import spack.binary_distribution
import spack.mirror
import spack.paths
import spack.stage
import spack.util.gpg
import spack.util.url
from spack.cmd.common import arguments

description = "handle GPG actions for spack"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help="GPG sub-commands")

    verify = subparsers.add_parser("verify", help=gpg_verify.__doc__)
    arguments.add_common_arguments(verify, ["installed_spec"])
    verify.add_argument("signature", type=str, nargs="?", help="the signature file")
    verify.set_defaults(func=gpg_verify)

    trust = subparsers.add_parser("trust", help=gpg_trust.__doc__)
    trust.add_argument("keyfile", type=str, help="add a key to the trust store")
    trust.set_defaults(func=gpg_trust)

    untrust = subparsers.add_parser("untrust", help=gpg_untrust.__doc__)
    untrust.add_argument("--signing", action="store_true", help="allow untrusting signing keys")
    untrust.add_argument("keys", nargs="+", type=str, help="remove keys from the trust store")
    untrust.set_defaults(func=gpg_untrust)

    sign = subparsers.add_parser("sign", help=gpg_sign.__doc__)
    sign.add_argument(
        "--output", metavar="DEST", type=str, help="the directory to place signatures"
    )
    sign.add_argument("--key", metavar="KEY", type=str, help="the key to use for signing")
    sign.add_argument(
        "--clearsign", action="store_true", help="if specified, create a clearsign signature"
    )
    arguments.add_common_arguments(sign, ["installed_spec"])
    sign.set_defaults(func=gpg_sign)

    create = subparsers.add_parser("create", help=gpg_create.__doc__)
    create.add_argument("name", type=str, help="the name to use for the new key")
    create.add_argument("email", type=str, help="the email address to use for the new key")
    create.add_argument(
        "--comment",
        metavar="COMMENT",
        type=str,
        default="GPG created for Spack",
        help="a description for the intended use of the key",
    )
    create.add_argument(
        "--expires", metavar="EXPIRATION", type=str, default="0", help="when the key should expire"
    )
    create.add_argument(
        "--export", metavar="DEST", type=str, help="export the public key to a file"
    )
    create.add_argument(
        "--export-secret",
        metavar="DEST",
        type=str,
        dest="secret",
        help="export the private key to a file",
    )
    create.set_defaults(func=gpg_create)

    list = subparsers.add_parser("list", help=gpg_list.__doc__)
    list.add_argument("--trusted", action="store_true", default=True, help="list trusted keys")
    list.add_argument(
        "--signing", action="store_true", help="list keys which may be used for signing"
    )
    list.set_defaults(func=gpg_list)

    init = subparsers.add_parser("init", help=gpg_init.__doc__)
    init.add_argument("--from", metavar="DIR", type=str, dest="import_dir", help=argparse.SUPPRESS)
    init.set_defaults(func=gpg_init)

    export = subparsers.add_parser("export", help=gpg_export.__doc__)
    export.add_argument("location", type=str, help="where to export keys")
    export.add_argument(
        "keys", nargs="*", help="the keys to export (all public keys if unspecified)"
    )
    export.add_argument("--secret", action="store_true", help="export secret keys")
    export.set_defaults(func=gpg_export)

    publish = subparsers.add_parser("publish", help=gpg_publish.__doc__)

    output = publish.add_mutually_exclusive_group(required=True)
    output.add_argument(
        "-d",
        "--directory",
        metavar="directory",
        type=str,
        help="local directory where keys will be published",
    )
    output.add_argument(
        "-m",
        "--mirror-name",
        metavar="mirror-name",
        type=str,
        help="name of the mirror where keys will be published",
    )
    output.add_argument(
        "--mirror-url",
        metavar="mirror-url",
        type=str,
        help="URL of the mirror where keys will be published",
    )
    publish.add_argument(
        "--update-index",
        "--rebuild-index",
        action="store_true",
        default=False,
        help="regenerate buildcache key index after publishing key(s)",
    )
    publish.add_argument(
        "keys", nargs="*", help="keys to publish (all public keys if unspecified)"
    )
    publish.set_defaults(func=gpg_publish)


def gpg_create(args):
    """create a new key"""
    if args.export or args.secret:
        old_sec_keys = spack.util.gpg.signing_keys()

    # Create the new key
    spack.util.gpg.create(
        name=args.name, email=args.email, comment=args.comment, expires=args.expires
    )
    if args.export or args.secret:
        new_sec_keys = set(spack.util.gpg.signing_keys())
        new_keys = new_sec_keys.difference(old_sec_keys)

    if args.export:
        spack.util.gpg.export_keys(args.export, new_keys)
    if args.secret:
        spack.util.gpg.export_keys(args.secret, new_keys, secret=True)


def gpg_export(args):
    """export a gpg key, optionally including secret key"""
    keys = args.keys
    if not keys:
        keys = spack.util.gpg.signing_keys()
    spack.util.gpg.export_keys(args.location, keys, args.secret)


def gpg_list(args):
    """list keys available in the keyring"""
    spack.util.gpg.list(args.trusted, args.signing)


def gpg_sign(args):
    """sign a package"""
    key = args.key
    if key is None:
        keys = spack.util.gpg.signing_keys()
        if len(keys) == 1:
            key = keys[0]
        elif not keys:
            raise RuntimeError("no signing keys are available")
        else:
            raise RuntimeError("multiple signing keys are available; please choose one")
    output = args.output
    if not output:
        output = args.spec[0] + ".asc"
    # TODO: Support the package format Spack creates.
    spack.util.gpg.sign(key, " ".join(args.spec), output, args.clearsign)


def gpg_trust(args):
    """add a key to the keyring"""
    spack.util.gpg.trust(args.keyfile)


def gpg_init(args):
    """add the default keys to the keyring"""
    import_dir = args.import_dir
    if import_dir is None:
        import_dir = spack.paths.gpg_keys_path

    for root, _, filenames in os.walk(import_dir):
        for filename in filenames:
            if not filename.endswith(".key"):
                continue
            spack.util.gpg.trust(os.path.join(root, filename))


def gpg_untrust(args):
    """remove a key from the keyring"""
    spack.util.gpg.untrust(args.signing, *args.keys)


def gpg_verify(args):
    """verify a signed package"""
    # TODO: Support the package format Spack creates.
    signature = args.signature
    if signature is None:
        signature = args.spec[0] + ".asc"
    spack.util.gpg.verify(signature, " ".join(args.spec))


def gpg_publish(args):
    """publish public keys to a build cache"""

    mirror = None
    if args.directory:
        url = spack.util.url.path_to_file_url(args.directory)
        mirror = spack.mirror.Mirror(url, url)
    elif args.mirror_name:
        mirror = spack.mirror.MirrorCollection(binary=True).lookup(args.mirror_name)
    elif args.mirror_url:
        mirror = spack.mirror.Mirror(args.mirror_url, args.mirror_url)

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
        spack.binary_distribution._url_push_keys(
            mirror, keys=args.keys, tmpdir=tmpdir, update_index=args.update_index
        )


def gpg(parser, args):
    if args.func:
        args.func(args)
