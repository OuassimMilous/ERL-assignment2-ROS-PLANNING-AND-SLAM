from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():

    test_robot_description_share = FindPackageShare(package='autonomous_planner').find('autonomous_planner')
    slam_params_file_path = os.path.join(test_robot_description_share, 'params/mapper_params_online_sync.yaml')
    params_file_path = os.path.join(test_robot_description_share, 'params/nav2_params.yaml')

    # Paths to the launch files
    robot_urdf_launch_dir = os.path.join(
        FindPackageShare('robot_urdf').find('robot_urdf'), 'launch')
    slam_toolbox_launch_dir = os.path.join(
        FindPackageShare('slam_toolbox').find('slam_toolbox'), 'launch')
    nav2_bringup_launch_dir = os.path.join(
        FindPackageShare('nav2_bringup').find('nav2_bringup'), 'launch')

    # Include the robot_urdf launch file
    robot_urdf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(robot_urdf_launch_dir, 'gazebo2.launch.py'))
    )

    # Include the slam_toolbox launch file with parameters
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(slam_toolbox_launch_dir, 'online_sync_launch.py')),
        launch_arguments={'slam_params_file': slam_params_file_path}.items()
    )

    # Include the nav2_bringup launch file with parameters
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_launch_dir, 'navigation_launch.py')),
        launch_arguments={'params_file': params_file_path}.items()
    )

    # Plansys2 launch file
    plansys2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            FindPackageShare('plansys2_bringup').find('plansys2_bringup'),
            'launch',
            'plansys2_bringup_launch_monolithic.py'
        )),
        launch_arguments={'model_file': os.path.join(test_robot_description_share, 'pddl/patrol.pddl')}.items()
    )

# aruco
    aruco_node = Node(
        package='ros2_aruco',
        executable='aruco_node',
        name='aruco_node',
        output='screen'
    )

    move_action_node = Node(
        package='autonomous_planner',
        executable='move_action_node',
        name='move_action_node',
        output='screen',
        parameters=[]
    )
    
    scan_action_node = Node(
        package='autonomous_planner',
        executable='scan_marker_action_node',
        name='scan_marker_action_node',
        output='screen',
        parameters=[]
    )
    
    

    return LaunchDescription([
        robot_urdf_launch,
        slam_toolbox_launch,
        nav2_bringup_launch,
        plansys2_launch,
        move_action_node,
        scan_action_node,
        aruco_node
    ])
