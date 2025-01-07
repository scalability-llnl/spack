# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import ast
import os
import re
import sys
from itertools import zip_longest
from typing import Dict, List, Optional

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.filesystem import working_dir

import spack.paths
import spack.repo
import spack.util.git
from spack.util.executable import Executable, which

description = "runs source code style checks on spack"
section = "developer"
level = "long"


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    for group in zip_longest(*args, fillvalue=fillvalue):
        yield filter(None, group)


#: List of directories to exclude from checks -- relative to spack root
exclude_directories = [os.path.relpath(spack.paths.external_path, spack.paths.prefix)]

#: Order in which tools should be run. flake8 is last so that it can
#: double-check the results of other tools (if, e.g., --fix was provided)
#: The list maps an executable name to a method to ensure the tool is
#: bootstrapped or present in the environment.
tool_names = ["import", "isort", "black", "flake8", "mypy"]

#: warnings to ignore in mypy
mypy_ignores = [
    # same as `disable_error_code = "annotation-unchecked"` in pyproject.toml, which
    # doesn't exist in mypy 0.971 for Python 3.6
    "[annotation-unchecked]"
]


def is_package(f):
    """Whether flake8 should consider a file as a core file or a package.

    We run flake8 with different exceptions for the core and for
    packages, since we allow `from spack import *` and poking globals
    into packages.
    """
    return f.startswith("var/spack/repos/") and f.endswith("package.py")


#: decorator for adding tools to the list
class tool:
    def __init__(self, name: str, required: bool = False, external: bool = True) -> None:
        self.name = name
        self.external = external
        self.required = required

    def __call__(self, fun):
        self.fun = fun
        tools[self.name] = self
        return fun

    @property
    def installed(self) -> bool:
        return bool(which(self.name)) if self.external else True

    @property
    def executable(self) -> Optional[Executable]:
        return which(self.name) if self.external else None


#: tools we run in spack style
tools: Dict[str, tool] = {}


def changed_files(base="develop", untracked=True, all_files=False, root=None):
    """Get list of changed files in the Spack repository.

    Arguments:
        base (str): name of base branch to evaluate differences with.
        untracked (bool): include untracked files in the list.
        all_files (bool): list all files in the repository.
        root (str): use this directory instead of the Spack prefix.
    """
    if root is None:
        root = spack.paths.prefix

    git = spack.util.git.git(required=True)

    # ensure base is in the repo
    base_sha = git(
        "rev-parse", "--quiet", "--verify", "--revs-only", base, fail_on_error=False, output=str
    )
    if git.returncode != 0:
        tty.die(
            "This repository does not have a '%s' revision." % base,
            "spack style needs this branch to determine which files changed.",
            "Ensure that '%s' exists, or specify files to check explicitly." % base,
        )

    range = "{0}...".format(base_sha.strip())

    git_args = [
        # Add changed files committed since branching off of develop
        ["diff", "--name-only", "--diff-filter=ACMR", range],
        # Add changed files that have been staged but not yet committed
        ["diff", "--name-only", "--diff-filter=ACMR", "--cached"],
        # Add changed files that are unstaged
        ["diff", "--name-only", "--diff-filter=ACMR"],
    ]

    # Add new files that are untracked
    if untracked:
        git_args.append(["ls-files", "--exclude-standard", "--other"])

    # add everything if the user asked for it
    if all_files:
        git_args.append(["ls-files", "--exclude-standard"])

    excludes = [os.path.realpath(os.path.join(root, f)) for f in exclude_directories]
    changed = set()

    for arg_list in git_args:
        files = git(*arg_list, output=str).split("\n")

        for f in files:
            # Ignore non-Python files
            if not (f.endswith(".py") or f == "bin/spack"):
                continue

            # Ignore files in the exclude locations
            if any(os.path.realpath(f).startswith(e) for e in excludes):
                continue

            changed.add(f)

    return sorted(changed)


def setup_parser(subparser):
    subparser.add_argument(
        "-b",
        "--base",
        action="store",
        default="develop",
        help="branch to compare against to determine changed files (default: develop)",
    )
    subparser.add_argument(
        "-a", "--all", action="store_true", help="check all files, not just changed files"
    )
    subparser.add_argument(
        "-r",
        "--root-relative",
        action="store_true",
        default=False,
        help="print root-relative paths (default: cwd-relative)",
    )
    subparser.add_argument(
        "-U",
        "--no-untracked",
        dest="untracked",
        action="store_false",
        default=True,
        help="exclude untracked files from checks",
    )
    subparser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        default=False,
        help="format automatically if possible (e.g., with isort, black)",
    )
    subparser.add_argument(
        "--root", action="store", default=None, help="style check a different spack instance"
    )

    tool_group = subparser.add_mutually_exclusive_group()
    tool_group.add_argument(
        "-t",
        "--tool",
        action="append",
        help="specify which tools to run (default: %s)" % ", ".join(tool_names),
    )
    tool_group.add_argument(
        "-s",
        "--skip",
        metavar="TOOL",
        action="append",
        help="specify tools to skip (choose from %s)" % ", ".join(tool_names),
    )

    subparser.add_argument("files", nargs=argparse.REMAINDER, help="specific files to check")


def cwd_relative(path, root, initial_working_dir):
    """Translate prefix-relative path to current working directory-relative."""
    return os.path.relpath(os.path.join(root, path), initial_working_dir)


def rewrite_and_print_output(
    output, args, re_obj=re.compile(r"^(.+):([0-9]+):"), replacement=r"{0}:{1}:"
):
    """rewrite ouput with <file>:<line>: format to respect path args"""

    # print results relative to current working directory
    def translate(match):
        return replacement.format(
            cwd_relative(match.group(1), args.root, args.initial_working_dir),
            *list(match.groups()[1:]),
        )

    for line in output.split("\n"):
        if not line:
            continue
        if any(ignore in line for ignore in mypy_ignores):
            # some mypy annotations can't be disabled in older mypys (e.g. .971, which
            # is the only mypy that supports python 3.6), so we filter them here.
            continue
        if not args.root_relative and re_obj:
            line = re_obj.sub(translate, line)
        print(line)


def print_style_header(file_list, args, tools_to_run):
    tty.msg("Running style checks on spack", "selected: " + ", ".join(tools_to_run))
    # translate modified paths to cwd_relative if needed
    paths = [filename.strip() for filename in file_list]
    if not args.root_relative:
        paths = [cwd_relative(filename, args.root, args.initial_working_dir) for filename in paths]

    tty.msg("Modified files", *paths)
    sys.stdout.flush()


def print_tool_header(tool):
    sys.stdout.flush()
    tty.msg("Running %s checks" % tool)
    sys.stdout.flush()


def print_tool_result(tool, returncode):
    if returncode == 0:
        color.cprint("  @g{%s checks were clean}" % tool)
    else:
        color.cprint("  @r{%s found errors}" % tool)


@tool("flake8", required=True)
def run_flake8(flake8_cmd, file_list, args):
    returncode = 0
    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        output = flake8_cmd(
            # always run with config from running spack prefix
            "--config=%s" % os.path.join(spack.paths.prefix, ".flake8"),
            *chunk,
            fail_on_error=False,
            output=str,
        )
        returncode |= flake8_cmd.returncode

        rewrite_and_print_output(output, args)

    print_tool_result("flake8", returncode)
    return returncode


@tool("mypy")
def run_mypy(mypy_cmd, file_list, args):
    # always run with config from running spack prefix
    common_mypy_args = [
        "--config-file",
        os.path.join(spack.paths.prefix, "pyproject.toml"),
        "--show-error-codes",
    ]
    mypy_arg_sets = [common_mypy_args + ["--package", "spack", "--package", "llnl"]]
    if "SPACK_MYPY_CHECK_PACKAGES" in os.environ:
        mypy_arg_sets.append(
            common_mypy_args + ["--package", "packages", "--disable-error-code", "no-redef"]
        )

    returncode = 0
    for mypy_args in mypy_arg_sets:
        output = mypy_cmd(*mypy_args, fail_on_error=False, output=str)
        returncode |= mypy_cmd.returncode

        rewrite_and_print_output(output, args)

    print_tool_result("mypy", returncode)
    return returncode


@tool("isort")
def run_isort(isort_cmd, file_list, args):
    # always run with config from running spack prefix
    isort_args = ("--settings-path", os.path.join(spack.paths.prefix, "pyproject.toml"))
    if not args.fix:
        isort_args += ("--check", "--diff")

    pat = re.compile("ERROR: (.*) Imports are incorrectly sorted")
    replacement = "ERROR: {0} Imports are incorrectly sorted"
    returncode = [0]

    def process_files(file_list, is_args):
        for chunk in grouper(file_list, 100):
            packed_args = is_args + tuple(chunk)
            output = isort_cmd(*packed_args, fail_on_error=False, output=str, error=str)
            returncode[0] |= isort_cmd.returncode

            rewrite_and_print_output(output, args, pat, replacement)

    packages_isort_args = (
        "--rm",
        "spack.pkgkit",
        "--rm",
        "spack.package_defs",
        "-a",
        "from spack.package import *",
    )
    packages_isort_args = packages_isort_args + isort_args

    # packages
    process_files(filter(is_package, file_list), packages_isort_args)
    # non-packages
    process_files(filter(lambda f: not is_package(f), file_list), isort_args)

    print_tool_result("isort", returncode[0])
    return returncode[0]


@tool("black")
def run_black(black_cmd, file_list, args):
    # always run with config from running spack prefix
    black_args = ("--config", os.path.join(spack.paths.prefix, "pyproject.toml"))
    if not args.fix:
        black_args += ("--check", "--diff")
        if color.get_color_when():  # only show color when spack would
            black_args += ("--color",)

    pat = re.compile("would reformat +(.*)")
    replacement = "would reformat {0}"
    returncode = 0
    output = ""
    # run in chunks of 100 at a time to avoid line length limit
    # filename parameter in config *does not work* for this reliably
    for chunk in grouper(file_list, 100):
        packed_args = black_args + tuple(chunk)
        output = black_cmd(*packed_args, fail_on_error=False, output=str, error=str)
        returncode |= black_cmd.returncode
        rewrite_and_print_output(output, args, pat, replacement)

    print_tool_result("black", returncode)

    return returncode


def _module_part(root: str, expr: str):
    parts = expr.split(".")
    # spack.pkg is for repositories, don't try to resolve it here.
    if ".".join(parts[:2]) == spack.repo.ROOT_PYTHON_NAMESPACE:
        return None
    while parts:
        f1 = os.path.join(root, "lib", "spack", *parts) + ".py"
        f2 = os.path.join(root, "lib", "spack", *parts, "__init__.py")

        if (
            os.path.exists(f1)
            # ensure case sensitive match
            and f"{parts[-1]}.py" in os.listdir(os.path.dirname(f1))
            or os.path.exists(f2)
        ):
            return ".".join(parts)
        parts.pop()
    return None


def _run_import_check(
    file_list: List[str],
    *,
    fix: bool,
    root_relative: bool,
    root=spack.paths.prefix,
    working_dir=spack.paths.prefix,
    out=sys.stdout,
):
    if sys.version_info < (3, 9):
        print("import check requires Python 3.9 or later")
        return 0

    is_use = re.compile(r"(?<!from )(?<!import )(?:llnl|spack)\.[a-zA-Z0-9_\.]+")

    # redundant imports followed by a `# comment` are ignored, cause there can be legimitate reason
    # to import a module: execute module scope init code, or to deal with circular imports.
    is_abs_import = re.compile(r"^import ((?:llnl|spack)\.[a-zA-Z0-9_\.]+)$", re.MULTILINE)

    exit_code = 0

    for file in file_list:
        to_add = set()
        to_remove = []

        pretty_path = file if root_relative else cwd_relative(file, root, working_dir)

        try:
            with open(file, "r", encoding="utf-8") as f:
                contents = f.read()
            parsed = ast.parse(contents)
        except Exception:
            exit_code = 1
            print(f"{pretty_path}: could not parse", file=out)
            continue

        for m in is_abs_import.finditer(contents):
            if contents.count(m.group(1)) == 1:
                to_remove.append(m.group(0))
                exit_code = 1
                print(f"{pretty_path}: redundant import: {m.group(1)}", file=out)

        # Clear all strings to avoid matching comments/strings etc.
        for node in ast.walk(parsed):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                node.value = ""

        filtered_contents = ast.unparse(parsed)  # novermin
        for m in is_use.finditer(filtered_contents):
            module = _module_part(root, m.group(0))
            if not module or module in to_add:
                continue
            if re.search(rf"import {re.escape(module)}\b(?!\.)", contents):
                continue
            to_add.add(module)
            exit_code = 1
            print(f"{pretty_path}: missing import: {module} ({m.group(0)})", file=out)

        if not fix or not to_add and not to_remove:
            continue

        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if to_add:
            # insert missing imports before the first import, delegate ordering to isort
            for node in parsed.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    first_line = node.lineno
                    break
            else:
                print(f"{pretty_path}: could not fix", file=out)
                continue
            lines.insert(first_line, "\n".join(f"import {x}" for x in to_add) + "\n")

        new_contents = "".join(lines)

        # remove redundant imports
        for statement in to_remove:
            new_contents = new_contents.replace(f"{statement}\n", "")

        with open(file, "w", encoding="utf-8") as f:
            f.write(new_contents)

    return exit_code


@tool("import", external=False)
def run_import_check(import_check_cmd, file_list, args):
    exit_code = _run_import_check(
        file_list,
        fix=args.fix,
        root_relative=args.root_relative,
        root=args.root,
        working_dir=args.initial_working_dir,
    )
    print_tool_result("import", exit_code)
    return exit_code


def validate_toolset(arg_value):
    """Validate --tool and --skip arguments (sets of optionally comma-separated tools)."""
    tools = set(",".join(arg_value).split(","))  # allow args like 'isort,flake8'
    for tool in tools:
        if tool not in tool_names:
            tty.die("Invalid tool: '%s'" % tool, "Choose from: %s" % ", ".join(tool_names))
    return tools


def missing_tools(tools_to_run: List[str]) -> List[str]:
    return [t for t in tools_to_run if not tools[t].installed]


def _bootstrap_dev_dependencies():
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_environment_dependencies()


def style(parser, args):
    # save initial working directory for relativizing paths later
    args.initial_working_dir = os.getcwd()

    # ensure that the config files we need actually exist in the spack prefix.
    # assertions b/c users should not ever see these errors -- they're checked in CI.
    assert os.path.isfile(os.path.join(spack.paths.prefix, "pyproject.toml"))
    assert os.path.isfile(os.path.join(spack.paths.prefix, ".flake8"))

    # validate spack root if the user provided one
    args.root = os.path.realpath(args.root) if args.root else spack.paths.prefix
    spack_script = os.path.join(args.root, "bin", "spack")
    if not os.path.exists(spack_script):
        tty.die("This does not look like a valid spack root.", "No such file: '%s'" % spack_script)

    file_list = args.files
    if file_list:

        def prefix_relative(path):
            return os.path.relpath(os.path.abspath(os.path.realpath(path)), args.root)

        file_list = [prefix_relative(p) for p in file_list]

    # process --tool and --skip arguments
    selected = set(tool_names)
    if args.tool is not None:
        selected = validate_toolset(args.tool)
    if args.skip is not None:
        selected -= validate_toolset(args.skip)

    if not selected:
        tty.msg("Nothing to run.")
        return

    tools_to_run = [t for t in tool_names if t in selected]
    if missing_tools(tools_to_run):
        _bootstrap_dev_dependencies()

    return_code = 0
    with working_dir(args.root):
        if not file_list:
            file_list = changed_files(args.base, args.untracked, args.all)

        print_style_header(file_list, args, tools_to_run)
        for tool_name in tools_to_run:
            tool = tools[tool_name]
            print_tool_header(tool_name)
            return_code |= tool.fun(tool.executable, file_list, args)

    if return_code == 0:
        tty.msg(color.colorize("@*{spack style checks were clean}"))
    else:
        tty.error(color.colorize("@*{spack style found errors}"))

    return return_code
