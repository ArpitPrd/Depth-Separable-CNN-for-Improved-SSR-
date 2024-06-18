import torch
from torch.utils.data import Dataset, Sampler
import random
import h5py
import numpy as np
import torch
import torch.nn.functional as F


cuda0 = torch.device('cuda:0')
    

# # PreparePatches- fnt to generate patches for training{use this (return)data when previous h5s have been used}- 15/7/'22
# #training h5 file
# class PreparePatches(Dataset):     #load list of path to __init__
#     def __init__(self):
#             self.h5f = h5py.File('/home/user/Documents/Paper May 2022/2^i/data/trainflip_bgu.h5','r')
#             self.keys = list(self.h5f.keys())
#             random.shuffle(self.keys)

#     def __len__(self):
#             return len(self.keys) 
            
           
#     def __getitem__(self,index):    #load each image/file in __getitem__
#             key = str(self.keys[index])
#             data = np.array(self.h5f[key])
#             data = torch.Tensor(data)
#             return  data[34:65,:,:], data[0:31,:,:]    #{0:31 has been stored as hyper data in FMB, 34-65 as interpolated RGB}


# #validation h5 file
# class PreparevalPatches(Dataset):     #load list of absolute path to __init__
#     def __init__(self):
#             self.h5f = h5py.File('/home/user/Documents/Paper May 2022/pool/data/testflip_bgu.h5','r')
#             self.keys = list(self.h5f.keys())
#             #print(len(self.keys))
#             random.shuffle(self.keys)

#     def __len__(self):
#             return len(self.keys) 
            
           
#     def __getitem__(self,index):    #load each image/file in __getitem__
#             key = str(self.keys[index])
#             data = np.array(self.h5f[key])
#             data = torch.Tensor(data)
#             #In Cave, the results were fixed by correctly using the below 'data' code
#             return  data[34:65,:,:], data[0:31,:,:]
        
#     def get_data_by_key(self, key):
#             #assert self.mode == 'test'
#             data = np.array(self.h5f[key])
#             data = torch.Tensor(data)
#             return data[34:65,:,:], data[0:31,:,:]


# #Use this for data[0:31]-[31:62]{use this when new h5 has been used}  - 19/7/'22
#create train h5 file
class PreparePatches(Dataset):     #load list of path to __init__
    def __init__(self):
        self.h5f = h5py.File('../data/BGU/Arpit/train.h5','r')
        self.keys = list(self.h5f.keys())
        #self.keys=list(self.keys[0])
        random.shuffle(self.keys)
    
    def __len__(self):
        return len(self.keys) 
        
    def key(self, index):
        return str(self.keys[index])
    
    def __getitem__(self,index):    #load each image/file in __getitem__
        key = str(self.keys[index])
        data = np.array(self.h5f[key])
        data = torch.Tensor(data)
        # print('printing shape of data', data.shape)
        inputs = torch.cat([data[0:31, :, :], torch.unsqueeze(data[30, :, :], 0)], dim = 0)
        labels = data[31:62, :, :]
        # print('inputs in PreparePateches', inputs.shape)
        # print('labels in PreparePateches', labels.shape)
        # return data[0:31,:,:], data[31:62,:,:]
        return inputs/255.0, labels

#create val h5 file
class PreparevalPatches(Dataset):     #load list of absolute path to __init__
    def __init__(self):
        #previous cave file
        self.h5f = h5py.File('../data/BGU/Arpit/val.h5','r')
        self.keys = list(self.h5f.keys())
        #self.keys=list(self.keys[0])
        random.shuffle(self.keys)
    
    def __len__(self):
        return len(self.keys) 
        
    def key(self, index):
        return str(self.keys[index])
    
    def __getitem__(self,index):    #load each image/file in __getitem__
        key = str(self.keys[index])
        data = np.array(self.h5f[key])
        data = torch.Tensor(data)
        inputs = torch.cat([data[0:31, :, :], torch.unsqueeze(data[30, :, :], 0)], dim = 0)
        #In Cave, the results were fixed by correctly using the below 'data' range
        return inputs/255.0, data[31:62,:,:]
    
    def get_data_by_key(self, key):
        #assert self.mode == 'test'
        print(self.keys)
        data = np.array(self.h5f[key])
        # data = np.array(self.h5f[key])
        data = torch.Tensor(data)
        return data[0:31,:,:]/255.0, data[31:62,:,:]

