# Source of this model

This folder contains an unchanged copy of the custom six-joint robot arm URDF and all seven STL mesh dependencies from CougarAI × Robotics@UH.

Source: https://github.com/Cougar-AI/robotarm-cai-ruh/tree/5bebc2e7a270d64ced6b34bcddc509881ad71ad3/software/robotviewer/models/RobotArm

Keep `Arm.urdf` and `meshes/` together. The model loads in MuJoCo 3.10.0 with six joint coordinates and no actuators. All joints are continuous in this source; physical limits and controllers still need validation by the team.

The source commit is March 11, 2026 (CDT). It is the best-supported current six-joint project model found, but the repository does not document a definitive CAD revision number.
