import{d as O,c as N,m as se,h as l,N as te,f as M,a as V,b as h,e as I,u as ne,g as re,p as ce,i as U,j as de,k as P,o as $,l as S,n as ue,q as ge,r as fe,s as pe,t as he,v as r,w as o,x as e,y as ye,z as A,A as H,B as z,C as me,D as C,E as T,W as ve,F as L,G as j,H as B,T as be,I as Y,J as xe,_ as ke}from"./index-BXrhl0aj.js";import{I as ie,W as oe,E as le,S as ae,N as we,a as E,R as Ce,b as W,c as K}from"./RefreshOutline-DrsxFm1q.js";import{N as Z,a as q,b as J,C as Q}from"./CheckmarkCircleOutline-CmUV44st.js";import{F as $e}from"./FlashOutline-CkFrgqm2.js";import{N as Se}from"./DataTable-HTkUYJTf.js";const _e={success:l(ae,null),error:l(le,null),warning:l(oe,null),info:l(ie,null)},ze=O({name:"ProgressCircle",props:{clsPrefix:{type:String,required:!0},status:{type:String,required:!0},strokeWidth:{type:Number,required:!0},fillColor:[String,Object],railColor:String,railStyle:[String,Object],percentage:{type:Number,default:0},offsetDegree:{type:Number,default:0},showIndicator:{type:Boolean,required:!0},indicatorTextColor:String,unit:String,viewBoxWidth:{type:Number,required:!0},gapDegree:{type:Number,required:!0},gapOffsetDegree:{type:Number,default:0}},setup(t,{slots:m}){const c=N(()=>{const n="gradient",{fillColor:s}=t;return typeof s=="object"?`${n}-${se(JSON.stringify(s))}`:n});function f(n,s,d,p){const{gapDegree:b,viewBoxWidth:x,strokeWidth:k}=t,u=50,w=0,g=u,i=0,a=2*u,v=50+k/2,_=`M ${v},${v} m ${w},${g}
      a ${u},${u} 0 1 1 ${i},${-a}
      a ${u},${u} 0 1 1 ${-i},${a}`,R=Math.PI*2*u,D={stroke:p==="rail"?d:typeof t.fillColor=="object"?`url(#${c.value})`:d,strokeDasharray:`${Math.min(n,100)/100*(R-b)}px ${x*8}px`,strokeDashoffset:`-${b/2}px`,transformOrigin:s?"center":void 0,transform:s?`rotate(${s}deg)`:void 0};return{pathString:_,pathStyle:D}}const y=()=>{const n=typeof t.fillColor=="object",s=n?t.fillColor.stops[0]:"",d=n?t.fillColor.stops[1]:"";return n&&l("defs",null,l("linearGradient",{id:c.value,x1:"0%",y1:"100%",x2:"100%",y2:"0%"},l("stop",{offset:"0%","stop-color":s}),l("stop",{offset:"100%","stop-color":d})))};return()=>{const{fillColor:n,railColor:s,strokeWidth:d,offsetDegree:p,status:b,percentage:x,showIndicator:k,indicatorTextColor:u,unit:w,gapOffsetDegree:g,clsPrefix:i}=t,{pathString:a,pathStyle:v}=f(100,0,s,"rail"),{pathString:_,pathStyle:R}=f(x,p,n,"fill"),D=100+d;return l("div",{class:`${i}-progress-content`,role:"none"},l("div",{class:`${i}-progress-graph`,"aria-hidden":!0},l("div",{class:`${i}-progress-graph-circle`,style:{transform:g?`rotate(${g}deg)`:void 0}},l("svg",{viewBox:`0 0 ${D} ${D}`},y(),l("g",null,l("path",{class:`${i}-progress-graph-circle-rail`,d:a,"stroke-width":d,"stroke-linecap":"round",fill:"none",style:v})),l("g",null,l("path",{class:[`${i}-progress-graph-circle-fill`,x===0&&`${i}-progress-graph-circle-fill--empty`],d:_,"stroke-width":d,"stroke-linecap":"round",fill:"none",style:R}))))),k?l("div",null,m.default?l("div",{class:`${i}-progress-custom-content`,role:"none"},m.default()):b!=="default"?l("div",{class:`${i}-progress-icon`,"aria-hidden":!0},l(te,{clsPrefix:i},{default:()=>_e[b]})):l("div",{class:`${i}-progress-text`,style:{color:u},role:"none"},l("span",{class:`${i}-progress-text__percentage`},x),l("span",{class:`${i}-progress-text__unit`},w))):null)}}}),Ne={success:l(ae,null),error:l(le,null),warning:l(oe,null),info:l(ie,null)},Be=O({name:"ProgressLine",props:{clsPrefix:{type:String,required:!0},percentage:{type:Number,default:0},railColor:String,railStyle:[String,Object],fillColor:[String,Object],status:{type:String,required:!0},indicatorPlacement:{type:String,required:!0},indicatorTextColor:String,unit:{type:String,default:"%"},processing:{type:Boolean,required:!0},showIndicator:{type:Boolean,required:!0},height:[String,Number],railBorderRadius:[String,Number],fillBorderRadius:[String,Number]},setup(t,{slots:m}){const c=N(()=>M(t.height)),f=N(()=>{var s,d;return typeof t.fillColor=="object"?`linear-gradient(to right, ${(s=t.fillColor)===null||s===void 0?void 0:s.stops[0]} , ${(d=t.fillColor)===null||d===void 0?void 0:d.stops[1]})`:t.fillColor}),y=N(()=>t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):""),n=N(()=>t.fillBorderRadius!==void 0?M(t.fillBorderRadius):t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):"");return()=>{const{indicatorPlacement:s,railColor:d,railStyle:p,percentage:b,unit:x,indicatorTextColor:k,status:u,showIndicator:w,processing:g,clsPrefix:i}=t;return l("div",{class:`${i}-progress-content`,role:"none"},l("div",{class:`${i}-progress-graph`,"aria-hidden":!0},l("div",{class:[`${i}-progress-graph-line`,{[`${i}-progress-graph-line--indicator-${s}`]:!0}]},l("div",{class:`${i}-progress-graph-line-rail`,style:[{backgroundColor:d,height:c.value,borderRadius:y.value},p]},l("div",{class:[`${i}-progress-graph-line-fill`,g&&`${i}-progress-graph-line-fill--processing`],style:{maxWidth:`${t.percentage}%`,background:f.value,height:c.value,lineHeight:c.value,borderRadius:n.value}},s==="inside"?l("div",{class:`${i}-progress-graph-line-indicator`,style:{color:k}},m.default?m.default():`${b}${x}`):null)))),w&&s==="outside"?l("div",null,m.default?l("div",{class:`${i}-progress-custom-content`,style:{color:k},role:"none"},m.default()):u==="default"?l("div",{role:"none",class:`${i}-progress-icon ${i}-progress-icon--as-text`,style:{color:k}},b,x):l("div",{class:`${i}-progress-icon`,"aria-hidden":!0},l(te,{clsPrefix:i},{default:()=>Ne[u]}))):null)}}});function ee(t,m,c=100){return`m ${c/2} ${c/2-t} a ${t} ${t} 0 1 1 0 ${2*t} a ${t} ${t} 0 1 1 0 -${2*t}`}const Pe=O({name:"ProgressMultipleCircle",props:{clsPrefix:{type:String,required:!0},viewBoxWidth:{type:Number,required:!0},percentage:{type:Array,default:[0]},strokeWidth:{type:Number,required:!0},circleGap:{type:Number,required:!0},showIndicator:{type:Boolean,required:!0},fillColor:{type:Array,default:()=>[]},railColor:{type:Array,default:()=>[]},railStyle:{type:Array,default:()=>[]}},setup(t,{slots:m}){const c=N(()=>t.percentage.map((n,s)=>`${Math.PI*n/100*(t.viewBoxWidth/2-t.strokeWidth/2*(1+2*s)-t.circleGap*s)*2}, ${t.viewBoxWidth*8}`)),f=(y,n)=>{const s=t.fillColor[n],d=typeof s=="object"?s.stops[0]:"",p=typeof s=="object"?s.stops[1]:"";return typeof t.fillColor[n]=="object"&&l("linearGradient",{id:`gradient-${n}`,x1:"100%",y1:"0%",x2:"0%",y2:"100%"},l("stop",{offset:"0%","stop-color":d}),l("stop",{offset:"100%","stop-color":p}))};return()=>{const{viewBoxWidth:y,strokeWidth:n,circleGap:s,showIndicator:d,fillColor:p,railColor:b,railStyle:x,percentage:k,clsPrefix:u}=t;return l("div",{class:`${u}-progress-content`,role:"none"},l("div",{class:`${u}-progress-graph`,"aria-hidden":!0},l("div",{class:`${u}-progress-graph-circle`},l("svg",{viewBox:`0 0 ${y} ${y}`},l("defs",null,k.map((w,g)=>f(w,g))),k.map((w,g)=>l("g",{key:g},l("path",{class:`${u}-progress-graph-circle-rail`,d:ee(y/2-n/2*(1+2*g)-s*g,n,y),"stroke-width":n,"stroke-linecap":"round",fill:"none",style:[{strokeDashoffset:0,stroke:b[g]},x[g]]}),l("path",{class:[`${u}-progress-graph-circle-fill`,w===0&&`${u}-progress-graph-circle-fill--empty`],d:ee(y/2-n/2*(1+2*g)-s*g,n,y),"stroke-width":n,"stroke-linecap":"round",fill:"none",style:{strokeDasharray:c.value[g],strokeDashoffset:0,stroke:typeof p[g]=="object"?`url(#gradient-${g})`:p[g]}})))))),d&&m.default?l("div",null,l("div",{class:`${u}-progress-text`},m.default())):null)}}}),Re=V([h("progress",{display:"inline-block"},[h("progress-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 `),I("line",`
 width: 100%;
 display: block;
 `,[h("progress-content",`
 display: flex;
 align-items: center;
 `,[h("progress-graph",{flex:1})]),h("progress-custom-content",{marginLeft:"14px"}),h("progress-icon",`
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
 `)])]),I("circle, dashboard",{width:"120px"},[h("progress-custom-content",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `),h("progress-text",`
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
 `),h("progress-icon",`
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
 `,[h("progress-text",`
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
 `)]),h("progress-content",{position:"relative"}),h("progress-graph",{position:"relative"},[h("progress-graph-circle",[V("svg",{verticalAlign:"bottom"}),h("progress-graph-circle-fill",`
 stroke: var(--n-fill-color);
 transition:
 opacity .3s var(--n-bezier),
 stroke .3s var(--n-bezier),
 stroke-dasharray .3s var(--n-bezier);
 `,[I("empty",{opacity:0})]),h("progress-graph-circle-rail",`
 transition: stroke .3s var(--n-bezier);
 overflow: hidden;
 stroke: var(--n-rail-color);
 `)]),h("progress-graph-line",[I("indicator-inside",[h("progress-graph-line-rail",`
 height: 16px;
 line-height: 16px;
 border-radius: 10px;
 `,[h("progress-graph-line-fill",`
 height: inherit;
 border-radius: 10px;
 `),h("progress-graph-line-indicator",`
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
 `,[h("progress-graph-line-rail",`
 flex: 1;
 transition: background-color .3s var(--n-bezier);
 `),h("progress-graph-line-indicator",`
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
 `)]),h("progress-graph-line-rail",`
 position: relative;
 overflow: hidden;
 height: var(--n-rail-height);
 border-radius: 5px;
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 `,[h("progress-graph-line-fill",`
 background: var(--n-fill-color);
 position: relative;
 border-radius: 5px;
 height: inherit;
 width: 100%;
 max-width: 0%;
 transition:
 background-color .3s var(--n-bezier),
 max-width .2s var(--n-bezier);
 `,[I("processing",[V("&::after",`
 content: "";
 background-image: var(--n-line-bg-processing);
 animation: progress-processing-animation 2s var(--n-bezier) infinite;
 `)])])])])])]),V("@keyframes progress-processing-animation",`
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
 `)]),De=Object.assign(Object.assign({},re.props),{processing:Boolean,type:{type:String,default:"line"},gapDegree:Number,gapOffsetDegree:Number,status:{type:String,default:"default"},railColor:[String,Array],railStyle:[String,Array],color:[String,Array,Object],viewBoxWidth:{type:Number,default:100},strokeWidth:{type:Number,default:7},percentage:[Number,Array],unit:{type:String,default:"%"},showIndicator:{type:Boolean,default:!0},indicatorPosition:{type:String,default:"outside"},indicatorPlacement:{type:String,default:"outside"},indicatorTextColor:String,circleGap:{type:Number,default:1},height:Number,borderRadius:[String,Number],fillBorderRadius:[String,Number],offsetDegree:Number}),Ie=O({name:"Progress",props:De,setup(t){const m=N(()=>t.indicatorPlacement||t.indicatorPosition),c=N(()=>{if(t.gapDegree||t.gapDegree===0)return t.gapDegree;if(t.type==="dashboard")return 75}),{mergedClsPrefixRef:f,inlineThemeDisabled:y}=ne(t),n=re("Progress","-progress",Re,ce,t,f),s=N(()=>{const{status:p}=t,{common:{cubicBezierEaseInOut:b},self:{fontSize:x,fontSizeCircle:k,railColor:u,railHeight:w,iconSizeCircle:g,iconSizeLine:i,textColorCircle:a,textColorLineInner:v,textColorLineOuter:_,lineBgProcessing:R,fontWeightCircle:D,[U("iconColor",p)]:X,[U("fillColor",p)]:G}}=n.value;return{"--n-bezier":b,"--n-fill-color":G,"--n-font-size":x,"--n-font-size-circle":k,"--n-font-weight-circle":D,"--n-icon-color":X,"--n-icon-size-circle":g,"--n-icon-size-line":i,"--n-line-bg-processing":R,"--n-rail-color":u,"--n-rail-height":w,"--n-text-color-circle":a,"--n-text-color-line-inner":v,"--n-text-color-line-outer":_}}),d=y?de("progress",N(()=>t.status[0]),s,t):void 0;return{mergedClsPrefix:f,mergedIndicatorPlacement:m,gapDeg:c,cssVars:y?void 0:s,themeClass:d?.themeClass,onRender:d?.onRender}},render(){const{type:t,cssVars:m,indicatorTextColor:c,showIndicator:f,status:y,railColor:n,railStyle:s,color:d,percentage:p,viewBoxWidth:b,strokeWidth:x,mergedIndicatorPlacement:k,unit:u,borderRadius:w,fillBorderRadius:g,height:i,processing:a,circleGap:v,mergedClsPrefix:_,gapDeg:R,gapOffsetDegree:D,themeClass:X,$slots:G,onRender:F}=this;return F?.(),l("div",{class:[X,`${_}-progress`,`${_}-progress--${t}`,`${_}-progress--${y}`],style:m,"aria-valuemax":100,"aria-valuemin":0,"aria-valuenow":p,role:t==="circle"||t==="line"||t==="dashboard"?"progressbar":"none"},t==="circle"||t==="dashboard"?l(ze,{clsPrefix:_,status:y,showIndicator:f,indicatorTextColor:c,railColor:n,fillColor:d,railStyle:s,offsetDegree:this.offsetDegree,percentage:p,viewBoxWidth:b,strokeWidth:x,gapDegree:R===void 0?t==="dashboard"?75:0:R,gapOffsetDegree:D,unit:u},G):t==="line"?l(Be,{clsPrefix:_,status:y,showIndicator:f,indicatorTextColor:c,railColor:n,fillColor:d,railStyle:s,percentage:p,processing:a,indicatorPlacement:k,unit:u,fillBorderRadius:g,railBorderRadius:w,height:i},G):t==="multiple-circle"?l(Pe,{clsPrefix:_,strokeWidth:x,railColor:n,fillColor:d,railStyle:s,viewBoxWidth:b,percentage:p,showIndicator:f,circleGap:v},G):null)}}),Te={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},je=O({name:"AlertCircleOutline",render:function(m,c){return $(),P("svg",Te,c[0]||(c[0]=[S("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),S("path",{d:"M250.26 166.05L256 288l5.73-121.95a5.74 5.74 0 0 0-5.79-6h0a5.74 5.74 0 0 0-5.68 6z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),S("path",{d:"M256 367.91a20 20 0 1 1 20-20a20 20 0 0 1-20 20z",fill:"currentColor"},null,-1)]))}}),We={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Oe=O({name:"TrendingUpOutline",render:function(m,c){return $(),P("svg",We,c[0]||(c[0]=[S("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 144h112v112"},null,-1),S("path",{d:"M48 368l121.37-121.37a32 32 0 0 1 45.26 0l50.74 50.74a32 32 0 0 0 45.26 0L448 160",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Me={class:"dashboard"},qe={class:"dashboard-header"},Ge={class:"stat-value"},Ae={key:0,class:"change-list"},Le={class:"task-name"},Ee={key:0,class:"more-hint"},Ve=O({__name:"Dashboard",setup(t){const m=ye(),c=ue(),f=ge(),y=fe(),n=pe(!0),s=i=>{if(i<60)return`${Math.floor(i)}秒`;if(i<3600)return`${Math.floor(i/60)}分钟`;if(i<86400){const a=Math.floor(i/3600),v=Math.floor(i%3600/60);return`${a}小时${v}分钟`}else{const a=Math.floor(i/86400),v=Math.floor(i%86400/3600);return`${a}天${v}小时`}},d=i=>{if(!i)return"-";try{return new Date(i).toLocaleString("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})}catch{return i}},p=N(()=>{const i=c.totalExecutions;return i===0?100:Math.round(c.successfulExecutions/i*100)}),b=N(()=>[...f.tasks].filter(i=>i.last_change).sort((i,a)=>{const v=new Date(i.last_change||0).getTime();return new Date(a.last_change||0).getTime()-v}).slice(0,5)),x=[{title:"任务名称",key:"name",ellipsis:{tooltip:!0}},{title:"状态",key:"status",width:100,render:i=>i.enabled?i.error_count>0?l(E,{type:"error",size:"small"},{default:()=>"错误"}):l(E,{type:"success",size:"small"},{default:()=>"正常"}):l(E,{type:"default",size:"small"},{default:()=>"已禁用"})},{title:"最后变化",key:"last_change",width:140,render:i=>d(i.last_change)},{title:"变化次数",key:"change_count",width:90,align:"center"}],k=async()=>{n.value=!0;try{await Promise.all([c.fetchStatus(),f.fetchTasks()])}finally{n.value=!1}},u=async()=>{await k()},w=()=>{m.push("/tasks")},g=()=>{m.push("/history")};return he(async()=>{await k()}),(i,a)=>($(),P("div",Me,[r(e(we),{show:n.value},{default:o(()=>[S("div",qe,[r(e(z),{align:"center"},{default:o(()=>[a[2]||(a[2]=S("h2",{class:"page-title"},"仪表盘",-1)),e(y).isConnected?($(),A(e(me),{key:0,trigger:"hover"},{trigger:o(()=>[r(e(E),{type:"success",size:"small",round:""},{icon:o(()=>[r(e(T),null,{default:o(()=>[r(e(ve))]),_:1})]),default:o(()=>[a[0]||(a[0]=C(" 实时更新 ",-1))]),_:1})]),default:o(()=>[a[1]||(a[1]=S("span",null,"SSE 实时连接已建立，数据将自动更新",-1))]),_:1})):H("",!0)]),_:1}),r(e(L),{quaternary:"",circle:"",onClick:u,loading:n.value},{icon:o(()=>[r(e(T),null,{default:o(()=>[r(e(Ce))]),_:1})]),_:1},8,["loading"])]),r(e(Z),{cols:24,"x-gap":16,"y-gap":16},{default:o(()=>[r(e(q),{span:6},{default:o(()=>[r(e(W),{class:"stat-card"},{default:o(()=>[r(e(z),{vertical:""},{default:o(()=>[r(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[a[3]||(a[3]=S("span",{class:"stat-label"},"任务总数",-1)),r(e(T),{size:"24",color:"#63e2b7"},{default:o(()=>[r(e($e))]),_:1})]),_:1}),r(e(J),{value:e(f).total},null,8,["value"]),r(e(j),{depth:"3"},{default:o(()=>[C("活跃: "+B(e(f).activeCount),1)]),_:1})]),_:1})]),_:1})]),_:1}),r(e(q),{span:6},{default:o(()=>[r(e(W),{class:"stat-card"},{default:o(()=>[r(e(z),{vertical:""},{default:o(()=>[r(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[a[4]||(a[4]=S("span",{class:"stat-label"},"检测到的变化",-1)),r(e(T),{size:"24",color:"#f2c97d"},{default:o(()=>[r(e(Oe))]),_:1})]),_:1}),r(e(J),{value:e(c).totalChanges},null,8,["value"]),r(e(j),{depth:"3"},{default:o(()=>[C("执行次数: "+B(e(c).totalExecutions),1)]),_:1})]),_:1})]),_:1})]),_:1}),r(e(q),{span:6},{default:o(()=>[r(e(W),{class:"stat-card"},{default:o(()=>[r(e(z),{vertical:""},{default:o(()=>[r(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[a[5]||(a[5]=S("span",{class:"stat-label"},"成功率",-1)),r(e(T),{size:"24",color:"#70c0e8"},{default:o(()=>[r(e(Q))]),_:1})]),_:1}),r(e(J),{value:p.value,suffix:"%"},null,8,["value"]),r(e(Ie),{type:"line",percentage:p.value,"show-indicator":!1,height:4,color:p.value>=80?"#63e2b7":p.value>=50?"#f2c97d":"#e88080"},null,8,["percentage","color"])]),_:1})]),_:1})]),_:1}),r(e(q),{span:6},{default:o(()=>[r(e(W),{class:"stat-card"},{default:o(()=>[r(e(z),{vertical:""},{default:o(()=>[r(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[a[6]||(a[6]=S("span",{class:"stat-label"},"运行时间",-1)),r(e(T),{size:"24",color:e(c).isRunning?"#63e2b7":"#909399"},{default:o(()=>[r(e(be))]),_:1},8,["color"])]),_:1}),S("div",Ge,[e(c).isRunning?($(),P(Y,{key:0},[C(B(s(e(c).uptime)),1)],64)):($(),A(e(j),{key:1,depth:"3"},{default:o(()=>[...a[7]||(a[7]=[C("已停止",-1)])]),_:1}))]),r(e(j),{depth:"3"},{default:o(()=>[a[8]||(a[8]=C(" 状态: ",-1)),r(e(j),{type:e(c).isRunning?"success":"default"},{default:o(()=>[C(B(e(c).isRunning?"运行中":"已停止"),1)]),_:1},8,["type"])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),r(e(Z),{cols:24,"x-gap":16,"y-gap":16,style:{"margin-top":"16px"}},{default:o(()=>[r(e(q),{span:12},{default:o(()=>[r(e(W),{title:"最近变化",class:"list-card"},{"header-extra":o(()=>[r(e(L),{text:"",type:"primary",onClick:g},{default:o(()=>[...a[9]||(a[9]=[C("查看全部",-1)])]),_:1})]),default:o(()=>[b.value.length>0?($(),P("div",Ae,[($(!0),P(Y,null,xe(b.value,v=>($(),P("div",{key:v.id,class:"change-item"},[r(e(z),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[r(e(z),{align:"center"},{default:o(()=>[r(e(T),{color:"#63e2b7"},{default:o(()=>[r(e(Q))]),_:1}),S("span",Le,B(v.name),1)]),_:2},1024),r(e(z),{align:"center"},{default:o(()=>[r(e(E),{size:"small",round:""},{default:o(()=>[C(B(v.change_count)+"次",1)]),_:2},1024),r(e(j),{depth:"3",style:{"font-size":"12px"}},{default:o(()=>[C(B(d(v.last_change)),1)]),_:2},1024)]),_:2},1024)]),_:2},1024)]))),128))])):($(),A(e(K),{key:1,description:"暂无变化记录"}))]),_:1})]),_:1}),r(e(q),{span:12},{default:o(()=>[r(e(W),{title:"任务概览",class:"list-card"},{"header-extra":o(()=>[r(e(L),{text:"",type:"primary",onClick:w},{default:o(()=>[...a[10]||(a[10]=[C("管理任务",-1)])]),_:1})]),default:o(()=>[e(f).tasks.length>0?($(),P(Y,{key:0},[r(e(Se),{columns:x,data:e(f).tasks.slice(0,5),bordered:!1,size:"small",pagination:!1},null,8,["data"]),e(f).total>5?($(),P("div",Ee,[r(e(j),{depth:"3"},{default:o(()=>[C("共 "+B(e(f).total)+" 个任务",1)]),_:1})])):H("",!0)],64)):($(),A(e(K),{key:1,description:"暂无任务"},{extra:o(()=>[r(e(L),{size:"small",onClick:w},{default:o(()=>[...a[11]||(a[11]=[C("添加任务",-1)])]),_:1})]),_:1}))]),_:1})]),_:1})]),_:1}),e(f).errorCount>0?($(),A(e(W),{key:0,class:"error-card",style:{"margin-top":"16px"}},{default:o(()=>[r(e(z),{align:"center"},{default:o(()=>[r(e(T),{size:"20",color:"#e88080"},{default:o(()=>[r(e(je))]),_:1}),r(e(j),{type:"error"},{default:o(()=>[C(B(e(f).errorCount)+" 个任务存在错误，请检查任务配置 ",1)]),_:1}),r(e(L),{size:"small",text:"",type:"primary",onClick:w},{default:o(()=>[...a[12]||(a[12]=[C(" 查看详情 ",-1)])]),_:1})]),_:1})]),_:1})):H("",!0)]),_:1},8,["show"])]))}}),Ue=ke(Ve,[["__scopeId","data-v-e4deed47"]]);export{Ue as default};
