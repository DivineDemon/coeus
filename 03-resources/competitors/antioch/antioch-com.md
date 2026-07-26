# Antioch

> Source: https://antioch.com/

[NewAntioch raises $8.5M to enable the agentic development of physical autonomy](https://antioch.com/blog/seed)

![](https://antioch.com/images/hero-bg.jpg)

# Develop autonomy  at the speed of software.

Automating the development and evaluation of physical AI.

[Onboard](https://antioch.com/#onboard) your hardware and software.

[Define](https://antioch.com/#define) realistic simulation scenarios.

[Simulate](https://antioch.com/#simulate) hundreds of tests in parallel.

[Analyze](https://antioch.com/#analyze) failure modes at software speed.

[Accelerate](https://antioch.com/#accelerate) development with the Antioch Agent.

console.antioch.com

CodeScenario TelemetryDocsControls

Excellent

STATEPlaying

FPS58

UPTIME0:00

lobby\_nav.ipynb

AMR Lobby Navigation

Waypoint tracking through a furnished lobby.

\[ \]

```
from antioch import Articulation, GroundPlane, Simulation, scenario
from antioch.lib.utils.assets import load_asset

sim = Simulation(livestream=True)
```

\[ \]

```
GroundPlane(sim, "/World/ground")
load_asset(sim, "/World/lobby", name="lobby-scene", version="1.0.0")
```

\[ \]

```
load_asset(sim, "/World/carter", name="nova_carter", version="1.0.0")
robot = Articulation(sim, "/World/carter")
sim.play()
```

\[ \]

```
WAYPOINTS = [\
    (20.0, 14.5), (15.0, 15.1),\
    (12.5, 15.3), (7.4, 15.2),\
]

with scenario(sim, "lobby-nav", tags=["nav", "obstacles"]) as run:
    for wp in WAYPOINTS:
        while not reached(robot, wp):
            steer_toward(robot, wp, speed=0.5)
            sim.step()
```

\[ \]

```
# scenario context exit auto-uploads telemetry
```

Add Cell

![](data:image/svg+xml,%3csvg%20width='307'%20height='142'%20viewBox='0%200%20307%20142'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M216.25%20142H177.818L157.495%20106.909L161.875%2099.3301H191.537L216.25%20142ZM38.4316%20141.995H0L24.7119%2099.293H63.1436L38.4316%20141.995ZM83.8066%20141.995H45.375L70.0879%2099.293H108.52L83.8066%20141.995ZM261.625%20141.995H223.193L198.48%2099.293H236.912L261.625%20141.995ZM307%20141.995H268.568L243.856%2099.293H282.288L307%20141.995ZM129.183%20141.983H90.751L115.463%2099.3135H153.895L129.183%20141.983ZM232.872%2092.3594H194.44L180.162%2067.6855L190.58%2049.6562H208.159L232.872%2092.3594ZM157.944%2092.3477H119.513L144.225%2049.6777H182.656L157.944%2092.3477ZM67.1826%2092.3389H28.751L53.4639%2049.6357H91.8945L67.1826%2092.3389ZM112.559%2092.3389H74.127L98.8389%2049.6357H137.271L112.559%2092.3389ZM278.247%2092.3389H239.815L215.104%2049.6357H253.534L278.247%2092.3389ZM187.486%2092.335H165.895L176.678%2073.6738L187.486%2092.335ZM186.608%2042.708H148.177L172.889%200.0371094H211.32L186.608%2042.708ZM95.8574%2042.7031H57.4258L82.1377%200H120.569L95.8574%2042.7031ZM141.232%2042.7031H102.801L127.514%200H165.945L141.232%2042.7031ZM204.208%2042.7021H194.6L199.399%2034.3945L204.208%2042.7021ZM249.593%2042.7021H211.162L202.87%2028.375L219.268%200H224.881L249.593%2042.7021Z'%20fill='black'/%3e%3c/svg%3e)lobby-nav

Loading simulation

Scenario Telemetry

Share

Robot Velocityt = 0.0s

0.60.30.0

linear (m/s)

angular (rad/s)

LiDAR Scan128k pts

20 Hz · 2D LiDAR

sim\_time1.00x

+0.0s

## See how Antioch accelerates your work

[Industrial autonomy](https://antioch.com/solutions/industrial) [Ground autonomy](https://antioch.com/solutions/ground) [Aerial autonomy](https://antioch.com/solutions/aerial) [Fixed perception](https://antioch.com/solutions/perception)

How it works

## A continuous loop from  hypothesis to insight.

01Onboard

### Antioch onboards your existing physical system into simulation.

Bring any robot unchanged into Antioch—ROS based, custom, or otherwise. Antioch automates the creation of digital twins, and connects these emulated systems to precision-calibrated virtual sensors and actuators.

Support for any robot software, middleware, and firmware

Cameras, LiDARs, radars, infrared sensors, IMUs, actuators, and more

Strict temporal determinism and replayability

White glove engineering and simulation support

Simulation harness

connected

Your modules

Perception modelPython · custom

ROS robotROS 2 · Humble

Antioch simulation

Camera30 Hz

LIDAR10 Hz

IMU200 Hz

Actuator120 Hz

readreadreadreadwrite

time-deterministicreproduciblezero clock drift

02Define

### Create complex and challenging scenarios with ease.

Use our Python SDK to programmatically spawn complex scenes and dynamic agents that are too dangerous, expensive, or rare to test physically. Define explicit pass/fail criteria and performance metrics using our interactive simulation workspace built for rapid iteration and quick insights.

Curated sim-ready asset library (or upload your own)

AI-generated assets, worlds, and gaussian splats

High-fidelity scans of physical premises

Intelligent deterministic animated agents

![Hospital lobby scene](https://antioch.com/images/scene-sdk.jpg)

hospital-lobby v1.4.0

scene.py

```
from antioch import Character, Light, LightType, Pose, Simulation, Vector3
from antioch.lib.utils.assets import load_asset

sim = Simulation(livestream=True, hide_ui=True)

# Load a photorealistic hospital environment
load_asset(sim, "/World/Hospital", name="hospital-lobby", version="1.4.0")

# Add warm overhead lighting
Light(
    sim,
    "/World/Light",
    light_type=LightType.DISTANT,
    intensity=30000.0,
    color=Vector3(x=1.0, y=0.95, z=0.9),
)

# Spawn seated patients in the waiting area
for i in range(4):
    load_asset(
        sim,
        f"/World/Patient_{i}",
        name="seated-human",
        version="1.0.0",
        world_pose=Pose.from_position(Vector3(x=2.0 + i * 0.6, y=3.0, z=0.0)),
    )

sim.play()
```

03Simulate

### Multiply your testing bandwidth.

Stop waiting on costly and slow physical testing. Instantly launch thousands of parallel simulations in Antioch Cloud, automatically discover failure modes, and optimize hardware and software decisions.

Parallel test runs with domain randomization

Hyperparameter sweeps for HW/SW decisions

CI/CD integration with regression gates

Deterministic telemetry and persistent artifacts

ScenariosExplorerSuites

7 suites

Lobby Detection

80% · 8 runs · Just now

Warehouse Forklift

80% · 7 runs · 2h ago

Data Center Intrusion

58% · 6 runs · Just now

Perimeter Fence

88% · 6 runs · Just now

Stairwell Emergency

83% · 5 runs · Just now

Parking Garage

70% · 5 runs · Just now

Retail Shopfloor

67% · 4 runs · Just now

#### Lobby Detection

suite:lobby-detection

View Runs →

Total Runs

8

Latest Pass Rate

80%

Scenarios per Run

20

Last Run

Just now

Pass Rate History

v2.0-osprey

v2.0-hawk

v2.0-kestrel

v2.1-merlin

v2.1-harrier

v2.1.1-swift

v2.1.1-phoenix

Recent RunsView all →

v2.1.1-phoenix

80%Oliver ParkJust now

v2.1.1-swift

65%Collin Schlager19h ago

v2.1-harrier

60%Alex ChenFeb 24

v2.1-peregrine

30%Oliver ParkFeb 22

v2.1-merlin

25%Alex ChenFeb 21

04Analyze

### Debug with full-stack telemetry.

Pinpoint the exact state of your autonomy stack at the moment of failure by replaying any execution frame-by-frame, and immediately validate whether proposed changes would have made the difference.

Unified and customizable visual telemetry explorer

Native Foxglove and Rerun integrations

Scenario suite comparison across versions

Fine-grained time control and pause/resume

obstacle\_avoidance · seed-03Failed

Custom telemetry

Joint Positions (rad)custom

shoulder

elbow

wrist

1.50.0-1.5

End-Effector Velocity (m/s)custom

linear

angular

2.01.00.0

Min Obstacle Distance (m)custom

clearance

1.00.50.0

0s▲ collision at t=141s300s

05Accelerate

### Enable the autonomous development of autonomy.

Antioch's built-in AI agents and MCP support unlocks the ability to autonomously improve physical systems, by providing insight into failure causes, immediate feedback on any changes, and supplying agents with a fully-interrogable learning gradient.

Model Context Protocol (MCP) support

Agent-controlled assets and environments

Automated test criteria development

Autonomous debug and validation

AI

Antioch Agent

running

Talk to our team

## Join teams using Antioch to ship autonomous systems with confidence, entirely in simulation.

Name

Email

Message

Get in touch