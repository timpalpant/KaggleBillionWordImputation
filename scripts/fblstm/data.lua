--
----  Copyright (c) 2014, Facebook, Inc.
----  All rights reserved.
----
----  This source code is licensed under the Apache 2 license found in the
----  LICENSE file in the root directory of this source tree. 
----

local stringx = require('pl.stringx')
-- local file = require('pl.file')

local ptb_path = "../../data/"

local vocab_idx = 0
local vocab_map = {}

-- Stacks replicated, shifted versions of x_inp
-- into a single matrix of size x_inp:size(1) x batch_size.
local function replicate(x_inp, batch_size)
   local s = x_inp:size(1)
   local x = torch.zeros(torch.floor(s / batch_size), batch_size)
   for i = 1, batch_size do
     local start = torch.round((i - 1) * s / batch_size) + 1
     local finish = start + x:size(1) - 1
     x:sub(1, x:size(1), i, i):copy(x_inp:sub(start, finish))
   end
   return x
end

local function load_data(fname)
   print("Loading " .. fname)
   local file = io.open(fname)
   local nx = 1000000
   local x = torch.zeros(nx)
   local j = 1
   local k = 1
   for line in file:lines() do
     line = stringx.replace(line, '\n', '<eos>')
     data = stringx.split(line)
     if j + #data >= nx then
       nx = 2 * nx
       print("Expanding x to : " .. nx)
       x:resize(nx)
     end
     
     for i = 1, #data do
        if vocab_map[data[i]] == nil then
           vocab_idx = vocab_idx + 1
           vocab_map[data[i]] = vocab_idx
        end
        x[j] = vocab_map[data[i]]
        j = j + 1
     end
     
     if k % 10000000 == 0 then
       print(k)
       x:resize(j)
       return x
     end
     
     k = k + 1
   end
   
   x:resize(j)
   return x
end

local function traindataset(batch_size)
   local x = load_data(ptb_path .. "train.train.lower.txt")
   x = replicate(x, batch_size)
   return x
end

-- Intentionally we repeat dimensions without offseting.
-- Pass over this batch corresponds to fully sequential processing.
local function testdataset(batch_size)
   local x = load_data(ptb_path .. "test.as_train.lower.txt")
   x = x:resize(x:size(1), 1):expand(x:size(1), batch_size)
   return x
end

local function validdataset(batch_size)
   local x = load_data(ptb_path .. "train.heldout.lower.txt")
   x = replicate(x, batch_size)
   return x
end

return {traindataset=traindataset,
        testdataset=testdataset,
        validdataset=validdataset}
