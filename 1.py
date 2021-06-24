# -*-coding:utf-8-*- 
import os 
lista = []
for root,dirs,files in os.walk("e:\\jd1awxj"): 
#  for dir in dirs: 
#   print(os.path.join(root,dir))
 for file in files: 
  lista.append(os.path.join(root,file))

for ele in lista:
    print(ele)