---
sidebar_position: 7
---

# Capstone Project: Object Recognition and Reaching Pipeline

## Overview

This capstone project demonstrates the integration of multiple concepts from this textbook into a complete robotic pipeline. We'll implement a system that can "see an object → plan a reach → execute" the reaching motion. This project combines computer vision, motion planning, and robot control in a practical application.

## System Architecture

The complete pipeline consists of four main components:

1. **Object Detection**: Identify objects in the robot's visual field
2. **Pose Estimation**: Determine the 3D position and orientation of the target object
3. **Motion Planning**: Compute a collision-free path from the current end-effector position to the target
4. **Trajectory Execution**: Execute the planned motion on the physical or simulated robot

## Prerequisites

Before implementing this system, ensure you have:

- A robot arm with known kinematics (real or simulated)
- ROS2 installed with MoveIt2 and vision packages
- A camera calibrated and mounted on the robot or in the workspace
- Basic understanding of:
  - ROS2 topics and services
  - TF2 for coordinate transformations
  - MoveIt2 motion planning

## Object Detection Module

### Vision Setup

First, we need to capture images from our camera and detect objects of interest:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')

        # Initialize CV bridge
        self.bridge = CvBridge()

        # Subscribe to camera topic
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publisher for detected object pose
        self.object_pose_pub = self.create_publisher(
            PoseStamped,
            '/detected_object_pose',
            10
        )

        # Parameters
        self.declare_parameter('object_color_lower', [0, 100, 100])  # HSV values
        self.declare_parameter('object_color_upper', [10, 255, 255])
        self.declare_parameter('min_object_area', 1000)

    def image_callback(self, msg):
        """Process incoming image and detect objects"""
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f'Could not convert image: {e}')
            return

        # Convert to HSV for color-based detection
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Get parameters
        lower = np.array(self.get_parameter('object_color_lower').value)
        upper = np.array(self.get_parameter('object_color_upper').value)
        min_area = self.get_parameter('min_object_area').value

        # Create mask for the target color
        mask = cv2.inRange(hsv, lower, upper)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour that meets minimum area requirement
        largest_contour = None
        max_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area and area > max_area:
                max_area = area
                largest_contour = contour

        if largest_contour is not None:
            # Calculate the center of the object in image coordinates
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                # Convert image coordinates to 3D world coordinates
                # This requires camera calibration and depth information
                object_pose = self.pixel_to_world(cx, cy, msg.header.frame_id)

                # Publish the detected object pose
                self.publish_object_pose(object_pose)

                # Visualize the detection
                cv2.drawContours(cv_image, [largest_contour], -1, (0, 255, 0), 2)
                cv2.circle(cv_image, (cx, cy), 5, (0, 0, 255), -1)

                # Publish visualization image (optional)
                # self.publish_visualization(cv_image)

    def pixel_to_world(self, u, v, camera_frame):
        """Convert pixel coordinates to world coordinates using camera calibration"""
        # This is a simplified version - in practice, you'd use camera info
        # and triangulation or depth data to get 3D position

        # For this example, we'll assume a fixed distance and simple transformation
        # In a real system, you'd use:
        # 1. Camera intrinsic matrix from camera_info topic
        # 2. Depth information from depth camera or stereo vision
        # 3. TF transforms to convert to robot base frame

        # Placeholder implementation - replace with actual calibration
        x = (u - 320) * 0.001  # Adjust based on your camera calibration
        y = (v - 240) * 0.001  # Adjust based on your camera calibration
        z = 0.5  # Placeholder depth - use actual depth data

        # Create PoseStamped message
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = camera_frame
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.w = 1.0  # No rotation for simplicity

        return pose
```

## Motion Planning Module

Now we'll implement the motion planning component using MoveIt2:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from moveit_msgs.srv import GetMotionPlan
from moveit_msgs.msg import MotionPlanRequest, Constraints
from moveit_msgs.msg import PositionConstraint, OrientationConstraint
from shape_msgs.msg import SolidPrimitive
from std_msgs.msg import Header
from tf2_ros import TransformListener, Buffer
import tf2_geometry_msgs
import numpy as np

class MotionPlanner(Node):
    def __init__(self):
        super().__init__('motion_planner')

        # Subscribe to detected object pose
        self.object_sub = self.create_subscription(
            PoseStamped,
            '/detected_object_pose',
            self.object_pose_callback,
            10
        )

        # TF buffer for coordinate transformations
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # MoveIt2 motion planning client
        self.motion_plan_cli = self.create_client(
            GetMotionPlan,
            '/plan_kinematic_path'
        )

        # Publisher for planned trajectory
        self.trajectory_pub = self.create_publisher(
            JointTrajectory,
            '/planned_trajectory',
            10
        )

        # Parameters
        self.declare_parameter('robot_group', 'manipulator')
        self.declare_parameter('end_effector_link', 'ee_link')
        self.declare_parameter('approach_distance', 0.05)  # 5cm before target

    def object_pose_callback(self, msg):
        """Plan motion to reach the detected object"""
        try:
            # Transform object pose to robot base frame
            target_pose = self.transform_pose_to_base_frame(msg)

            # Plan motion to approach the object
            self.plan_motion_to_object(target_pose)

        except Exception as e:
            self.get_logger().error(f'Error in motion planning: {e}')

    def transform_pose_to_base_frame(self, pose_stamped):
        """Transform pose to robot base frame"""
        try:
            # Wait for transform to be available
            self.tf_buffer.wait_for_transform_async(
                'base_link',  # Robot base frame
                pose_stamped.header.frame_id,
                rclpy.time.Time()
            )

            # Transform the pose
            transformed_pose = self.tf_buffer.transform(
                pose_stamped,
                'base_link'
            )

            return transformed_pose

        except Exception as e:
            self.get_logger().error(f'Could not transform pose: {e}')
            return pose_stamped  # Return original if transform fails

    def plan_motion_to_object(self, target_pose):
        """Plan motion to reach the target object"""
        # Add approach offset to avoid collision
        approach_pose = PoseStamped()
        approach_pose.header = target_pose.header

        # Calculate approach direction (from current to target)
        # For simplicity, approach from above
        approach_pose.pose.position.x = target_pose.pose.position.x
        approach_pose.pose.position.y = target_pose.pose.position.y
        approach_pose.pose.position.z = target_pose.pose.position.z + 0.1  # 10cm above target

        # Copy orientation
        approach_pose.pose.orientation = target_pose.pose.orientation

        # Create motion planning request
        request = MotionPlanRequest()
        request.workspace_parameters.header.frame_id = 'base_link'
        request.workspace_parameters.min_corner.x = -1.0
        request.workspace_parameters.min_corner.y = -1.0
        request.workspace_parameters.min_corner.z = -1.0
        request.workspace_parameters.max_corner.x = 1.0
        request.workspace_parameters.max_corner.y = 1.0
        request.workspace_parameters.max_corner.z = 1.0

        # Set start state (current robot state)
        # This would typically come from joint state or robot state topic
        # For now, we'll use a placeholder
        request.start_state = RobotState()  # Placeholder

        # Set goal constraints
        goal_constraints = Constraints()

        # Position constraint
        pos_constraint = PositionConstraint()
        pos_constraint.header = approach_pose.header
        pos_constraint.link_name = self.get_parameter('end_effector_link').value

        # Define the target region as a sphere around the target
        sphere = SolidPrimitive()
        sphere.type = SolidPrimitive.SPHERE
        sphere.dimensions = [0.02]  # 2cm tolerance
        pos_constraint.constraint_region.primitives.append(sphere)

        # Position offset
        pos_constraint.constraint_region.primitive_poses.append(approach_pose.pose)
        pos_constraint.weight = 1.0

        goal_constraints.position_constraints.append(pos_constraint)

        # Orientation constraint
        orient_constraint = OrientationConstraint()
        orient_constraint.header = approach_pose.header
        orient_constraint.link_name = self.get_parameter('end_effector_link').value
        orient_constraint.orientation = approach_pose.pose.orientation
        orient_constraint.absolute_x_axis_tolerance = 0.1
        orient_constraint.absolute_y_axis_tolerance = 0.1
        orient_constraint.absolute_z_axis_tolerance = 0.1
        orient_constraint.weight = 1.0

        goal_constraints.orientation_constraints.append(orient_constraint)

        request.goal_constraints.append(goal_constraints)

        # Set planning parameters
        request.group_name = self.get_parameter('robot_group').value
        request.num_planning_attempts = 10
        request.allowed_planning_time = 5.0
        request.max_velocity_scaling_factor = 0.5
        request.max_acceleration_scaling_factor = 0.5

        # Call motion planner service
        if self.motion_plan_cli.wait_for_service(timeout_sec=1.0):
            future = self.motion_plan_cli.call_async(
                GetMotionPlan.Request(motion_plan_request=request)
            )
            future.add_done_callback(self.motion_plan_callback)
        else:
            self.get_logger().error('Motion planning service not available')

    def motion_plan_callback(self, future):
        """Handle motion planning response"""
        try:
            response = future.result()

            if response.motion_plan_response.error_code.val == 1:  # SUCCESS
                # Publish the planned trajectory
                trajectory = response.motion_plan_response.trajectory.joint_trajectory
                self.trajectory_pub.publish(trajectory)

                self.get_logger().info('Motion plan successful')
            else:
                self.get_logger().error(
                    f'Motion planning failed: {response.motion_plan_response.error_code}'
                )

        except Exception as e:
            self.get_logger().error(f'Error in motion plan callback: {e}')
```

## Trajectory Execution Module

Finally, we'll implement the trajectory execution component:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from builtin_interfaces.msg import Duration
import time

class TrajectoryExecutor(Node):
    def __init__(self):
        super().__init__('trajectory_executor')

        # Subscribe to planned trajectory
        self.trajectory_sub = self.create_subscription(
            JointTrajectory,
            '/planned_trajectory',
            self.trajectory_callback,
            10
        )

        # Action client for trajectory execution
        self.trajectory_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )

        # Parameters
        self.declare_parameter('execution_timeout', 30.0)

    def trajectory_callback(self, msg):
        """Execute the received trajectory"""
        self.get_logger().info('Received trajectory for execution')

        # Wait for action server
        if not self.trajectory_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Trajectory execution server not available')
            return

        # Create goal
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = msg

        # Send goal
        self.get_logger().info('Sending trajectory to controller')
        future = self.trajectory_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Trajectory goal rejected')
            return

        self.get_logger().info('Trajectory goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle result of trajectory execution"""
        result = future.result().result
        if result.error_code == 0:  # SUCCESS
            self.get_logger().info('Trajectory executed successfully')
        else:
            self.get_logger().error(f'Trajectory execution failed: {result.error_code}')

    def feedback_callback(self, feedback_msg):
        """Handle trajectory execution feedback"""
        feedback = feedback_msg.feedback
        # Log progress or handle feedback as needed
        self.get_logger().debug(f'Trajectory progress: {feedback}')
```

## Complete System Integration

To tie everything together, we create a main node that coordinates the three modules:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory
import threading
import time

class ObjectReachingSystem(Node):
    def __init__(self):
        super().__init__('object_reaching_system')

        # Initialize the three modules
        self.object_detector = ObjectDetector()
        self.motion_planner = MotionPlanner()
        self.trajectory_executor = TrajectoryExecutor()

        # Publisher to signal system readiness
        self.ready_pub = self.create_publisher(Bool, '/system_ready', 10)

        # Timer to publish readiness status
        self.timer = self.create_timer(1.0, self.publish_readiness)

        self.get_logger().info('Object Reaching System initialized')

    def publish_readiness(self):
        """Publish system readiness status"""
        msg = Bool()
        msg.data = True  # System is ready
        self.ready_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    # Create the main system node
    system = ObjectReachingSystem()

    try:
        rclpy.spin(system)
    except KeyboardInterrupt:
        system.get_logger().info('Shutting down Object Reaching System')
    finally:
        system.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Launch File

Create a launch file to start all components:

```python
# launch/object_reaching_system.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'
        ),

        # Object detector node
        Node(
            package='object_reaching',
            executable='object_detector',
            name='object_detector',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'object_color_lower': [0, 100, 100]},
                {'object_color_upper': [10, 255, 255]},
                {'min_object_area': 1000}
            ],
            output='screen'
        ),

        # Motion planner node
        Node(
            package='object_reaching',
            executable='motion_planner',
            name='motion_planner',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'robot_group': 'manipulator'},
                {'end_effector_link': 'ee_link'},
                {'approach_distance': 0.05}
            ],
            output='screen'
        ),

        # Trajectory executor node
        Node(
            package='object_reaching',
            executable='trajectory_executor',
            name='trajectory_executor',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'execution_timeout': 30.0}
            ],
            output='screen'
        ),

        # Main system coordinator
        Node(
            package='object_reaching',
            executable='object_reaching_system',
            name='object_reaching_system',
            parameters=[
                {'use_sim_time': use_sim_time}
            ],
            output='screen'
        )
    ])
```

## Testing and Validation

### Simulation Testing

Before testing on real hardware, validate the system in simulation:

1. **Gazebo Simulation**: Use Gazebo with a robot model and objects
2. **RViz Visualization**: Monitor TF transforms and planning results
3. **RQT Tools**: Monitor topics and debug parameters

### Safety Considerations

When deploying on real hardware:

1. **Workspace Limits**: Define safe operational boundaries
2. **Collision Checking**: Verify trajectory safety
3. **Emergency Stop**: Implement safety stop mechanisms
4. **Velocity Limits**: Ensure smooth, controlled motions

## Extensions and Improvements

### Advanced Object Detection
- Use deep learning models (YOLO, Detectron2) for better detection
- Implement 6-DOF pose estimation using libraries like PyPose
- Add object recognition for specific objects

### Enhanced Motion Planning
- Implement Cartesian path planning for more natural motions
- Add collision avoidance with dynamic obstacles
- Implement compliant control for safe interaction

### Learning-Based Approaches
- Reinforcement learning for improved reaching strategies
- Imitation learning from human demonstrations
- Few-shot learning for new objects

This capstone project demonstrates the integration of computer vision, motion planning, and robot control in a practical application, showcasing how multiple concepts from this textbook work together to create an intelligent robotic system.