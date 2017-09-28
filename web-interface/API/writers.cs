using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WebInterface.Repository.Writers;
using WebInterface.Model;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebInterface.API
{
    [Route("api/[controller]")]
    public class Writers : Controller
    {
        private IWriterRepository repository;

        public Writers(IWriterRepository repository)
        {
            this.repository = repository;
        }
        [HttpGet]
        public IEnumerable<string> Get()
        {
            return repository.GetList();
        }
        [HttpGet("{id}")]
        public Writer Get(string id)
        {
            return repository.Get(id);
        }
    }
}
