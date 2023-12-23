#include "progressBar_display/progressbar_visual.h"

namespace progressBar_plugin
{

ProgressBar_Visual::ProgressBar_Visual(Ogre::SceneManager *SceneManager, Ogre::SceneNode *ParentNode)
{
    scene_manager_ = SceneManager;

    frame_node_ = ParentNode->createChildSceneNode();

    progressBar_info_.reset(new rviz::MovableText("?\%"));
    progressBar_info_->setCharacterHeight(0.5);
    frame_node_->attachObject(progressBar_info_.get());

    //create shape of ProgressBar
    base_pose_ = std::make_shared<Ogre::Vector3>(Ogre::Vector3::ZERO);
    offsets_ = std::make_shared<Ogre::Vector3>(Ogre::Vector3::ZERO);
    orientation_ = std::make_shared<Ogre::Vector3>(Ogre::Vector3(float(0.0), float(90.0), float(0.0)));

    background_color = Ogre::ColourValue(1, 0.5, 0.5, 0.5);
    ProgressBar_color = Ogre::ColourValue(1, 1, 0.5, 1);
    header_color = Ogre::ColourValue(0.5, 1, 1, 1);
    createProgressBarShape(1.0);
}

ProgressBar_Visual::~ProgressBar_Visual()
{
    scene_manager_->destroySceneNode(frame_node_);
}

void ProgressBar_Visual::setMessage(const plugin_msg::ProgressBarMsg::ConstPtr &Msg)
{
    int h = 0;
    int v = 0;
    progressBar_info_->setTextAlignment((rviz::MovableText::HorizontalAlignment)h, (rviz::MovableText::VerticalAlignment)v);
    rviz::StringProperty text("text", (std::to_string(Msg->value) + "\%").c_str());
    progressBar_info_->setCaption(text.getStdString());
    progressBar_info_->setLineSpacing(0.5);
}

void ProgressBar_Visual::createProgressBarShape(double PowerRatio)
{
    for (auto& it : ProgressBar_shape_)
    {
        it.reset();
    }
    ProgressBar_shape_.clear();
    ProgressBar_shape_.resize(3);

    Ogre::Matrix3 mat;
    mat.FromEulerAnglesXYZ(Ogre::Degree(orientation_->x), Ogre::Degree(orientation_->y), Ogre::Degree(orientation_->z));
    Ogre::Quaternion orientation;
    orientation.FromRotationMatrix(mat);

    //background
    ProgressBar_shape_[0].reset(new rviz::Shape(rviz::Shape::Cylinder,scene_manager_));
    ProgressBar_shape_[0]->setScale(Ogre::Vector3(float(0.5 * size_),float(3 * size_),float(0.5 * size_)));
    ProgressBar_shape_[0]->setPosition(Ogre::Vector3(base_pose_->x + offsets_->x,
                                                base_pose_->y + offsets_->y,
                                                base_pose_->z + offsets_->z));
    ProgressBar_shape_[0]->setOrientation(orientation);
    ProgressBar_shape_[0]->setColor(background_color);

    //ProgressBar
    float length = 2.8 * size_;
    //ProgressBar center pos
    Ogre::Vector3 ProgressBar_vec3(0.0,- float(0.5 * length *(1 - PowerRatio)),0.0);
    Ogre::Vector3 ProgressBar_pos = orientation * ProgressBar_vec3;
    ProgressBar_shape_[1].reset(new rviz::Shape(rviz::Shape::Cylinder,scene_manager_));
    ProgressBar_shape_[1]->setScale(Ogre::Vector3(float(0.3 * size_),length * PowerRatio,float(0.3 * size_)));
    ProgressBar_shape_[1]->setPosition(Ogre::Vector3(base_pose_->x + ProgressBar_pos.x + offsets_->x,
                                                base_pose_->y + ProgressBar_pos.y + offsets_->y,
                                                base_pose_->z + ProgressBar_pos.z + offsets_->z));
    ProgressBar_shape_[1]->setOrientation(orientation);
    ProgressBar_shape_[1]->setColor(ProgressBar_color);

    //header
    float head_length = 0.1 * size_ * 0.5;
    //header center pos
    Ogre::Vector3 head_vec3(0.0,- float(0.5 * length *(1 - 2 * PowerRatio)) + head_length * 0.5,0.0);
    Ogre::Vector3 head_pos = orientation * head_vec3;
    ProgressBar_shape_[2].reset(new rviz::Shape(rviz::Shape::Cube,scene_manager_));
    ProgressBar_shape_[2]->setScale(Ogre::Vector3(float(0.3 * size_),head_length,float(0.3 * size_)));
    ProgressBar_shape_[2]->setPosition(Ogre::Vector3(base_pose_->x + head_pos.x + offsets_->x,
                                                base_pose_->y + head_pos.y + offsets_->y,
                                                base_pose_->z + head_pos.z + offsets_->z));
    ProgressBar_shape_[2]->setOrientation(orientation);
    ProgressBar_shape_[2]->setColor(header_color);
}

void ProgressBar_Visual::setFramePosition(const Ogre::Vector3 &Position)
{
    *base_pose_ = Position;
    frame_node_->setPosition(Position);
}

void ProgressBar_Visual::setFrameOrientation(const Ogre::Quaternion &Orientation)
{
    frame_node_->setOrientation(Orientation);
}

void ProgressBar_Visual::setTextColor(const Ogre::ColourValue &Color)
{
    progressBar_info_->setColor(Color);
}

void ProgressBar_Visual::setTextColor(float Red, float Green, float Blue, float Alpha)
{
    setTextColor(Ogre::ColourValue(Red, Green, Blue, Alpha));
}

void ProgressBar_Visual::setBackgroundColor(float Red, float Green, float Blue, float Alpha)
{
    background_color = Ogre::ColourValue(Red, Green, Blue, Alpha);
}

void ProgressBar_Visual::setProgressBarColor(float Red, float Green, float Blue, float Alpha)
{
    ProgressBar_color = Ogre::ColourValue(Red, Green, Blue, Alpha);
}

void ProgressBar_Visual::setHeaderColor(float Red, float Green, float Blue, float Alpha)
{
    header_color = Ogre::ColourValue(Red, Green, Blue, Alpha);
}

void ProgressBar_Visual::setTextSize(float Size)
{
    progressBar_info_->setCharacterHeight(Size);
}

void ProgressBar_Visual::setGraphSize(float Size)
{
    size_ = Size;
}

void ProgressBar_Visual::setOffsets(const Ogre::Vector3 &Offsets)
{
    *offsets_ = Offsets;
    progressBar_info_->setLocalTranslation(Ogre::Vector3(-offsets_->y, offsets_->z, -offsets_->x));
}

void ProgressBar_Visual::setOrientation(const Ogre::Vector3 &Orientation)
{
    *orientation_ = Orientation;
}

}
