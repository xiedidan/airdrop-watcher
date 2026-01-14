import{d as O,c as z,m as ne,h as r,N as ee,I as te,W as re,E as ie,S as oe,f as M,a as E,b as v,e as D,u as ae,g as se,p as le,i as H,j as ce,k as T,o as $,l as g,n as de,q as ue,r as ge,s as fe,t as pe,v as i,w as o,x as e,y as he,z as W,A as F,B as j,C as ye,D as N,F as P,G as me,H as q,J as S,K as ve,P as be,L as I,T as xe,M as Y,O as J,Q as ke,_ as Ce}from"./index-CLpEAGPE.js";import{N as _e,a as A,R as we,F as $e,b as K}from"./RefreshOutline-CHu-auid.js";import{N as U,a as G,C as Q}from"./CheckmarkCircleOutline-CdKgrDXq.js";import{N as Se}from"./DataTable-CjsYMp0x.js";const ze={success:r(oe,null),error:r(ie,null),warning:r(re,null),info:r(te,null)},Ne=O({name:"ProgressCircle",props:{clsPrefix:{type:String,required:!0},status:{type:String,required:!0},strokeWidth:{type:Number,required:!0},fillColor:[String,Object],railColor:String,railStyle:[String,Object],percentage:{type:Number,default:0},offsetDegree:{type:Number,default:0},showIndicator:{type:Boolean,required:!0},indicatorTextColor:String,unit:String,viewBoxWidth:{type:Number,required:!0},gapDegree:{type:Number,required:!0},gapOffsetDegree:{type:Number,default:0}},setup(t,{slots:x}){const s=z(()=>{const l="gradient",{fillColor:a}=t;return typeof a=="object"?`${l}-${ne(JSON.stringify(a))}`:l});function h(l,a,u,y){const{gapDegree:k,viewBoxWidth:C,strokeWidth:_}=t,f=50,w=0,p=f,c=0,d=2*f,n=50+_/2,m=`M ${n},${n} m ${w},${p}
      a ${f},${f} 0 1 1 ${c},${-d}
      a ${f},${f} 0 1 1 ${-c},${d}`,B=Math.PI*2*f,R={stroke:y==="rail"?u:typeof t.fillColor=="object"?`url(#${s.value})`:u,strokeDasharray:`${Math.min(l,100)/100*(B-k)}px ${C*8}px`,strokeDashoffset:`-${k/2}px`,transformOrigin:a?"center":void 0,transform:a?`rotate(${a}deg)`:void 0};return{pathString:m,pathStyle:R}}const b=()=>{const l=typeof t.fillColor=="object",a=l?t.fillColor.stops[0]:"",u=l?t.fillColor.stops[1]:"";return l&&r("defs",null,r("linearGradient",{id:s.value,x1:"0%",y1:"100%",x2:"100%",y2:"0%"},r("stop",{offset:"0%","stop-color":a}),r("stop",{offset:"100%","stop-color":u})))};return()=>{const{fillColor:l,railColor:a,strokeWidth:u,offsetDegree:y,status:k,percentage:C,showIndicator:_,indicatorTextColor:f,unit:w,gapOffsetDegree:p,clsPrefix:c}=t,{pathString:d,pathStyle:n}=h(100,0,a,"rail"),{pathString:m,pathStyle:B}=h(C,y,l,"fill"),R=100+u;return r("div",{class:`${c}-progress-content`,role:"none"},r("div",{class:`${c}-progress-graph`,"aria-hidden":!0},r("div",{class:`${c}-progress-graph-circle`,style:{transform:p?`rotate(${p}deg)`:void 0}},r("svg",{viewBox:`0 0 ${R} ${R}`},b(),r("g",null,r("path",{class:`${c}-progress-graph-circle-rail`,d,"stroke-width":u,"stroke-linecap":"round",fill:"none",style:n})),r("g",null,r("path",{class:[`${c}-progress-graph-circle-fill`,C===0&&`${c}-progress-graph-circle-fill--empty`],d:m,"stroke-width":u,"stroke-linecap":"round",fill:"none",style:B}))))),_?r("div",null,x.default?r("div",{class:`${c}-progress-custom-content`,role:"none"},x.default()):k!=="default"?r("div",{class:`${c}-progress-icon`,"aria-hidden":!0},r(ee,{clsPrefix:c},{default:()=>ze[k]})):r("div",{class:`${c}-progress-text`,style:{color:f},role:"none"},r("span",{class:`${c}-progress-text__percentage`},C),r("span",{class:`${c}-progress-text__unit`},w))):null)}}}),Be={success:r(oe,null),error:r(ie,null),warning:r(re,null),info:r(te,null)},Pe=O({name:"ProgressLine",props:{clsPrefix:{type:String,required:!0},percentage:{type:Number,default:0},railColor:String,railStyle:[String,Object],fillColor:[String,Object],status:{type:String,required:!0},indicatorPlacement:{type:String,required:!0},indicatorTextColor:String,unit:{type:String,default:"%"},processing:{type:Boolean,required:!0},showIndicator:{type:Boolean,required:!0},height:[String,Number],railBorderRadius:[String,Number],fillBorderRadius:[String,Number]},setup(t,{slots:x}){const s=z(()=>M(t.height)),h=z(()=>{var a,u;return typeof t.fillColor=="object"?`linear-gradient(to right, ${(a=t.fillColor)===null||a===void 0?void 0:a.stops[0]} , ${(u=t.fillColor)===null||u===void 0?void 0:u.stops[1]})`:t.fillColor}),b=z(()=>t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):""),l=z(()=>t.fillBorderRadius!==void 0?M(t.fillBorderRadius):t.railBorderRadius!==void 0?M(t.railBorderRadius):t.height!==void 0?M(t.height,{c:.5}):"");return()=>{const{indicatorPlacement:a,railColor:u,railStyle:y,percentage:k,unit:C,indicatorTextColor:_,status:f,showIndicator:w,processing:p,clsPrefix:c}=t;return r("div",{class:`${c}-progress-content`,role:"none"},r("div",{class:`${c}-progress-graph`,"aria-hidden":!0},r("div",{class:[`${c}-progress-graph-line`,{[`${c}-progress-graph-line--indicator-${a}`]:!0}]},r("div",{class:`${c}-progress-graph-line-rail`,style:[{backgroundColor:u,height:s.value,borderRadius:b.value},y]},r("div",{class:[`${c}-progress-graph-line-fill`,p&&`${c}-progress-graph-line-fill--processing`],style:{maxWidth:`${t.percentage}%`,background:h.value,height:s.value,lineHeight:s.value,borderRadius:l.value}},a==="inside"?r("div",{class:`${c}-progress-graph-line-indicator`,style:{color:_}},x.default?x.default():`${k}${C}`):null)))),w&&a==="outside"?r("div",null,x.default?r("div",{class:`${c}-progress-custom-content`,style:{color:_},role:"none"},x.default()):f==="default"?r("div",{role:"none",class:`${c}-progress-icon ${c}-progress-icon--as-text`,style:{color:_}},k,C):r("div",{class:`${c}-progress-icon`,"aria-hidden":!0},r(ee,{clsPrefix:c},{default:()=>Be[f]}))):null)}}});function Z(t,x,s=100){return`m ${s/2} ${s/2-t} a ${t} ${t} 0 1 1 0 ${2*t} a ${t} ${t} 0 1 1 0 -${2*t}`}const Re=O({name:"ProgressMultipleCircle",props:{clsPrefix:{type:String,required:!0},viewBoxWidth:{type:Number,required:!0},percentage:{type:Array,default:[0]},strokeWidth:{type:Number,required:!0},circleGap:{type:Number,required:!0},showIndicator:{type:Boolean,required:!0},fillColor:{type:Array,default:()=>[]},railColor:{type:Array,default:()=>[]},railStyle:{type:Array,default:()=>[]}},setup(t,{slots:x}){const s=z(()=>t.percentage.map((l,a)=>`${Math.PI*l/100*(t.viewBoxWidth/2-t.strokeWidth/2*(1+2*a)-t.circleGap*a)*2}, ${t.viewBoxWidth*8}`)),h=(b,l)=>{const a=t.fillColor[l],u=typeof a=="object"?a.stops[0]:"",y=typeof a=="object"?a.stops[1]:"";return typeof t.fillColor[l]=="object"&&r("linearGradient",{id:`gradient-${l}`,x1:"100%",y1:"0%",x2:"0%",y2:"100%"},r("stop",{offset:"0%","stop-color":u}),r("stop",{offset:"100%","stop-color":y}))};return()=>{const{viewBoxWidth:b,strokeWidth:l,circleGap:a,showIndicator:u,fillColor:y,railColor:k,railStyle:C,percentage:_,clsPrefix:f}=t;return r("div",{class:`${f}-progress-content`,role:"none"},r("div",{class:`${f}-progress-graph`,"aria-hidden":!0},r("div",{class:`${f}-progress-graph-circle`},r("svg",{viewBox:`0 0 ${b} ${b}`},r("defs",null,_.map((w,p)=>h(w,p))),_.map((w,p)=>r("g",{key:p},r("path",{class:`${f}-progress-graph-circle-rail`,d:Z(b/2-l/2*(1+2*p)-a*p,l,b),"stroke-width":l,"stroke-linecap":"round",fill:"none",style:[{strokeDashoffset:0,stroke:k[p]},C[p]]}),r("path",{class:[`${f}-progress-graph-circle-fill`,w===0&&`${f}-progress-graph-circle-fill--empty`],d:Z(b/2-l/2*(1+2*p)-a*p,l,b),"stroke-width":l,"stroke-linecap":"round",fill:"none",style:{strokeDasharray:s.value[p],strokeDashoffset:0,stroke:typeof y[p]=="object"?`url(#gradient-${p})`:y[p]}})))))),u&&x.default?r("div",null,r("div",{class:`${f}-progress-text`},x.default())):null)}}}),De=E([v("progress",{display:"inline-block"},[v("progress-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 `),D("line",`
 width: 100%;
 display: block;
 `,[v("progress-content",`
 display: flex;
 align-items: center;
 `,[v("progress-graph",{flex:1})]),v("progress-custom-content",{marginLeft:"14px"}),v("progress-icon",`
 width: 30px;
 padding-left: 14px;
 height: var(--n-icon-size-line);
 line-height: var(--n-icon-size-line);
 font-size: var(--n-icon-size-line);
 `,[D("as-text",`
 color: var(--n-text-color-line-outer);
 text-align: center;
 width: 40px;
 font-size: var(--n-font-size);
 padding-left: 4px;
 transition: color .3s var(--n-bezier);
 `)])]),D("circle, dashboard",{width:"120px"},[v("progress-custom-content",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `),v("progress-text",`
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
 `),v("progress-icon",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 color: var(--n-icon-color);
 font-size: var(--n-icon-size-circle);
 `)]),D("multiple-circle",`
 width: 200px;
 color: inherit;
 `,[v("progress-text",`
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
 `)]),v("progress-content",{position:"relative"}),v("progress-graph",{position:"relative"},[v("progress-graph-circle",[E("svg",{verticalAlign:"bottom"}),v("progress-graph-circle-fill",`
 stroke: var(--n-fill-color);
 transition:
 opacity .3s var(--n-bezier),
 stroke .3s var(--n-bezier),
 stroke-dasharray .3s var(--n-bezier);
 `,[D("empty",{opacity:0})]),v("progress-graph-circle-rail",`
 transition: stroke .3s var(--n-bezier);
 overflow: hidden;
 stroke: var(--n-rail-color);
 `)]),v("progress-graph-line",[D("indicator-inside",[v("progress-graph-line-rail",`
 height: 16px;
 line-height: 16px;
 border-radius: 10px;
 `,[v("progress-graph-line-fill",`
 height: inherit;
 border-radius: 10px;
 `),v("progress-graph-line-indicator",`
 background: #0000;
 white-space: nowrap;
 text-align: right;
 margin-left: 14px;
 margin-right: 14px;
 height: inherit;
 font-size: 12px;
 color: var(--n-text-color-line-inner);
 transition: color .3s var(--n-bezier);
 `)])]),D("indicator-inside-label",`
 height: 16px;
 display: flex;
 align-items: center;
 `,[v("progress-graph-line-rail",`
 flex: 1;
 transition: background-color .3s var(--n-bezier);
 `),v("progress-graph-line-indicator",`
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
 `)]),v("progress-graph-line-rail",`
 position: relative;
 overflow: hidden;
 height: var(--n-rail-height);
 border-radius: 5px;
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 `,[v("progress-graph-line-fill",`
 background: var(--n-fill-color);
 position: relative;
 border-radius: 5px;
 height: inherit;
 width: 100%;
 max-width: 0%;
 transition:
 background-color .3s var(--n-bezier),
 max-width .2s var(--n-bezier);
 `,[D("processing",[E("&::after",`
 content: "";
 background-image: var(--n-line-bg-processing);
 animation: progress-processing-animation 2s var(--n-bezier) infinite;
 `)])])])])])]),E("@keyframes progress-processing-animation",`
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
 `)]),Te=Object.assign(Object.assign({},se.props),{processing:Boolean,type:{type:String,default:"line"},gapDegree:Number,gapOffsetDegree:Number,status:{type:String,default:"default"},railColor:[String,Array],railStyle:[String,Array],color:[String,Array,Object],viewBoxWidth:{type:Number,default:100},strokeWidth:{type:Number,default:7},percentage:[Number,Array],unit:{type:String,default:"%"},showIndicator:{type:Boolean,default:!0},indicatorPosition:{type:String,default:"outside"},indicatorPlacement:{type:String,default:"outside"},indicatorTextColor:String,circleGap:{type:Number,default:1},height:Number,borderRadius:[String,Number],fillBorderRadius:[String,Number],offsetDegree:Number}),Ie=O({name:"Progress",props:Te,setup(t){const x=z(()=>t.indicatorPlacement||t.indicatorPosition),s=z(()=>{if(t.gapDegree||t.gapDegree===0)return t.gapDegree;if(t.type==="dashboard")return 75}),{mergedClsPrefixRef:h,inlineThemeDisabled:b}=ae(t),l=se("Progress","-progress",De,le,t,h),a=z(()=>{const{status:y}=t,{common:{cubicBezierEaseInOut:k},self:{fontSize:C,fontSizeCircle:_,railColor:f,railHeight:w,iconSizeCircle:p,iconSizeLine:c,textColorCircle:d,textColorLineInner:n,textColorLineOuter:m,lineBgProcessing:B,fontWeightCircle:R,[H("iconColor",y)]:V,[H("fillColor",y)]:L}}=l.value;return{"--n-bezier":k,"--n-fill-color":L,"--n-font-size":C,"--n-font-size-circle":_,"--n-font-weight-circle":R,"--n-icon-color":V,"--n-icon-size-circle":p,"--n-icon-size-line":c,"--n-line-bg-processing":B,"--n-rail-color":f,"--n-rail-height":w,"--n-text-color-circle":d,"--n-text-color-line-inner":n,"--n-text-color-line-outer":m}}),u=b?ce("progress",z(()=>t.status[0]),a,t):void 0;return{mergedClsPrefix:h,mergedIndicatorPlacement:x,gapDeg:s,cssVars:b?void 0:a,themeClass:u?.themeClass,onRender:u?.onRender}},render(){const{type:t,cssVars:x,indicatorTextColor:s,showIndicator:h,status:b,railColor:l,railStyle:a,color:u,percentage:y,viewBoxWidth:k,strokeWidth:C,mergedIndicatorPlacement:_,unit:f,borderRadius:w,fillBorderRadius:p,height:c,processing:d,circleGap:n,mergedClsPrefix:m,gapDeg:B,gapOffsetDegree:R,themeClass:V,$slots:L,onRender:X}=this;return X?.(),r("div",{class:[V,`${m}-progress`,`${m}-progress--${t}`,`${m}-progress--${b}`],style:x,"aria-valuemax":100,"aria-valuemin":0,"aria-valuenow":y,role:t==="circle"||t==="line"||t==="dashboard"?"progressbar":"none"},t==="circle"||t==="dashboard"?r(Ne,{clsPrefix:m,status:b,showIndicator:h,indicatorTextColor:s,railColor:l,fillColor:u,railStyle:a,offsetDegree:this.offsetDegree,percentage:y,viewBoxWidth:k,strokeWidth:C,gapDegree:B===void 0?t==="dashboard"?75:0:B,gapOffsetDegree:R,unit:f},L):t==="line"?r(Pe,{clsPrefix:m,status:b,showIndicator:h,indicatorTextColor:s,railColor:l,fillColor:u,railStyle:a,percentage:y,processing:d,indicatorPlacement:_,unit:f,fillBorderRadius:p,railBorderRadius:w,height:c},L):t==="multiple-circle"?r(Re,{clsPrefix:m,strokeWidth:C,railColor:l,fillColor:u,railStyle:a,viewBoxWidth:k,percentage:y,showIndicator:h,circleGap:n},L):null)}}),Oe={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Me=O({name:"AlertCircleOutline",render:function(x,s){return $(),T("svg",Oe,s[0]||(s[0]=[g("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),g("path",{d:"M250.26 166.05L256 288l5.73-121.95a5.74 5.74 0 0 0-5.79-6h0a5.74 5.74 0 0 0-5.68 6z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),g("path",{d:"M256 367.91a20 20 0 1 1 20-20a20 20 0 0 1-20 20z",fill:"currentColor"},null,-1)]))}}),We={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},je=O({name:"TrendingUpOutline",render:function(x,s){return $(),T("svg",We,s[0]||(s[0]=[g("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 144h112v112"},null,-1),g("path",{d:"M48 368l121.37-121.37a32 32 0 0 1 45.26 0l50.74 50.74a32 32 0 0 0 45.26 0L448 160",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),qe={class:"dashboard"},Ge={class:"dashboard-header"},Le={class:"stat-content"},Ae={class:"stat-header"},Ee={class:"stat-value"},Ve={class:"stat-desc"},Xe={class:"stat-content"},Fe={class:"stat-header"},He={class:"stat-value"},Ye={class:"stat-desc"},Je={class:"stat-content"},Ke={class:"stat-header"},Ue={class:"stat-value"},Qe={class:"stat-content"},Ze={class:"stat-header"},et={class:"stat-value"},tt={class:"stat-desc"},rt={key:0,class:"change-list"},it={class:"task-name"},ot={class:"change-time"},st={key:0,class:"more-hint"},nt={class:"stat-desc"},at=O({__name:"Dashboard",setup(t){const x=he(),s=de(),h=ue(),b=ge(),l=fe(!0),a=d=>{if(d<60)return`${Math.floor(d)}秒`;if(d<3600)return`${Math.floor(d/60)}分钟`;if(d<86400){const n=Math.floor(d/3600),m=Math.floor(d%3600/60);return`${n}小时${m}分钟`}else{const n=Math.floor(d/86400),m=Math.floor(d%86400/3600);return`${n}天${m}小时`}},u=d=>{if(!d)return"-";try{return new Date(d).toLocaleString("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})}catch{return d}},y=z(()=>{const d=s.totalExecutions;return d===0?100:Math.round(s.successfulExecutions/d*100)}),k=z(()=>[...h.tasks].filter(d=>d.last_change).sort((d,n)=>{const m=new Date(d.last_change||0).getTime();return new Date(n.last_change||0).getTime()-m}).slice(0,5)),C=[{title:"任务名称",key:"name",ellipsis:{tooltip:!0}},{title:"状态",key:"status",width:100,render:d=>d.enabled?d.error_count>0?r(A,{type:"error",size:"small"},{default:()=>"错误"}):r(A,{type:"success",size:"small"},{default:()=>"正常"}):r(A,{type:"default",size:"small"},{default:()=>"已禁用"})},{title:"最后变化",key:"last_change",width:140,render:d=>u(d.last_change)},{title:"变化次数",key:"change_count",width:90,align:"center"}],_=async()=>{l.value=!0;try{await Promise.all([s.fetchStatus(),h.fetchTasks()])}finally{l.value=!1}},f=async()=>{await _()},w=()=>{x.push("/tasks")},p=()=>{x.push("/history")},c=async()=>{s.isRunning?await s.stopMonitor():await s.startMonitor()};return pe(async()=>{await _()}),(d,n)=>($(),T("div",qe,[i(e(_e),{show:l.value},{default:o(()=>[g("div",Ge,[i(e(j),{align:"center"},{default:o(()=>[n[2]||(n[2]=g("h2",{class:"page-title"},"仪表盘",-1)),e(b).isConnected?($(),W(e(ye),{key:0,trigger:"hover"},{trigger:o(()=>[i(e(A),{type:"success",size:"small",round:""},{icon:o(()=>[i(e(P),null,{default:o(()=>[i(e(me))]),_:1})]),default:o(()=>[n[0]||(n[0]=N(" 实时更新 ",-1))]),_:1})]),default:o(()=>[n[1]||(n[1]=g("span",null,"SSE 实时连接已建立，数据将自动更新",-1))]),_:1})):F("",!0)]),_:1}),i(e(j),{align:"center",size:12},{default:o(()=>[i(e(q),{type:e(s).isRunning?"error":"success",onClick:c,loading:e(s).loading},{icon:o(()=>[i(e(P),null,{default:o(()=>[e(s).isRunning?($(),W(e(ve),{key:0})):($(),W(e(be),{key:1}))]),_:1})]),default:o(()=>[N(" "+S(e(s).isRunning?"停止监控":"开始监控"),1)]),_:1},8,["type","loading"]),i(e(q),{quaternary:"",circle:"",onClick:f,loading:l.value},{icon:o(()=>[i(e(P),null,{default:o(()=>[i(e(we))]),_:1})]),_:1},8,["loading"])]),_:1})]),i(e(U),{cols:24,"x-gap":16,"y-gap":16},{default:o(()=>[i(e(G),{span:6},{default:o(()=>[i(e(I),{class:"stat-card"},{default:o(()=>[g("div",Le,[g("div",Ae,[n[3]||(n[3]=g("span",{class:"stat-label"},"任务总数",-1)),i(e(P),{size:"24",color:"#3b82f6"},{default:o(()=>[i(e($e))]),_:1})]),g("div",Ee,S(e(h).total),1),g("div",Ve,"活跃: "+S(e(h).activeCount),1)])]),_:1})]),_:1}),i(e(G),{span:6},{default:o(()=>[i(e(I),{class:"stat-card"},{default:o(()=>[g("div",Xe,[g("div",Fe,[n[4]||(n[4]=g("span",{class:"stat-label"},"检测到的变化",-1)),i(e(P),{size:"24",color:"#f59e0b"},{default:o(()=>[i(e(je))]),_:1})]),g("div",He,S(e(s).totalChanges),1),g("div",Ye,"执行次数: "+S(e(s).totalExecutions),1)])]),_:1})]),_:1}),i(e(G),{span:6},{default:o(()=>[i(e(I),{class:"stat-card"},{default:o(()=>[g("div",Je,[g("div",Ke,[n[5]||(n[5]=g("span",{class:"stat-label"},"成功率",-1)),i(e(P),{size:"24",color:"#06b6d4"},{default:o(()=>[i(e(Q))]),_:1})]),g("div",Ue,S(y.value)+"%",1),i(e(Ie),{type:"line",percentage:y.value,"show-indicator":!1,height:4,color:y.value>=80?"#10b981":y.value>=50?"#f59e0b":"#ef4444"},null,8,["percentage","color"])])]),_:1})]),_:1}),i(e(G),{span:6},{default:o(()=>[i(e(I),{class:"stat-card"},{default:o(()=>[g("div",Qe,[g("div",Ze,[n[6]||(n[6]=g("span",{class:"stat-label"},"运行时间",-1)),i(e(P),{size:"24",color:e(s).isRunning?"#10b981":"#64748b"},{default:o(()=>[i(e(xe))]),_:1},8,["color"])]),g("div",et,S(e(s).isRunning?a(e(s).uptime):"已停止"),1),g("div",tt,[n[7]||(n[7]=N(" 状态: ",-1)),i(e(Y),{type:e(s).isRunning?"success":"default"},{default:o(()=>[N(S(e(s).isRunning?"运行中":"已停止"),1)]),_:1},8,["type"])])])]),_:1})]),_:1})]),_:1}),i(e(U),{cols:24,"x-gap":16,"y-gap":16,style:{"margin-top":"16px"}},{default:o(()=>[i(e(G),{span:12},{default:o(()=>[i(e(I),{title:"最近变化",class:"list-card"},{"header-extra":o(()=>[i(e(q),{text:"",type:"primary",onClick:p},{default:o(()=>[...n[8]||(n[8]=[N("查看全部",-1)])]),_:1})]),default:o(()=>[k.value.length>0?($(),T("div",rt,[($(!0),T(J,null,ke(k.value,m=>($(),T("div",{key:m.id,class:"change-item"},[i(e(j),{align:"center",justify:"space-between",style:{width:"100%"}},{default:o(()=>[i(e(j),{align:"center"},{default:o(()=>[i(e(P),{color:"#10b981"},{default:o(()=>[i(e(Q))]),_:1}),g("span",it,S(m.name),1)]),_:2},1024),i(e(j),{align:"center"},{default:o(()=>[i(e(A),{size:"small",round:""},{default:o(()=>[N(S(m.change_count)+"次",1)]),_:2},1024),g("span",ot,S(u(m.last_change)),1)]),_:2},1024)]),_:2},1024)]))),128))])):($(),W(e(K),{key:1,description:"暂无变化记录"}))]),_:1})]),_:1}),i(e(G),{span:12},{default:o(()=>[i(e(I),{title:"任务概览",class:"list-card"},{"header-extra":o(()=>[i(e(q),{text:"",type:"primary",onClick:w},{default:o(()=>[...n[9]||(n[9]=[N("管理任务",-1)])]),_:1})]),default:o(()=>[e(h).tasks.length>0?($(),T(J,{key:0},[i(e(Se),{columns:C,data:e(h).tasks.slice(0,5),bordered:!1,size:"small",pagination:!1},null,8,["data"]),e(h).total>5?($(),T("div",st,[g("span",nt,"共 "+S(e(h).total)+" 个任务",1)])):F("",!0)],64)):($(),W(e(K),{key:1,description:"暂无任务"},{extra:o(()=>[i(e(q),{size:"small",onClick:w},{default:o(()=>[...n[10]||(n[10]=[N("添加任务",-1)])]),_:1})]),_:1}))]),_:1})]),_:1})]),_:1}),e(h).errorCount>0?($(),W(e(I),{key:0,class:"error-card",style:{"margin-top":"16px"}},{default:o(()=>[i(e(j),{align:"center"},{default:o(()=>[i(e(P),{size:"20",color:"#ef4444"},{default:o(()=>[i(e(Me))]),_:1}),i(e(Y),{type:"error"},{default:o(()=>[N(S(e(h).errorCount)+" 个任务存在错误，请检查任务配置 ",1)]),_:1}),i(e(q),{size:"small",text:"",type:"primary",onClick:w},{default:o(()=>[...n[11]||(n[11]=[N(" 查看详情 ",-1)])]),_:1})]),_:1})]),_:1})):F("",!0)]),_:1},8,["show"])]))}}),gt=Ce(at,[["__scopeId","data-v-5dea3459"]]);export{gt as default};
