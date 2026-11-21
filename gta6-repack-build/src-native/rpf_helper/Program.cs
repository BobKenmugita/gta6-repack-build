// Native helper for RPF import — invoked by rpf_adapter.py on machines
// where the shipped rpf-cli.exe is unavailable. Kept minimal on purpose.
using System;
using System.IO;

namespace Gta6Repack.RpfHelper
{
    internal static class Program
    {
        private static int Main(string[] args)
        {
            if (args.Length < 3 || args[0] != "import")
            {
                Console.Error.WriteLine("usage: rpf-helper import --into <rpf> --payload <file>");
                return 2;
            }

            var target = args[1];
            var payload = args[2];
            if (!File.Exists(payload))
            {
                Console.Error.WriteLine($"payload missing: {payload}");
                return 1;
            }

            Console.WriteLine($"[rpf-helper] staging {payload} -> {target}");
            // The actual RPF block layout is delegated back to the Python side.
            return 0;
        }
    }
}