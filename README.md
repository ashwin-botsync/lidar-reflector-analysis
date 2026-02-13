# LiDAR Reflective Marker Analysis

This repository documents two tasks related to identifying reflective markers using LiDAR data.

---

## Task 1: Reflective Marker Identification using ROS

### Objective
To identify reflective markers from LiDAR point cloud data recorded in a ROS bag file by filtering high-intensity points.

### Data
- ROS1 bag file containing `sensor_msgs/PointCloud2`
- LiDAR intensity channel available

### Method
1. Played the ROS bag using `rosbag play`
2. Subscribed to the LiDAR point cloud topic
3. Extracted intensity values from `PointCloud2`
4. Applied intensity thresholding to filter high-intensity points
5. Published filtered points on a new ROS topic
6. Visualized filtered points in RViz
7. Adjusted intensity threshold dynamically for analysis

### Outcome
High-intensity LiDAR returns corresponding to reflective markers were successfully isolated and visualized in RViz.

---

## Task 2: Reflective Marker Identification using CloudCompare

### Objective
To visually analyze and isolate reflective markers using CloudCompare without ROS.

### Tools
- CloudCompare (Windows)

### Method
1. Loaded PCD file in CloudCompare
2. Activated intensity scalar field
3. Visualized point cloud colored by intensity
4. Applied intensity-based filtering to isolate reflective points

### Outcome
Reflective markers were clearly identified as high-intensity points at specific heights, confirming their physical placement in the warehouse.

---

## Notes
- Intensity threshold values depend on the LiDAR sensor and environment
- Visual validation is necessary when selecting thresholds
