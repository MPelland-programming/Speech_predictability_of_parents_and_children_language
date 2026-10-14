import torch
import gc
from transformers import AutoTokenizer, MistralForCausalLM
from torch import cuda
import pandas as pd

device ='cuda'

#modelname = config.get("model","/home/mpelland/links/projects/def-eporte2/mpelland/predictability/lang_models/mistral/m7Bv03/snapshots/caa1feb0e54d415e2df31207e5f4e273e33509b1/")
modelname ="/home/mpelland/links/projects/def-eporte2/mpelland/predictability/lang_models/mistral/m7Bv03/snapshots/caa1feb0e54d415e2df31207e5f4e273e33509b1/"

# load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(modelname, use_fast=True, local_files_only=True)
model = MistralForCausalLM.from_pretrained(modelname, local_files_only=True).to(device)

vocab_size = len(tokenizer.vocab)
batch_sizes =     [8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 96, 128, 192, 256]
context_lengths = [1, 2, 4, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 96]

listsizes = [(ii,jj) for ii in batch_sizes for jj in context_lengths]

# get memory usage of model
torch.cuda.synchronize()
torch.cuda.reset_peak_memory_stats()
mem_model = torch.cuda.max_memory_allocated()

l_bs = []
l_cl = []
l_alloc = []
l_reser = []

#get memory usage
with torch.no_grad():
    for ss in listsizes:
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()

        input_ids = torch.randint(low=0, high=vocab_size, size = ss, dtype=torch.int64, device=device)
        attention_mask = torch.ones(input_ids.shape, device=device,dtype=torch.int8)
        modelinputs = {"input_ids": input_ids, "attention_mask": attention_mask}
        oo = model(**modelinputs)

        torch.cuda.synchronize()
        l_alloc.append(torch.cuda.max_memory_allocated())
        l_reser.append(torch.cuda.max_memory_reserved())
        l_bs.append(ss[0])
        l_cl.append(ss[1])

        del oo, modelinputs, input_ids, attention_mask
        gc.collect()
        torch.cuda.empty_cache()

results = pd.DataFrame({'batch':l_bs,'lenght':l_cl,'alloc':l_alloc,'reserved':l_reser})
results.to_csv('assess_memory.csv',index=False)
