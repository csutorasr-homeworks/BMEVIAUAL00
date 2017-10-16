using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebInterface.Model;

namespace WebInterface.Repository.Writings
{
    public interface IWritingRepository
    {
        Writing Get(string writerId, string writingId);
        object SetLine(string writerId, string writingId, int strokeIndex, string type);
        object RemoveLine(string writerId, string writingId, int strokeIndex);
        object Set(string writerId, string writingId, string type);
    }
}
