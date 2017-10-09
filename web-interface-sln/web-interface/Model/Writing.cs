using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebInterface.Model
{
    public class Writing
    {
        public string WriterId { get; set; }
        public string WritingId { get; set; }
        public IEnumerable<Stroke> Strokes { get; set; }
        public DateTime CaptureTime { get; internal set; }
        public string Text { get; internal set; }
    }
}
