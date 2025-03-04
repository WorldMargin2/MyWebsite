let fireworks;

$(document).ready(() => {
    let canvas = document.getElementById("background_canvas");
    let ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight
    ctx.setTransform(1, 0, 0, -1, 0, canvas.height);

    fireworks = new FireworkCanvas(ctx, canvas.width, canvas.height, 5,
        {
            gravity: 60,
            speed: 200,
            life_time: 3,
            explode_time: 2,
            explode_particles: 125,
            wake_particles: 60,
            radius: 1,
            color_random: false
        }
    );
    fireworks.updateSize(canvas,window);
    fireworks.autoResize(canvas,window);
    fireworks.setAutoCloseOrStart();
    fireworks.start();
    setInterval(() => {
            fireworks.addRandomFirework();
    }, Math.random() * 1000 + 1000);
});
