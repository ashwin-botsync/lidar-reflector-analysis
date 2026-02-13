#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Header, String
from dynamic_reconfigure.server import Server
from lidar_intensity_filter.cfg import IntensityFilterConfig


class IntensityFilterNode:
    def __init__(self):
        # Default threshold (will be overridden by rqt)
        self.threshold = 100.0

        # Publisher for filtered point cloud
        self.cloud_pub = rospy.Publisher(
            "/reflective_points_filtered",
            PointCloud2,
            queue_size=1
        )

        # Publisher for timestamp/debug info
        self.info_pub = rospy.Publisher(
            "/reflective_points_info",
            String,
            queue_size=10
        )

        # Subscriber to raw LiDAR point cloud
        rospy.Subscriber(
            "/mag_cb_004/lidar3d1/velodyne_points",
            PointCloud2,
            self.cloud_callback,
            queue_size=1
        )

        # Dynamic reconfigure server (rqt slider)
        self.server = Server(IntensityFilterConfig, self.reconfigure_callback)

    def reconfigure_callback(self, config, level):
        self.threshold = config.intensity_threshold
        rospy.loginfo(f"[IntensityFilter] Threshold updated: {self.threshold}")
        return config

    def cloud_callback(self, msg):
        filtered_points = []
        max_intensity = 0.0

        # Iterate over points in the cloud
        for x, y, z, intensity in pc2.read_points(
                msg,
                field_names=("x", "y", "z", "intensity"),
                skip_nans=True):

            if intensity >= self.threshold:
                filtered_points.append((x, y, z, intensity))
                if intensity > max_intensity:
                    max_intensity = intensity

        # If no reflective points found, do nothing
        if not filtered_points:
            return

        # Create filtered PointCloud2 message
        header = Header()
        header.stamp = msg.header.stamp      # BAG TIMESTAMP
        header.frame_id = msg.header.frame_id

        fields = [
            PointField("x", 0, PointField.FLOAT32, 1),
            PointField("y", 4, PointField.FLOAT32, 1),
            PointField("z", 8, PointField.FLOAT32, 1),
            PointField("intensity", 12, PointField.FLOAT32, 1),
        ]

        cloud_out = pc2.create_cloud(header, fields, filtered_points)
        self.cloud_pub.publish(cloud_out)

        # Publish timestamp + stats
        info_msg = String()
        info_msg.data = (
            f"time={msg.header.stamp.to_sec():.3f}, "
            f"count={len(filtered_points)}, "
            f"max_intensity={max_intensity:.1f}"
        )
        self.info_pub.publish(info_msg)


if __name__ == "__main__":
    rospy.init_node("lidar_intensity_filter")
    IntensityFilterNode()
    rospy.spin()
