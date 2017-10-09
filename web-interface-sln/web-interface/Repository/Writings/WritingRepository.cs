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
            // General info
            var generalElement = doc.Root.Element("General");
            // Capture time
            var captureTimeElement = generalElement.Element("CaptureTime");
            var captureTime = new DateTime(Int32.Parse(captureTimeElement.Attribute("year").Value),
                Int32.Parse(captureTimeElement.Attribute("month").Value),
                Int32.Parse(captureTimeElement.Attribute("dayOfMonth").Value));
            // Transcription
            var transcriptionElement = doc.Root.Element("Transcription");
            var textElement = transcriptionElement.Element("Text");
            string text;
            using (var reader = textElement.CreateReader())
            {
                reader.MoveToContent();
                text = reader.ReadInnerXml().Trim();
            }
            // Strokes
            var strokeSetElement = doc.Root.Element("StrokeSet");
            var strokes = strokeSetElement.Elements("Stroke")
                .Select(stroke => new Stroke()
                {
                    Points = stroke.Elements("Point")
                        .Select(point => new Point
                        {
                            X = Int32.Parse(point.Attribute("x").Value),
                            Y = Int32.Parse(point.Attribute("y").Value),
                            Time = point.Attribute("time").Value
                        })
                });
            return new Writing()
            {
                WriterId = writerId,
                WritingId = writingId,
                CaptureTime = captureTime,
                Text = text,
                Strokes = strokes
            };
        }
    }
}
