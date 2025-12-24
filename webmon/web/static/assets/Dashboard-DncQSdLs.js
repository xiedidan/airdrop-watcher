import{d as W,c as N,m as ae,h as o,N as te,f as q,a as V,b as m,e as I,u as se,g as re,p as ce,i as U,j as de,k as D,o as S,l as z,n as ue,q as ge,r as fe,s as pe,t as he,v as r,w as i,x as e,y as ye,z as j,A as H,B as _,C as me,D as $,E as R,W as ve,F as G,G as B,S as be,P as xe,H as O,T as ke,I as Y,J as we,_ as Ce}from"./index-D1UTLBHZ.js";import{I as ie,W as oe,E as le,S as ne,N as $e,a as E,R as Se,b as M,c as K}from"./RefreshOutline-mAhTtdF8.js";import{N as Z,a as A,b as J,C as Q}from"./CheckmarkCircleOutline-DbKc66Ds.js";import{F as _e}from"./FlashOutline-KqVfevxK.js";import{N as ze}from"./DataTable-BBBAetvx.js";const Ne={success:o(ne,null),error:o(le,null),warning:o(oe,null),info:o(ie,null)},Be=W({name:"ProgressCircle",props:{clsPrefix:{type:String,required:!0},status:{type:String,required:!0},strokeWidth:{type:Number,required:!0},fillColor:[String,Object],railColor:String,railStyle:[String,Object],percentage:{type:Number,default:0},offsetDegree:{type:Number,default:0},showIndicator:{type:Boolean,required:!0},indicatorTextColor:String,unit:String,viewBoxWidth:{type:Number,required:!0},gapDegree:{type:Number,required:!0},gapOffsetDegree:{type:Number,default:0}},setup(t,{slots:b}){const n=N(()=>{const s="gradient",{fillColor:a}=t;return typeof a=="object"?`${s}-${ae(JSON.stringify(a))}`:s});function p(s,a,u,h){const{gapDegree:x,viewBoxWidth:k,strokeWidth:w}=t,g=50,C=0,f=g,c=0,d=2*g,l=50+w/2,y=`M ${l},${l} m ${C},${f}
      a ${g},${g} 0 1 1 ${c},${-d}
      a ${g},${g} 0 1 1 ${-c},${d}`,P=Math.PI*2*g,T={stroke:h==="rail"?u:typeof t.fillColor=="object"?`url(#${n.value})`:u,strokeDasharray:`${Math.min(s,100)/100*(P-x)}px ${k*8}px`,strokeDashoffset:`-${x/2}px`,transformOrigin:a?"center":void 0,transform:a?`rotate(${a}deg)`:void 0};return{pathString:y,pathStyle:T}}const v=()=>{const s=typeof t.fillColor=="object",a=s?t.fillColor.stops[0]:"",u=s?t.fillColor.stops[1]:"";return s&&o("defs",null,o("linearGradient",{id:n.value,x1:"0%",y1:"100%",x2:"100%",y2:"0%"},o("stop",{offset:"0%","stop-color":a}),o("stop",{offset:"100%","stop-color":u})))};return()=>{const{fillColor:s,railColor:a,strokeWidth:u,offsetDegree:h,status:x,percentage:k,showIndicator:w,indicatorTextColor:g,unit:C,gapOffsetDegree:f,clsPrefix:c}=t,{pathString:d,pathStyle:l}=p(100,0,a,"rail"),{pathString:y,pathStyle:P}=p(k,h,s,"fill"),T=100+u;return o("div",{class:`${c}-progress-content`,role:"none"},o("div",{class:`${c}-progress-graph`,"aria-hidden":!0},o("div",{class:`${c}-progress-graph-circle`,style:{transform:f?`rotate(${f}deg)`:void 0}},o("svg",{viewBox:`0 0 ${T} ${T}`},v(),o("g",null,o("path",{class:`${c}-progress-graph-circle-rail`,d,"stroke-width":u,"stroke-linecap":"round",fill:"none",style:l})),o("g",null,o("path",{class:[`${c}-progress-graph-circle-fill`,k===0&&`${c}-progress-graph-circle-fill--empty`],d:y,"stroke-width":u,"stroke-linecap":"round",fill:"none",style:P}))))),w?o("div",null,b.default?o("div",{class:`${c}-progress-custom-content`,role:"none"},b.default()):x!=="default"?o("div",{class:`${c}-progress-icon`,"aria-hidden":!0},o(te,{clsPrefix:c},{default:()=>Ne[x]})):o("div",{class:`${c}-progress-text`,style:{color:g},role:"none"},o("span",{class:`${c}-progress-text__percentage`},k),o("span",{class:`${c}-progress-text__unit`},C))):null)}}}),Pe={success:o(ne,null),error:o(le,null),warning:o(oe,null),info:o(ie,null)},Re=W({name:"ProgressLine",props:{clsPrefix:{type:String,required:!0},percentage:{type:Number,default:0},railColor:String,railStyle:[String,Object],fillColor:[String,Object],status:{type:String,required:!0},indicatorPlacement:{type:String,required:!0},indicatorTextColor:String,unit:{type:String,default:"%"},processing:{type:Boolean,required:!0},showIndicator:{type:Boolean,required:!0},height:[String,Number],railBorderRadius:[String,Number],fillBorderRadius:[String,Number]},setup(t,{slots:b}){const n=N(()=>q(t.height)),p=N(()=>{var a,u;return typeof t.fillColor=="object"?`linear-gradient(to right, ${(a=t.fillColor)===null||a===void 0?void 0:a.stops[0]} , ${(u=t.fillColor)===null||u===void 0?void 0:u.stops[1]})`:t.fillColor}),v=N(()=>t.railBorderRadius!==void 0?q(t.railBorderRadius):t.height!==void 0?q(t.height,{c:.5}):""),s=N(()=>t.fillBorderRadius!==void 0?q(t.fillBorderRadius):t.railBorderRadius!==void 0?q(t.railBorderRadius):t.height!==void 0?q(t.height,{c:.5}):"");return()=>{const{indicatorPlacement:a,railColor:u,railStyle:h,percentage:x,unit:k,indicatorTextColor:w,status:g,showIndicator:C,processing:f,clsPrefix:c}=t;return o("div",{class:`${c}-progress-content`,role:"none"},o("div",{class:`${c}-progress-graph`,"aria-hidden":!0},o("div",{class:[`${c}-progress-graph-line`,{[`${c}-progress-graph-line--indicator-${a}`]:!0}]},o("div",{class:`${c}-progress-graph-line-rail`,style:[{backgroundColor:u,height:n.value,borderRadius:v.value},h]},o("div",{class:[`${c}-progress-graph-line-fill`,f&&`${c}-progress-graph-line-fill--processing`],style:{maxWidth:`${t.percentage}%`,background:p.value,height:n.value,lineHeight:n.value,borderRadius:s.value}},a==="inside"?o("div",{class:`${c}-progress-graph-line-indicator`,style:{color:w}},b.default?b.default():`${x}${k}`):null)))),C&&a==="outside"?o("div",null,b.default?o("div",{class:`${c}-progress-custom-content`,style:{color:w},role:"none"},b.default()):g==="default"?o("div",{role:"none",class:`${c}-progress-icon ${c}-progress-icon--as-text`,style:{color:w}},x,k):o("div",{class:`${c}-progress-icon`,"aria-hidden":!0},o(te,{clsPrefix:c},{default:()=>Pe[g]}))):null)}}});function ee(t,b,n=100){return`m ${n/2} ${n/2-t} a ${t} ${t} 0 1 1 0 ${2*t} a ${t} ${t} 0 1 1 0 -${2*t}`}const De=W({name:"ProgressMultipleCircle",props:{clsPrefix:{type:String,required:!0},viewBoxWidth:{type:Number,required:!0},percentage:{type:Array,default:[0]},strokeWidth:{type:Number,required:!0},circleGap:{type:Number,required:!0},showIndicator:{type:Boolean,required:!0},fillColor:{type:Array,default:()=>[]},railColor:{type:Array,default:()=>[]},railStyle:{type:Array,default:()=>[]}},setup(t,{slots:b}){const n=N(()=>t.percentage.map((s,a)=>`${Math.PI*s/100*(t.viewBoxWidth/2-t.strokeWidth/2*(1+2*a)-t.circleGap*a)*2}, ${t.viewBoxWidth*8}`)),p=(v,s)=>{const a=t.fillColor[s],u=typeof a=="object"?a.stops[0]:"",h=typeof a=="object"?a.stops[1]:"";return typeof t.fillColor[s]=="object"&&o("linearGradient",{id:`gradient-${s}`,x1:"100%",y1:"0%",x2:"0%",y2:"100%"},o("stop",{offset:"0%","stop-color":u}),o("stop",{offset:"100%","stop-color":h}))};return()=>{const{viewBoxWidth:v,strokeWidth:s,circleGap:a,showIndicator:u,fillColor:h,railColor:x,railStyle:k,percentage:w,clsPrefix:g}=t;return o("div",{class:`${g}-progress-content`,role:"none"},o("div",{class:`${g}-progress-graph`,"aria-hidden":!0},o("div",{class:`${g}-progress-graph-circle`},o("svg",{viewBox:`0 0 ${v} ${v}`},o("defs",null,w.map((C,f)=>p(C,f))),w.map((C,f)=>o("g",{key:f},o("path",{class:`${g}-progress-graph-circle-rail`,d:ee(v/2-s/2*(1+2*f)-a*f,s,v),"stroke-width":s,"stroke-linecap":"round",fill:"none",style:[{strokeDashoffset:0,stroke:x[f]},k[f]]}),o("path",{class:[`${g}-progress-graph-circle-fill`,C===0&&`${g}-progress-graph-circle-fill--empty`],d:ee(v/2-s/2*(1+2*f)-a*f,s,v),"stroke-width":s,"stroke-linecap":"round",fill:"none",style:{strokeDasharray:n.value[f],strokeDashoffset:0,stroke:typeof h[f]=="object"?`url(#gradient-${f})`:h[f]}})))))),u&&b.default?o("div",null,o("div",{class:`${g}-progress-text`},b.default())):null)}}}),Te=V([m("progress",{display:"inline-block"},[m("progress-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 `),I("line",`
 width: 100%;
 display: block;
 `,[m("progress-content",`
 display: flex;
 align-items: center;
 `,[m("progress-graph",{flex:1})]),m("progress-custom-content",{marginLeft:"14px"}),m("progress-icon",`
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
 `)])]),I("circle, dashboard",{width:"120px"},[m("progress-custom-content",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `),m("progress-text",`
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
 `),m("progress-icon",`
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
 `,[m("progress-text",`
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
 `)]),m("progress-content",{position:"relative"}),m("progress-graph",{position:"relative"},[m("progress-graph-circle",[V("svg",{verticalAlign:"bottom"}),m("progress-graph-circle-fill",`
 stroke: var(--n-fill-color);
 transition:
 opacity .3s var(--n-bezier),
 stroke .3s var(--n-bezier),
 stroke-dasharray .3s var(--n-bezier);
 `,[I("empty",{opacity:0})]),m("progress-graph-circle-rail",`
 transition: stroke .3s var(--n-bezier);
 overflow: hidden;
 stroke: var(--n-rail-color);
 `)]),m("progress-graph-line",[I("indicator-inside",[m("progress-graph-line-rail",`
 height: 16px;
 line-height: 16px;
 border-radius: 10px;
 `,[m("progress-graph-line-fill",`
 height: inherit;
 border-radius: 10px;
 `),m("progress-graph-line-indicator",`
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
 `,[m("progress-graph-line-rail",`
 flex: 1;
 transition: background-color .3s var(--n-bezier);
 `),m("progress-graph-line-indicator",`
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
 `)]),m("progress-graph-line-rail",`
 position: relative;
 overflow: hidden;
 height: var(--n-rail-height);
 border-radius: 5px;
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 `,[m("progress-graph-line-fill",`
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
 `)]),Ie=Object.assign(Object.assign({},re.props),{processing:Boolean,type:{type:String,default:"line"},gapDegree:Number,gapOffsetDegree:Number,status:{type:String,default:"default"},railColor:[String,Array],railStyle:[String,Array],color:[String,Array,Object],viewBoxWidth:{type:Number,default:100},strokeWidth:{type:Number,default:7},percentage:[Number,Array],unit:{type:String,default:"%"},showIndicator:{type:Boolean,default:!0},indicatorPosition:{type:String,default:"outside"},indicatorPlacement:{type:String,default:"outside"},indicatorTextColor:String,circleGap:{type:Number,default:1},height:Number,borderRadius:[String,Number],fillBorderRadius:[String,Number],offsetDegree:Number}),Oe=W({name:"Progress",props:Ie,setup(t){const b=N(()=>t.indicatorPlacement||t.indicatorPosition),n=N(()=>{if(t.gapDegree||t.gapDegree===0)return t.gapDegree;if(t.type==="dashboard")return 75}),{mergedClsPrefixRef:p,inlineThemeDisabled:v}=se(t),s=re("Progress","-progress",Te,ce,t,p),a=N(()=>{const{status:h}=t,{common:{cubicBezierEaseInOut:x},self:{fontSize:k,fontSizeCircle:w,railColor:g,railHeight:C,iconSizeCircle:f,iconSizeLine:c,textColorCircle:d,textColorLineInner:l,textColorLineOuter:y,lineBgProcessing:P,fontWeightCircle:T,[U("iconColor",h)]:X,[U("fillColor",h)]:L}}=s.value;return{"--n-bezier":x,"--n-fill-color":L,"--n-font-size":k,"--n-font-size-circle":w,"--n-font-weight-circle":T,"--n-icon-color":X,"--n-icon-size-circle":f,"--n-icon-size-line":c,"--n-line-bg-processing":P,"--n-rail-color":g,"--n-rail-height":C,"--n-text-color-circle":d,"--n-text-color-line-inner":l,"--n-text-color-line-outer":y}}),u=v?de("progress",N(()=>t.status[0]),a,t):void 0;return{mergedClsPrefix:p,mergedIndicatorPlacement:b,gapDeg:n,cssVars:v?void 0:a,themeClass:u?.themeClass,onRender:u?.onRender}},render(){const{type:t,cssVars:b,indicatorTextColor:n,showIndicator:p,status:v,railColor:s,railStyle:a,color:u,percentage:h,viewBoxWidth:x,strokeWidth:k,mergedIndicatorPlacement:w,unit:g,borderRadius:C,fillBorderRadius:f,height:c,processing:d,circleGap:l,mergedClsPrefix:y,gapDeg:P,gapOffsetDegree:T,themeClass:X,$slots:L,onRender:F}=this;return F?.(),o("div",{class:[X,`${y}-progress`,`${y}-progress--${t}`,`${y}-progress--${v}`],style:b,"aria-valuemax":100,"aria-valuemin":0,"aria-valuenow":h,role:t==="circle"||t==="line"||t==="dashboard"?"progressbar":"none"},t==="circle"||t==="dashboard"?o(Be,{clsPrefix:y,status:v,showIndicator:p,indicatorTextColor:n,railColor:s,fillColor:u,railStyle:a,offsetDegree:this.offsetDegree,percentage:h,viewBoxWidth:x,strokeWidth:k,gapDegree:P===void 0?t==="dashboard"?75:0:P,gapOffsetDegree:T,unit:g},L):t==="line"?o(Re,{clsPrefix:y,status:v,showIndicator:p,indicatorTextColor:n,railColor:s,fillColor:u,railStyle:a,percentage:h,processing:d,indicatorPlacement:w,unit:g,fillBorderRadius:f,railBorderRadius:C,height:c},L):t==="multiple-circle"?o(De,{clsPrefix:y,strokeWidth:k,railColor:s,fillColor:u,railStyle:a,viewBoxWidth:x,percentage:h,showIndicator:p,circleGap:l},L):null)}}),je={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Me=W({name:"AlertCircleOutline",render:function(b,n){return S(),D("svg",je,n[0]||(n[0]=[z("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),z("path",{d:"M250.26 166.05L256 288l5.73-121.95a5.74 5.74 0 0 0-5.79-6h0a5.74 5.74 0 0 0-5.68 6z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),z("path",{d:"M256 367.91a20 20 0 1 1 20-20a20 20 0 0 1-20 20z",fill:"currentColor"},null,-1)]))}}),We={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},qe=W({name:"TrendingUpOutline",render:function(b,n){return S(),D("svg",We,n[0]||(n[0]=[z("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 144h112v112"},null,-1),z("path",{d:"M48 368l121.37-121.37a32 32 0 0 1 45.26 0l50.74 50.74a32 32 0 0 0 45.26 0L448 160",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Ge={class:"dashboard"},Ae={class:"dashboard-header"},Le={class:"stat-value"},Ee={key:0,class:"change-list"},Ve={class:"task-name"},Xe={key:0,class:"more-hint"},Fe=W({__name:"Dashboard",setup(t){const b=ye(),n=ue(),p=ge(),v=fe(),s=pe(!0),a=d=>{if(d<60)return`${Math.floor(d)}秒`;if(d<3600)return`${Math.floor(d/60)}分钟`;if(d<86400){const l=Math.floor(d/3600),y=Math.floor(d%3600/60);return`${l}小时${y}分钟`}else{const l=Math.floor(d/86400),y=Math.floor(d%86400/3600);return`${l}天${y}小时`}},u=d=>{if(!d)return"-";try{return new Date(d).toLocaleString("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})}catch{return d}},h=N(()=>{const d=n.totalExecutions;return d===0?100:Math.round(n.successfulExecutions/d*100)}),x=N(()=>[...p.tasks].filter(d=>d.last_change).sort((d,l)=>{const y=new Date(d.last_change||0).getTime();return new Date(l.last_change||0).getTime()-y}).slice(0,5)),k=[{title:"任务名称",key:"name",ellipsis:{tooltip:!0}},{title:"状态",key:"status",width:100,render:d=>d.enabled?d.error_count>0?o(E,{type:"error",size:"small"},{default:()=>"错误"}):o(E,{type:"success",size:"small"},{default:()=>"正常"}):o(E,{type:"default",size:"small"},{default:()=>"已禁用"})},{title:"最后变化",key:"last_change",width:140,render:d=>u(d.last_change)},{title:"变化次数",key:"change_count",width:90,align:"center"}],w=async()=>{s.value=!0;try{await Promise.all([n.fetchStatus(),p.fetchTasks()])}finally{s.value=!1}},g=async()=>{await w()},C=()=>{b.push("/tasks")},f=()=>{b.push("/history")},c=async()=>{n.isRunning?await n.stopMonitor():await n.startMonitor()};return he(async()=>{await w()}),(d,l)=>(S(),D("div",Ge,[r(e($e),{show:s.value},{default:i(()=>[z("div",Ae,[r(e(_),{align:"center"},{default:i(()=>[l[2]||(l[2]=z("h2",{class:"page-title"},"仪表盘",-1)),e(v).isConnected?(S(),j(e(me),{key:0,trigger:"hover"},{trigger:i(()=>[r(e(E),{type:"success",size:"small",round:""},{icon:i(()=>[r(e(R),null,{default:i(()=>[r(e(ve))]),_:1})]),default:i(()=>[l[0]||(l[0]=$(" 实时更新 ",-1))]),_:1})]),default:i(()=>[l[1]||(l[1]=z("span",null,"SSE 实时连接已建立，数据将自动更新",-1))]),_:1})):H("",!0)]),_:1}),r(e(_),{align:"center",size:12},{default:i(()=>[r(e(G),{type:e(n).isRunning?"error":"success",onClick:c,loading:e(n).loading},{icon:i(()=>[r(e(R),null,{default:i(()=>[e(n).isRunning?(S(),j(e(be),{key:0})):(S(),j(e(xe),{key:1}))]),_:1})]),default:i(()=>[$(" "+B(e(n).isRunning?"停止监控":"开始监控"),1)]),_:1},8,["type","loading"]),r(e(G),{quaternary:"",circle:"",onClick:g,loading:s.value},{icon:i(()=>[r(e(R),null,{default:i(()=>[r(e(Se))]),_:1})]),_:1},8,["loading"])]),_:1})]),r(e(Z),{cols:24,"x-gap":16,"y-gap":16},{default:i(()=>[r(e(A),{span:6},{default:i(()=>[r(e(M),{class:"stat-card"},{default:i(()=>[r(e(_),{vertical:""},{default:i(()=>[r(e(_),{align:"center",justify:"space-between",style:{width:"100%"}},{default:i(()=>[l[3]||(l[3]=z("span",{class:"stat-label"},"任务总数",-1)),r(e(R),{size:"24",color:"#63e2b7"},{default:i(()=>[r(e(_e))]),_:1})]),_:1}),r(e(J),{value:e(p).total},null,8,["value"]),r(e(O),{depth:"3"},{default:i(()=>[$("活跃: "+B(e(p).activeCount),1)]),_:1})]),_:1})]),_:1})]),_:1}),r(e(A),{span:6},{default:i(()=>[r(e(M),{class:"stat-card"},{default:i(()=>[r(e(_),{vertical:""},{default:i(()=>[r(e(_),{align:"center",justify:"space-between",style:{width:"100%"}},{default:i(()=>[l[4]||(l[4]=z("span",{class:"stat-label"},"检测到的变化",-1)),r(e(R),{size:"24",color:"#f2c97d"},{default:i(()=>[r(e(qe))]),_:1})]),_:1}),r(e(J),{value:e(n).totalChanges},null,8,["value"]),r(e(O),{depth:"3"},{default:i(()=>[$("执行次数: "+B(e(n).totalExecutions),1)]),_:1})]),_:1})]),_:1})]),_:1}),r(e(A),{span:6},{default:i(()=>[r(e(M),{class:"stat-card"},{default:i(()=>[r(e(_),{vertical:""},{default:i(()=>[r(e(_),{align:"center",justify:"space-between",style:{width:"100%"}},{default:i(()=>[l[5]||(l[5]=z("span",{class:"stat-label"},"成功率",-1)),r(e(R),{size:"24",color:"#70c0e8"},{default:i(()=>[r(e(Q))]),_:1})]),_:1}),r(e(J),{value:h.value,suffix:"%"},null,8,["value"]),r(e(Oe),{type:"line",percentage:h.value,"show-indicator":!1,height:4,color:h.value>=80?"#63e2b7":h.value>=50?"#f2c97d":"#e88080"},null,8,["percentage","color"])]),_:1})]),_:1})]),_:1}),r(e(A),{span:6},{default:i(()=>[r(e(M),{class:"stat-card"},{default:i(()=>[r(e(_),{vertical:""},{default:i(()=>[r(e(_),{align:"center",justify:"space-between",style:{width:"100%"}},{default:i(()=>[l[6]||(l[6]=z("span",{class:"stat-label"},"运行时间",-1)),r(e(R),{size:"24",color:e(n).isRunning?"#63e2b7":"#909399"},{default:i(()=>[r(e(ke))]),_:1},8,["color"])]),_:1}),z("div",Le,[e(n).isRunning?(S(),D(Y,{key:0},[$(B(a(e(n).uptime)),1)],64)):(S(),j(e(O),{key:1,depth:"3"},{default:i(()=>[...l[7]||(l[7]=[$("已停止",-1)])]),_:1}))]),r(e(O),{depth:"3"},{default:i(()=>[l[8]||(l[8]=$(" 状态: ",-1)),r(e(O),{type:e(n).isRunning?"success":"default"},{default:i(()=>[$(B(e(n).isRunning?"运行中":"已停止"),1)]),_:1},8,["type"])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),r(e(Z),{cols:24,"x-gap":16,"y-gap":16,style:{"margin-top":"16px"}},{default:i(()=>[r(e(A),{span:12},{default:i(()=>[r(e(M),{title:"最近变化",class:"list-card"},{"header-extra":i(()=>[r(e(G),{text:"",type:"primary",onClick:f},{default:i(()=>[...l[9]||(l[9]=[$("查看全部",-1)])]),_:1})]),default:i(()=>[x.value.length>0?(S(),D("div",Ee,[(S(!0),D(Y,null,we(x.value,y=>(S(),D("div",{key:y.id,class:"change-item"},[r(e(_),{align:"center",justify:"space-between",style:{width:"100%"}},{default:i(()=>[r(e(_),{align:"center"},{default:i(()=>[r(e(R),{color:"#63e2b7"},{default:i(()=>[r(e(Q))]),_:1}),z("span",Ve,B(y.name),1)]),_:2},1024),r(e(_),{align:"center"},{default:i(()=>[r(e(E),{size:"small",round:""},{default:i(()=>[$(B(y.change_count)+"次",1)]),_:2},1024),r(e(O),{depth:"3",style:{"font-size":"12px"}},{default:i(()=>[$(B(u(y.last_change)),1)]),_:2},1024)]),_:2},1024)]),_:2},1024)]))),128))])):(S(),j(e(K),{key:1,description:"暂无变化记录"}))]),_:1})]),_:1}),r(e(A),{span:12},{default:i(()=>[r(e(M),{title:"任务概览",class:"list-card"},{"header-extra":i(()=>[r(e(G),{text:"",type:"primary",onClick:C},{default:i(()=>[...l[10]||(l[10]=[$("管理任务",-1)])]),_:1})]),default:i(()=>[e(p).tasks.length>0?(S(),D(Y,{key:0},[r(e(ze),{columns:k,data:e(p).tasks.slice(0,5),bordered:!1,size:"small",pagination:!1},null,8,["data"]),e(p).total>5?(S(),D("div",Xe,[r(e(O),{depth:"3"},{default:i(()=>[$("共 "+B(e(p).total)+" 个任务",1)]),_:1})])):H("",!0)],64)):(S(),j(e(K),{key:1,description:"暂无任务"},{extra:i(()=>[r(e(G),{size:"small",onClick:C},{default:i(()=>[...l[11]||(l[11]=[$("添加任务",-1)])]),_:1})]),_:1}))]),_:1})]),_:1})]),_:1}),e(p).errorCount>0?(S(),j(e(M),{key:0,class:"error-card",style:{"margin-top":"16px"}},{default:i(()=>[r(e(_),{align:"center"},{default:i(()=>[r(e(R),{size:"20",color:"#e88080"},{default:i(()=>[r(e(Me))]),_:1}),r(e(O),{type:"error"},{default:i(()=>[$(B(e(p).errorCount)+" 个任务存在错误，请检查任务配置 ",1)]),_:1}),r(e(G),{size:"small",text:"",type:"primary",onClick:C},{default:i(()=>[...l[12]||(l[12]=[$(" 查看详情 ",-1)])]),_:1})]),_:1})]),_:1})):H("",!0)]),_:1},8,["show"])]))}}),Ze=Ce(Fe,[["__scopeId","data-v-90b7c86f"]]);export{Ze as default};
