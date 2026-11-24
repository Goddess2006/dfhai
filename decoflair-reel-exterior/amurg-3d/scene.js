/* global THREE */
(() => {
  const params = new URLSearchParams(location.search);
  const width = Number(params.get('width') || 1080);
  const height = Number(params.get('height') || 1920);
  const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
  renderer.setSize(width, height);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.12;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = false;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(49, width / height, 0.035, 190);
  document.body.appendChild(renderer.domElement);

  let state = 107;
  function rand() {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 4294967296;
  }

  const noise = `
    float hash3(vec3 p) { p=fract(p*.3183099+.17)*17.; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
    float noise3(vec3 p) {
      vec3 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
      vec2 e=vec2(0,1);
      return mix(mix(mix(hash3(i),hash3(i+e.yxx),f.x),mix(hash3(i+e.xyx),hash3(i+e.yyx),f.x),f.y),
                 mix(mix(hash3(i+e.xxy),hash3(i+e.yxy),f.x),mix(hash3(i+e.xyy),hash3(i+e.yyy),f.x),f.y),f.z);
    }
  `;

  function surface(color, amplitude = 0.13, scale = 15, roughness = .87) {
    const material = new THREE.MeshStandardMaterial({color, roughness});
    material.customProgramCacheKey = () => 'material-world';
    material.onBeforeCompile = shader => {
      shader.uniforms.textureStrength = {value: amplitude};
      shader.uniforms.textureScale = {value: scale};
      shader.vertexShader = 'varying vec3 surfaceP;\n' + shader.vertexShader.replace('#include <begin_vertex>', `
        #include <begin_vertex>
        surfaceP = (modelMatrix * vec4(transformed, 1.)).xyz;
      `);
      shader.fragmentShader = 'varying vec3 surfaceP; uniform float textureStrength,textureScale;\n' + noise +
        shader.fragmentShader.replace('#include <color_fragment>', `
          #include <color_fragment>
          float detail = (.6*noise3(surfaceP*textureScale)+.4*noise3(surfaceP*3.4)-.48);
          float grain = (hash3(floor(surfaceP*480.))-.5);
          diffuseColor.rgb *= 1. + textureStrength * (detail*1.5 + grain*.28);
        `);
    };
    return material;
  }

  const wall = surface(0xb5a38d, .28, 72);
  const quoins = surface(0xe2cdb0, .17, 105);
  const stone = surface(0xc4aa8f, .30, 24);
  const base = surface(0x85746a, .38, 16);
  const roof = surface(0x514344, .35, 17);
  const seam = surface(0x352d30, .18);
  const iron = surface(0x363032, .21, 24, .54);
  const wood = surface(0x614637, .34, 22);
  const paving = surface(0x867468, .37, 28);
  const paving2 = surface(0x917e6e, .38, 34);
  const ground = surface(0x545845, .76, 26);
  const bark = surface(0x4c3931, .55, 18);
  const leaf = [0x535841, 0x615c3b, 0x766345, 0x464e41, 0x72573a].map(color => surface(color, .48, 49));
  const windowFrame = surface(0x403c3d, .12, 28, .5);
  const paleFrame = surface(0xaf9c83, .14, 61);
  const bulb = new THREE.MeshBasicMaterial({color: 0xffd19a});
  const groups = new Map();

  function geometry(shape, material, shade = true) {
    let group = groups.get(material);
    if (!group) {
      group = {parts: [], shade};
      groups.set(material, group);
    }
    if (shape.index) {
      const indexed = shape;
      shape = shape.toNonIndexed();
      indexed.dispose();
    }
    group.parts.push(shape);
  }

  function box(x, y, z, w, h, d, material, shade = true, angle = 0) {
    const shape = new THREE.BoxGeometry(w, h, d);
    shape.rotateY(angle).translate(x, y, z);
    geometry(shape, material, shade);
  }

  function beam(a, b, r1, r2, material, sides = 6, shade = true) {
    const start = new THREE.Vector3(...a);
    const end = new THREE.Vector3(...b);
    const axis = end.clone().sub(start);
    const center = start.clone().addScaledVector(axis, .5);
    const shape = new THREE.CylinderGeometry(r2, r1, axis.length(), sides, 1);
    const rotation = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), axis.normalize());
    shape.applyQuaternion(rotation).translate(center.x, center.y, center.z);
    geometry(shape, material, shade);
  }

  // Six masonry sections leave actual openings for the windows and door.
  const halfW = 4.35, halfD = 3.05;
  const wallY = 5.85;
  box(0,.19,0,9,.38,6.40,base);
  box(0,.415,0,8.94,.095,6.34,stone);
  box(0,wallY/2,-halfD,8.7,wallY,.22,wall);
  box(-halfW,wallY/2,0,.22,wallY,6.1,wall);

  function glass(materialColor, lightness) {
    const mat = new THREE.ShaderMaterial({
      uniforms: {
        cloth: {value: new THREE.Color(materialColor)},
        strength: {value: lightness}
      },
      vertexShader: `varying vec2 vUv; void main(){vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
      fragmentShader: `
        uniform vec3 cloth; uniform float strength; varying vec2 vUv;
        ${noise}
        void main(){
          vec2 p=vUv; float fold=.65+.17*cos(p.x*105.+sin(p.y*3.)*1.3)+.11*cos(p.x*191.);
          float falloff=exp(-((p.x-.49)*(p.x-.49)*5.+(p.y-.34)*(p.y-.34)*2.8));
          float edge=smoothstep(.0,.16,min(p.x,1.-p.x))*.29+.71;
          vec3 c=cloth*(strength*(.27+.73*falloff)*fold*edge);
          float reflected=pow(max(0.,p.y),2.)*noise3(vec3(p*vec2(5.,12.),1.1))*.24;
          c+=reflected*vec3(.38,.49,.77);
          gl_FragColor=vec4(c,1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }
      `
    });
    return mat;
  }

  const interior = [glass(0xffb066,1.75),glass(0xffbe7f,1.18),glass(0xf4cfac,.65),glass(0xf1b578,1.46)];

  function facade(windows, side) {
    const extent = side ? halfD : halfW;
    function board(u, y, outward, w, h, d, material) {
      if (side) box(halfW+outward,y,-u,d,h,w,material);
      else box(u,y,halfD+outward,w,h,d,material);
    }
    const boundaries = [...new Set([-.02, .44, wallY, ...windows.flatMap(win => [win.y, win.y+win.h])])].sort((a,b)=>a-b);
    for(let i=0;i<boundaries.length-1;i++){
      const low=boundaries[i], high=boundaries[i+1], y=(low+high)/2;
      const apertures=windows.filter(win=>y>win.y && y<win.y+win.h).sort((a,b)=>a.u-b.u);
      let left=-extent;
      for(const win of apertures){
        const start=win.u-win.w/2;
        board((left+start)/2,y,-.115,start-left,high-low,.230,wall);
        left=win.u+win.w/2;
      }
      board((left+extent)/2,y,-.115,extent-left,high-low,.230,wall);
    }

    for(const {u,y,w,h,index,door} of windows) {
      const cy=y+h*.5;
      const pane=new THREE.PlaneGeometry(w-.105,h-.105);
      if(side) pane.rotateY(Math.PI/2).translate(halfW-.13,cy,-u);
      else pane.translate(u,cy,halfD-.13);
      geometry(pane,interior[index],false);
      const frame=door?wood:windowFrame;
      for(const sign of [-1,1]){
        board(u+sign*(w/2+.052),cy,.035,.116,h+.145,.135,paleFrame);
        board(u+sign*(w/2-.028),cy,-.072,.066,h,.12,frame);
        board(u,cy+sign*(h/2-.028),-.072,w,.062,.12,frame);
      }
      board(u,y+h+.068,.055,w+.31,.126,.175,stone);
      board(u,y+h+.137,.075,w+.37,.033,.205,quoins);
      board(u,y-.043,.068,w+.32,.083,.267,stone);
      board(u,cy,-.077,.043,h,.084,frame);
      if(door){
        board(u,y+.30,-.06,w-.06,.5,.075,wood);
        board(u+.095,y+.91,.005,.032,.25,.055,stone);
      }else{
        board(u,y+h*.70,-.078,w,.028,.08,frame);
        board(u,y+h*.37,-.078,w,.024,.075,frame);
      }
    }
    for (const [level,h,d] of [[3.22,.095,.11],[3.31,.029,.14],[5.73,.13,.18],[5.83,.08,.27],[5.91,.095,.35],[5.99,.045,.39]]) {
      board(0,level,d*.4,extent*2+d/2,h,d,level<3.8 ? stone : quoins);
    }
  }

  const win = (u,y,w,h,index,door=false) => ({u,y,w,h,index,door});
  facade([
    win(-2.69,.92,1.32,1.79,0), win(0,.44,1.34,2.43,3,true), win(2.55,.92,1.30,1.79,1),
    win(-2.69,3.73,1.34,1.57,1),win(0,3.64,1.39,1.79,2),win(2.55,3.73,1.32,1.57,3),
  ],false);
  facade([
    win(-1.17,.92,1.47,1.77,3),win(1.43,1.16,1.02,1.53,2),
    win(-1.17,3.72,1.47,1.58,1),win(1.43,3.72,1.02,1.58,2),
  ],true);

  // Each 1 m module has five equal bands, 30 mm relief, and 300 mm legs.
  function corner(x, z, xSign, zSign) {
    for (let module=0;module<6;module++){
      for(let strip=0;strip<5;strip++){
        const y=.47+module+strip*.20;
        if(y>5.69 || (y>=3.17&&y<=3.33)) continue;
        const coords=[[-.300,.026],[.026,.026],[.026,-.300],[-.004,-.300],[-.004,-.004],[-.300,-.004]];
        const outline=new THREE.Shape(coords.map(([a,b])=>new THREE.Vector2(a*xSign,-b*zSign)));
        const shape=new THREE.ExtrudeGeometry(outline,{depth:.182,bevelEnabled:true,bevelThickness:.003,bevelSize:.003,bevelSegments:1,curveSegments:1});
        shape.rotateX(-Math.PI/2).translate(x,y,z);
        geometry(shape,quoins);
      }
    }
  }
  corner(halfW,halfD,1,1);
  corner(-halfW,halfD,-1,1);
  corner(halfW,-halfD,1,-1);

  // Hipped roof with standing seams, dark wet metal and separate gutters.
  const eave=6.00, ridge=7.88, span=4.67, depth=3.43, cap=1.53;
  function face(points, material){
    const shape=new THREE.BufferGeometry();
    const vertices=new Float32Array(points.flat());
    shape.setAttribute('position',new THREE.BufferAttribute(vertices,3));
    shape.computeVertexNormals();
    geometry(shape,material);
  }
  roof.side=THREE.DoubleSide;
  for(const s of [-1,1]){
    const panel=[[-span,eave,s*depth],[span,eave,s*depth],[cap,ridge,0],[-cap,ridge,0]];
    if(s<0) panel.reverse();
    face([panel[0],panel[1],panel[2],panel[0],panel[2],panel[3]],roof);
    for(let x=-span+.13;x<span;x+=.30){
      const peak=Math.abs(x)<=cap?1:(span-Math.abs(x))/(span-cap);
      beam([x,eave+.014,s*depth],[x,eave+(ridge-eave)*peak+.02,s*depth*(1-peak)],.011,.011,seam,4);
    }
    const side=[[s*span,eave,-depth],[s*span,eave,depth],[s*cap,ridge,0]];
    if(s>0)side.reverse();
    face(side,roof);
    for(let z=-depth+.15;z<depth;z+=.31){
      const peak=1-Math.abs(z)/depth;
      beam([s*span,eave+.02,z],[s*(span-(span-cap)*peak),eave+(ridge-eave)*peak+.02,z],.010,.01,seam,4);
    }
    beam([-span,eave,s*depth],[span,eave,s*depth],.046,.046,iron,8);
    beam([s*span,eave,-depth],[s*span,eave,depth],.046,.046,iron,8);
    for(const k of [-1,1]) beam([s*span,eave+.03,k*depth],[s*cap,ridge+.03,0],.024,.024,iron,6);
  }
  beam([-cap,ridge+.025,0],[cap,ridge+.025,0],.035,.035,iron,8);
  box(-1.32,7.12,-1.36,.62,2.07,.62,stone);
  box(-1.32,8.17,-1.36,.81,.11,.81,iron);
  box(-1.32,8.25,-1.36,.53,.10,.53,iron);
  beam([4.53,5.98,-2.89],[4.46,.42,-2.89],.032,.032,iron,8);

  // Door hood, two practical lanterns and short steps.
  for(const [y,w,d] of [[.085,2.65,1.50],[.211,2.43,1.28],[.342,2.23,1.07]]){
    box(0,y,3.05+d/2,w,.16,d,stone);
  }
  box(0,3.02,3.44,2.22,.16,.95,stone);
  box(0,3.13,3.43,2.29,.075,.99,iron);
  for(const x of [-.98,.98]) beam([x,2.68,3.10],[x,2.96,3.61],.043,.032,iron,6);

  for (const x of [-1.38,1.38]) {
    box(x,2.05,3.071,.13,.30,.061,iron);
    box(x,2.02,3.23,.14,.20,.14,bulb,false);
    for(const dx of [-.087,.087]){
      for(const dz of [-.087,.087]){
        box(x+dx,2.02,3.23+dz,.018,.24,.018,iron);
      }
    }
    box(x,1.895,3.23,.21,.035,.22,iron);
    const lantern = new THREE.ConeGeometry(.157,.12,4).rotateY(Math.PI/4).translate(x,2.19,3.23);
    geometry(lantern,iron);
    const glow=new THREE.PointLight(0xffb478,7.4,4.0,2);
    glow.position.set(x,2.02,3.38); scene.add(glow);
  }
  const wallWash=new THREE.SpotLight(0xffb578,24,8,.48,.85,2);
  wallWash.position.set(5.35,.39,3.95);
  wallWash.target.position.set(4.28,2.9,3.0);
  scene.add(wallWash,wallWash.target);

  box(0,-.075,0,175,.12,175,ground,false);
  box(0,-.025,10.7,2.72,.045,13.7,base,false);
  for(let row=0;row<24;row++){
    for(let col=0;col<5;col++){
      const z=4.14+row*.56+(col%2)*.15;
      box((col-2)*.52,.002,z,.509,.048,.541,(row+col)%7===0?paving2:paving,false);
    }
  }
  for(let i=0;i<140;i++){
    const x=(rand()-.50)*29, z=3.3+rand()*20;
    if(Math.abs(x)<1.55 || (Math.abs(x)<4.9 && z<4.4))continue;
    box(x,.007,z,.02+rand()*.12,.026,.014+rand()*.075,leaf[i%5],false,rand()*Math.PI);
  }


  // Small two-sided leaf silhouettes catch the blue and warm light independently.
  const leafGeometry = new THREE.BufferGeometry();
  const leafVertices = [
    0,0,0,  -.36,.40,.06,  0,.46,.17,  0,0,0,  0,.46,.17,  .31,.48,.04,
    -.36,.40,.06,  -.28,.72,.02,  0,.46,.17,  -.28,.72,.02,  0,1,0,  0,.46,.17,
    0,.46,.17,  0,1,0,  .27,.76,.025,  0,.46,.17,  .27,.76,.025,  .31,.48,.04
  ];
  leafGeometry.setAttribute('position',new THREE.Float32BufferAttribute(leafVertices,3));
  leafGeometry.computeVertexNormals();
  leaf.forEach(material => {material.side = THREE.DoubleSide;});
  const plantVolume = new THREE.IcosahedronGeometry(1,1);
  function bush(x,z,radius,height) {
    for(let i=0;i<18;i++){
      const a=rand()*Math.PI*2, r=radius*Math.sqrt(rand())*.8;
      const form=plantVolume.clone().scale(.18,.13,.155).rotateY(a);
      form.translate(x+Math.cos(a)*r,.065+height*.43*Math.sqrt(1-(r/radius)**2),z+Math.sin(a)*r);
      geometry(form,leaf[3],false);
    }
    for(let i=0;i<500;i++){
      const angle=rand()*Math.PI*2, r=radius*Math.sqrt(rand());
      const hs=Math.sqrt(Math.max(0,1-(r/radius)**2));
      const sz=.038+rand()*.070;
      const shape=leafGeometry.clone().scale(sz,sz,sz).rotateX(.55+rand()*2.4).rotateY(angle);
      shape.translate(x+Math.cos(angle)*r,.048+height*hs*(.49+rand()*.57),z+Math.sin(angle)*r);
      geometry(shape,leaf[i%5],false);
    }
  }

  const grassVertices = [];
  for(let i=0;i<19000;i++){
    const x=(rand()-.5)*27, z=3.23+rand()*21;
    if(Math.abs(x)<1.40&&z<17.5) continue;
    const patch=.35+.65*Math.abs(Math.sin(x*2.63+z*.87)*Math.sin(z*.71));
    if(rand()>patch)continue;
    const angle=rand()*Math.PI, w=.012+rand()*.023, h=.023+rand()*.085;
    const dx=Math.cos(angle)*w, dz=Math.sin(angle)*w;
    grassVertices.push(x-dx,0,z-dz, x+dx,0,z+dz, x+dx*.75,h,z-dz*.6);
  }
  const grass = new THREE.BufferGeometry();
  grass.setAttribute('position',new THREE.Float32BufferAttribute(grassVertices,3));
  grass.computeVertexNormals();
  geometry(grass,leaf[3],false);

  for (const coords of [[-3.3,3.68,.77,.51],[-4.39,3.77,.84,.78],[2.69,3.70,.55,.45],[3.52,3.67,.50,.37],
                         [5.41,1.82,.78,.65],[-2.14,8.13,.64,.55],[7.3,10.8,1.16,.62],[-5.4,11.2,1.1,.57],
                         [-7.1,1.5,1.3,.86],[6.32,-1.45,1.1,.68],[-5.9,5.2,1.15,.68]]) bush(...coords);

  function tree(x,z,h) {
    const trunk=[[x,0,z],[x+.12,h*.38,z+.05],[x-.19,h*.73,z+.16],[x+.02,h,z+.28]];
    for(let i=1;i<trunk.length;i++)beam(trunk[i-1],trunk[i],.155*(1-(i-1)/3),.146*(1-i/3)+.008,bark,7,false);
    const cluster=leafGeometry;
    for(let j=0;j<14;j++){
      const theta=j*2.4;
      const level=.40+j*.033;
      const origin=[x,level*h,z];
      const stretch=(.8+rand()*.5)*h*(1-level)*.55;
      const end=[x+Math.cos(theta)*stretch,(level+.18+rand()*.09)*h,z+Math.sin(theta)*stretch];
      beam(origin,end,.05*(1-level),.009,bark,5,false);
      for(let k=0;k<103;k++){
        const phi=rand()*Math.PI*2, rr=(.14+rand()*.9)*h*.108;
        const center=[end[0]+Math.cos(phi)*rr,end[1]+(rand()-.3)*h*.18,end[2]+Math.sin(phi)*rr];
        const s=h*(.012+rand()*.022);
        const shape=cluster.clone().scale(s*1.1,s,s).rotateX(rand()*3.).rotateY(phi).translate(...center);
        geometry(shape,leaf[(j+k)%5],false);
      }
    }
  }
  for(const t of [[-7.5,1.2,7.7],[-6.9,-4.4,8],[-10.1,6.2,7],[6.6,-4.6,8.8],[9,-2.3,8.5],[-4,-10,9],
                  [3.1,-10.5,9],[-15,8,10],[11.2,9.8,10.4],[-10,-10,9],[11,-9,11]])tree(...t);

  for(const [material,{parts,shade}] of groups){
    const count=parts.reduce((sum,g)=>sum+g.attributes.position.count,0);
    const pos=new Float32Array(3*count), normals=new Float32Array(3*count), uv=new Float32Array(2*count);
    let offset=0;
    for(const part of parts){
      pos.set(part.attributes.position.array,3*offset);
      normals.set(part.attributes.normal.array,3*offset);
      if(part.attributes.uv) uv.set(part.attributes.uv.array,2*offset);
      offset+=part.attributes.position.count;
      part.dispose();
    }
    const combined=new THREE.BufferGeometry();
    combined.setAttribute('position',new THREE.BufferAttribute(pos,3));
    combined.setAttribute('normal',new THREE.BufferAttribute(normals,3));
    combined.setAttribute('uv',new THREE.BufferAttribute(uv,2));
    const mesh=new THREE.Mesh(combined,material);
    mesh.castShadow=shade;
    mesh.receiveShadow=!(material instanceof THREE.ShaderMaterial);
    scene.add(mesh);
  }

  const sky = new THREE.Mesh(new THREE.SphereGeometry(120,24,16),new THREE.ShaderMaterial({
    side: THREE.BackSide,
    depthWrite: false,
    uniforms: {time:{value:0}},
    vertexShader: `varying vec3 ray; void main(){ray=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader: `
      varying vec3 ray;
      uniform float time;
      ${noise}
      void main(){
        vec3 dir=normalize(ray);
        float elevation=max(0.,dir.y);
        vec3 horizon=vec3(.44,.229,.173), high=vec3(.046,.081,.167);
        float warm=pow(max(0.,dot(dir,normalize(vec3(-.85,.10,-.36)))),3.);
        vec3 color=mix(horizon*(.74+.32*warm),high,smoothstep(-.07,.47,elevation));
        vec3 cl=vec3(dir.x*5.,dir.y*21.,dir.z*6.+time*.010);
        float cloud=.53*noise3(cl)+.28*noise3(cl*2.2)+.19*noise3(cl*4.64);
        float veil=smoothstep(.38,.68,cloud)*smoothstep(.025,.10,elevation);
        color=mix(color,vec3(.47,.331,.31)*(.77+.65*warm),veil*.40);
        gl_FragColor=vec4(color,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }
    `
  }));
  scene.add(sky);
  scene.add(new THREE.HemisphereLight(0xb7c4f0,0x625046,1.30));
  const evening = new THREE.DirectionalLight(0xffca9f,1.38);
  evening.position.set(-5,5.3,12);
  evening.castShadow=true;
  evening.shadow.mapSize.set(2048,2048);
  Object.assign(evening.shadow.camera,{left:-11,right:11,top:11,bottom:-10,near:.25,far:28});
  evening.shadow.bias=-.00020;
  evening.shadow.normalBias=.013;
  scene.add(evening);
  const bounce = new THREE.DirectionalLight(0xa9c1fc,.48);
  bounce.position.set(8,5,-8);
  scene.add(bounce);

  const smooth = (a,b,t) => {
    const v=THREE.MathUtils.clamp((t-a)/(b-a),0,1);
    return v*v*(3-2*v);
  };
  const film = new THREE.WebGLRenderTarget(width,height,{depthTexture:new THREE.DepthTexture(width,height)});
  const image = new THREE.Scene();
  const screen = new THREE.ShaderMaterial({
    uniforms:{
      colorFrame:{value:film.texture}, depthFrame:{value:film.depthTexture},
      pixel:{value:new THREE.Vector2(1/width,1/height)}, focus:{value:1.9}, time:{value:0},
    },
    depthWrite:false,
    vertexShader:`varying vec2 p; void main(){p=uv;gl_Position=vec4(position.xy,0.,1.);}`,
    fragmentShader:`
      varying vec2 p;
      uniform sampler2D colorFrame,depthFrame;
      uniform vec2 pixel;
      uniform float focus,time;
      void main(){
        float d=texture2D(depthFrame,p).r;
        float meters=(.035*190.)/(190.-d*(190.-.035));
        float radius=clamp(abs(1./max(.05,meters)-1./focus)*7.,0.,3.0);
        vec2 dx=vec2(pixel.x*radius,0.),dy=vec2(0.,pixel.y*radius);
        vec3 c=texture2D(colorFrame,p).rgb*.46;
        c+=.135*(texture2D(colorFrame,p+dx).rgb+texture2D(colorFrame,p-dx).rgb+
                 texture2D(colorFrame,p+dy).rgb+texture2D(colorFrame,p-dy).rgb);
        c*=1.-.135*pow(length((p-.5)*vec2(1.26,1.06)),1.8);
        float grain=fract(52.9829189*fract(dot(gl_FragCoord.xy+fract(time)*57.0,vec2(.06711056,.00583715))));
        c+=(grain-.5)*.011;
        gl_FragColor=vec4(c,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }
    `
  });
  image.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),screen));
  const flat=new THREE.Camera();
  let first = true;
  window.renderFrame = (frame, fps=30) => {
    const t=frame/fps;
    const pull=smooth(.12,11.15,t), glide=smooth(8.7,16.0,t);
    const sweep=smooth(.22,10.75,t);
    camera.position.set(
      5.69+2.79*sweep-.70*glide+.009*Math.sin(t*2.2),
      2.43+.11*pull+.012*Math.sin(t*2.45),
      4.54+16.42*pull+.53*glide
    );
    camera.lookAt(
      4.32-4.49*sweep-.12*glide,
      2.42+.59*sweep+.008*Math.sin(t*1.95),
      3.00-3.23*sweep
    );
    sky.material.uniforms.time.value=t;
    if(first){renderer.shadowMap.needsUpdate=true; first=false;}
    screen.uniforms.focus.value = camera.position.distanceTo(new THREE.Vector3(
      4.32-4.49*sweep-.12*glide, 2.42+.59*sweep, 3.-3.23*sweep
    ));
    screen.uniforms.time.value=t;
    renderer.setRenderTarget(film);
    renderer.render(scene,camera);
    renderer.setRenderTarget(null);
    renderer.render(image,flat);
    return renderer.domElement;
  };
})();
