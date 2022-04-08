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

problem_list = ["AlexNet_layer1", "AlexNet_layer2","AlexNet_layer3", "VGG02_layer1", "VGG02_layer2", "VGG02_layer3"]
num_lanes_list = [1,2,4,8,16]

tot_energy = {prob:[None]*len(num_lanes_list) for prob in problem_list}
tot_cycles = {prob:[None]*len(num_lanes_list) for prob in problem_list}
tot_area = {prob:[None]*len(num_lanes_list) for prob in problem_list} 
tot_util = {prob:[None]*len(num_lanes_list) for prob in problem_list}
tot_perf = {prob:[None]*len(num_lanes_list) for prob in problem_list}


for prob in problem_list:
    for i, num_lanes in enumerate(num_lanes_list):
        path = f"src/output_45nm/{prob}/{num_lanes}_lanes/timeloop-mapper.stats.txt"
        energy, cycles, area, util = results_parser(path)
        tot_energy[prob][i] = energy # uJ
        tot_cycles[prob][i] = cycles
        tot_area[prob][i] = area
        tot_util[prob][i] = util
        tot_perf[prob][i] = util*cycles*num_lanes/(energy*10**3) # Conversion to GFLOP/J (*10^6/10^9 => 1/10^3)

style_list = ["rx--", "ro--", "r^--", "bx-", "bo-", "b^-"]

# Energy
for i, prob in enumerate(problem_list):
    plt.plot(num_lanes_list, tot_energy[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.legend(problem_list)
plt.ylabel('Energy')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/energy.png')
plt.close()

# Cycles
for i, prob in enumerate(problem_list):
    plt.plot(num_lanes_list, tot_cycles[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.legend(problem_list)
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
for i, prob in enumerate(problem_list):
    plt.plot(num_lanes_list, tot_area[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.legend(problem_list)
plt.ylabel('Area')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/area.png')
plt.close()

# Utilization
for i, prob in enumerate(problem_list):
    plt.plot(num_lanes_list, tot_util[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.legend(problem_list)
plt.ylabel('Utilization %')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/utilization.png')
plt.close()

# Performance
for i, prob in enumerate(problem_list):
    plt.plot(num_lanes_list, tot_perf[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.legend(problem_list)
plt.ylabel('Performance [GFLOP/J]')
plt.xlabel('Number of Lanes')
plt.xscale('log',basex=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_intermediate/fig/performance.png')
plt.close()
