#!/usr/bin/env python

import rospy
import rospkg
import xml.etree.ElementTree as ET
import argparse

def convert_urdf_paths(urdf_file):
    # Initialize the ROS Node
    rospy.init_node('urdf_path_converter')

    # Create an instance of the rospkg.RosPack class to locate packages
    rospack = rospkg.RosPack()

    # Parse the URDF file
    tree = ET.parse(urdf_file)
    root = tree.getroot()

    # Iterate through all <mesh> elements
    for mesh_elem in root.iter('mesh'):
        if 'filename' in mesh_elem.attrib:
            original_path = mesh_elem.attrib['filename']
            
            # Check if the path is package-relative
            if original_path.startswith('package://'):
                # Extract the package name and resource path
                package_name, resource_path = original_path[len('package://'):].split('/', 1)
                
                # Get the absolute path to the package
                package_path = rospack.get_path(package_name)
                
                # Build the absolute path to the resource
                absolute_path = package_path + '/' + resource_path
                
                # Update the <mesh> element with the absolute path
                mesh_elem.attrib['filename'] = absolute_path
                rospy.loginfo(f"Updated path: {original_path} -> {absolute_path}")

    # Save the modified URDF to a new file
    new_urdf_file = urdf_file.replace('.urdf', '_absolute_paths.urdf')
    tree.write(new_urdf_file)
    rospy.loginfo(f"Modified URDF saved as {new_urdf_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert package-relative URDF paths to absolute paths.')
    parser.add_argument('urdf_file', help='Path to the URDF file')
    args = parser.parse_args()
    
    urdf_file = args.urdf_file
    convert_urdf_paths(urdf_file)
