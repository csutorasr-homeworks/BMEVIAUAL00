using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Xml.Linq;
using WebInterface.Model;

namespace WebInterface.Repository.Writings
{
    public class WritingRepository : IWritingRepository
    {
        private DirectoryInfo directory;

        public WritingRepository(string directory)
        {
            this.directory = Directory.CreateDirectory(directory);
        }

        /// <summary>
        /// Gets data about a writing
        /// </summary>
        /// <param name="writerId">writerId</param>
        /// <param name="writingId">writerId-writingDir_filenameWithoutExtension</param>
        /// <returns>The writing</returns>
        Writing IWritingRepository.Get(string writerId, string writingId)
        {
            string writingDir = writingId.Substring(0, writingId.IndexOf('_'));
            string filename = writingId.Substring(writingId.IndexOf('_') + 1) + ".xml";
            var file = directory.EnumerateDirectories()
                .FirstOrDefault(x => x.Name == writerId)
                ?.EnumerateDirectories()
                .FirstOrDefault(x => x.Name == writingDir)
                ?.EnumerateFiles()
                .FirstOrDefault(x => x.Name == filename);
            if (file == null)
            {
                return null;
            }
            XDocument doc = XDocument.Load(file.OpenRead());
            var generalElement = doc.Root.Element("General");
            var captureTimeElement = generalElement.Element("CaptureTime");
            var captureTime = new DateTime(Int32.Parse(captureTimeElement.Attribute("year").Value),
                Int32.Parse(captureTimeElement.Attribute("month").Value),
                Int32.Parse(captureTimeElement.Attribute("dayOfMonth").Value));
            return new Writing(writerId, writingId, captureTime);
        }
    }
}
