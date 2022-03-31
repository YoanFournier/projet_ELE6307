from scoreboard import *
from dataflow import *
from mac import *
from mem import *

def flatten(t):
    return [item for sublist in t for item in sublist]

o_data = []
i_data = []
f_data = []

K = 32
P = 16
R = 3

I = 18

mac_unit_pwr = 0.56
main_mem_pwr_rd = 7.95
glob_buf_pwr_rd = 0.42
main_mem_pwr_wr = 5.45
glob_buf_pwr_wr = 0.42

data = {'o':[], 'i':[], 'f':[]}

for k in range(0, K):
	data['o'].append([])
	for p in range(0, P):
		data['o'][k].append("o" + str(k).zfill(2) + str(p).zfill(2))

for i in range(0, I):
	data['i'].append("i" + str(i).zfill(2))

for k in range(0, K):
	data['f'].append([])
	for r in range(0, R):
		data['f'][k].append("f" + str(k).zfill(2) + str(r).zfill(2))



scrbrd = scoreboard([0, 1])
main_mem = mem(0, [], [], scrbrd)
glob_buf = mem(1, [], [], scrbrd, main_mem)
mac_unit = mac(scrbrd, glob_buf)
dataf = dataflow(mac_unit, [main_mem, glob_buf], [], [], data)

# # WS
p = [16, 1, 3, 2, 16, 1]
dataf.set_params(p)
main_mem.sizes = {'o':512, 'i':18, 'f':96}
glob_buf.sizes = {'o':p[3]*p[4], 'i':16, 'f':p[3]*p[5]}
main_mem.data = {'o':[], 'i':data['i'], 'f':flatten(data['f'])}
glob_buf.data = {'o':[], 'i':[], 'f':[]}

scrbrd.initialize_counters()
I = [1, 16, 3, 1, 2, 16]
permut = {'k1':1, 'p1':0, 'r1':2, 'k2':4, 'p2':5, 'r2':3}
dataf.do_sim(I,permut)
print("\n\nWS")
scrbrd.print_results()
print((scrbrd.mac_calc * mac_unit_pwr 
      + scrbrd.read_access[0] * main_mem_pwr_rd 
      + scrbrd.read_access[1] * glob_buf_pwr_rd 
      + scrbrd.write_access[0] * main_mem_pwr_wr
      + scrbrd.write_access[1] * glob_buf_pwr_wr)/1536)

# untiled OS 1
p = [32, 16, 1, 1, 1, 3]
dataf.set_params(p)
main_mem.sizes = {'o':512, 'i':18, 'f':96}
glob_buf.sizes = {'o':p[3]*p[4], 'i':p[5], 'f':p[3]*p[5]}
main_mem.data = {'o':[], 'i':data['i'], 'f':flatten(data['f'])}
glob_buf.data = {'o':[], 'i':[], 'f':[]}

scrbrd.initialize_counters()
I = [32, 1, 16, 1, 1, 3]
permut = {'k1':0, 'p1':2, 'r1':1, 'k2':3, 'p2':4, 'r2':5}
dataf.do_sim(I, permut)
print("\n\nuntiled OS 1")
scrbrd.print_results()
print((scrbrd.mac_calc * mac_unit_pwr 
      + scrbrd.read_access[0] * main_mem_pwr_rd 
      + scrbrd.read_access[1] * glob_buf_pwr_rd 
      + scrbrd.write_access[0] * main_mem_pwr_wr
      + scrbrd.write_access[1] * glob_buf_pwr_wr)/1536)

# # untiled OS 2
p = [32, 16, 1, 1, 1, 3]
dataf.set_params(p)
main_mem.sizes = {'o':512, 'i':18, 'f':96}
glob_buf.sizes = {'o':p[3]*p[4], 'i':p[5], 'f':p[3]*p[5]}
main_mem.data = {'o':[], 'i':data['i'], 'f':flatten(data['f'])}
glob_buf.data = {'o':[], 'i':[], 'f':[]}

scrbrd.initialize_counters()
I = [16, 1, 32, 1, 1, 3]
permut = {'k1':2, 'p1':0, 'r1':1, 'k2':4, 'p2':3, 'r2':5}
dataf.do_sim(I, permut)
print("\n\nuntiled OS 2")
scrbrd.print_results()
print((scrbrd.mac_calc * mac_unit_pwr 
      + scrbrd.read_access[0] * main_mem_pwr_rd 
      + scrbrd.read_access[1] * glob_buf_pwr_rd 
      + scrbrd.write_access[0] * main_mem_pwr_wr
      + scrbrd.write_access[1] * glob_buf_pwr_wr)/1536)

# # tiled OS 1
p = [4, 16, 1, 8, 1, 3]
dataf.set_params(p)
main_mem.sizes = {'o':512, 'i':18, 'f':96}
glob_buf.sizes = {'o':p[3]*p[4], 'i':p[5], 'f':p[3]*p[5]}
main_mem.data = {'o':[], 'i':data['i'], 'f':flatten(data['f'])}
glob_buf.data = {'o':[], 'i':[], 'f':[]}

scrbrd.initialize_counters()
I = [4, 1, 16, 8, 1, 3]
permut = {'k1':0, 'p1':2, 'r1':1, 'k2':3, 'p2':4, 'r2':5}
dataf.do_sim(I, permut)
print("\n\ntiled OS 1")
scrbrd.print_results()
print((scrbrd.mac_calc * mac_unit_pwr 
      + scrbrd.read_access[0] * main_mem_pwr_rd 
      + scrbrd.read_access[1] * glob_buf_pwr_rd 
      + scrbrd.write_access[0] * main_mem_pwr_wr
      + scrbrd.write_access[1] * glob_buf_pwr_wr)/1536)

## tiled OS 2
p = [32, 2, 1, 1, 8, 3]
dataf.set_params(p)
dataf.permut = [['p','r','k'],['r','p','k']]
main_mem.sizes = {'o':512, 'i':18, 'f':96}
glob_buf.sizes = {'o':p[3]*p[4], 'i':10, 'f':p[3]*p[5]}
main_mem.data = {'o':[], 'i':data['i'], 'f':flatten(data['f'])}
glob_buf.data = {'o':[], 'i':[], 'f':[]}

scrbrd.initialize_counters()
I = [2, 1, 32, 8, 1, 3]
permut = {'k1':2, 'p1':0, 'r1':1, 'k2':4, 'p2':3, 'r2':5}
dataf.do_sim(I, permut)
print("\n\ntiled OS 2")
scrbrd.print_results()
print((scrbrd.mac_calc * mac_unit_pwr 
      + scrbrd.read_access[0] * main_mem_pwr_rd 
      + scrbrd.read_access[1] * glob_buf_pwr_rd 
      + scrbrd.write_access[0] * main_mem_pwr_wr
      + scrbrd.write_access[1] * glob_buf_pwr_wr)/1536)

print("END")



