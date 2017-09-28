using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebInterface.Model
{
    public class Point
    {
        public int X { get; set; }
        public int Y { get; set; }
        public string Time { get; internal set; }
    }
}
