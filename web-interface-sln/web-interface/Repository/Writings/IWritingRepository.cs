﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebInterface.Model;

namespace WebInterface.Repository.Writings
{
    public interface IWritingRepository
    {
        Writing Get(string writerId, string writingId);
    }
}
