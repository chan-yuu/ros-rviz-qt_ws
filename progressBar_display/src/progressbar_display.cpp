#include "progressBar_display/progressbar_display.h"
#include "progressBar_display/progressbar_visual.h"

#include <OGRE/OgreSceneNode.h>
#include <OGRE/OgreSceneManager.h>

#include <rviz/window_manager_interface.h>
#include <rviz/visualization_manager.h>
#include <rviz/properties/color_property.h>
#include <rviz/properties/float_property.h>
#include <rviz/properties/int_property.h>
#include <rviz/properties/vector_property.h>
#include <rviz/properties/bool_property.h>
#include <rviz/properties/string_property.h>
#include <pluginlib/class_list_macros.h>

namespace progressBar_plugin
{
ProgressBar_Display::ProgressBar_Display()
{
    text_color_property_ = new rviz::ColorProperty("Text Color", QColor(138, 226, 52),
                                                   "Color of progressBar info text.",
                                                   this, SLOT(updateTextColorAndAlpha()));

    text_alpha_property_ = new rviz::FloatProperty("Text Alpha", 1.0,
                                                    "0 is fully transparent, 1.0 is fully opaque.",
                                                   this, SLOT(updateTextColorAndAlpha()));

    text_size_property_ = new rviz::FloatProperty("Text Size", 0.5,
                                                  "Character size of progressBar info text.",
                                                  this, SLOT(updateTextSize()));

    background_color_property_ = new rviz::ColorProperty("Background Color", QColor(255,128,128),
                                                         "Color of progressBar background.",
                                                         this, SLOT(updateBackgroundrColor()));

    progressBar_color_property_ = new rviz::ColorProperty("ProgressBar Color", QColor(255,255,128),
                                                     "Color of progressBar.",
                                                     this, SLOT(updateProgressBarColor()));

    header_color_property_ = new rviz::ColorProperty("Header Color", QColor(128,255,255),
                                                     "Color of progressBar header.",
                                                     this, SLOT(updateHeaderColor()));

    graph_size_property_ = new rviz::FloatProperty("Graph Size", 1.0,
                                                   "Character size of progressBar graph.",
                                                   this, SLOT(updateGraphSize()));


    history_length_property_ = new rviz::IntProperty("History Length", 1,
                                                     "Number of prior measurements to display.",
                                                     this, SLOT(updateHistoryLength()));
    history_length_property_->setMin(1);
    history_length_property_->setMax(100000);

    offsets_property_ = new rviz::VectorProperty("Offsets", Ogre::Vector3::ZERO,
                                                 "Offsets to frame",
                                                 this, SLOT(updateOffsets()));

    orientation_property_ = new rviz::VectorProperty("Orientation", Ogre::Vector3(float(0.0), float(90.0), float(0.0)),
                                                     "Orientation of progressBar symbol",
                                                     this, SLOT(updateOrientation()));
}

ProgressBar_Display::~ProgressBar_Display()
{

}

// after the top-level rviz::Display::initialize() does its own setup,
// it calls the subclass's onInitialize() function
// this is where all the workings of the class is instantiated
// make sure to also call the immediate super-class's onInitialize() function,
// since it does important stuff setting up the message filter
//
// note that "MFDClass" is a typedef of `MessageFilterDisplay<message type>`,
// to save typing that long templated class name every time the superclass needs to be refered
void ProgressBar_Display::onInitialize()
{
    MFDClass::onInitialize();
    updateTextColorAndAlpha();
    updateHistoryLength();
    updateTextSize();
    updateGraphSize();
    updateOffsets();
    updateOrientation();
}

// clear the visuals by deleting their objects
void ProgressBar_Display::reset()
{
    MFDClass::reset();
    visuals_.clear();
}

// set the current color and alpha values for each visual
void ProgressBar_Display::updateTextColorAndAlpha()
{
    float alpha = text_alpha_property_->getFloat();
    Ogre::ColourValue color = text_color_property_->getOgreColor();

    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setTextColor(color.r, color.g, color.b, alpha);
    }
}

void ProgressBar_Display::updateBackgroundrColor()
{
    Ogre::ColourValue color = background_color_property_->getOgreColor();

    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setBackgroundColor(color.r, color.g, color.b, 0.5);
    }
}

void ProgressBar_Display::updateProgressBarColor()
{
    Ogre::ColourValue color = progressBar_color_property_->getOgreColor();

    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setProgressBarColor(color.r, color.g, color.b, 1);
    }
}

void ProgressBar_Display::updateHeaderColor()
{
    Ogre::ColourValue color = header_color_property_->getOgreColor();

    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setHeaderColor(color.r, color.g, color.b, 1);
    }
}

// set the number of past visuals to show
void ProgressBar_Display::updateHistoryLength()
{
    visuals_.rset_capacity(history_length_property_->getInt());
}

void ProgressBar_Display::updateTextSize()
{
    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setTextSize(text_size_property_->getFloat());
    }
}

void ProgressBar_Display::updateGraphSize()
{
    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setGraphSize(graph_size_property_->getFloat());
    }
}

void ProgressBar_Display::updateOffsets()
{
    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setOffsets(offsets_property_->getVector());
    }
}

void ProgressBar_Display::updateOrientation()
{
    for (size_t i = 0; i < visuals_.size(); ++i)
    {
        visuals_[i]->setOrientation(orientation_property_->getVector());
    }
}

void ProgressBar_Display::processMessage(const plugin_msg::ProgressBarMsg::ConstPtr& Msg)
{
    // call the rviz::FrameManager to get the transform from the fixed frame to the frame in the header of this progressBar message
    // if it fails, do nothing and return
    Ogre::Quaternion orientation;
    Ogre::Vector3 position;
    if (!context_->getFrameManager()->getTransform(Msg->header.frame_id,Msg->header.stamp, position, orientation))
    {
        ROS_DEBUG("error transforming from frame '%s' to frame '%s'",
                  Msg->header.frame_id.c_str(), qPrintable(fixed_frame_));
        return;
    }

    // keeping a circular buffer of visual pointers
    // this gets the next one, or creates and stores it if the buffer is not full
    std::shared_ptr<ProgressBar_Visual> visual;
    if (visuals_.full())
    {
        visual = visuals_.front();
    }
    else
    {
        visual.reset(new ProgressBar_Visual(context_->getSceneManager(), scene_node_));
    }

    // set or update the contents of the chosen visual
    float alpha = text_alpha_property_->getFloat();
    Ogre::ColourValue color = text_color_property_->getOgreColor();
    visual->setTextColor(color.r, color.g, color.b, alpha);

    color = background_color_property_->getOgreColor();
    visual->setBackgroundColor(color.r, color.g, color.b, 0.5);

    color = progressBar_color_property_->getOgreColor();
    visual->setProgressBarColor(color.r, color.g, color.b, 1);

    color = header_color_property_->getOgreColor();
    visual->setHeaderColor(color.r, color.g, color.b, 1);

    visual->createProgressBarShape(Msg->value / 100.0);
    visual->setMessage(Msg);
    visual->setFramePosition(position);
    visual->setFrameOrientation(orientation);

    // send it to the end of the circular buffer
    visuals_.push_back(visual);
}
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(progressBar_plugin::ProgressBar_Display, rviz::Display)

}
