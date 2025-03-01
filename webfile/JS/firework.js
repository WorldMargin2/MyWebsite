const args_template = {
    ctx: null,                  //canvas上下文(canvas context)
    color: "black",             //粒子颜色(particle color)
    color_random: false,        //是否启用随机颜色(random color)
    frameRate: 60,              //帧率(frame rate)

    life_time: 2 ,              // 发射时长(life time of launch)
    explode_time: 1 ,           // 爆炸(life time of explode) 
                                // 完整生命周期(the life time of complete)= (life_time + explode_time + ( wake_particles/frameRate ))s 
    wake_particles: 20,         // 尾迹数量(number of wake particles)
    explode_particles: 100,     // 爆炸后产生的粒子数量(number of particles after explode)
    angle: 90,                  // 发射角度(angle of launch)
    speed: 2,                   // 发射速度(speed of launch)
    gravity: 1,                 // 重力(gravity)
    x: 0,                       // 发射点x坐标(x coordinate of launch point)
    y: 0,                       // 发射点y坐标(y coordinate of launch point)
    life_time_callback: null,   // 发射结束回调(callback when launch is over)
    radius: 1                   // 粒子半径(radius of particle)
};

class Particle {
    wakes = []; // [x, y]
    now_life = 0;
    constructor(arg={},type="e"? "e":"l") {// e:爆炸 l:发射
        this.arg = arg;
        this.life_time = type=="l"? arg.life_time:arg.explode_time;
        this.type = type;
    };
    update() {
        if (this.now_life >= (this.life_time * this.arg.frameRate)) {
            if ((this.arg.life_time_callback)&&(this.type == "l")) {
                this.arg.life_time_callback(this.arg.x, this.arg.y);
            };
            if(this.type == "e") {
                this.ease_out();
            };
            return;
        };
        let vx = Math.cos(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        let vy = Math.sin(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        vy -= this.arg.gravity/this.arg.frameRate;
        this.arg.angle = Math.atan2(vy, vx) * 180 / Math.PI;
        this.arg.speed = Math.sqrt(vx * vx + vy * vy);
        vx /= this.arg.frameRate;
        vy /= this.arg.frameRate;
        this.arg.x += vx;
        this.arg.y += vy;
        this.now_life++;
        this.wakes.push([this.arg.x, this.arg.y]);
        if (this.wakes.length > this.arg.wake_particles) {
            this.wakes.shift();
        };
        this.draw();
    };
    draw() {
        let ctx = this.arg.ctx;
        ctx.beginPath();
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        for (let i = 1; i < this.wakes.length; i++) {
            ctx.moveTo(this.wakes[i][0], this.wakes[i][1]);
            ctx.arc(this.wakes[i][0], this.wakes[i][1],this.arg.radius*(i / this.wakes.length),0,2*Math.PI);
        };
        ctx.fillStyle = this.arg.color; 
        ctx.fill();
        ctx.closePath();
    };
    ease_out() {
        let vx = Math.cos(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        let vy = Math.sin(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        vy -= this.arg.gravity/this.arg.frameRate;
        this.arg.angle = Math.atan2(vy, vx) * 180 / Math.PI;
        this.arg.speed = Math.sqrt(vx * vx + vy * vy);
        vx /= this.arg.frameRate;
        vy /= this.arg.frameRate;
        this.arg.x += vx;
        this.arg.y += vy;
        if(this.wakes.length == 0) {
            if (this.arg.life_time_callback) {
                this.arg.life_time_callback(this.arg.x, this.arg.y);
            };
            return;
        };
        this.wakes.push([this.arg.x, this.arg.y]);
        this.wakes.shift();
        this.wakes.shift();
        this.draw();
    };
};

class Firework {
    particles = [];
    ease_out_ = [];
    now_life = 0;
    wakes = [];
    constructor(arg,end_callback) {
        this.arg = arg;
        this.end_callback = end_callback;
    };
    update() {
        if (this.now_life == 0) {
            this.now_life++;
            let arg = { ...this.arg };
            arg.life_time_callback = (x,y)=> {
                this.explode(x,y);
            };
            this.particles.push(new Particle(arg,"l"));
        };
        for (let i = 0; i < this.particles.length; i++) {
            this.particles[i].update();
        };
    };
    explode(x,y) {
        this.particles = [];
        for (let i = 0; i < this.arg.explode_particles; i++) {
            let arg = { ...this.arg };
            if (i == 0) {
                arg.life_time_callback = ()=>{ this.particles = []; this.end_callback(this); };
            };
            let angle = (360 / this.arg.explode_particles)*i + Math.random() * 2;
            arg.angle = angle;
            arg.speed = this.arg.speed*(Math.random()*(Math.random() +0.8) );
            arg.x = x;
            arg.y = y;
            if (this.arg.color_random) {
                arg.color = `rgb(${Math.random() * 255},${Math.random() * 255},${Math.random() * 255})`;
            } else {
                arg.color = this.arg.color;
            };
            this.particles.push(new Particle(arg,"e"));
        };
    };
};

class FireworkCanvas {
    #started = false;
    #auto_resize = false;
    #fireworks = [];
    #width = 0;
    #height = 0;
    #ctx = null;
    #interval = null;
    #max_fireworks = 0;
    #args = {};
    constructor(ctx, width, height,  max_fireworks = 10,args = {}) {
        this.#ctx = ctx;
        this.#width = width;
        this.#height = height;
        this.#max_fireworks = max_fireworks; // 最大并行更新烟花数量
        this.#args = {...args_template,...args};
    };

    addFirework(arg) {
        if(!this.#started) {
            return;
        };
        arg = { ...this.#args, ...arg };
        this.#fireworks.push(new Firework(arg,(firework) => {
            this.#fireworks.splice(this.#fireworks.indexOf(firework), 1);
        }));
    };

    addRandomFirework() {
        let arg = {};
        arg.ctx = this.#ctx;
        arg.x = Math.random() * this.#width;
        arg.color = `rgb(${Math.random() * 255},${Math.random() * 255},${Math.random() * 255})`;
        this.addFirework(arg);
    };

    is_running() {
        return (this.#started==true);
    };

    #mainLoop() {
        if(!this.#started) {
            return;
        };
        this.#ctx.clearRect(0, 0, this.#width, this.#height);
        for (let i = 0; i < this.#fireworks.length; i++) {
            this.#fireworks[i].update();
        };
        if (this.#fireworks.length > this.#max_fireworks*2) {
            this.#fireworks = this.#fireworks.slice(0, this.#max_fireworks);
        };
    };

    start() {
        if (this.#started) {
            return;
        };
        this.#started = true;
        this.#interval = setInterval(()=> {
            this.#mainLoop(this);
        }, 1000 / this.#args.frameRate);
    };

    stop() {
        if (!this.#started) {
            return;
        };
        clearInterval(this.#interval);
        this.#started = false;
    };

    updateSize(canvas,element) {
        this.#width = element.innerWidth;
        this.#height = element.innerHeight;
        canvas.width = element.innerWidth;
        canvas.height = element.innerHeight;
        this.#ctx.setTransform(1,0,0,-1,0,canvas.height);
    };

    autoResize(canvas,element=window) {
        if(this.#auto_resize) {
            return;
        }
        this.#auto_resize = true;
        window.addEventListener('resize',()=>{
            this.updateSize(canvas,element);
        } );
    };

    stopAutoResize() {
        if(!this.#auto_resize) {
            return;
        }
        this.#auto_resize = false;
        window.removeEventListener('resize',()=>{
            this.updateSize(canvas,element);
        } );
    };

    setArgs(arg) {
        this.#args = { ...this.#args, ...arg };
    }

    setMaxFireworks(max) {
        this.#max_fireworks = max;
    }
};

