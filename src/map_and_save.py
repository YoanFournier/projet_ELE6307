import os
import re

# Il faut etre au root du projet (PROJET_ELE6307) pour run le script

def arch_modif(orig='src/arch/ARA_arch_base.yaml', dest='src/arch/ARA_arch.yaml', num_lanes=2, tech_node=22):
    with open(orig, 'r') as orig_file:
        txt = orig_file.read()
        txt_new = txt.replace('$tech_node$', '{0}nm'.format(tech_node))
        if num_lanes > 1 :
            txt_new = txt_new.replace('$num_lanes$', '[{0}..{1}]'.format(0, num_lanes-1))
        else :
            txt_new  = txt_new.replace('$num_lanes$', '')
        with open(dest, 'w') as dest_file:
            dest_file.write(txt_new)

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

problems = ['AlexNet_layer1','AlexNet_layer2','AlexNet_layer3','VGG02_layer1','VGG02_layer2','VGG02_layer3']

tech_node_list = [45]
num_lanes_list = [1,2,4,8,16]

tot_energy_list = []
tot_cycles_list = []
tot_area_list   = [] 
tot_util_list   = []
 
for tech_node in tech_node_list:
    print("TECHNOLOGY NODE : {0}nm".format(tech_node))

    for problem in problems:
        print("\t---------------------------------------")
        print("\tPROBLEM :", problem)

        for num_lanes in num_lanes_list:

            print("\t---------------------------------------")
            print("\tSTARTING TIMELOOP MAPPER FOR {0} LANES".format(num_lanes))

            out_folder = 'src/output_{0}nm/{1}/{2}_lanes/'.format(tech_node, problem, num_lanes)
            command = "timeloop-mapper src/arch/ARA_arch.yaml src/map/mapper.yaml src/prob/{0}.yaml -o {1}".format(problem, out_folder) + " >/dev/null 2>&1"

            print("\t\tCOMMAND:", command)

            arch_modif(num_lanes=num_lanes, tech_node=tech_node)
            os.system(command)

            tot_energy, tot_cycles, tot_area, tot_util = results_parser(out_folder + 'timeloop-mapper.stats.txt')   

            tot_energy_list.append(tot_energy) 
            tot_cycles_list.append(tot_cycles) 
            tot_area_list.append(tot_area)
            tot_util_list.append(tot_util)

            print("\t\tENERGY:", tot_energy)
            print("\t\tCYCLES:", tot_cycles)
            print("\t\tAREA:", tot_area)
            print("\t\tUTILIZATION:", tot_util)

            print("\tFINISHING TIMELOOP MAPPER FOR {0} LANES".format(num_lanes))
print("FINAL RESULTS : ")
with open('src/results.txt', 'w') as file:
    file.write(str(tot_energy_list) + '\n')
    file.write(str(tot_cycles_list) + '\n')
    file.write(str(tot_area_list  ) + '\n')
    file.write(str(tot_util_list  ) + '\n')

print("tot_energy_list :", tot_energy_list)
print("tot_cycles_list :", tot_cycles_list)
print("tot_area_list   :", tot_area_list  )
print("tot_util_list   :", tot_util_list  )