#include <ros/ros.h>
#include <nav_msgs/Path.h>
#include <geometry_msgs/Quaternion.h>
#include <geometry_msgs/PoseStamped.h>
#include <car_interfaces/GlobalPathPlanningInterface.h>

std::vector<double> x_list;
std::vector<double> y_list;

void planMapCallback(const car_interfaces::GlobalPathPlanningInterface::ConstPtr& msg)
{
    x_list.assign(msg->x_list.begin(), msg->x_list.end());
    y_list.assign(msg->y_list.begin(), msg->y_list.end());

    // 输出填充后的值
    std::cout << "x_list: ";
    for (const auto& x : x_list) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    std::cout << "y_list: ";
    for (const auto& y : y_list) {
        std::cout << y << " ";
    }
    std::cout << std::endl;
}

int main(int argc, char* argv[])
{
    ros::init(argc, argv, "by_path");

    ros::NodeHandle nh;
    ros::Publisher path_pub = nh.advertise<nav_msgs::Path>("trajectory", 1, true);
    ros::Subscriber plan_map_sub = nh.subscribe("/global_path_planning_data", 1, planMapCallback);

    ros::Rate loop_rate(1);
    while (ros::ok())
    {
        nav_msgs::Path path;
        path.header.stamp = ros::Time::now();
        path.header.frame_id = "/map";

        // Check if x_list and y_list have been populated
        if (!x_list.empty() && !y_list.empty() && x_list.size() == y_list.size())
        {
            // Populate poses with x_list and y_list
            for (size_t i = 0; i < x_list.size(); ++i)
            {
                geometry_msgs::PoseStamped pose_stamped;
                pose_stamped.header.stamp = ros::Time::now();
                pose_stamped.header.frame_id = "/map";

                // Set position
                pose_stamped.pose.position.x = x_list[i];
                pose_stamped.pose.position.y = y_list[i];
				
                pose_stamped.pose.position.z = 0.0;

                // Set orientation (no rotation)
                pose_stamped.pose.orientation.x = 0.0;
                pose_stamped.pose.orientation.y = 0.0;
                pose_stamped.pose.orientation.z = 0.0;
                pose_stamped.pose.orientation.w = 1.0;

                path.poses.push_back(pose_stamped);
            }

            path_pub.publish(path);
        }

        ros::spinOnce();  // Process callbacks
        loop_rate.sleep();
    }

    return 0;
}