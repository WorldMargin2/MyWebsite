

$(document).ready(function() {

let tmp_w = 0;
let tmp_h = 0;
let tmp_w_center = 0;
let tmp_h_center = 0;
let scale;
let tmp_clock_h=0;

$(document).on("scroll", function() {
    const title = $("#title");
    const vh=window.innerHeight;
    const vw =window.innerWidth; // 获取窗口宽度
    const s_t = $(this).scrollTop(); // 获取滚动条位置

    if (title.attr("changed") === "false") {
        title.attr("changed", "true");
        title.css("width", "max-content");
        title.css("height", "max-content");
        tmp_w = title.width();
        tmp_h = title.height();
        tmp_clock_h= $("#clock").height();
    }

    tmp_w_center = vw / 2 - tmp_w / 2;
    tmp_h_center = vh / 2 - tmp_h / 2;

    scale=(1-(s_t/vh));

    changed_left = scale > 0 ? tmp_w_center * scale : 0;
    if(tmp_w*scale<=vw){
        changed_left=scale > 0 ? changed_left*scale  : 0;
    }
    title.css("left", changed_left+"px");


    changed_top = tmp_h_center*scale;
    changed_top = changed_top > 0 ? changed_top : 0;
    title.css("top", changed_top+"px");

    changed_font_size = 75*scale;
    changed_font_size = changed_font_size > 30 ? changed_font_size : 30;
    title.css("font-size", changed_font_size+"px");
    title.css("line-height", changed_font_size + "px");
    container=$("#container");
    container_h=vh*scale;
    container_h=container_h>35?container_h:35;
    container.css("height",container_h+"px");
    if(container_h<=37){
        container.css("background-color","rgb(3,3,3)");
    }else{
        container.css("background-color","transparent")
    }


    clock_height=tmp_clock_h*scale > 30 ? tmp_clock_h*scale : 30;
    clock=$("#clock");
    clock.css("--clock-height", clock_height+"px");

});

});
