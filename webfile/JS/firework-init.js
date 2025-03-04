

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
            gravity: 50,
            speed: 150,
            life_time: 2,
            explode_time: 2,
            explode_particles: 125,
            wake_particles: 60,
            radius: 2,
            color_random: false,
        }
    );
    let visiable = true;
    
    fireworks.setAutoCloseOrStart(() =>{visiable = true;},()=>{visiable = false;});
    fireworks.autoResize(canvas,window);
    fireworks.start();
    setInterval(() => {
        if(visiable){
            fireworks.addRandomFirework();
        }
    }, Math.random() * 1000 + 1000);
});
