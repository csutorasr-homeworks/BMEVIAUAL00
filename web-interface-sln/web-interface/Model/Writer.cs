using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebInterface.Model
{
    public class Writer
    {
        private string name;
        private IEnumerable<string> writings;

        public Writer(string name, IEnumerable<string> writings)
        {
            this.name = name;
            this.writings = writings;
        }

        public string Name
        {
            get { return name; }
        }

        public IEnumerable<string> Writings
        {
            get { return writings; }
        }
    }
}
