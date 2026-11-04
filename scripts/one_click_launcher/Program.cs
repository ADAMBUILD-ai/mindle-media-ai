using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

internal static class Program
{
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBoxW(IntPtr hWnd, string text, string caption, uint type);

    private static bool VcRuntimePresent()
    {
        string systemRoot = Environment.GetEnvironmentVariable("SystemRoot") ?? @"C:\Windows";
        return File.Exists(Path.Combine(systemRoot, "System32", "msvcp140.dll"));
    }

    private static void EnsureVcRuntime(string dataRoot)
    {
        if (VcRuntimePresent())
            return;

        string prerequisiteRoot = Path.Combine(dataRoot, "prerequisites");
        Directory.CreateDirectory(prerequisiteRoot);
        string installer = Path.Combine(prerequisiteRoot, "vc_redist.x64.exe");
        string scriptPath = Path.Combine(prerequisiteRoot, "install_vc_runtime.ps1");
        string receipt = Path.Combine(prerequisiteRoot, "VC_RUNTIME_INSTALL_RESULT.json");
        static string PsQuote(string value) => value.Replace("'", "''");

        string script =
            "$ErrorActionPreference='Stop'\r\n" +
            "$Url='https://aka.ms/vc14/vc_redist.x64.exe'\r\n" +
            "$Installer='" + PsQuote(installer) + "'\r\n" +
            "$Receipt='" + PsQuote(receipt) + "'\r\n" +
            "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12\r\n" +
            "Invoke-WebRequest -UseBasicParsing -Uri $Url -OutFile $Installer\r\n" +
            "$Sig=Get-AuthenticodeSignature -LiteralPath $Installer\r\n" +
            "if ($Sig.Status -ne 'Valid' -or $Sig.SignerCertificate.Subject -notmatch '(^|,\\s*)O=Microsoft Corporation(,|$)') { throw 'Microsoft Visual C++ Redistributable signature verification failed' }\r\n" +
            "$Sha=(Get-FileHash -LiteralPath $Installer -Algorithm SHA256).Hash.ToLower()\r\n" +
            "$Proc=Start-Process -FilePath $Installer -ArgumentList '/install','/quiet','/norestart' -Verb RunAs -Wait -PassThru\r\n" +
            "$Ok=$Proc.ExitCode -in @(0,1638,3010)\r\n" +
            "[ordered]@{status=if($Ok){'OFFICIAL_VC_RUNTIME_INSTALLER_COMPLETED'}else{'FAILED'};source_url=$Url;sha256=$Sha;signature=[string]$Sig.Status;publisher=$Sig.SignerCertificate.Subject;exit_code=$Proc.ExitCode;reboot_required=($Proc.ExitCode -eq 3010);system32_copy_performed=$false}|ConvertTo-Json|Set-Content -LiteralPath $Receipt -Encoding UTF8\r\n" +
            "if (-not $Ok) { exit $Proc.ExitCode }\r\n";
        File.WriteAllText(scriptPath, script, new UTF8Encoding(true));

        var psi = new ProcessStartInfo
        {
            FileName = "powershell.exe",
            WorkingDirectory = prerequisiteRoot,
            UseShellExecute = false,
            CreateNoWindow = true,
            WindowStyle = ProcessWindowStyle.Hidden
        };
        psi.ArgumentList.Add("-NoProfile");
        psi.ArgumentList.Add("-ExecutionPolicy");
        psi.ArgumentList.Add("Bypass");
        psi.ArgumentList.Add("-File");
        psi.ArgumentList.Add(scriptPath);

        using Process process = Process.Start(psi) ?? throw new InvalidOperationException("Microsoft Visual C++ Runtime 자동 설치를 시작하지 못했습니다.");
        process.WaitForExit();
        if (process.ExitCode != 0 || !VcRuntimePresent())
            throw new InvalidOperationException("Microsoft Visual C++ Runtime 자동 준비가 완료되지 않았습니다.");
    }

    [STAThread]
    private static int Main()
    {
        try
        {
            string root = AppContext.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string manifest = Path.Combine(root, "PACKAGE_MANIFEST.json");
            string pythonw = Path.Combine(root, "runtime", "python", "pythonw.exe");
            string launcher = Path.Combine(root, "app", "launcher", "employee_package_launcher.py");

            if (!File.Exists(manifest))
                throw new FileNotFoundException("패키지 정보 파일을 찾을 수 없습니다.", manifest);
            if (!File.Exists(pythonw))
                throw new FileNotFoundException("내장 Python Runtime을 찾을 수 없습니다.", pythonw);
            if (!File.Exists(launcher))
                throw new FileNotFoundException("MINDLE MEDIA AI 실행 모듈을 찾을 수 없습니다.", launcher);

            string dataRoot = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "MINDLE", "MEDIA_AI_DATA");
            Directory.CreateDirectory(Path.Combine(dataRoot, "logs"));
            EnsureVcRuntime(dataRoot);
            string logPath = Path.Combine(dataRoot, "logs", "bootstrap.log");
            File.AppendAllText(logPath, $"{DateTimeOffset.Now:o} START root={root}{Environment.NewLine}", Encoding.UTF8);

            var psi = new ProcessStartInfo
            {
                FileName = pythonw,
                WorkingDirectory = root,
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden
            };
            psi.ArgumentList.Add(launcher);
            psi.Environment["MINDLE_ONE_CLICK_BOOTSTRAP"] = "1";
            psi.Environment["PYTHONNOUSERSITE"] = "1";
            psi.Environment.Remove("PYTHONHOME");
            psi.Environment.Remove("PYTHONPATH");
            psi.Environment.Remove("HF_TOKEN");
            psi.Environment.Remove("HUGGING_FACE_HUB_TOKEN");

            using Process process = Process.Start(psi) ?? throw new InvalidOperationException("MINDLE MEDIA AI 실행 프로세스를 시작하지 못했습니다.");
            process.WaitForExit();
            File.AppendAllText(logPath, $"{DateTimeOffset.Now:o} EXIT code={process.ExitCode}{Environment.NewLine}", Encoding.UTF8);
            if (process.ExitCode != 0)
                throw new InvalidOperationException($"MINDLE MEDIA AI 실행 준비가 실패했습니다. (code={process.ExitCode})\n로그: {logPath}");
            return 0;
        }
        catch (Exception ex)
        {
            MessageBoxW(IntPtr.Zero, ex.Message, "MINDLE MEDIA AI", 0x10);
            return 1;
        }
    }
}
