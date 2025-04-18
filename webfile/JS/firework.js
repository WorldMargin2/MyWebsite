const args_template = {
    ctx: null,                  //canvas上下文(canvas context)
    color: "black",             //粒子颜色(particle color)
    color_random: false,        //是否启用随机颜色(random color)

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

    calculatePosition(delta) {
        let vx = Math.cos(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        let vy = Math.sin(this.arg.angle / 180 * Math.PI) * this.arg.speed;
        vy -= (this.arg.gravity*delta)/1000;
        this.arg.angle = Math.atan2(vy, vx) * 180 / Math.PI;
        this.arg.speed = Math.sqrt(vx * vx + vy * vy);
        this.arg.x += (vx*delta)/1000;
        this.arg.y += (vy*delta)/1000;
    }

    update(delta) {
        if (this.now_life >= (this.life_time * 1000)) {
            if(this.type == "e") {
                this.ease_out(delta);
            }else if (this.type == "l") {
                this.arg.life_time_callback?this.arg.life_time_callback(this.arg.x, this.arg.y):0;
            };
            return;
        };
        this.calculatePosition(delta);
        this.now_life+= delta;
        this.wakes.push([this.arg.x, this.arg.y]);
        if (this.wakes.length > this.arg.wake_particles) {
            this.wakes.shift();
        };
        this.draw();
    };

    ease_out(delta) {
        this.calculatePosition(delta);
        if(this.wakes.length == 0) {
            if (this.arg.life_time_callback) {
                this.arg.life_time_callback();
            };
            return;
        };
        this.wakes.push([this.arg.x, this.arg.y]);
        this.wakes.shift();
        this.wakes.shift();
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
    
};

class Firework {
    particles = [];
    ease_out_ = [];
    now_life = 0;
    wakes = [];
    explode_position = null;
    animate_end=false;
    launch_end=false;
    constructor(arg,end_callback) {
        this.arg = arg;
        this.end_callback = end_callback;
    };

    update(delta) {
        if(this.animate_end) {
            this.end_callback(this);
            return;
        }
        if(this.launch_end) {
            if(this.explode_position!=null){
                this.particles=[];
                this.explode(this.explode_position[0],this.explode_position[1]);
                this.explode_position = null;
            }
        }
        for (let i = 0; i < this.particles.length; i++) {
            this.particles[i].update(delta);
        };
        if (this.now_life == 0) {
            this.now_life+=delta;
            let arg = { ...this.arg };
            arg.life_time_callback = ((x,y)=> {
                this.explode_position = [x,y];
                this.launch_end = true;
            }).bind(this);
            this.particles.push(new Particle(arg,"l"));
        };
    };
    explode(x,y) {
        for (let i = 0; i < this.arg.explode_particles; i++) {
            let arg = { ...this.arg };
            if (i == 0) {
                arg.life_time_callback = ()=>{ this.animate_end = true; };
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
    #max_fireworks = 0;
    #args = {};
    #last_frame_time=0;
    #requestAnimationFrame = null;
    #hidden_canvas = null;
    #hidden_ctx= null;
    constructor(ctx, width, height,  max_fireworks = 10,args = {}) {
        this.#ctx = ctx;
        this.init_hidden_canvas(width,height);
        this.#width = width;
        this.#height = height;
        this.#max_fireworks = max_fireworks; // 最大并行更新烟花数量
        this.#args = {...args_template,...args};
    };

    init_hidden_canvas(width ,height){
        this.#hidden_canvas = document.createElement('canvas');
        this.#hidden_canvas.width = width;
        this.#hidden_canvas.height = height;
        this.#hidden_ctx = this.#hidden_canvas.getContext('2d');
    }

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
        arg.ctx = this.#hidden_ctx;
        arg.x = Math.random() * this.#width;
        arg.color = `rgb(${Math.random() * 255},${Math.random() * 255},${Math.random() * 255})`;
        this.addFirework(arg);
    };

    is_running() {
        return (this.#started==true);
    };

    #mainLoop(frame_start_time) {
        let delta =this.#last_frame_time !=0? frame_start_time - this.#last_frame_time:16;
        this.#last_frame_time = frame_start_time;
        if(!this.#started) {
            return;
        };
        this.#ctx.clearRect(0, 0, this.#width, this.#height);
        this.#ctx.drawImage(this.#hidden_canvas,0,0);
        this.#hidden_ctx.clearRect(0, 0, this.#width, this.#height);
        for (let i = 0; i < this.#fireworks.length; i++) {
            this.#fireworks[i].update(delta);
        };
        if (this.#fireworks.length > this.#max_fireworks*2) {
            this.#fireworks = this.#fireworks.slice(this.#max_fireworks, this.#max_fireworks*2);
        };
        this.#ctx.drawImage(this.#hidden_canvas,0,0);
        this.#requestAnimationFrame=requestAnimationFrame((frame_start_time)=>{this.#mainLoop(frame_start_time);});
    };

    start() {
        if (this.#started) {
            return;
        };
        if(this.#requestAnimationFrame != null) {
            cancelAnimationFrame(this.#requestAnimationFrame);
        }
        this.#started = true;
        this.#mainLoop();
    };

    stop() {
        if (!this.#started) {
            return;
        };
        if(this.#requestAnimationFrame != null) {
            cancelAnimationFrame(this.#requestAnimationFrame);
        }
        this.#last_frame_time=0;
        this.#started = false;
    };

    updateSize(canvas,element) {
        this.#width = element.innerWidth;
        this.#height = element.innerHeight;

        canvas.width = element.innerWidth;
        canvas.height = element.innerHeight;
        this.#ctx.setTransform(1,0,0,-1,0,canvas.height);
        //更新
        this.#hidden_canvas.width = element.innerWidth;
        this.#hidden_canvas.height = element.innerHeight;
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

    setAutoCloseOrStart(start_func=null,stop_func=null) {
        this.removeAutoCloseOrStart();
        window.addEventListener('visibilitychange',()=> {
            if(document.hidden) {
                if(stop_func != null) stop_func();
                this.stop();
            } else {
                if(start_func != null) start_func();
                this.start();
            }
        });
    }

    removeAutoCloseOrStart(start_func=null,stop_func=null) {
        window.removeEventListener('visibilitychange',()=> {
            if(document.hidden) {
                if(stop_func != null) stop_func();
                this.stop();
            } else {
                if(start_func != null) start_func();
                this.start();
            }
        });
    }
};

