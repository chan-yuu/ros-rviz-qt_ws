#ifndef PANEL_WIDGET_H
#define PANEL_WIDGET_H

#include <QWidget>

namespace Ui {
class Panel_Widget;
}

namespace progressBar_panel {

class Panel_Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Panel_Widget(QWidget *parent = 0);
    ~Panel_Widget();

Q_SIGNALS:
    void sigToUpdateTopicAndProgressBarValue(QString topic,float value);

private:
    Ui::Panel_Widget *ui;
};

}

#endif // PANEL_WIDGET_H
