# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# The following global variables are used/set by Bash programmable completion
#     COMP_CWORD: An index into ${COMP_WORDS} of the word containing the
#                 current cursor position
#     COMP_LINE:  The current command line
#     COMP_WORDS: an array containing individual command arguments typed so far
#     COMPREPLY:  an array containing possible completions as a result of your
#                 function

# Bash programmable completion for Spack
function _bash_completion_spack {
    # In all following examples, let the cursor be denoted by brackets, i.e. []

    # For our purposes, flags should not affect tab completion. For instance,
    # `spack install []` and `spack -d install --jobs 8 []` should both give the same
    # possible completions. Therefore, we need to ignore any flags in COMP_WORDS.
    local COMP_WORDS_NO_FLAGS=()
    local index=0
    while [[ "$index" -lt "$COMP_CWORD" ]]
    do
        if [[ "${COMP_WORDS[$index]}" == [a-z]* ]]
        then
            COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$index]}")
        fi
        let index++
    done

    # Options will be listed by a subfunction named after non-flag arguments.
    # For example, `spack -d install []` will call _spack_install
    # and `spack compiler add []` will call _spack_compiler_add
    local subfunction=$(IFS='_'; echo "_${COMP_WORDS_NO_FLAGS[*]}")
    # Translate dashes to underscores, as dashes are not permitted in
    # compatibility mode. See https://github.com/spack/spack/pull/4079
    subfunction=${subfunction//-/_}

    # However, the word containing the current cursor position needs to be
    # added regardless of whether or not it is a flag. This allows us to
    # complete something like `spack install --keep-st[]`
    COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$COMP_CWORD]}")

    # Since we have removed all words after COMP_CWORD, we can safely assume
    # that COMP_CWORD_NO_FLAGS is simply the index of the last element
    local COMP_CWORD_NO_FLAGS=$(( ${#COMP_WORDS_NO_FLAGS[@]} - 1 ))

    # There is no guarantee that the cursor is at the end of the command line
    # when tab completion is envoked. For example, in the following situation:
    #     `spack -d [] install`
    # if the user presses the TAB key, a list of valid flags should be listed.
    # Note that we cannot simply ignore everything after the cursor. In the
    # previous scenario, the user should expect to see a list of flags, but
    # not of other subcommands. Obviously, `spack -d list install` would be
    # invalid syntax. To accomplish this, we use the variable list_options
    # which is true if the current word starts with '-' or if the cursor is
    # not at the end of the line.
    local list_options=false
    if [[ "${COMP_WORDS[$COMP_CWORD]}" == -* || \
          "$COMP_CWORD" -ne "${#COMP_WORDS[@]}-1" ]]
    then
        list_options=true
    fi

    # In general, when envoking tab completion, the user is not expecting to
    # see optional flags mixed in with subcommands or package names. Tab
    # completion is used by those who are either lazy or just bad at spelling.
    # If someone doesn't remember what flag to use, seeing single letter flags
    # in their results won't help them, and they should instead consult the
    # documentation. However, if the user explicitly declares that they are
    # looking for a flag, we can certainly help them out.
    #     `spack install -[]`
    # and
    #     `spack install --[]`
    # should list all flags and long flags, respectively. Furthermore, if a
    # subcommand has no non-flag completions, such as `spack arch []`, it
    # should list flag completions.

    local cur=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS]}
    local prev=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS-1]}

    #_test_vars

    # Make sure function exists before calling it
    if [[ "$(type -t $subfunction)" == "function" ]]
    then
        COMPREPLY=($($subfunction))
    fi
}

# Spack commands

function _spack {
    if $list_options
    then
        compgen -W "-h --help -H --all-help --color -C --config-scope
                    -d --debug --pdb -e --env -D --env-dir -E --no-env
                    --use-env-repo -k --insecure -l --enable-locks
                    -L --disable-locks -m --mock -p --profile
                    --sorted-profile --lines -v --verbose --stacktrace
                    -V --version --print-shell-vars" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

function _spack_activate {
    if $list_options
    then
        compgen -W "-h --help -f --force -v --view" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_add {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_arch {
    compgen -W "-h --help -p --platform -o --operating-system
                -t --target --known-targets" -- "$cur"
}

function _spack_blame {
    if $list_options
    then
        compgen -W "-h --help -t --time -p --percent -g --git" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_bootstrap {
    compgen -W "-h --help -j --jobs --keep-prefix --keep-stage
                -n --no-checksum -v --verbose --use-cache --no-cache
                --clean --dirty" -- "$cur"
}

function _spack_build {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_build_env {
    if $list_options
    then
        compgen -W "-h --help --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_buildcache {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create install keys list" -- "$cur"
    fi
}

function _spack_buildcache_create {
    if $list_options
    then
        compgen -W "-h --help -r --rel -f --force -u --unsigned -a --allow-root
                    -k --key -d --directory" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_buildcache_install {
    if $list_options
    then
        compgen -W "-h --help -f --force -m --multiple -a --allow-root -u
                    --unsigned" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_buildcache_keys {
    compgen -W "-h --help -i --install -t --trust -f --force" -- "$cur"
}

function _spack_buildcache_list {
    if $list_options
    then
        compgen -W "-h --help -f --force" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_cd {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir
                    -p --package-dir -P --packages -s --stage-dir -S --stages
                    -b --build-dir -e --env" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_checksum {
    if $list_options
    then
        compgen -W "-h --help --keep-stage" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_clean {
    if $list_options
    then
        compgen -W "-h --help -s --stage -d --downloads
                    -m --misc-cache -p --python-cache -a --all" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_clone {
    if $list_options
    then
        compgen -W "-h --help -r --remote" -- "$cur"
    fi
}

function _spack_commands {
    if $list_options
    then
        compgen -W "-h --help --format --header --update" -- "$cur"
    fi
}

function _spack_compiler {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "find add remove rm list info" -- "$cur"
    fi
}

function _spack_compiler_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

function _spack_compiler_find {
    # Alias to `spack compiler add`
    _spack_compiler_add
}

function _spack_compiler_info {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

function _spack_compiler_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_compiler_remove {
    if $list_options
    then
        compgen -W "-h --help -a --all --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

function _spack_compiler_rm {
    # Alias to `spack compiler remove`
    _spack_compiler_remove
}

function _spack_compilers {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_concretize {
    compgen -W "-h --help -f --force" -- "$cur"
}

function _spack_config {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "blame edit get" -- "$cur"
    fi
}

function _spack_config_blame {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "mirrors repos modules packages config compilers" -- "$cur"
    fi
}

function _spack_config_edit {
    if $list_options
    then
        compgen -W "-h --help --print-file" -- "$cur"
    else
        compgen -W "mirrors repos modules packages config compilers" -- "$cur"
    fi
}

function _spack_config_get {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "mirrors repos modules packages config compilers" -- "$cur"
    fi
}

function _spack_configure {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_create {
    if $list_options
    then
        compgen -W "-h --help --keep-stage -n --name -t --template -r --repo
                    -N --namespace -f --force --skip-editor" -- "$cur"
    fi
}

function _spack_deactivate {
    if $list_options
    then
        compgen -W "-h --help -f --force -v --view -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_debug {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create-db-tarball" -- "$cur"
    fi
}

function _spack_debug_create_db_tarball {
    compgen -W "-h --help" -- "$cur"
}

function _spack_dependencies {
    if $list_options
    then
        compgen -W "-h --help -i --installed -t --transitive -V
                    --no-expand-virtuals" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_dependents {
    if $list_options
    then
        compgen -W "-h --help -i --installed -t --transitive" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_diy {
    if $list_options
    then
        compgen -W "-h --help -j --jobs -d --source-path
                    -i --ignore-dependencies -n --no-checksum
                    --keep-prefix --skip-patch -q --quiet --clean
                    --dirty -u --until" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_docs {
    compgen -W "-h --help" -- "$cur"
}

function _spack_edit {
    if $list_options
    then
        compgen -W "-h --help -b --build-system -c --command -d --docs -t
                    --test -m --module -r --repo -N --namespace" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_env {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "activate create deactivate list ls loads
                    remove rm status st" -- "$cur"
    fi
}

function _spack_env_activate {
    if $list_options
    then
        compgen -W "-h --help --sh --csh -d --dir -p --prompt" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

function _spack_env_create {
    if $list_options
    then
        compgen -W "-h --help -d --dir" -- "$cur"
    fi
}

function _spack_env_deactivate {
    compgen -W "-h --help --sh --csh" -- "$cur"
}

function _spack_env_list {
    compgen -W "-h --help" -- "$cur"
}

function _spack_env_ls {
    # Alias to `spack env list`
    _spack_env_list
}

function _spack_env_loads {
    if $list_options
    then
        compgen -W "-h --help -m --module-type --input-only -p --prefix
                    -x --exclude -r --dependencies" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

function _spack_env_remove {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_environments)" -- "$cur"
    fi
}

function _spack_env_rm {
    # Alias to `spack env remove`
    _spack_env_remove
}

function _spack_env_status {
    compgen -W "-h --help" -- "$cur"
}

function _spack_env_st {
    # Alias to `spack env status`
    _spack_env_status
}

function _spack_extensions {
    if $list_options
    then
        compgen -W "-h --help -l --long -p --paths -d --deps
                    -s --show -v --view" -- "$cur"
    else
        compgen -W "aspell go-bootstrap go icedtea java jdk lua
                    matlab mofem-cephas octave perl python r ruby
                    rust tcl yorick" -- "$cur"
    fi
}

function _spack_fetch {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -m --missing
                    -D --dependencies" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_find {
    if $list_options
    then
        compgen -W "-h --help -s --short -d --deps -p --paths
                    --format --json --groups --no-groups -l --long
                    -L --very-long -t --tags -c --show-concretized
                    -f --show-flags --show-full-compiler -x --explicit
                    -X --implicit -u --unknown -m --missing -v --variants
                    -M --only-missing -N --namespace --start-date
                    --end-date" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_flake8 {
    if $list_options
    then
        compgen -W "-h --help -b --base -k --keep-temp -a --all -o --output
                    -r --root-relative -U --no-untracked" -- "$cur"
    fi
}

function _spack_gpg {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create export init list sign trust untrust verify" -- "$cur"
    fi
}

function _spack_gpg_create {
    if $list_options
    then
        compgen -W "-h --help --comment --expires --export" -- "$cur"
    fi
}

function _spack_gpg_export {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_gpg_init {
    compgen -W "-h --help" -- "$cur"
}

function _spack_gpg_list {
    compgen -W "-h --help --trusted --signing" -- "$cur"
}

function _spack_gpg_sign {
    if $list_options
    then
        compgen -W "-h --help --output --key --clearsign" -- "$cur"
    else
        compgen -W "$(installed_packages)" -- "$cur"
    fi
}

function _spack_gpg_trust {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_gpg_untrust {
    if $list_options
    then
        compgen -W "-h --help --signing" -- "$cur"
    fi
}

function _spack_gpg_verify {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(installed_packages)" -- "$cur"
    fi
}

function _spack_graph {
    if $list_options
    then
        compgen -W "-h --help -a --ascii -d --dot -n --normalize -s --static
                    -i --installed -t --deptype" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_help {
    if $list_options
    then
        compgen -W "-h --help -a --all --spec" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

function _spack_info {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_install {
    if $list_options
    then
        compgen -W "-h --help --only -j --jobs --overwrite --keep-prefix
                    --keep-stage --dont-restage --use-cache --no-cache
                    --cache-only --show-log-on-error --source -n --no-checksum
                    -v --verbose --fake --only-concrete -f --file --clean
                    --dirty --test --run-tests --log-format --log-file
                    --cdash-upload-url --cdash-build --cdash-site --cdash-track
                    --cdash-buildstamp --help-cdash -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_license {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list-files verify" -- "$cur"
    fi
}

function _spack_license_list_files {
    compgen -W "-h --help" -- "$cur"
}

function _spack_license_verify {
    compgen -W "-h --help --root" -- "$cur"
}

function _spack_list {
    if $list_options
    then
        compgen -W "-h --help -d --search-description --format --update
                    -t --tags" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_load {
    if $list_options
    then
        compgen -W "-h --help -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_location {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir
                    -p --package-dir -P --packages -s --stage-dir -S --stages
                    -b --build-dir -e --env" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_log_parse {
    if $list_options
    then
        compgen -W "-h --help --show -c --context -p --profile -w --width
                    -j --jobs" -- "$cur"
    fi
}

function _spack_maintainers {
    if $list_options
    then
        compgen -W "-h --help -a --all --maintained --unmaintained
                    --by-user" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_mirror {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "add create list remove rm" -- "$cur"
    fi
}

function _spack_mirror_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

function _spack_mirror_create {
    if $list_options
    then
        compgen -W "-h --help -d --directory -f --file
                    -D --dependencies -n --versions-per-spec" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_mirror_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_mirror_remove {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_mirrors)" -- "$cur"
    fi
}

function _spack_mirror_rm {
    # Alias to `spack mirror remove`
    _spack_mirror_remove
}

function _spack_module {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "lmod tcl" -- "$cur"
    fi
}

function _spack_module_tcl {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "refresh find rm loads" -- "$cur"
    fi
}


function _spack_module_tcl_find {
    if $list_options
    then
        compgen -W "-h --help --full-path -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_tcl_loads {
    if $list_options
    then
        compgen -W "-h --help --input-only -p --prefix -x --exclude
                    -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi

}

function _spack_module_tcl_refresh {
    if $list_options
    then
        compgen -W "-h --help --delete-tree -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_tcl_rm {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}


function _spack_module_lmod {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "refresh find rm loads setdefault" -- "$cur"
    fi
}


function _spack_module_lmod_find {
    if $list_options
    then
        compgen -W "-h --help --full-path -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_lmod_loads {
    if $list_options
    then
        compgen -W "-h --help --input-only -p --prefix -x --exclude
                    -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi

}

function _spack_module_lmod_refresh {
    if $list_options
    then
        compgen -W "-h --help --delete-tree -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_lmod_rm {
    if $list_options
    then
        compgen -W "-h --help -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_lmod_setdefault {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_patch {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_pkg {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add added diff list removed" -- "$cur"
    fi
}

function _spack_pkg_add {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_pkg_added {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_pkg_diff {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_pkg_list {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_pkg_removed {
    # FIXME: How to list git revisions?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_providers {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_providers)" -- "$cur"
    fi
}

function _spack_pydoc {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_python {
    if $list_options
    then
        compgen -W "-h --help -c" -- "$cur"
    fi
}

function _spack_reindex {
    compgen -W "-h --help" -- "$cur"
}

function _spack_remove {
    if $list_options
    then
        compgen -W "-h --help -a --all -f --force" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_repo {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add create list remove rm" -- "$cur"
    fi
}

function _spack_repo_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    fi
}

function _spack_repo_create {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_repo_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_repo_remove {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_repos)" -- "$cur"
    fi
}

function _spack_repo_rm {
    # Alias to `spack repo remove`
    _spack_repo_remove
}

function _spack_resource {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list show" -- "$cur"
    fi
}

function _spack_resource_list {
    compgen -W "-h --help --only-hashes" -- "$cur"
}

function _spack_resource_show {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_resource_hashes)" -- "$cur"
    fi
}

function _spack_restage {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_setup {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies -n --no-checksum
                    -v --verbose --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_spec {
    if $list_options
    then
        compgen -W "-h --help -l --long -L --very-long -I --install-status
                    -j --json -y --yaml -c --cover -N --namespaces
                    -t --types -u --uarch-flags" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_stage {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -p --path" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_test {
    if $list_options
    then
        compgen -W "-h --help -H --pytest-help -l --list
                    -L --long-list" -- "$cur"
    else
        compgen -W "$(_tests)" -- "$cur"
    fi
}

function _spack_uninstall {
    if $list_options
    then
        compgen -W "-h --help -f --force -R --dependents
                    -y --yes-to-all -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_unload {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)"
    fi
}

function _spack_unuse {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)"
    fi
}

function _spack_url {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list parse stats summary" -- "$cur"
    fi
}

function _spack_url_list {
    compgen -W "-h --help -c --color -e --extrapolation
                -n --incorrect-name -N --correct-name
                -v --incorrect-version -V --correct-version" -- "$cur"
}

function _spack_url_parse {
    if $list_options
    then
        compgen -W "-h --help -s --spider" -- "$cur"
    fi
}

function _spack_url_stats {
    compgen -W "-h --help" -- "$cur"
}

function _spack_url_summary {
    compgen -W "-h --help" -- "$cur"
}

function _spack_use {
    if $list_options
    then
        compgen -W "-h --help -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_versions {
    if $list_options
    then
        compgen -W "-h --help -s --safe-only" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_view {
    if $list_options
    then
        compgen -W "-h --help -v --verbose -e --exclude
                    -d --dependencies" -- "$cur"
    else
        compgen -W "add check hard hardlink remove rm soft
                    statlink status symlink" -- "$cur"
    fi
}

function _spack_view_add {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

function _spack_view_check {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

function _spack_view_hard {
    # Alias for `spack view hardlink`
    _spack_view_hardlink
}

function _spack_view_hardlink {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-conflicts" -- "$cur"
    fi
}

function _spack_view_remove {
    if $list_options
    then
        compgen -W "-h --help --no-remove-dependents -a --all" -- "$cur"
    fi
}

function _spack_view_rm {
    # Alias for `spack view remove`
    _spack_view_remove
}

function _spack_view_soft {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

function _spack_view_statlink {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    fi
}

function _spack_view_status {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

function _spack_view_symlink {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-conflicts" -- "$cur"
    fi
}

# Helper functions for subcommands

function _subcommands {
    spack commands
}

function _all_packages {
    spack list
}

function _all_resource_hashes {
    spack resource list --only-hashes
}

function _installed_packages {
    spack --color=never find --no-groups
}

function _installed_compilers {
    spack compilers | egrep -v "^(-|=)"
}

function _providers {
    spack providers
}

function _mirrors {
    spack mirror list | awk '{print $1}'
}

function _repos {
    spack repo list | awk '{print $1}'
}

function _tests {
    spack test -l
}

function _environments {
    spack env list
}

# Testing functions

function _test_vars {
    echo "-----------------------------------------------------"             >> temp
    echo "Full line:                '$COMP_LINE'"                            >> temp
    echo                                                                     >> temp
    echo "Word list w/ flags:       $(_pretty_print COMP_WORDS[@])"          >> temp
    echo "# words w/ flags:         '${#COMP_WORDS[@]}'"                     >> temp
    echo "Cursor index w/ flags:    '$COMP_CWORD'"                           >> temp
    echo                                                                     >> temp
    echo "Word list w/out flags:    $(_pretty_print COMP_WORDS_NO_FLAGS[@])" >> temp
    echo "# words w/out flags:      '${#COMP_WORDS_NO_FLAGS[@]}'"            >> temp
    echo "Cursor index w/out flags: '$COMP_CWORD_NO_FLAGS'"                  >> temp
    echo                                                                     >> temp
    echo "Subfunction:              '$subfunction'"                          >> temp
    if $list_options
    then
        echo "List options:             'True'"  >> temp
    else
        echo "List options:             'False'" >> temp
    fi
    echo "Current word:             '$cur'"  >> temp
    echo "Previous word:            '$prev'" >> temp
}

# Pretty-prints one or more arrays
# Syntax: _pretty_print array1[@] ...
function _pretty_print {
    for arg in $@
    do
        local array=("${!arg}")
        echo -n "$arg: ["
        printf   "'%s'" "${array[0]}"
        printf ", '%s'" "${array[@]:1}"
        echo "]"
    done
}

complete -o default -F _bash_completion_spack spack
