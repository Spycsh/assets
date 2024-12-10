""""Usage:

export WORLD_SIZE=2
export RANK=0  # 1 on the other node
# change the MASTER_ADDR to your Master external IP

python test_hccl_allreduce.py

"""

import os
import torch

import habana_frameworks.torch.core as htcore

import platform

torch.manual_seed(0)
#load hpu backend for PyTorch

device = torch.device('hpu')


def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'# change to your Master IP
    os.environ['MASTER_PORT'] = '12340'
    #os.environ['OMPI_MCA_btl_tcp_if_include'] = 'eth0'
    #Import the distributed package for HCCL, set the backend to HCCL

    import habana_frameworks.torch.distributed.hccl

    torch.distributed.init_process_group(backend='hccl', rank=rank, world_size=world_size)


def cleanup():
    torch.distributed.destroy_process_group()

def allReduce(rank):
    _tensor = torch.ones(8).to(device)
    torch.distributed.all_reduce(_tensor)
    _tensor_cpu = _tensor.cpu()
    # Optionally, print the result for debugging
    if rank == 0:
        print(_tensor_cpu)


def run_allreduce(rank, world_size):
    setup(rank, world_size)
    print("setup")

    for i in range(100):
        allReduce(rank)

    cleanup()

def main():
    #Run Habana's Initialize HPU function to collect the world size and rank

    from habana_frameworks.torch.distributed.hccl import initialize_distributed_hpu

    world_size, rank, local_rank = initialize_distributed_hpu()

    run_allreduce(rank, world_size)

if __name__ == '__main__':
    main()
