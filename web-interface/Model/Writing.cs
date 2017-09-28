using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebInterface.Model
{
    public class Writing
    {
        private string writerId;
        private string writingId;
        private DateTime captureTime;

        public Writing(string writerId, string writingId, DateTime captureTime)
        {
            this.writerId = writerId;
            this.writingId = writingId;
            this.captureTime = captureTime;
        }

        public String WriterId
        {
            get { return writerId; }
        }
        public String WritingId
        {
            get { return writingId; }
        }
        public DateTime CaptureTime
        {
            get { return captureTime; }
        }


    }
}
