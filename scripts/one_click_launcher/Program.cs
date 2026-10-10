using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

internal static class Program
{
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBoxW(IntPtr hWnd, string text, string caption, uint type);

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
