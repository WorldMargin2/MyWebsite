const args_template = {
    ctx: null,
    color: "black",
    color_random: false,
    frameRate: 60,
    life_time: 2 ,
    explode_time: 1 , // 完整生命周期 = life_time + explode_time
    wake_particles: 20,
    explode_particles: 100, // 爆炸后产生的粒子数量
    angle: 90,
    speed: 2,
    gravity: 1,
    x: 0,
    y: 0,
    life_time_callback: null,
    radius: 1
};

class Particle {
    wakes = []; // [x, y]
    now_life = 0;
    constructor(arg) {
        this.arg = arg;
        this.life_time = arg.life_time;
    }
    update() {
        //计算执行时间
        if (this.now_life >= (this.life_time * this.arg.frameRate)) {
            if (this.arg.life_time_callback) {
                this.arg.life_time_callback(this.arg.x, this.arg.y);
            }
            return;
        }
        let vx = Math.cos(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        let vy = Math.sin(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        vy -= this.arg.gravity/this.arg.frameRate;
        this.arg.speed = Math.sqrt(vx * vx + vy * vy);
        this.arg.x += vx;
        this.arg.y += vy;
        vx /= this.arg.frameRate;
        vy /= this.arg.frameRate;
        this.arg.angle = Math.atan2(vy, vx) * 180 / Math.PI; // 使用 atan2 代替 atan
        this.now_life++;
        this.wakes.push([this.arg.x, this.arg.y]);
        if (this.wakes.length > this.arg.wake_particles) {
            this.wakes.shift();
        }
        this.draw();
    }
    draw() {
        let ctx = this.arg.ctx;
        ctx.beginPath();
        ctx.moveTo(this.wakes[0][0], this.wakes[0][1]);
        for (let i = 1; i < this.wakes.length; i++) {
            ctx.arc(this.wakes[i][0], this.wakes[i][1],this.arg.radius*(i / this.wakes.length),0,2*Math.PI);
        }
        ctx.fillStyle = this.arg.color; 
        ctx.fill();
        ctx.closePath();
    }
}

class Firework {
    particles = [];
    now_life = 0;
    wakes = [];
    constructor(arg,end_callback) {
        this.arg = arg;
        this.end_callback = end_callback;
    }
    update() {
        if (this.now_life == 0) {
            this.now_life++;
            let arg = { ...this.arg };
            let $this = this;
            arg.life_time_callback = function(x,y) {
                $this.explode(x,y);
            };
            this.particles.push(new Particle(arg));
        }
        for (let i = 0; i < this.particles.length; i++) {
            this.particles[i].update();
        }
    }
    explode(x,y) {
        this.particles = [];
        let $this = this;
        for (let i = 0; i < this.arg.explode_particles; i++) {
            let arg = { ...this.arg };
            if (i == 0) {
                arg.life_time_callback = ()=>{ $this.particles = []; $this.end_callback($this); };
            }
            arg.life_time = this.arg.explode_time;
            let angle = (360 / this.arg.explode_particles)*i + Math.random() * 2;
            arg.angle = angle;
            arg.speed = this.arg.speed*(Math.random()*(Math.random() +0.5) );
            arg.x = x;
            arg.y = y;
            if (this.arg.color_random) {
                arg.color = `rgb(${Math.random() * 255},${Math.random() * 255},${Math.random() * 255})`;
            } else {
                arg.color = this.arg.color;
            }
            this.particles.push(new Particle(arg));
        }
    }

}

class FireworkCanvas {
    fireworks = [];
    ctx = null;
    gravity = 0;
    frameRate = 60;
    interval = null;
    constructor(ctx, width, height, gravity = 0, frameRate = 60, max_fireworks = 10) {
        this.ctx = ctx;
        this.width = width;
        this.height = height;
        this.gravity = gravity;
        this.frameRate = frameRate;
        this.max_fireworks = max_fireworks; // 最大并行更新烟花数量
    }
    addFirework(arg) {
        this.fireworks.push(new Firework(arg,(firework) => {
            this.fireworks.splice(this.fireworks.indexOf(firework), 1);
        }));
    }
    addRandomFirework() {
        let arg = { ...args_template };
        arg.ctx = this.ctx;
        arg.x = Math.random() * this.width;
        arg.color = `rgb(${Math.random() * 255},${Math.random() * 255},${Math.random() * 255})`;
        this.addFirework(arg);
    }
    mainLoop($this) {
        $this.ctx.clearRect(0, 0, $this.width, $this.height);
        for (let i = 0; i < $this.fireworks.length; i++) {
            $this.fireworks[i].update();
        }
        if ($this.fireworks.length > $this.max_fireworks*2) {
            $this.fireworks = $this.fireworks.slice(0, $this.max_fireworks);
        }
    }
    start() {
        let $this = this;
        this.interval = setInterval(function() {
            $this.mainLoop($this);
        }, 1000 / this.frameRate);
    }
    stop() {
        clearInterval(this.interval);
    }
}

let fireworks;

$(document).ready(() => {
    let canvas = document.getElementById("background_canvas");
    let ctx = canvas.getContext("2d");
    ctx.setTransform(1, 0, 0, -1, 0, canvas.height);
    fireworks = new FireworkCanvas(ctx, canvas.width, canvas.height, 1, 60, 5);    
    fireworks.start();
    setInterval(() => {
        fireworks.addRandomFirework();
    }, 2000);
});
