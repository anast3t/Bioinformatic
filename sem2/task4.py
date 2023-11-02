import pymol2
import os

representations = {
    'wireframe': {'lines'},
    'backbone': {'ribbon'},
    'spacefill': {'sphere'},
    'ribbons': {'cartoon', 'ribbon'},
    'molecular_suface': {'surface'},
}


width = 2000
height = width


pm = pymol2.PyMOL()
pm.start()
pm.cmd.load('./8esi.pdb.gz')

def prepare_domain():
    pm.cmd.util.cbc(_self=pm.cmd)

def prepare_cpk():
    pm.cmd.util.cbag(_self=pm.cmd)

coloring_modes = {
    'cpk': prepare_cpk,
    'domain': prepare_domain,
}

os.makedirs('res', exist_ok=True)

for mode_name, mode_f in coloring_modes.items():
    rd=f'res/{mode_name}'
    os.makedirs(rd, exist_ok=True)

    for name, reprs in representations.items():
        pm.cmd.hide()
        for r in reprs:
            pm.cmd.show(r)
        pm.cmd.zoom()
        mode_f()
        pm.cmd.png(f'{rd}/{name}.png', width, height)
