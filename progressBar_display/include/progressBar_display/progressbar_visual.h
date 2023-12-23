#ifndef PROGRESSBAR_VISUAL_H
#define PROGRESSBAR_VISUAL_H

#include <OGRE/OgreVector3.h>
#include <OGRE/OgreSceneNode.h>
#include <OGRE/OgreSceneManager.h>
#include <OGRE/OgreBillboard.h>
#include <OGRE/OgreBillboardSet.h>
#include <rviz/properties/string_property.h>
#include <rviz/ogre_helpers/movable_text.h>
#include <rviz/ogre_helpers/shape.h>
#include <rviz/display_context.h>

#include "plugin_msg/ProgressBarMsg.h"

namespace Ogre
{
    class Vector3;
    class Quaternion;
    class BillboardSet;
    class SceneManager;
    class SceneNode;
    class ColourValue;
}

namespace rviz
{
    class MovableText;
    class Shape;
    class IntProperty;
}

namespace progressBar_plugin {

class ProgressBar_Visual
{
public:
    ProgressBar_Visual(Ogre::SceneManager* SceneManager, Ogre::SceneNode* ParentNode);

    virtual ~ProgressBar_Visual();

    void setMessage(const plugin_msg::ProgressBarMsg::ConstPtr& Msg);
    void createProgressBarShape(double PowerRatio);

    void setFramePosition(const Ogre::Vector3& Position);
    void setFrameOrientation(const Ogre::Quaternion& Orientation);

    void setTextColor(const Ogre::ColourValue& Color);
    void setTextColor(float Red, float Green, float Blue, float Alpha);
    void setBackgroundColor(float Red, float Green, float Blue, float Alpha);
    void setProgressBarColor(float Red, float Green, float Blue, float Alpha);
    void setHeaderColor(float Red, float Green, float Blue, float Alpha);

    void setTextSize(float Size);
    void setGraphSize(float Size);

    void setOffsets(const Ogre::Vector3& Offsets);
    void setOrientation(const Ogre::Vector3& Orientation);

private:
    float size_{ 1.0 };
    std::shared_ptr<Ogre::Vector3> base_pose_{ nullptr };
    std::shared_ptr<Ogre::Vector3> offsets_{ nullptr };
    std::shared_ptr<Ogre::Vector3> orientation_{ nullptr };
    // the object implementing the actual text
    std::shared_ptr<rviz::MovableText> progressBar_info_{ nullptr };
    // the object of ProgressBar shape
    std::vector<std::shared_ptr<rviz::Shape>> ProgressBar_shape_;

    // a SceneNode whose pose is set to match the coordinate frame of the plugin_msg::ProgressBarMsg message header
    Ogre::SceneNode* frame_node_{ nullptr };

    // the SceneManager, kept here only so the destructor can ask it to destroy the `frame_node_`
    Ogre::SceneManager* scene_manager_{ nullptr };

    Ogre::ColourValue background_color;
    Ogre::ColourValue ProgressBar_color;
    Ogre::ColourValue header_color;
};

}


#endif // PROGRESSBAR_VISUAL_H
