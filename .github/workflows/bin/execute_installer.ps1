$ proc = Start-Process  ${{ env.spack_installer }}\spack.exe "/install /quiet" -Passthru
$handle = $proc.Handle # cache proc.Handle
$proc.WaitForExit();

if ($proc.ExitCode -ne 0) {
    Write-Warning "$_ exited with status code $($proc.ExitCode)"
}
