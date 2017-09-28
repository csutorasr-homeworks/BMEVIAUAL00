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

        IEnumerable<Writer> IWriterRepository.GetList()
        {
            return directory.GetDirectories().Select(dir => new Writer(dir.Name));
        }
    }
}
