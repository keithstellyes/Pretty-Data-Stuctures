import yaml

lines = open('typechart.csv', 'r').readlines()

types = [t.strip() for t in lines[0].split(',')[1:]]

alphabet = types + ['0', '0.25', '0.5', '1', '2', '4', ' ']

d = {'init':'qReadMove', 'accept':'qAccept', 'reject':'NOPE'}

d['alphabet'] = alphabet

# generate readmove states

d['qReadMove'] = []
for t in types:
    d['qReadMove'].append({'if':t, 'wr':' ', 'to':'q' + t, 'tape':'RIGHT'})

# build type table
type_table = {}

for i in range(1, len(lines)):
    line = lines[i].split(',')
    type_table[line[0]] = {}

    for i in range(1, len(line)):
        type_table[line[0]][types[i-1]] = line[i].strip()

# build processing
for attacking_type in types:
    d['q'+attacking_type] = []
    dat = d['q'+attacking_type]
    done = {'if':' ', 'to':'qComputeStart', 'tape':'LEFT'}
    dat.append(done)

    for defending_type in types:
        pairing = {'if':defending_type, 'to':'q'+attacking_type,
                   'wr':type_table[attacking_type][defending_type],
                   'tape':'RIGHT'}
        dat.append(pairing)

# compute step
d['qComputeStart'] = []
d['qComputeStart'].append({'if':'0', 'to':'qAccept'})
d['qComputeStart'].append({'if':'0.5', 'to':'qComputeP5', 'tape':'LEFT'})
d['qComputeStart'].append({'if':'1', 'to':'qCompute1', 'tape':'LEFT'})
d['qComputeStart'].append({'if':'2', 'to':'qCompute2', 'tape':'LEFT'})

d['qComputeP5'] = []
d['qComputeP5'].append({'if':'0', 'to':'qAccept'})
d['qComputeP5'].append({'if':'0.5', 'wr':'0.25', 'to':'qAccept'})
d['qComputeP5'].append({'if':'1', 'wr':'0.5', 'to':'qAccept'})
d['qComputeP5'].append({'if':'2', 'wr': '1', 'to':'qAccept'})

d['qCompute1'] = []
for n in ('0', '0.5', '1', '2'):
    d['qCompute1'].append({'if':n, 'to':'qAccept'})

d['qCompute2'] = []
d['qCompute2'].append({'if':'0', 'to':'qAccept'})
d['qCompute2'].append({'if':'0.5', 'wr':'1', 'to':'qAccept'})
d['qCompute2'].append({'if':'1', 'wr':'2', 'to':'qAccept'})
d['qCompute2'].append({'if':'2', 'wr':'4', 'to':'qAccept'})
d['qCompute2'].append({'if':' ', 'tape':'RIGHT', 'to':'qAccept'})

f = open('pkmntypes.yml', 'w')
f.write(yaml.dump(d, default_flow_style=False))

f.close()
