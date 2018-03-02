import numpy as np
import xml.etree.cElementTree as ET
import logging
import math

def parse_motions(path):
    xml_tree = ET.parse(path)
    xml_root = xml_tree.getroot()
    xml_motions = xml_root.findall('Motion')
    motions = []

    if len(xml_motions) > 1:
        logging.warn('more than one <Motion> tag in file "%s", only parsing the first one', path)
    motions.append(_parse_motion(xml_motions[0], path))
    return motions

def _parse_motion(xml_motion, path):
    xml_joint_order = xml_motion.find('JointOrder')
    if xml_joint_order is None:
        raise RuntimeError('<JointOrder> not found')

    joint_names = []
    joint_indexes = []
    for idx, xml_joint in enumerate(xml_joint_order.findall('Joint')):
        name = xml_joint.get('name')
        if name is None:
            raise RuntimeError('<Joint> has no name')
        joint_indexes.append(idx)
        joint_names.append(name)

    frames = []
    xml_frames = xml_motion.find('MotionFrames')
    if xml_frames is None:
        raise RuntimeError('<MotionFrames> not found')
    for xml_frame in xml_frames.findall('MotionFrame'):
        frames.append(_parse_frame(xml_frame, joint_indexes))

    return joint_names, frames
	

def _parse_frame(xml_frame, joint_indexes):
    n_joints = len(joint_indexes)
    xml_joint_pos = xml_frame.find('JointPosition')
    if xml_joint_pos is None:
        raise RuntimeError('<JointPosition> not found')
    joint_pos = _parse_list(xml_joint_pos, n_joints, joint_indexes)
    return joint_pos
	
def _parse_list(xml_elem, length, indexes=None):
    if indexes is None:
        indexes = range(length)
    elems = [float(x) for idx, x in enumerate(xml_elem.text.rstrip().split(' ')) if idx in indexes]
    if len(elems) != length:
        raise RuntimeError('invalid number of elements')
    return elems
	
def proccess (joint_pos):
	x=0
	print (len(joint_pos),len(joint_pos[1]))
	data= np.tile(0,(len(joint_pos),11) ).astype(int)

	for i in range(len(joint_pos)):
		x=0
		for j in [30,28,36,14,12,20]:
		#for j in [28,29,36,12,13,20]:
			data[i][x+3]=(joint_pos[i][j] * 180)/math.pi
			x+=1

	return (data)
		
if __name__ == '__main__':
	x=parse_motions('MMM.xml')
	print (proccess(x[0][1]))