#!/usr/bin/env python3

import ase.cluster
import ase.lattice


def create_cube(num_layers: "int", kind: "str" = "Cu") -> "ase.Atoms":
    """
    Creates an FCC cube with faces on the {100} family of planes.

    :param num_layers: Number of unit cells along each side of the cube.
    :type num_layers: int
    :param kind: The element making up the skeleton. Defaults to "Cu"
    :type kind: str

    :return: An ASE atoms object containing the cube skeleton
    """

    lattice = ase.lattice.cubic.FaceCenteredCubic(kind, size=[num_layers] * 3)
    cube = ase.build.cut(lattice, extend=1.01)
    return cube


def create_sphere(num_layers: "int", kind: "str" = "Cu", unit_cell_length: "float" = 3.61) -> "ase.Atoms":
    """
    Inscribes a sphere inside a cube and makes it a nanoparticle. Perfect symmetry not guaranteed.

    :param num_layers: The size of the lattice containing the inscribed sphere.
    :type num_layers: int
    :param kind: The element making up the skeleton. Defaults to "Cu"
    :type kind: str
    :param unit_cell_length: The edge-length of the unit cell.
    :type unit_cell_length: float

    :return: An ASE atoms object containing the sphere skeleton.
    """

    # Create the cube
    cube = create_cube(num_layers, kind)

    # Simple geometry
    center = cube.positions.mean(0)
    cutoff_radius = num_layers * unit_cell_length / 1.99
    distance_list = map(ase.np.linalg.norm,
                        ase.geometry.get_distances(cube.get_positions(), p2=center)[1])

    # Build the sphere using atoms that are within the cutoff
    sphere = ase.Atoms()
    for atom, distance in zip(cube, distance_list):
        if distance <= cutoff_radius:
            sphere += atom

    return sphere
