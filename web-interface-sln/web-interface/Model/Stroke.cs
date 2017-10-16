using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebInterface.Model
{
    public class Stroke
    {
        public IEnumerable<Point> Points { get; set; }
        public bool isHorizontal;
        public string strokeDirection;
    }
}
