using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WebInterface.Repository.Writers;
using WebInterface.Model;
using WebInterface.Repository.Writings;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebInterface.API
{
    [Route("api/[controller]")]
    public class Writers : Controller
    {
        private IWriterRepository writerRepository;
        private IWritingRepository writingRepository;

        public Writers(IWriterRepository writerRepository, IWritingRepository writingRepository)
        {
            this.writerRepository = writerRepository;
            this.writingRepository = writingRepository;
        }
        [HttpGet]
        public IEnumerable<string> Get()
        {
            return writerRepository.GetList();
        }
        [HttpGet("{id}")]
        public Writer Get(string id)
        {
            return writerRepository.Get(id);
        }
        [HttpGet("{id}/{writingId}")]
        public Writing Get(string id, string writingId)
        {
            return writingRepository.Get(id, writingId);
        }
    }
}
