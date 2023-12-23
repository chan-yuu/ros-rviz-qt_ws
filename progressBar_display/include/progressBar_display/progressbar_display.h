#ifndef PROGRESSBAR_DISPLAY_H
#define PROGRESSBAR_DISPLAY_H

#ifndef Q_MOC_RUN
#include <boost/circular_buffer.hpp>

#include <rviz/message_filter_display.h>
#include <rviz/panel_dock_widget.h>

#include "plugin_msg/ProgressBarMsg.h"
#endif

namespace Ogre
{
    class SceneNode;
    class ColourValue;
}

namespace rviz
{
    class ColorProperty;
    class FloatProperty;
    class IntProperty;
    class VectorProperty;
    class BoolProperty;
    class StringProperty;
}

namespace progressBar_plugin {

class ProgressBar_Visual;

class ProgressBar_Display: public rviz::MessageFilterDisplay<plugin_msg::ProgressBarMsg>
{
    Q_OBJECT
public:
    ProgressBar_Display();
    virtual ~ProgressBar_Display();

protected:
    virtual void onInitialize();
    // a helper function to clear this display back to the initial state
    virtual void reset();

private Q_SLOTS:
    // these Qt slots get connected to signals indicating changes in the user-editable properties
    void updateTextColorAndAlpha();
    void updateBackgroundrColor();
    void updateProgressBarColor();
    void updateHeaderColor();
    void updateHistoryLength();
    void updateTextSize();
    void updateGraphSize();
    void updateOffsets();
    void updateOrientation();

private:
    // function to handle an incoming ROS message
    void processMessage(const plugin_msg::ProgressBarMsg::ConstPtr& Msg);

private:
    // storage for the list of visuals. It is a circular buffer,
    // where data gets popped from the front (oldest) and pushed to the back (newest)
    boost::circular_buffer<std::shared_ptr<ProgressBar_Visual>> visuals_;

    // user-editable property variables
    rviz::ColorProperty* text_color_property_;
    rviz::FloatProperty* text_alpha_property_;
    rviz::ColorProperty* background_color_property_;
    rviz::ColorProperty* progressBar_color_property_;
    rviz::ColorProperty* header_color_property_;
    rviz::IntProperty* history_length_property_;
    rviz::FloatProperty* text_size_property_;
    rviz::FloatProperty* graph_size_property_;
    rviz::VectorProperty* offsets_property_;
    rviz::VectorProperty* orientation_property_;

};

}


#endif // PROGRESSBAR_DISPLAY_H
