import torch
import gc


def flush():
    gc.collect()
    torch.cuda.empty_cache()
