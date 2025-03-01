

$(document).ready(() => {
    let canvas = document.getElementById("background_canvas");
    let ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight
    ctx.setTransform(1, 0, 0, -1, 0, canvas.height);

    let fireworks = new FireworkCanvas(ctx, canvas.width, canvas.height, 3,
        {
            frameRate: 60,
            gravity: 30,
            speed: 125,
            life_time: 3,
            explode_time: 2,
            explode_particles: 75,
            wake_particles: 100,
            radius: 1.5
        }
    );
    var visiable = true;
    $(document).on("visibilitychange", function() {
        if (document.hidden) {
            fireworks.stop();
            visiable = false;
        } else {
            if (!visiable) {
                fireworks.start();
                visiable = true;
            };
        };
    });
    fireworks.autoResize(canvas,window);
    fireworks.start();
    setInterval(() => {
        if(visiable){
            fireworks.addRandomFirework();
        }
    }, Math.random() * 1000 + 1500);
});
