using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebInterface.Model;

namespace WebInterface.Repository.Writers
{
    public interface IWriterRepository
    {
        IEnumerable<Writer> GetList();
    }
}
