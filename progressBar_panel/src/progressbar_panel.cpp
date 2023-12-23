#include "progressBar_panel/progressbar_panel.h"

#include <rviz/properties/bool_property.h>
#include <rviz/properties/float_property.h>
#include <rviz/properties/string_property.h>
#include <rviz/window_manager_interface.h>
#include <rviz/display_context.h>
#include <QVBoxLayout>
#include <QDebug>
#include <QDateTime>

namespace progressBar_panel
{

ProgressBar_Panel::ProgressBar_Panel(QWidget* parent): rviz::Panel( parent )
{
    panel_widget = new Panel_Widget;
    connect(panel_widget,&Panel_Widget::sigToUpdateTopicAndProgressBarValue,this,&ProgressBar_Panel::updateTopicAndProgressBarValue);
    QVBoxLayout* layout = new QVBoxLayout;
    layout->addWidget(panel_widget);
    setLayout(layout);
}

void ProgressBar_Panel::load(const rviz::Config &config)
{
    rviz::Panel::load( config );
}

void ProgressBar_Panel::save(rviz::Config config) const
{
    rviz::Panel::save( config );
}

void ProgressBar_Panel::updateTopicAndProgressBarValue(QString topic, float value)
{
    if( topic != output_topic_ )
    {
        output_topic_ = topic;
        // If the topic is the empty string, don't publish anything.
        if( output_topic_ == "" )
        {
            progressBar_publisher_.shutdown();
        }
        else
        {
            // The old ``velocity_publisher_`` is destroyed by this assignment,
            // and thus the old topic advertisement is removed.  The call to
            // nh_advertise() says we want to publish data on the new topic
            // name.
            progressBar_publisher_ = nh_.advertise<plugin_msg::ProgressBarMsg>( output_topic_.toStdString(), 1 );
        }
        // rviz::Panel defines the configChanged() signal.  Emitting it
        // tells RViz that something in this panel has changed that will
        // affect a saved config file.  Ultimately this signal can cause
        // QWidget::setWindowModified(true) to be called on the top-level
        // rviz::VisualizationFrame, which causes a little asterisk ("*")
        // to show in the window's title bar indicating unsaved changes.
        Q_EMIT configChanged();
    }


    if( ros::ok() && progressBar_publisher_ )
    {
        plugin_msg::ProgressBarMsg msg;
        msg.header.frame_id = "map";//output_topic_.toStdString();
        msg.header.stamp = ros::Time(QDateTime::currentSecsSinceEpoch());
        msg.value = value;
        progressBar_publisher_.publish( msg );
        //qDebug()<<"publisher msg";
    }

}

}

// 声明此类是一个rviz的插件
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(progressBar_panel::ProgressBar_Panel,rviz::Panel )
