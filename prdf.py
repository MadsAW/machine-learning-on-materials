from __future__ import division
from __future__ import print_function

import numpy as np
from ase import Atoms, Atom
from ase.neighborlist import NeighborList


def s2i(symbols):
    """
    Examples:
    >>> symbols=['H', 'Li', 'H', 'F']
    >>> s2i(symbols)
    {'H': [0, 2], 'F': [3], 'Li': [1]}
    """
    out = {}
    for i, symbol in enumerate(symbols):
        if symbol not in out:
            out[symbol] = []
        out[symbol].append(i)
    return out


def get_count(symbols):
    """
    Examples:
    >>> get_stuff(['Li', 'H', 'Li'])
    >>> {'Li': 2, 'H': 1}
    """
    return dict([(e, symbols.count(e)) for e in set(symbols)])


def get_shell_volume(r, dr):
    return 4 / 3 * np.pi * ((r + dr)**3 - r**3)


def get_cluster(atoms, a, nl):
    """
    Parameters
    ----------
    atoms: Atoms
    a: int
        atom index that will be the center of the cluster
    nl: NeighborList
    """
    cell = atoms.get_cell()
    indices, offsets = nl.get_neighbors(a)
    atoms2 = Atoms()
    for i, o in zip(indices, offsets):
        pos = atoms[i].position + np.dot(o, cell)
        atoms2.append(Atom(atoms[i].symbol, position=pos))

    atoms2 = atoms[a: a+1] + atoms2
    return atoms2


def get_shell(atoms, r, dr, a=0):
    """Shell of atoms centered at atoms[a]

    Parameters
    ----------
    atoms: Atoms
    r: float
        inner radius of spherical shell
    dr: float
        shell thikness
    a: {0, int}, optional
        atom index that defines the center of the spherical shell
    """
    n = len(atoms)
    d_0j = atoms.get_distances(0, range(n))
    indices = np.arange(n)[(d_0j > r) * (d_0j < r + dr)]
    return atoms[indices]


def get_rdf(atoms, a, rs, dr, rmax, nl=None):
    """number of atoms in a shell between r and r+dr
       centered around atom a and normalized by the shell volume.
       The number of atoms are devided into types according to
       their atomic number.
    """
    V_r = get_shell_volume(rs, dr)
    if nl is None:
        cutoffs = [rmax / 2 + 0.1, ] * len(atoms)
        nl = NeighborList(cutoffs=cutoffs,
                          skin=0,
                          self_interaction=False,
                          bothways=True)
        nl.update(atoms)

    cluster = get_cluster(atoms, a=a, nl=nl)  # first atom in the cluser -> a=0
    zs = set(atoms.get_chemical_symbols())
    p = dict([[z, np.zeros(len(rs))] for z in zs])
    for ir, r in enumerate(rs):
        shell = get_shell(atoms=cluster,
                          r=r,
                          dr=dr,
                          a=0)
        zs_shell, count = np.unique(shell.get_chemical_symbols(),
                                    return_counts=True)
        zc = dict([(z, c) for z, c in zip(zs_shell, count)])
        for z in zs:
            if z in zc:
                p[z][ir] = zc[z]
            else:
                p[z][ir] = 0
    for z in zs:
        p[z] /= V_r

    return p


def prdf(atoms, rs, dr, r_max):
    """
    Partial radial destribution function

    Parameters
    ----------
    atoms: Atoms object
    rs: (Nr, ) ndarray
        radiis where the prdb is evaluated
    dr: float
        thickness of the shell
    r_max: float
        cutoff radius

    Returns
    -------
    (Ntypes, Ntypes, Nr) ndarray, (Ntypes, ) str list

    References:
        K. T. Schutt et al. PRB 89, 205118 (2014)

    """
    eta = 0.1
    cutoffs = [r_max / 2 + eta, ] * len(atoms)
    nl = NeighborList(cutoffs=cutoffs,
                      skin=0,
                      self_interaction=False,
                      bothways=True)
    nl.update(atoms)
    s2a = s2i(atoms.get_chemical_symbols())  # e.g. {'H': [0, 2], 'Li': [1]}
    types = [t for t in s2a.keys()]  # e.g. ['H', 'Li']
    nt = len(types)
    p_ttr = np.zeros((nt, nt, len(rs)))
    for i, alpha in enumerate(types):  # e.g. 0, 'H'
        alpha_indices = s2a[alpha]
        for a in alpha_indices:  # loop over atoms with a certain type
            p_tr = get_rdf(atoms, a, rs, dr, r_max, nl)
            for j, beta in enumerate(types):
                p_r = p_tr.get(beta)
                if p_r is not None:
                    p_ttr[i, j] += p_r / len(alpha_indices)

    return p_ttr, types


if __name__ == '__main__':
    from ase.build import bulk
    import matplotlib.pyplot as plt

    rmax = 10.0
    dr = 0.2
    atoms = bulk('Si')
    atoms.set_chemical_symbols(['Si', 'F'])
    rs = np.arange(0, rmax - dr, dr / 5)
    p_ttr, types = prdf(atoms, rs, dr, rmax)
    print('ordering:')
    for i, t in enumerate(types):
        print('{0}, {1}'.format(i, t))

    ntypes = len(types)
    for i in range(ntypes):
        for j in range(ntypes):
            plt.plot(rs, p_ttr[i, j], label='{0}, {1}'.format(types[i],
                                                              types[j]))

    plt.legend()
    plt.show()
