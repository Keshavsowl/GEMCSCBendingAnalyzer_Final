
f = open("GEMAllZeroes_13_v1.csv", "w")

x=0

y=0
z=0
phix=0
phiy=0
phiz=0

for i in [-1, 1]:

  for j in [1, 2]:
    for k in range (1,37):
      if k <10:
        f.writelines("{i}{j}0{k}1, {x}, {y}, {z}, {phix}, {phiy}, {phiz}\n".format(i=i, j=j, k=k, x=x, y=y, z=z, phix=phix, phiy=phiy, phiz=phiz))
        f.writelines("{i}{j}0{k}2, {x}, {y}, {z}, {phix}, {phiy}, {phiz}\n".format(i=i, j=j, k=k, x=x, y=y, z=z, phix=phix, phiy=phiy, phiz=phiz))
      else:
        f.writelines("{i}{j}{k}1, {x}, {y}, {z}, {phix}, {phiy}, {phiz}\n".format(i=i, j=j, k=k, x=x, y=y, z=z, phix=phix, phiy=phiy, phiz=phiz))
        f.writelines("{i}{j}{k}2, {x}, {y}, {z}, {phix}, {phiy}, {phiz}\n".format(i=i, j=j, k=k, x=x, y=y, z=z, phix=phix, phiy=phiy, phiz=phiz))


f.close()
