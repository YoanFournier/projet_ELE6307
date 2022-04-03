import os
import re
import matplotlib
import matplotlib.pyplot as plt


def results_parser(path='src/output/timeloop-mapper.stats.txt'):
    with open(path, 'r') as file:
        txt = file.read()
        regex = re.compile('Summary Stats.*', re.DOTALL)
        summary_text = regex.findall(txt)[0]
        
        tot_energy = re.findall("Energy.*", summary_text)[0]
        tot_energy = float(re.findall("[0-9]+\.[0-9]+", tot_energy)[0])
        
        tot_cycles = re.findall("Cycles.*", summary_text)[0]
        tot_cycles = int(re.findall("[0-9]+", tot_cycles)[0])

        tot_area = re.findall("Area.*", summary_text)[0]
        tot_area = re.findall("[0-9]+\.[0-9]+", tot_area)[0]

        tot_util = re.findall("Utilization.*", summary_text)[0]
        tot_util = float(re.findall("[0-9]+\.[0-9]+", tot_util)[0])
    return tot_energy, tot_cycles, tot_area, tot_util

tech_node_list = [22, 45]
num_lanes_list = [1,2,4,8,16]

tot_energy = {tech:[None]*len(num_lanes_list) for tech in tech_node_list}
tot_cycles = {tech:[None]*len(num_lanes_list) for tech in tech_node_list}
tot_area = {tech:[None]*len(num_lanes_list) for tech in tech_node_list} 
tot_util = {tech:[None]*len(num_lanes_list) for tech in tech_node_list}
tot_perf = {tech:[None]*len(num_lanes_list) for tech in tech_node_list}


for tech in tech_node_list:
    for i, num_lanes in enumerate(num_lanes_list):
        path = f"src/output_{tech}nm/{num_lanes}_lanes/timeloop-mapper.stats.txt"
        energy, cycles, area, util = results_parser(path)
        tot_energy[tech][i] = energy # uJ
        tot_cycles[tech][i] = cycles
        tot_area[tech][i] = area
        tot_util[tech][i] = util
        tot_perf[tech][i] = util*cycles*num_lanes/(energy*10**3) # Conversion to GFLOP/J (*10^6/10^9 => 1/10^3)



# Energy 
fig, ax1 = plt.subplots()

color = 'tab:red'
plt.xscale('log',basex=2)
ax1.set_xlabel('Number of Lanes')
ax1.set_ylabel('Energy [uJ]', color=color)
lns1 = ax1.plot(num_lanes_list, tot_energy[22], 'rx--', linewidth=0.75, fillstyle='none', label='22nm')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Energy [uJ]', color=color)  # we already handled the x-label with ax1
lns2 = ax2.plot(num_lanes_list, tot_energy[45], 'bo-', linewidth=0.75, fillstyle='none', label='45nm')

plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='best')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('tex_intermediate/fig/energy.png')
plt.close()

# Cycles
plt.plot(num_lanes_list, tot_cycles[22], 'rx--', linewidth=0.75, fillstyle='none')
plt.plot(num_lanes_list, tot_cycles[45], 'bo-', linewidth=0.75, fillstyle='none')
plt.legend(['22nm', '45nm'])
plt.ylabel('Cycles')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.yscale('log',basey=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/cycles.png')
plt.close()


# Area
fig, ax1 = plt.subplots()

color = 'tab:red'
plt.xscale('log',basex=2)
ax1.set_xlabel('Number of Lanes')
ax1.set_ylabel('Area [mm^2]', color=color)
lns1 = ax1.plot(num_lanes_list, tot_area[22], 'rx--', linewidth=0.75, fillstyle='none', label='22nm')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Area [mm^2]', color=color)  # we already handled the x-label with ax1
lns2 = ax2.plot(num_lanes_list, tot_area[45], 'bo-', linewidth=0.75, fillstyle='none', label='45nm')

plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper left')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('tex_intermediate/fig/area.png')
plt.close()

# Utilization
plt.plot(num_lanes_list, tot_util[22], 'rx--', linewidth=0.75, fillstyle='none')
plt.plot(num_lanes_list, tot_util[45], 'bo-', linewidth=0.75, fillstyle='none')
ax = plt.gca()
ax.set_ylim([0, 1.1])
plt.legend(['22nm', '45nm'])
plt.ylabel('Utilization %')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/utilization.png')
plt.close()


# Performance
fig, ax1 = plt.subplots()

color = 'tab:red'
plt.xscale('log',basex=2)
ax1.set_xlabel('Number of Lanes')
ax1.set_ylabel('Performance [GFLOP/J]', color=color)
lns1 = ax1.plot(num_lanes_list, tot_perf[22], 'rx--', linewidth=0.75, fillstyle='none', label='22nm')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Performance [GFLOP/J]', color=color)  # we already handled the x-label with ax1
lns2 = ax2.plot(num_lanes_list, tot_perf[45], 'bo-', linewidth=0.75, fillstyle='none', label='45nm')

plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper left')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('tex_intermediate/fig/performance.png')
plt.close()