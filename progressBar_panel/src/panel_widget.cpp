#include "progressBar_panel/panel_widget.h"
#include "ui_panel_widget.h"

namespace progressBar_panel {

Panel_Widget::Panel_Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Panel_Widget)
{
    ui->setupUi(this);

    connect(ui->topic_name,&QLineEdit::editingFinished,this,[=](){
        Q_EMIT sigToUpdateTopicAndProgressBarValue(ui->topic_name->text(),ui->progressBar_value->text().toFloat());
    });
    connect(ui->progressBar_value,&QLineEdit::editingFinished,this,[=](){
        Q_EMIT sigToUpdateTopicAndProgressBarValue(ui->topic_name->text(),ui->progressBar_value->text().toFloat());
    });
    connect(ui->pushButton_add,&QPushButton::clicked,this,[=](){
        ui->progressBar_value->setText(QString::number(ui->progressBar_value->text().toFloat() + 5));
        Q_EMIT sigToUpdateTopicAndProgressBarValue(ui->topic_name->text(),ui->progressBar_value->text().toFloat());
        if(ui->progressBar_value->text().toFloat() == 100)
            ui->progressBar_value->setText("0");
    });
}

Panel_Widget::~Panel_Widget()
{
    delete ui;
}

}
