"""Check forward kinematics in MuJoCo: joint angles in, hand position out.

Usage:
  python fk_check.py two_link 30 60                          (2 angles, DEGREES)
  python fk_check.py two_link 35                             (link 1 alone: elbow)
  python fk_check.py teaching_arm 0.55 0.45 -0.95 0 0.35 0   (6 angles, RADIANS)

Options:
  --rad   read two_link angles as radians
  --deg   read teaching_arm angles as degrees

The XML files must sit in the same folder as this script. No physics runs:
the script sets qpos, calls mj_forward, and prints where the "hand" site is.
"""
import math
import os
import sys

import mujoco

HERE = os.path.dirname(os.path.abspath(__file__))

ARMS = {
    # name: (xml file, number of angles, default unit)
    "two_link": ("two_link_arm.xml", 2, "deg"),
    "teaching_arm": ("teaching_arm_6dof.xml", 6, "rad"),
}


def usage(message):
    print("Error: " + message, file=sys.stderr)
    print(__doc__.strip().split("\n\nThe XML")[0], file=sys.stderr)
    sys.exit(2)


def main(argv):
    flags = [a for a in argv if a in ("--rad", "--deg")]
    args = [a for a in argv if a not in ("--rad", "--deg")]
    if not args or args[0] in ("-h", "--help"):
        usage("give an arm name and its joint angles.")
    name, values = args[0], args[1:]
    if name not in ARMS:
        usage("unknown arm '%s'. Use one of: %s." % (name, ", ".join(ARMS)))
    xml_file, n_angles, unit = ARMS[name]
    if flags:
        unit = flags[-1][2:]
    one_link = name == "two_link" and len(values) == 1
    if len(values) != n_angles and not one_link:
        usage("%s needs %d angles, got %d." % (name, n_angles, len(values)))
    try:
        angles = [float(v) for v in values]
    except ValueError:
        usage("angles must be numbers, got: %s" % " ".join(values))

    model = mujoco.MjModel.from_xml_path(os.path.join(HERE, xml_file))
    data = mujoco.MjData(model)
    # MuJoCo always stores hinge angles in radians.
    if one_link:
        angles.append(0.0)
    data.qpos[:] = [math.radians(a) for a in angles] if unit == "deg" else angles
    mujoco.mj_forward(model, data)  # forward kinematics only, no time step

    hand = data.site("hand").xpos
    if one_link:
        elbow = data.site("elbow").xpos
        print("elbow = (%.3f, %.3f) m" % (elbow[0], elbow[1]))
    elif name == "two_link":
        print("hand = (%.3f, %.3f) m" % (hand[0], hand[1]))
    else:
        print("hand = (%.3f, %.3f, %.3f) m" % (hand[0], hand[1], hand[2]))


if __name__ == "__main__":
    main(sys.argv[1:])
