# Dynamics Project
"""
This implements a dynamic analysis of the rowing machine. It can be used to compare the power produced by rowers of different heights given the same original force exerted.

Author: Lana Savkovic
"""

import math
import numpy as np

# assume that width of all limbs is 4cm
WIDTH = 0.8

# assume that height of all limbs is 4cm
HEIGHT = 0.8

# assume that density of all limbs is 33kg/m
DENSITY = 33

# Each stroke on the rowing machine is done at rate 20, each part of the drive is assumed to take 1/3 of the time (1s)
TIME = 1

# The layback angle for the trunk at the end of the drive (10 degrees)
LAYBACK = 0.17453293


def power_stroke(force_applied: float, height: float):
    """
    Return the power generated from the stroke on the rowing machine.
    """
    # lengths of body parts
    len_shins = 0.25 * height
    len_thighs = 0.28 * height
    len_trunk = 0.31 * height
    len_upper_arm = 0.18 * height
    len_lower_arm = 0.19 * height
    length_drive = 0.75 * height

    # masses of chunks of body
    mass_upper_body = mass(len_upper_arm + len_lower_arm + len_trunk)
    mass_arms = mass(len_upper_arm + len_lower_arm)

    # tension generated at each part of the drive
    tension_legs = leg_drive_tension(
        len_shins, len_thighs, force_applied, mass_upper_body)
    tension_body = trunk_tension(len_trunk, force_applied, mass_arms)
    tension_arms = arm_tension(len_upper_arm, len_lower_arm, force_applied)

    return ((tension_legs * 0.5 * length_drive) + (tension_body * 0.25 * length_drive) + (tension_arms * 0.25 * length_drive)) / TIME


def mass(length: float):
    """
    Returns the mass of a limb given its length. The width, height, and density of all limbs is assumed.
    """
    return DENSITY * length * WIDTH * HEIGHT


# Functions relating to leg drive
def ang_vel_shins():
    """
    Returns the angular velocity of the shins. Constant value.
    """
    return 3 * math.sqrt(2)


def ang_vel_thigh(len_shins: float, len_thighs: float) -> float:
    """
    Returns the angular velocity of the thigh given its length and the length of the shins.
    """
    theta = math.acos(len_shins / len_thighs)
    return 3 * ((1 - math.sqrt(2)) * len_shins / len_thighs + 1 - math.sin(theta))


def leg_drive_tension(len_shins: float, len_thighs: float, force_applied: float, mass_upper_body: float):
    """
    Returns the tension of the leg drive on the rowing machine given the initial force exerted and the length of the shins and thighs. The force of tension equals fnetx_upper_body + fnetx_thigh + initial force applied by feet.
    """
    # accelerations of limbs in the x direction
    ang_v_shins = ang_vel_shins()
    ang_v_thigh = ang_vel_thigh(len_shins, len_thighs)
    acc_shins = - (ang_v_shins ** 2) * (len_shins / 2)
    acc_thigh = -(ang_v_thigh ** 2) * \
        (len_thighs / 2) + 2 * ang_v_shins
    acc_body = -(ang_v_thigh
                 * (len_thighs / 2)) + 2 * ang_v_shins

    # mass of limbs
    mass_shins = mass(len_shins)
    mass_thigh = mass(len_thighs)

    return force_applied + acc_shins * mass_shins + acc_thigh * mass_thigh + acc_body * mass_upper_body


# Functions relating to trunk

def trunk_tension(len_trunk: float, force_applied: float, mass_arms: float):
    """
    Returns the tension on the handle of the rowing machine of the drive created by rotating the trunk given the length of the trunk.
    """
    # the angle between the trunk and the horizontal plane at the end of the drive
    theta = math.pi / 2 - LAYBACK

    # the angular acceleration and velocity of the trunk during the drive
    ang_acc_trunk = 36 * math.sin(LAYBACK) * math.cos(LAYBACK)
    ang_vel_trunk = 6 * math.sin(LAYBACK)

    # accelerations in the x direction
    acc_trunk = ang_acc_trunk * len_trunk * math.sin(theta) / 2 + \
        (ang_vel_trunk ** 2) * len_trunk * math.cos(theta)
    acc_arms = 2 * acc_trunk

    # mass of the trunk
    mass_trunk = mass(len_trunk)

    return force_applied + acc_trunk * mass_trunk + acc_arms * mass_arms


# Functions relating to arms

def ang_acc_lo_arm(len_upper_arm: float, len_lower_arm: float, theta: float):
    """
    returns the angular acceleration of the forearm given its length, the upper arm's length, and the angle between the forearm and the horizontal plane.
    """
    return 9 * math.sin(theta) * ((1 - math.sqrt(2)) * len_upper_arm / len_lower_arm + 1 - math.cos(theta))


def ang_vel_lo_arm(len_upper_arm: float, len_lower_arm: float, theta: float):
    """
    returns the angular velocity of the forearm given its length, the upper arm's length, and the angle between the forearm and the horizontal plane.
    """
    return 3 * ((1 - math.sqrt(2)) * len_upper_arm / len_lower_arm + 1 - math.cos(theta))


def acc_lower_arm(len_lower_arm: float, len_upper_arm: float):
    """
    Returns the acceleration of the upper arm in the x direction when given its length
    """
    # Find angle of lower arm to horizontal plane
    theta = math.asin(len_upper_arm / len_lower_arm)

    ang_acc = ang_acc_lo_arm(len_upper_arm, len_lower_arm, theta)
    ang_vel = ang_vel_lo_arm(len_upper_arm, len_lower_arm, theta)

    return ang_acc * (len_lower_arm * math.sin(theta) / 2) + (ang_vel ** 2) * (len_lower_arm * math.cos(theta) / 2)


def arm_tension(len_upper_arm: float, len_lower_arm: float, force_applied: float):
    """
    Returns the tension on the handle of the rowing machine of the arm drive given the length of the upper and lower arm.
    """
    # find mass of arm parts
    mass_lower_arm = mass(len_lower_arm)

    # find accelerations in the x direction of arm parts
    acc_lo_arm = acc_lower_arm(len_lower_arm, len_upper_arm)

    return force_applied + mass_lower_arm * acc_lo_arm


if __name__ == '__main__':
    print("Hello! If you love rowing as much as we do, we hope you'll enjoy this program :)")
    height = float(input("Please enter your height (m): "))
    force_applied = float(input("Please enter the original force applied: "))
    wattage = power_stroke(force_applied, height)
    print(f"Your expected wattage produced is {wattage:.2f} W")

