#  Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
#  Spack Project Developers. See the top-level COPYRIGHT file for details.

#  SPDX-License-Identifier: (Apache-2.0 OR MIT)
# #######################################################################

function Compare-CommonArgs {
    $CMDArgs = $args[0]
    # These aruments take precedence and call for no futher parsing of arguments
    # invoke actual Spack entrypoint with that context and exit after
    "--help", "-h", "--version", "-V" | ForEach-Object {
        $arg_opt = $_
        if(($CMDArgs) -and ([bool]($CMDArgs.Where({$_ -eq $arg_opt})))) {
            return $true
        }
    }
    return $false
}

function Read-SpackArgs {
    $SpackCMD_params = @()
    $SpackSubCommand = $NULL
    $SpackSubCommandArgs = @()
    $args_ = $args[0]
    $args_ | ForEach-Object {
        if (!$SpackSubCommand) {
            if($_.SubString(0,1) -eq "-")
            {
                $SpackCMD_params += $_
            }
            else{
                $SpackSubCommand = $_
            }
        }
        else{
            $SpackSubCommandArgs += $_
        }
    }
    return $SpackCMD_params, $SpackSubCommand, $SpackSubCommandArgs
}

function Set-SpackEnv {
    # This method is responsible
    # for processing the return from $(spack <command>)
    # which are returned as System.Object[]'s containing
    # a list of env commands
    # Invoke-Expression can only handle one command at a time
    # so we iterate over the list to invoke the env modification
    # expressions one at a time
    foreach($envop in $args[0]){
        Invoke-Expression $envop
    }
}


function Invoke-SpackCD {
    if (Compare-CommonArgs $SpackSubCommandArgs) {
        python "$Env:SPACK_ROOT/bin/spack" cd -h
    }
    else {
        $LOC = $(python "$Env:SPACK_ROOT/bin/spack" location $SpackSubCommandArgs)
        if (($NULL -ne $LOC)){
            if ( Test-Path -Path $LOC){
                Set-Location $LOC
            }
            else{
                exit 1
            }
        }
        else {
            exit 1
        }
    }
}

function Invoke-SpackEnv {
    if (Compare-CommonArgs $SpackSubCommandArgs[0]) {
        python "$Env:SPACK_ROOT/bin/spack" env -h
    }
    else {
        $SubCommandSubCommand = $SpackSubCommandArgs[0]
        $SubCommandSubCommandArgs = $SpackSubCommandArgs[1..$SpackSubCommandArgs.Count]
        switch ($SubCommandSubCommand) {
            "activate" {
                if (Compare-CommonArgs $SubCommandSubCommandArgs) {
                    python "$Env:SPACK_ROOT/bin/spack" env activate $SubCommandSubCommandArgs
                }
                elseif ([bool]($SubCommandSubCommandArgs.Where({$_ -eq "--pwsh"}))) {
                    python "$Env:SPACK_ROOT/bin/spack" env activate $SubCommandSubCommandArgs
                }
                elseif (!$SubCommandSubCommandArgs) {
                    python "$Env:SPACK_ROOT/bin/spack" env activate $SubCommandSubCommandArgs
                }
                else {
                    $SpackEnv = $(python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params env activate "--pwsh" $SubCommandSubCommandArgs)
                    Set-SpackEnv $SpackEnv
                }
            }
            "deactivate" {
                if ([bool]($SubCommandSubCommandArgs.Where({$_ -eq "--pwsh"}))) {
                    python"$Env:SPACK_ROOT/bin/spack" env deactivate $SubCommandSubCommandArgs
                }
                elseif($SubCommandSubCommandArgs) {
                    python "$Env:SPACK_ROOT/bin/spack" env deactivate -h
                }
                else {
                    $SpackEnv = $(python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params env deactivate "--pwsh")
                    Set-SpackEnv $SpackEnv
                }
            }
            default {python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand $SpackSubCommandArgs}
        }
    }
}

function Invoke-SpackLoad {
    if (Compare-CommonArgs $SpackSubCommandArgs) {
        python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand $SpackSubCommandArgs
    }
    elseif ([bool]($SpackSubCommandArgs.Where({($_ -eq "--pwsh") -or ($_ -eq "--list")}))) {
        python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand $SpackSubCommandArgs
    }
    else {
        $SpackEnv = $(python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand "--pwsh" $SpackSubCommandArgs)
        Set-SpackEnv $SpackEnv
    }
}


$SpackCMD_params, $SpackSubCommand, $SpackSubCommandArgs = Read-SpackArgs $args

if (Compare-CommonArgs $SpackCMD_params) {
    python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand $SpackSubCommandArgs
    exit $LASTEXITCODE
}

# Process Spack commands with special conditions
# all other commands are piped directly to Spack
switch($SpackSubCommand)
{
    "cd"     {Invoke-SpackCD}
    "env"    {Invoke-SpackEnv}
    "load"   {Invoke-SpackLoad}
    "unload" {Invoke-SpackLoad}
    default  {python "$Env:SPACK_ROOT/bin/spack" $SpackCMD_params $SpackSubCommand $SpackSubCommandArgs}
}

exit $LASTEXITCODE
