#ifndef PROGRESSBAR_PANEL_H
#define PROGRESSBAR_PANEL_H

#include <rviz/panel.h>
#include <ros/ros.h>
#include <rviz/panel.h>

#include "panel_widget.h"
#include "plugin_msg/ProgressBarMsg.h"

namespace progressBar_panel {

class ProgressBar_Panel: public rviz::Panel
{
public:
    ProgressBar_Panel(QWidget* parent = 0 );

    virtual void load( const rviz::Config& config );
    virtual void save( rviz::Config config ) const;

public Q_SLOTS:
    void updateTopicAndProgressBarValue(QString topic,float value);

private:
    Panel_Widget *panel_widget;

    // The current name of the output topic.
    QString output_topic_;

    // The ROS publisher for the command velocity.
    ros::Publisher progressBar_publisher_;

    // The ROS node handle.
    ros::NodeHandle nh_;
};

}

#endif // PROGRESSBAR_PANEL_H
