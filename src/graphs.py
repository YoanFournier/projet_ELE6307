import re
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

def plot_triple_axis(xlist, ylist, xlabel, ylabel, legendlist, savename, xlog=False, ylog=False):
    fig, host = plt.subplots()

    par1 = host.twinx()
    par2 = host.twinx()

    host.set_xlabel(xlabel)
    host.set_ylabel(ylabel)
    par1.set_ylabel(ylabel)
    par2.set_ylabel(ylabel)

    p1, = host.plot(xlist, ylist[0], "rx-", label=legendlist[0],  linewidth=0.75, fillstyle='none')
    p2, = par1.plot(xlist, ylist[1], "bo-", label=legendlist[1],  linewidth=0.75, fillstyle='none')
    p3, = par2.plot(xlist, ylist[2], "g^-", label=legendlist[2],  linewidth=0.75, fillstyle='none')

    lns = [p1, p2, p3]
    par2.spines['right'].set_position(('outward', 60))

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    if ylog:
        host.set_yscale('log', base=2)
        par1.set_yscale('log', base=2)
        par2.set_yscale('log', base=2)

    if xlog:
        plt.xscale('log', base=2)
    
    plt.grid()
    plt.minorticks_on()
    plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)

    fig.tight_layout()

    par2.legend(handles=lns, loc='best', framealpha=0.5)

    plt.savefig(savename)
    plt.close()    

def plot_single_axis(xlist, ylist, xlabel, ylabel, legendlist, savename, xlog=False, ylog=False):
    fig, host = plt.subplots()

    host.set_xlabel(xlabel)
    host.set_ylabel(ylabel)

    p1, = host.plot(xlist, ylist[0], "rx-", label=legendlist[0],  linewidth=0.75, fillstyle='none')
    p2, = host.plot(xlist, ylist[1], "bo-", label=legendlist[1],  linewidth=0.75, fillstyle='none')
    p3, = host.plot(xlist, ylist[2], "g^-", label=legendlist[2],  linewidth=0.75, fillstyle='none')

    lns = [p1, p2, p3]

    host.yaxis.label.set_color(p1.get_color())

    if ylog:
        host.set_yscale('log', base=2)

    if xlog:
        plt.xscale('log', base=2)
    
    plt.grid()
    plt.minorticks_on()
    plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)

    fig.tight_layout()

    host.legend(handles=lns, loc='best', framealpha=1)

    plt.savefig(savename)
    plt.close()

alex_list = ["AlexNet_layer1", "AlexNet_layer2","AlexNet_layer3"]
vgg_list = ["VGG02_layer1", "VGG02_layer2", "VGG02_layer3"]
problem_list = alex_list+vgg_list
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


# Energy VGG
energy_list = [tot_energy['VGG02_layer1'],tot_energy['VGG02_layer2'],tot_energy['VGG02_layer3']]
plot_triple_axis(num_lanes_list, energy_list, "Number of Lanes", "Energy [uJ]", vgg_list, 'tex_final/fig/VGG_energy.png')

# Energy Alex
energy_list = [tot_energy['AlexNet_layer1'],tot_energy['AlexNet_layer2'],tot_energy['AlexNet_layer3']]
plot_triple_axis(num_lanes_list, energy_list, "Number of Lanes", "Energy [uJ]", alex_list, 'tex_final/fig/Alex_energy.png')

# Perf VGG
perf_list = [tot_perf['VGG02_layer1'],tot_perf['VGG02_layer2'],tot_perf['VGG02_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Performance [GFLOP/J]", vgg_list, 'tex_final/fig/VGG_performance.png')

# Perf Alex
perf_list = [tot_perf['AlexNet_layer1'],tot_perf['AlexNet_layer2'],tot_perf['AlexNet_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Performance [GFLOP/J]", alex_list, 'tex_final/fig/Alex_performance.png')

# Cycles VGG
perf_list = [tot_cycles['VGG02_layer1'],tot_cycles['VGG02_layer2'],tot_cycles['VGG02_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Cycles", vgg_list, 'tex_final/fig/VGG_cycles.png', True, True)

# Cycles Alex
perf_list = [tot_cycles['AlexNet_layer1'],tot_cycles['AlexNet_layer2'],tot_cycles['AlexNet_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Cycles", alex_list, 'tex_final/fig/Alex_cycles.png', True, True)

# Utilization VGG
perf_list = [tot_util['VGG02_layer1'],tot_util['VGG02_layer2'],tot_util['VGG02_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Utilization", vgg_list, 'tex_final/fig/VGG_utilization.png', True)

# Utilization Alex
perf_list = [tot_util['AlexNet_layer1'],tot_util['AlexNet_layer2'],tot_util['AlexNet_layer3']]
plot_single_axis(num_lanes_list, perf_list, "Number of Lanes", "Utilization", alex_list, 'tex_final/fig/Alex_utilization.png', True)

style_list = ["rx--", "ro--", "r^--", "bx-", "bo-", "b^-"]

# Area
prob = problem_list[0]
plt.plot(num_lanes_list, tot_area[prob], style_list[i], linewidth=0.75, fillstyle='none')
plt.ylabel('Area')
plt.xlabel('Number of Lanes')
plt.xscale('log',base=2)
plt.grid()
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.25)
plt.savefig('tex_final/fig/area.png')
plt.close()