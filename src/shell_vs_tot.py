import os
import numpy as np
import matplotlib.pyplot as plt
from npdb import db_inter
import plot_defaults

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = True
plt.rcParams['legend.fontsize'] = 14

for opt in plt.rcParams:
    if plt.rcParams[opt] == 'bold':
        plt.rcParams[opt] = 'normal'


def build_nmet2_nmet2shell_plot(metals, shape, num_shells,
                                show_ee=True, show=True, save=False):
    shell_dict = {s: db_inter.build_atoms_in_shell_list(shape, s)
                  for s in range(2, num_shells + 1)}

    # add central atom to first shell
    shell_dict[2].append(0)

    # 5 shell NP
    nanoparticles = db_inter.get_bimet_result(metals=metals, shape=shape,
                                              num_shells=num_shells)

    results = np.zeros((len(nanoparticles), len(shell_dict) + 2))

    for i, nanop in enumerate(nanoparticles):
        results[i, 0] = nanop.n_metal2
        for s in shell_dict:
            shell_atoms = nanop.build_atoms_obj()[shell_dict[s]]
            nmet2_shell = sum([1 for a in shell_atoms
                               if a.symbol == nanop.metal2])
            results[i, s - 1] = nmet2_shell
        results[i, s] = nanop.EE

    # ensure shell counts were correctly calculated
    assert (results[:, 0] == results[:, 1:-1].sum(1)).all()

    shell_color = ['gray', 'green', 'red', 'blue', 'cyan', 'gold',
                   'orange', 'purple', 'pink']

    fig, ax = plt.subplots(figsize=(9, 7))

    if show_ee:
        # excess energy secondary axis
        ee_color = 'deepskyblue'
        ax2 = ax.twinx()
        ax2.tick_params(axis='y', labelcolor=ee_color)
        ax2.plot(results[:, 0], results[:, -1], '^', label='EE',
                color=ee_color, zorder=-100)
        ax2.set_ylabel('Excess Energy (eV / atom)', color=ee_color)
        # ax2.set_ylim(-0.03, 0.03)

    # plot ni vs ni-shell
    for i in range(1, results.shape[1] - 1):
        ax.plot(results[:, 0], results[:, i], 'o-', color=shell_color[i],
                label='Shell %i' % i, zorder=i)

    # used to match Larsen et al.'s plot
    if num_shells == 5:
        ax.set_xlim(0, 315)
        ax.set_ylim(0, 180)

    ax.set_xlabel('$\\rm N_{%s}$ in NP' % nanop.metal2)
    ax.set_ylabel('$\\rm N_{%s}$ in shell' % nanop.metal2)

    title = '%s atom %s%s %s NP' % (nanop.num_atoms, nanop.metal1,
                                    nanop.metal2, nanop.shape)
    ax.set_title(title)

    ax.legend(loc='upper center', ncol=3)
    fig.tight_layout()
    path = 'C:\\Users\\YLA\\Box Sync\\Michael_Cowan_PhD_research\\np_ga\\' \
        'FIGURES\\nmet_vs_nmetshell-LARSON\\%s%s-%s\\' % (nanop.metal1,
                                                          nanop.metal2,
                                                          nanop.shape[:3])
    if save:
        if not os.path.isdir(path):
            os.mkdir(path)
        fig.savefig(path + title.replace(' ', '_') + '.png')
    if show:
        plt.show()
    return fig, results

if __name__ == '__main__':
    metals = 'aucu'
    shape = 'icosahedron'
    shell_range = range(2, 10)
    for num_shells in [4]:
        build_nmet2_nmet2shell_plot(metals,
                                    shape,
                                    num_shells,
                                    show=True,
                                    save=False,
                                    show_ee=True)
