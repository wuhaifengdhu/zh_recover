#!/usr/bin/python
#coding: utf-8
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

# data generation
data = vstack((rand(150,2) + array([.5,.5]),rand(150,2)))  #vstack 连接作用

print data.shape


# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(data, 2)
# assign each sample to a cluster
idx,_ = vq(data,centroids)

print idx.shape

print idx == 0, 0
# some plotting using numpy's logical indexing
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()