# Request a Demo — Antioch

> Source: https://antioch.com/demo

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