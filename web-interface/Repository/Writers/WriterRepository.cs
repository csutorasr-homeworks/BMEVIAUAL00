using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.IO;
using WebInterface.Model;

namespace WebInterface.Repository.Writers
{
    public class WriterRepository : IWriterRepository
    {
        private DirectoryInfo directory;

        public WriterRepository(string directory)
        {
            this.directory = Directory.CreateDirectory(directory);
        }

        IEnumerable<string> IWriterRepository.GetList()
        {
            return directory.EnumerateDirectories().Select(dir => dir.Name);
        }

        Writer IWriterRepository.Get(string id)
        {
            return new Writer(id,
                directory.EnumerateDirectories()
                .FirstOrDefault(x => x.Name == id)
                ?.EnumerateDirectories()
                .SelectMany(x => x
                    .EnumerateFiles("*.xml")
                    .Select(file => $"{x.Name}_{Path.GetFileNameWithoutExtension(file.Name)}")
                ));
        }
    }
}
