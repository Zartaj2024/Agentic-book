---
sidebar_position: 4
---

# ROS2 Fundamentals

## Introduction to ROS2

Robot Operating System 2 (ROS2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

Unlike traditional operating systems, ROS2 is not an actual OS but rather a middleware that provides services designed for a heterogeneous computer cluster. It includes hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

## The ROS2 Architecture

### Nodes

A node is a process that performs computation. ROS2 is designed with the philosophy that nodes should be as lightweight as possible. A single system usually runs many nodes, each potentially on different machines connected by a network.

#### Node Characteristics
- **Lightweight**: Nodes should perform a single task
- **Modular**: Each node operates independently
- **Communicative**: Nodes communicate through topics, services, or actions

#### Creating Nodes
Nodes are typically written in C++ or Python and use the ROS2 client library (rcl) to interface with the ROS2 system.

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        # Node initialization code here
```

### Topics and Messages

Topics provide a way for nodes to communicate with each other through a publish/subscribe model. Each topic has a specific message type that determines the data structure.

#### Publish/Subscribe Pattern
- **Publisher**: Node that sends messages to a topic
- **Subscriber**: Node that receives messages from a topic
- **Messages**: Data structures that carry information between nodes

#### Message Types
Messages are defined using the `.msg` interface definition language and are automatically converted to language-specific implementations (C++, Python, etc.).

Common message types include:
- `std_msgs`: Basic data types (Int32, Float64, String)
- `geometry_msgs`: Spatial data (Point, Pose, Twist)
- `sensor_msgs`: Sensor data (LaserScan, Image, JointState)

### Services

Services provide a request/reply communication model, where one node sends a request and waits for a response from another node. This is synchronous communication.

#### Service Characteristics
- **Synchronous**: Request blocks until response is received
- **Point-to-point**: Direct communication between two nodes
- **Request/Response**: Defined message types for both directions

#### Service Types
Services are defined using `.srv` files that specify both request and response message types.

### Actions

Actions are used for long-running tasks that require feedback and the ability to cancel. They combine the features of services and topics.

#### Action Characteristics
- **Asynchronous**: Non-blocking communication
- **Feedback**: Continuous updates on task progress
- **Goal Management**: Ability to send goals, receive results, and cancel
- **Status**: Task status information (active, succeeded, cancelled, aborted)

#### Action States
- **Goal**: Requested task to be executed
- **Feedback**: Continuous updates during execution
- **Result**: Final outcome when task completes

## The ROS2 Graph

The ROS2 graph refers to the network of nodes, topics, services, and actions that make up a running ROS2 system. The graph is dynamic and can change as nodes are started or stopped.

### Graph Visualization
The `ros2 topic list`, `ros2 service list`, and `ros2 node list` commands allow you to inspect the current state of the graph.

### Launch Files
Launch files (`.launch.py`) are used to start multiple nodes with a single command, defining the initial structure of the ROS2 graph.

## ROS2 Communication Patterns

### Publisher-Subscriber Pattern
Best for:
- Broadcasting sensor data
- Broadcasting robot state
- Continuous data streams

### Client-Service Pattern
Best for:
- Configuration requests
- One-time computations
- Synchronous operations

### Action Client-Server Pattern
Best for:
- Navigation goals
- Manipulation tasks
- Long-running operations with feedback

## Quality of Service (QoS)

ROS2 provides Quality of Service profiles to handle different communication requirements:

- **Reliability**: Best effort vs. Reliable delivery
- **Durability**: Volatile vs. Transient local (for late-joining subscribers)
- **History**: Keep last N messages vs. keep all messages
- **Deadline**: Maximum time between messages
- **Liveliness**: How to detect if a publisher is alive

## ROS2 Middleware (RMW)

ROS2 uses a pluggable middleware layer that allows different communication implementations:
- **Fast DDS**: Default middleware, optimized for real-time systems
- **Cyclone DDS**: Lightweight alternative
- **RTI Connext**: Commercial option with additional features

## Parameter System

ROS2 provides a unified parameter system that allows nodes to have configurable parameters that can be set at runtime:

```python
self.declare_parameter('param_name', default_value)
param_value = self.get_parameter('param_name').value
```

## Time and Transformations

### ROS2 Time
ROS2 provides a unified time system that can use system time, simulation time, or other time sources.

### TF2 (Transform Library)
TF2 is ROS2's transform library that keeps track of multiple coordinate frames over time, essential for robot localization and mapping.

## Best Practices

### Node Design
- Keep nodes focused on single responsibilities
- Use meaningful node names
- Implement proper error handling
- Use parameters for configuration

### Communication Design
- Choose the right communication pattern for your use case
- Use appropriate QoS settings
- Consider network bandwidth and latency
- Design robust message structures

### System Architecture
- Plan your topic and service architecture before implementation
- Use launch files to manage complex systems
- Implement proper logging and diagnostics
- Consider security requirements

## ROS2 Ecosystem

ROS2 includes many packages and tools:
- **Navigation2**: For robot navigation
- **MoveIt2**: For robot manipulation
- **Gazebo/Horizon**: For simulation
- **RViz2**: For visualization
- **rosbag2**: For data recording and playback

ROS2's modular architecture allows you to use only the components you need, making it suitable for a wide range of robot applications from simple educational robots to complex industrial systems.