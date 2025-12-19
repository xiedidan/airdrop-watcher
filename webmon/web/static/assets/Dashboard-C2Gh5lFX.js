import{d as W,c as N,m as ne,h as o,N as te,f as M,a as L,b as y,e as I,u as se,g as re,p as ce,i as U,j as de,k as P,o as _,l as S,n as ue,r as ge,q as fe,s as pe,t as i,w as a,v as e,x as he,y as E,z as J,B as A,A as j,C as z,D as T,E as C,F as B,T as ye,G as H,H as me,_ as ve}from"./index-D2gWhZYU.js";import{I as ie,W as oe,E as ae,S as le,u as be,N as xe,R as ke,a as V,b as we}from"./task-DEx63VkS.js";import{N as K,a as q,b as Y,C as Z}from"./CheckmarkCircleOutline-CksryUod.js";import{N as O,a as Q}from"./Card-H1W3Whul.js";import{F as Ce}from"./FlashOutline-B0mtTne6.js";const $e={success:o(le,null),error:o(ae,null),warning:o(oe,null),info:o(ie,null)},_e=W({name:"ProgressCircle",props:{clsPrefix:{type:String,required:!0},status:{type:String,required:!0},strokeWidth:{type:Number,required:!0},fillColor:[String,Object],railColor:String,railStyle:[String,Object],percentage:{type:Number,default:0},offsetDegree:{type:Number,default:0},showIndicator:{type:Boolean,required:!0},indicatorTextColor:String,unit:String,viewBoxWidth:{type:Number,required:!0},gapDegree:{type:Number,required:!0},gapOffsetDegree:{type:Number,default:0}},setup(t,{slots:m}){const c=N(()=>{const s="gradient",{fillColor:l}=t;return typeof l=="object"?`${s}-${ne(JSON.stringify(l))}`:s});function f(s,l,d,h){const{gapDegree:b,viewBoxWidth:k,strokeWidth:x}=t,u=50,w=0,g=u,r=0,n=2*u,v=50+x/2,$=`M ${v},${v} m ${w},${g}
      a ${u},${u} 0 1 1 ${r},${-n}
      a ${u},${u} 0 1 1 ${-r},${n}`,R=Math.PI*2*u,D={stroke:h==="rail"?d:typeof t.fillColor=="object"?`url(#${c.value})`:d,strokeDasharray:`${Math.min(s,100)/100*(R-b)}px ${k*8}px`,strokeDashoffset:`-${b/2}px`,transformOrigin:l?"center":void 0,transform:l?`rotate(${l}deg)`:void 0};return{pathString:$,pathStyle:D}}const p=()=>{const s=typeof t.fillColor=="object",l=s?t.fillColor.stops[0]:"",d=s?t.fillColor.stops[1]:"";return s&&o("defs",null,o("linearGradient",{id:c.value,x1:"0%",y1:"100%",x2:"100%",y2:"0%"},o("stop",{offset:"0%","stop-color":l}),o("stop",{offset:"100%","stop-color":d})))};return()=>{const{fillColor:s,railColor:l,strokeWidth:d,offsetDegree:h,status:b,percentage:k,showIndicator:x,indicatorTextColor:u,unit:w,gapOffsetDegree:g,clsPrefix:r}=t,{pathString:n,pathStyle:v}=f(100,0,l,"rail"),{pathString:$,pathStyle:R}=f(k,h,s,"fill"),D=100+d;return o("div",{class:`${r}-progress-content`,role:"none"},o("div",{class:`${r}-progress-graph`,"aria-hidden":!0},o("div",{class:`${r}-progress-graph-circle`,style:{transform:g?`rotate(${g}deg)`:void 0}},o("svg",{viewBox:`0 0 ${D} ${D}`},p(),o("g",null,o("path",{class:`${r}-progress-graph-circle-rail`,d:n,"stroke-width":d,"stroke-linecap":"round",fill:"none",style:v})),o("g",null,o("path",{class:[`${r}-progress-graph-circle-fill`,k===0&&`${r}-progress-graph-circle-fill--empty`],d:$,"stroke-width":d,"stroke-linecap":"round",fill:"none",style:R}))))),x?o("div",null,m.default?o("div",{class:`${r}-progress-custom-content`,role:"none"},m.default()):b!=="default"?o("div",{class:`${r}-progress-icon`,"aria-hidden":!0},o(te,{clsPrefix:r},{default:()=>$e[b]})):o("div",{class:`${r}-progress-text`,style:{color:u},role:"none"},o("span",{class:`${r}-progress-text__percentage`},k),o("span",{class:`${r}-progress-text__unit`},w))):null)}}}),Se={success:o(le,null),error:o(ae,null),warning:o(oe,null),info:o(ie,null)},ze=W({name:"ProgressLine",props:{clsPrefix:{type:String,required:!0},percentage:{type:Number,default:0},railColor:String,railStyle:[String,Object],fillColor:[String,Object],status:{type:String,required:!0},indicatorPlacement:{type:String,required:!0},indicatorTextColor:String,unit:{type:String,default:"%"},processing:{type:Boolean,required:!0},showIndicator:{type:Boolean,required:!0},height:[String,Number],railBorderRadius:[String,Number],fillBorderRadius:[String,Number]},setup(t,{slots:m}){const c=N(()=>M(t.height)),f=N(()=>{var l,d;return typeof t.fillColor=="object"?`linear-gradient(to right, ${(l=t.fillColor)===null||l===void 0?void 0:l.stops[0]} , ${(d=t.fillColor)===null||d===void 0?void 0:d.stops[1]})`:t.fillColor}),p=N(()=>t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):""),s=N(()=>t.fillBorderRadius!==void 0?M(t.fillBorderRadius):t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):"");return()=>{const{indicatorPlacement:l,railColor:d,railStyle:h,percentage:b,unit:k,indicatorTextColor:x,status:u,showIndicator:w,processing:g,clsPrefix:r}=t;return o("div",{class:`${r}-progress-content`,role:"none"},o("div",{class:`${r}-progress-graph`,"aria-hidden":!0},o("div",{class:[`${r}-progress-graph-line`,{[`${r}-progress-graph-line--indicator-${l}`]:!0}]},o("div",{class:`${r}-progress-graph-line-rail`,style:[{backgroundColor:d,height:c.value,borderRadius:p.value},h]},o("div",{class:[`${r}-progress-graph-line-fill`,g&&`${r}-progress-graph-line-fill--processing`],style:{maxWidth:`${t.percentage}%`,background:f.value,height:c.value,lineHeight:c.value,borderRadius:s.value}},l==="inside"?o("div",{class:`${r}-progress-graph-line-indicator`,style:{color:x}},m.default?m.default():`${b}${k}`):null)))),w&&l==="outside"?o("div",null,m.default?o("div",{class:`${r}-progress-custom-content`,style:{color:x},role:"none"},m.default()):u==="default"?o("div",{role:"none",class:`${r}-progress-icon ${r}-progress-icon--as-text`,style:{color:x}},b,k):o("div",{class:`${r}-progress-icon`,"aria-hidden":!0},o(te,{clsPrefix:r},{default:()=>Se[u]}))):null)}}});function ee(t,m,c=100){return`m ${c/2} ${c/2-t} a ${t} ${t} 0 1 1 0 ${2*t} a ${t} ${t} 0 1 1 0 -${2*t}`}const Ne=W({name:"ProgressMultipleCircle",props:{clsPrefix:{type:String,required:!0},viewBoxWidth:{type:Number,required:!0},percentage:{type:Array,default:[0]},strokeWidth:{type:Number,required:!0},circleGap:{type:Number,required:!0},showIndicator:{type:Boolean,required:!0},fillColor:{type:Array,default:()=>[]},railColor:{type:Array,default:()=>[]},railStyle:{type:Array,default:()=>[]}},setup(t,{slots:m}){const c=N(()=>t.percentage.map((s,l)=>`${Math.PI*s/100*(t.viewBoxWidth/2-t.strokeWidth/2*(1+2*l)-t.circleGap*l)*2}, ${t.viewBoxWidth*8}`)),f=(p,s)=>{const l=t.fillColor[s],d=typeof l=="object"?l.stops[0]:"",h=typeof l=="object"?l.stops[1]:"";return typeof t.fillColor[s]=="object"&&o("linearGradient",{id:`gradient-${s}`,x1:"100%",y1:"0%",x2:"0%",y2:"100%"},o("stop",{offset:"0%","stop-color":d}),o("stop",{offset:"100%","stop-color":h}))};return()=>{const{viewBoxWidth:p,strokeWidth:s,circleGap:l,showIndicator:d,fillColor:h,railColor:b,railStyle:k,percentage:x,clsPrefix:u}=t;return o("div",{class:`${u}-progress-content`,role:"none"},o("div",{class:`${u}-progress-graph`,"aria-hidden":!0},o("div",{class:`${u}-progress-graph-circle`},o("svg",{viewBox:`0 0 ${p} ${p}`},o("defs",null,x.map((w,g)=>f(w,g))),x.map((w,g)=>o("g",{key:g},o("path",{class:`${u}-progress-graph-circle-rail`,d:ee(p/2-s/2*(1+2*g)-l*g,s,p),"stroke-width":s,"stroke-linecap":"round",fill:"none",style:[{strokeDashoffset:0,stroke:b[g]},k[g]]}),o("path",{class:[`${u}-progress-graph-circle-fill`,w===0&&`${u}-progress-graph-circle-fill--empty`],d:ee(p/2-s/2*(1+2*g)-l*g,s,p),"stroke-width":s,"stroke-linecap":"round",fill:"none",style:{strokeDasharray:c.value[g],strokeDashoffset:0,stroke:typeof h[g]=="object"?`url(#gradient-${g})`:h[g]}})))))),d&&m.default?o("div",null,o("div",{class:`${u}-progress-text`},m.default())):null)}}}),Be=L([y("progress",{display:"inline-block"},[y("progress-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 `),I("line",`
 width: 100%;
 display: block;
 `,[y("progress-content",`
 display: flex;
 align-items: center;
 `,[y("progress-graph",{flex:1})]),y("progress-custom-content",{marginLeft:"14px"}),y("progress-icon",`
 width: 30px;
 padding-left: 14px;
 height: var(--n-icon-size-line);
 line-height: var(--n-icon-size-line);
 font-size: var(--n-icon-size-line);
 `,[I("as-text",`
 color: var(--n-text-color-line-outer);
 text-align: center;
 width: 40px;
 font-size: var(--n-font-size);
 padding-left: 4px;
 transition: color .3s var(--n-bezier);
 `)])]),I("circle, dashboard",{width:"120px"},[y("progress-custom-content",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `),y("progress-text",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 color: inherit;
 font-size: var(--n-font-size-circle);
 color: var(--n-text-color-circle);
 font-weight: var(--n-font-weight-circle);
 transition: color .3s var(--n-bezier);
 white-space: nowrap;
 `),y("progress-icon",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 color: var(--n-icon-color);
 font-size: var(--n-icon-size-circle);
 `)]),I("multiple-circle",`
 width: 200px;
 color: inherit;
 `,[y("progress-text",`
 font-weight: var(--n-font-weight-circle);
 color: var(--n-text-color-circle);
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 transition: color .3s var(--n-bezier);
 `)]),y("progress-content",{position:"relative"}),y("progress-graph",{position:"relative"},[y("progress-graph-circle",[L("svg",{verticalAlign:"bottom"}),y("progress-graph-circle-fill",`
 stroke: var(--n-fill-color);
 transition:
 opacity .3s var(--n-bezier),
 stroke .3s var(--n-bezier),
 stroke-dasharray .3s var(--n-bezier);
 `,[I("empty",{opacity:0})]),y("progress-graph-circle-rail",`
 transition: stroke .3s var(--n-bezier);
 overflow: hidden;
 stroke: var(--n-rail-color);
 `)]),y("progress-graph-line",[I("indicator-inside",[y("progress-graph-line-rail",`
 height: 16px;
 line-height: 16px;
 border-radius: 10px;
 `,[y("progress-graph-line-fill",`
 height: inherit;
 border-radius: 10px;
 `),y("progress-graph-line-indicator",`
 background: #0000;
 white-space: nowrap;
 text-align: right;
 margin-left: 14px;
 margin-right: 14px;
 height: inherit;
 font-size: 12px;
 color: var(--n-text-color-line-inner);
 transition: color .3s var(--n-bezier);
 `)])]),I("indicator-inside-label",`
 height: 16px;
 display: flex;
 align-items: center;
 `,[y("progress-graph-line-rail",`
 flex: 1;
 transition: background-color .3s var(--n-bezier);
 `),y("progress-graph-line-indicator",`
 background: var(--n-fill-color);
 font-size: 12px;
 transform: translateZ(0);
 display: flex;
 vertical-align: middle;
 height: 16px;
 line-height: 16px;
 padding: 0 10px;
 border-radius: 10px;
 position: absolute;
 white-space: nowrap;
 color: var(--n-text-color-line-inner);
 transition:
 right .2s var(--n-bezier),
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `)]),y("progress-graph-line-rail",`
 position: relative;
 overflow: hidden;
 height: var(--n-rail-height);
 border-radius: 5px;
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 `,[y("progress-graph-line-fill",`
 background: var(--n-fill-color);
 position: relative;
 border-radius: 5px;
 height: inherit;
 width: 100%;
 max-width: 0%;
 transition:
 background-color .3s var(--n-bezier),
 max-width .2s var(--n-bezier);
 `,[I("processing",[L("&::after",`
 content: "";
 background-image: var(--n-line-bg-processing);
 animation: progress-processing-animation 2s var(--n-bezier) infinite;
 `)])])])])])]),L("@keyframes progress-processing-animation",`
 0% {
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 right: 100%;
 opacity: 1;
 }
 66% {
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 right: 0;
 opacity: 0;
 }
 100% {
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 right: 0;
 opacity: 0;
 }
 `)]),Pe=Object.assign(Object.assign({},re.props),{processing:Boolean,type:{type:String,default:"line"},gapDegree:Number,gapOffsetDegree:Number,status:{type:String,default:"default"},railColor:[String,Array],railStyle:[String,Array],color:[String,Array,Object],viewBoxWidth:{type:Number,default:100},strokeWidth:{type:Number,default:7},percentage:[Number,Array],unit:{type:String,default:"%"},showIndicator:{type:Boolean,default:!0},indicatorPosition:{type:String,default:"outside"},indicatorPlacement:{type:String,default:"outside"},indicatorTextColor:String,circleGap:{type:Number,default:1},height:Number,borderRadius:[String,Number],fillBorderRadius:[String,Number],offsetDegree:Number}),Re=W({name:"Progress",props:Pe,setup(t){const m=N(()=>t.indicatorPlacement||t.indicatorPosition),c=N(()=>{if(t.gapDegree||t.gapDegree===0)return t.gapDegree;if(t.type==="dashboard")return 75}),{mergedClsPrefixRef:f,inlineThemeDisabled:p}=se(t),s=re("Progress","-progress",Be,ce,t,f),l=N(()=>{const{status:h}=t,{common:{cubicBezierEaseInOut:b},self:{fontSize:k,fontSizeCircle:x,railColor:u,railHeight:w,iconSizeCircle:g,iconSizeLine:r,textColorCircle:n,textColorLineInner:v,textColorLineOuter:$,lineBgProcessing:R,fontWeightCircle:D,[U("iconColor",h)]:X,[U("fillColor",h)]:G}}=s.value;return{"--n-bezier":b,"--n-fill-color":G,"--n-font-size":k,"--n-font-size-circle":x,"--n-font-weight-circle":D,"--n-icon-color":X,"--n-icon-size-circle":g,"--n-icon-size-line":r,"--n-line-bg-processing":R,"--n-rail-color":u,"--n-rail-height":w,"--n-text-color-circle":n,"--n-text-color-line-inner":v,"--n-text-color-line-outer":$}}),d=p?de("progress",N(()=>t.status[0]),l,t):void 0;return{mergedClsPrefix:f,mergedIndicatorPlacement:m,gapDeg:c,cssVars:p?void 0:l,themeClass:d?.themeClass,onRender:d?.onRender}},render(){const{type:t,cssVars:m,indicatorTextColor:c,showIndicator:f,status:p,railColor:s,railStyle:l,color:d,percentage:h,viewBoxWidth:b,strokeWidth:k,mergedIndicatorPlacement:x,unit:u,borderRadius:w,fillBorderRadius:g,height:r,processing:n,circleGap:v,mergedClsPrefix:$,gapDeg:R,gapOffsetDegree:D,themeClass:X,$slots:G,onRender:F}=this;return F?.(),o("div",{class:[X,`${$}-progress`,`${$}-progress--${t}`,`${$}-progress--${p}`],style:m,"aria-valuemax":100,"aria-valuemin":0,"aria-valuenow":h,role:t==="circle"||t==="line"||t==="dashboard"?"progressbar":"none"},t==="circle"||t==="dashboard"?o(_e,{clsPrefix:$,status:p,showIndicator:f,indicatorTextColor:c,railColor:s,fillColor:d,railStyle:l,offsetDegree:this.offsetDegree,percentage:h,viewBoxWidth:b,strokeWidth:k,gapDegree:R===void 0?t==="dashboard"?75:0:R,gapOffsetDegree:D,unit:u},G):t==="line"?o(ze,{clsPrefix:$,status:p,showIndicator:f,indicatorTextColor:c,railColor:s,fillColor:d,railStyle:l,percentage:h,processing:n,indicatorPlacement:x,unit:u,fillBorderRadius:g,railBorderRadius:w,height:r},G):t==="multiple-circle"?o(Ne,{clsPrefix:$,strokeWidth:k,railColor:s,fillColor:d,railStyle:l,viewBoxWidth:b,percentage:h,showIndicator:f,circleGap:v},G):null)}}),De={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Ie=W({name:"AlertCircleOutline",render:function(m,c){return _(),P("svg",De,c[0]||(c[0]=[S("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),S("path",{d:"M250.26 166.05L256 288l5.73-121.95a5.74 5.74 0 0 0-5.79-6h0a5.74 5.74 0 0 0-5.68 6z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),S("path",{d:"M256 367.91a20 20 0 1 1 20-20a20 20 0 0 1-20 20z",fill:"currentColor"},null,-1)]))}}),Te={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},je=W({name:"TrendingUpOutline",render:function(m,c){return _(),P("svg",Te,c[0]||(c[0]=[S("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 144h112v112"},null,-1),S("path",{d:"M48 368l121.37-121.37a32 32 0 0 1 45.26 0l50.74 50.74a32 32 0 0 0 45.26 0L448 160",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Oe={class:"dashboard"},We={class:"dashboard-header"},Me={class:"stat-value"},qe={key:0,class:"change-list"},Ge={class:"task-name"},Ae={key:0,class:"more-hint"},Le=W({__name:"Dashboard",setup(t){const m=he(),c=ue(),f=be();let p=null;const s=ge(!0),l=r=>{if(r<60)return`${Math.floor(r)}秒`;if(r<3600)return`${Math.floor(r/60)}分钟`;if(r<86400){const n=Math.floor(r/3600),v=Math.floor(r%3600/60);return`${n}小时${v}分钟`}else{const n=Math.floor(r/86400),v=Math.floor(r%86400/3600);return`${n}天${v}小时`}},d=r=>{if(!r)return"-";try{return new Date(r).toLocaleString("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})}catch{return r}},h=N(()=>{const r=c.totalExecutions;return r===0?100:Math.round(c.successfulExecutions/r*100)}),b=N(()=>[...f.tasks].filter(r=>r.last_change).sort((r,n)=>{const v=new Date(r.last_change||0).getTime();return new Date(n.last_change||0).getTime()-v}).slice(0,5)),k=[{title:"任务名称",key:"name",ellipsis:{tooltip:!0}},{title:"状态",key:"status",width:100,render:r=>r.enabled?r.error_count>0?o(V,{type:"error",size:"small"},{default:()=>"错误"}):o(V,{type:"success",size:"small"},{default:()=>"正常"}):o(V,{type:"default",size:"small"},{default:()=>"已禁用"})},{title:"最后变化",key:"last_change",width:140,render:r=>d(r.last_change)},{title:"变化次数",key:"change_count",width:90,align:"center"}],x=async()=>{s.value=!0;try{await Promise.all([c.fetchStatus(),f.fetchTasks()])}finally{s.value=!1}},u=async()=>{await x()},w=()=>{m.push("/tasks")},g=()=>{m.push("/history")};return fe(async()=>{await x(),p=window.setInterval(x,3e4)}),pe(()=>{p&&clearInterval(p)}),(r,n)=>(_(),P("div",Oe,[i(e(xe),{show:s.value},{default:a(()=>[S("div",We,[n[0]||(n[0]=S("h2",{class:"page-title"},"仪表盘",-1)),i(e(A),{quaternary:"",circle:"",onClick:u},{icon:a(()=>[i(e(j),null,{default:a(()=>[i(e(ke))]),_:1})]),_:1})]),i(e(K),{cols:24,"x-gap":16,"y-gap":16},{default:a(()=>[i(e(q),{span:6},{default:a(()=>[i(e(O),{class:"stat-card"},{default:a(()=>[i(e(z),{vertical:""},{default:a(()=>[i(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:a(()=>[n[1]||(n[1]=S("span",{class:"stat-label"},"任务总数",-1)),i(e(j),{size:"24",color:"#63e2b7"},{default:a(()=>[i(e(Ce))]),_:1})]),_:1}),i(e(Y),{value:e(f).total},null,8,["value"]),i(e(T),{depth:"3"},{default:a(()=>[C("活跃: "+B(e(f).activeCount),1)]),_:1})]),_:1})]),_:1})]),_:1}),i(e(q),{span:6},{default:a(()=>[i(e(O),{class:"stat-card"},{default:a(()=>[i(e(z),{vertical:""},{default:a(()=>[i(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:a(()=>[n[2]||(n[2]=S("span",{class:"stat-label"},"检测到的变化",-1)),i(e(j),{size:"24",color:"#f2c97d"},{default:a(()=>[i(e(je))]),_:1})]),_:1}),i(e(Y),{value:e(c).totalChanges},null,8,["value"]),i(e(T),{depth:"3"},{default:a(()=>[C("执行次数: "+B(e(c).totalExecutions),1)]),_:1})]),_:1})]),_:1})]),_:1}),i(e(q),{span:6},{default:a(()=>[i(e(O),{class:"stat-card"},{default:a(()=>[i(e(z),{vertical:""},{default:a(()=>[i(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:a(()=>[n[3]||(n[3]=S("span",{class:"stat-label"},"成功率",-1)),i(e(j),{size:"24",color:"#70c0e8"},{default:a(()=>[i(e(Z))]),_:1})]),_:1}),i(e(Y),{value:h.value,suffix:"%"},null,8,["value"]),i(e(Re),{type:"line",percentage:h.value,"show-indicator":!1,height:4,color:h.value>=80?"#63e2b7":h.value>=50?"#f2c97d":"#e88080"},null,8,["percentage","color"])]),_:1})]),_:1})]),_:1}),i(e(q),{span:6},{default:a(()=>[i(e(O),{class:"stat-card"},{default:a(()=>[i(e(z),{vertical:""},{default:a(()=>[i(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:a(()=>[n[4]||(n[4]=S("span",{class:"stat-label"},"运行时间",-1)),i(e(j),{size:"24",color:e(c).isRunning?"#63e2b7":"#909399"},{default:a(()=>[i(e(ye))]),_:1},8,["color"])]),_:1}),S("div",Me,[e(c).isRunning?(_(),P(H,{key:0},[C(B(l(e(c).uptime)),1)],64)):(_(),E(e(T),{key:1,depth:"3"},{default:a(()=>[...n[5]||(n[5]=[C("已停止",-1)])]),_:1}))]),i(e(T),{depth:"3"},{default:a(()=>[n[6]||(n[6]=C(" 状态: ",-1)),i(e(T),{type:e(c).isRunning?"success":"default"},{default:a(()=>[C(B(e(c).isRunning?"运行中":"已停止"),1)]),_:1},8,["type"])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),i(e(K),{cols:24,"x-gap":16,"y-gap":16,style:{"margin-top":"16px"}},{default:a(()=>[i(e(q),{span:12},{default:a(()=>[i(e(O),{title:"最近变化",class:"list-card"},{"header-extra":a(()=>[i(e(A),{text:"",type:"primary",onClick:g},{default:a(()=>[...n[7]||(n[7]=[C("查看全部",-1)])]),_:1})]),default:a(()=>[b.value.length>0?(_(),P("div",qe,[(_(!0),P(H,null,me(b.value,v=>(_(),P("div",{key:v.id,class:"change-item"},[i(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:a(()=>[i(e(z),{align:"center"},{default:a(()=>[i(e(j),{color:"#63e2b7"},{default:a(()=>[i(e(Z))]),_:1}),S("span",Ge,B(v.name),1)]),_:2},1024),i(e(z),{align:"center"},{default:a(()=>[i(e(V),{size:"small",round:""},{default:a(()=>[C(B(v.change_count)+"次",1)]),_:2},1024),i(e(T),{depth:"3",style:{"font-size":"12px"}},{default:a(()=>[C(B(d(v.last_change)),1)]),_:2},1024)]),_:2},1024)]),_:2},1024)]))),128))])):(_(),E(e(Q),{key:1,description:"暂无变化记录"}))]),_:1})]),_:1}),i(e(q),{span:12},{default:a(()=>[i(e(O),{title:"任务概览",class:"list-card"},{"header-extra":a(()=>[i(e(A),{text:"",type:"primary",onClick:w},{default:a(()=>[...n[8]||(n[8]=[C("管理任务",-1)])]),_:1})]),default:a(()=>[e(f).tasks.length>0?(_(),P(H,{key:0},[i(e(we),{columns:k,data:e(f).tasks.slice(0,5),bordered:!1,size:"small",pagination:!1},null,8,["data"]),e(f).total>5?(_(),P("div",Ae,[i(e(T),{depth:"3"},{default:a(()=>[C("共 "+B(e(f).total)+" 个任务",1)]),_:1})])):J("",!0)],64)):(_(),E(e(Q),{key:1,description:"暂无任务"},{extra:a(()=>[i(e(A),{size:"small",onClick:w},{default:a(()=>[...n[9]||(n[9]=[C("添加任务",-1)])]),_:1})]),_:1}))]),_:1})]),_:1})]),_:1}),e(f).errorCount>0?(_(),E(e(O),{key:0,class:"error-card",style:{"margin-top":"16px"}},{default:a(()=>[i(e(z),{align:"center"},{default:a(()=>[i(e(j),{size:"20",color:"#e88080"},{default:a(()=>[i(e(Ie))]),_:1}),i(e(T),{type:"error"},{default:a(()=>[C(B(e(f).errorCount)+" 个任务存在错误，请检查任务配置 ",1)]),_:1}),i(e(A),{size:"small",text:"",type:"primary",onClick:w},{default:a(()=>[...n[10]||(n[10]=[C(" 查看详情 ",-1)])]),_:1})]),_:1})]),_:1})):J("",!0)]),_:1},8,["show"])]))}}),Ye=ve(Le,[["__scopeId","data-v-2307ecea"]]);export{Ye as default};
