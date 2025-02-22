//翻页式时钟，翻页(.show_num)

const hour = {
    time: 0,
    update: function() {
        now_time = new Date();
        this.time = now_time.getHours();
        this.show();
    },show: function() {
        //4个元素分，ele1,ele2用于存储上一秒的上下两半;ele3,ele4存储下一秒的上下两半;ele2和ele3背面相靠，背面不可见
        var $time=this.time<10?"0"+this.time:this.time;
        const ele1=$("#hour .ele1");
        const ele2=$("#hour .ele2");
        const ele3=$("#hour .ele3");
        const ele4=$("#hour .ele4");
        ele3.text($time);
        ele4.text($time);
        ele2.addClass("show_back");
        ele3.addClass("show_back");
        setTimeout(function(){
            ele1.text($time);
            ele2.text($time);
            ele2.removeClass("show_back");
            ele3.removeClass("show_back");
        },500);
    }
};
const minute = {
    time: 0,
    update: function() {
        now_time = new Date();
        this.time = now_time.getMinutes();
        this.show();
        if(this.time==0){
            hour.update();
        }
    },show: function() {
        var $time=this.time<10?"0"+this.time:this.time;
        const ele1=$("#minute .ele1");
        const ele2=$("#minute .ele2");
        const ele3=$("#minute .ele3");
        const ele4=$("#minute .ele4");
        ele3.text($time);
        ele4.text($time);
        ele2.addClass("show_back");
        ele3.addClass("show_back");
        setTimeout(function(){
            ele1.text($time);
            ele2.text($time);
            ele2.removeClass("show_back");
            ele3.removeClass("show_back");
        },500);
    }
};
const second = {
    time: 0,
    update: function() {
        now_time = new Date();
        this.time = now_time.getSeconds();
        this.show();
        if(this.time==0){
            minute.update();
        }
    },show: function() {
        //保留两位数
        var $time=this.time<10?"0"+this.time:this.time;
        const ele1=$("#second .ele1");
        const ele2=$("#second .ele2");
        const ele3=$("#second .ele3");
        const ele4=$("#second .ele4");
        ele3.text($time);
        ele4.text($time);
        ele2.addClass("show_back");
        ele3.addClass("show_back");
        setTimeout(function(){
            ele1.text($time);
            ele2.text($time);
            ele2.removeClass("show_back");
            ele3.removeClass("show_back");
        },500);
    }
};

$(function(){
    // 获取当前毫秒数，计算距离下一秒的毫秒数timeout，延迟执行,设置定时器，每秒更新一次
    var now_time = new Date();
    var timeout = 1000 - now_time.getMilliseconds();
    setTimeout(function(){
        setInterval(function(){
            second.update();
        },1000);
        second.update();
        minute.update();
        hour.update();
    },timeout);
    $(window).on("visibilitychange",function(){
        second.update();
        minute.update();
        hour.update();
    });
})

