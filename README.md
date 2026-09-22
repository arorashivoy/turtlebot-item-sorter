# TurtleBot item sorter

A multi-robot controller for the **AURO** assessment at the University of York:
three TurtleBot3 Waffle Pi robots in Gazebo collect coloured items from an arena
and deposit each colour in its matching zone, without driving into each other.

This repository holds **my controller only**. The module's simulation packages —
the arena, the item and zone sensors, the message definitions — are the
instructor's and are not redistributed here. See *Running it* below.

> A GIF of two or more robots sorting belongs here.

## What the controller does

Each robot runs one `RobotController` node, constructed with its own name, target
zone and item colour, so three instances cover the three colours.

### The state machine

The robot cycles through: **search for an item** → **navigate to it** → **pick it
up** → **search for the matching zone** → **navigate to the zone** → **offload**.
Searching is a rotate-and-scan; navigation is proportional steering on the bearing
to the target, taken from the item and zone camera topics. `control_loop` runs on
a timer and dispatches on the current state.

### Collision avoidance, in two independent layers

The interesting part is that neither layer alone is enough.

**Between robots — odometry, not sensing.** Each controller subscribes to the
other robots' `/odom` topics through `other_robot_odom_callback` and keeps their
positions. `avoid_collision_with_robots` compares them against
`COLLISION_THRESHOLD` and backs off. This works where the LiDAR does not: another
TurtleBot is a small, low, round obstacle that a planar scan sees late and
intermittently, and by then two robots converging on the same item are already
committed.

**Against everything else — a four-sector LaserScan gate.** `scan_callback`
reduces the full scan to four booleans — front, left, back, right — by taking the
minimum range in each quadrant and comparing it to `SCAN_THRESHOLD = 0.6` m. The
controller then checks `scan_triggered[SCAN_FRONT]` first, then left, then right,
and turns away from whichever sector is blocked. Reducing a 360-point scan to four
bits is crude, but it makes the avoidance behaviour deterministic and debuggable,
which matters more than precision when three robots are interacting.

## Running it

You need the AURO module's simulation packages (`assessment`,
`assessment_interfaces`, `auro_interfaces`) in the same workspace. They are the
University of York's, not mine, so they are not included here — obtain them from
the module.

Drop this package into `~/auro_ws/src/`, then:

```sh
cd ~/auro_ws && colcon build && source install/setup.bash

# arena, with three robots
ros2 launch assessment assessment_launch.py num_robots:=3

# one controller per robot
ros2 run solution controller0
ros2 run solution controller1
ros2 run solution controller2
```

`start_ros.sh` opens all of the above in separate terminals, with a 20-second
delay so the simulation is up before the controllers attach.

## Provenance

`robot_controller.py` began as the module's skeleton controller; the state
machine, the odometry-based inter-robot avoidance and the LaserScan sector gating
are mine. The commit history in this repository is the record of that work.

Licensed under the Apache License 2.0.
