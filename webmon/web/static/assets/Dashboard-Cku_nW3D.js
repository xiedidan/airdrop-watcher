import{i as Ne,c as C,r as F,o as Be,v as ye,a as Pe,d as I,h as n,b as De,g as Ie,p as X,m as ae,V as Te,u as ne,e as Q,f as be,j as Ge,t as ue,k as je,l as Oe,n as Me,q as ce,s as Ee,w as We,N as xe,x as L,y as U,z as w,A as j,B as te,C as Ae,D as de,E as we,F as J,G as Z,H as Le,I as qe,J as T,K as N,L as _,M as Ve,O as Fe,P as d,Q as f,R as t,S as Xe,T as K,U as fe,W as Y,X as E,Y as D,Z as O,_ as z,$ as G,a0 as Ye,a1 as re,a2 as He,a3 as Qe}from"./index-ComyWp1J.js";import{I as Se,W as $e,E as Ce,S as ke,u as Ue,N as Je,R as Ze,F as Ke,a as ee,b as et}from"./task-kn7F48PQ.js";import{N as W,a as pe}from"./Card-DTIctG9o.js";function tt(e){if(typeof e=="number")return{"":e.toString()};const o={};return e.split(/ +/).forEach(s=>{if(s==="")return;const[u,c]=s.split(":");c===void 0?o[""]=u:o[u]=c}),o}function q(e,o){var s;if(e==null)return;const u=tt(e);if(o===void 0)return u[""];if(typeof o=="string")return(s=u[o])!==null&&s!==void 0?s:u[""];if(Array.isArray(o)){for(let c=o.length-1;c>=0;--c){const l=o[c];if(l in u)return u[l]}return u[""]}else{let c,l=-1;return Object.keys(u).forEach(r=>{const a=Number(r);!Number.isNaN(a)&&o>=a&&a>=l&&(l=a,c=u[r])}),c}}const rt={xs:0,s:640,m:1024,l:1280,xl:1536,"2xl":1920};function it(e){return`(min-width: ${e}px)`}const H={};function st(e=rt){if(!Ne)return C(()=>[]);if(typeof window.matchMedia!="function")return C(()=>[]);const o=F({}),s=Object.keys(e),u=(c,l)=>{c.matches?o.value[l]=!0:o.value[l]=!1};return s.forEach(c=>{const l=e[c];let r,a;H[l]===void 0?(r=window.matchMedia(it(l)),r.addEventListener?r.addEventListener("change",g=>{a.forEach(v=>{v(g,c)})}):r.addListener&&r.addListener(g=>{a.forEach(v=>{v(g,c)})}),a=new Set,H[l]={mql:r,cbs:a}):(r=H[l].mql,a=H[l].cbs),a.add(u),r.matches&&a.forEach(g=>{g(r,c)})}),Be(()=>{s.forEach(c=>{const{cbs:l}=H[e[c]];l.has(u)&&l.delete(u)})}),C(()=>{const{value:c}=o;return s.filter(l=>c[l])})}function nt(e){var o;const s=(o=e.dirs)===null||o===void 0?void 0:o.find(({dir:u})=>u===ye);return!!(s&&s.value===!1)}const ge=1,_e=Pe("n-grid"),Re=1,ot={span:{type:[Number,String],default:Re},offset:{type:[Number,String],default:0},suffix:Boolean,privateOffset:Number,privateSpan:Number,privateColStart:Number,privateShow:{type:Boolean,default:!0}},V=I({__GRID_ITEM__:!0,name:"GridItem",alias:["Gi"],props:ot,setup(){const{isSsrRef:e,xGapRef:o,itemStyleRef:s,overflowRef:u,layoutShiftDisabledRef:c}=De(_e),l=Ie();return{overflow:u,itemStyle:s,layoutShiftDisabled:c,mergedXGap:C(()=>X(o.value||0)),deriveStyle:()=>{e.value;const{privateSpan:r=Re,privateShow:a=!0,privateColStart:g=void 0,privateOffset:v=0}=l.vnode.props,{value:$}=o,x=X($||0);return{display:a?"":"none",gridColumn:`${g??`span ${r}`} / span ${r}`,marginLeft:v?`calc((100% - (${r} - 1) * ${x}) / ${r} * ${v} + ${x} * ${v})`:""}}}},render(){var e,o;if(this.layoutShiftDisabled){const{span:s,offset:u,mergedXGap:c}=this;return n("div",{style:{gridColumn:`span ${s} / span ${s}`,marginLeft:u?`calc((100% - (${s} - 1) * ${c}) / ${s} * ${u} + ${c} * ${u})`:""}},this.$slots)}return n("div",{style:[this.itemStyle,this.deriveStyle()]},(o=(e=this.$slots).default)===null||o===void 0?void 0:o.call(e,{overflow:this.overflow}))}}),lt={xs:0,s:640,m:1024,l:1280,xl:1536,xxl:1920},ze=24,ie="__ssr__",at={layoutShiftDisabled:Boolean,responsive:{type:[String,Boolean],default:"self"},cols:{type:[Number,String],default:ze},itemResponsive:Boolean,collapsed:Boolean,collapsedRows:{type:Number,default:1},itemStyle:[Object,String],xGap:{type:[Number,String],default:0},yGap:{type:[Number,String],default:0}},he=I({name:"Grid",inheritAttrs:!1,props:at,setup(e){const{mergedClsPrefixRef:o,mergedBreakpointsRef:s}=ne(e),u=/^\d+$/,c=F(void 0),l=st(s?.value||lt),r=Q(()=>!!(e.itemResponsive||!u.test(e.cols.toString())||!u.test(e.xGap.toString())||!u.test(e.yGap.toString()))),a=C(()=>{if(r.value)return e.responsive==="self"?c.value:l.value}),g=Q(()=>{var y;return(y=Number(q(e.cols.toString(),a.value)))!==null&&y!==void 0?y:ze}),v=Q(()=>q(e.xGap.toString(),a.value)),$=Q(()=>q(e.yGap.toString(),a.value)),x=y=>{c.value=y.contentRect.width},m=y=>{Ee(x,y)},S=F(!1),b=C(()=>{if(e.responsive==="self")return m}),i=F(!1),p=F();return be(()=>{const{value:y}=p;y&&y.hasAttribute(ie)&&(y.removeAttribute(ie),i.value=!0)}),Ge(_e,{layoutShiftDisabledRef:ue(e,"layoutShiftDisabled"),isSsrRef:i,itemStyleRef:ue(e,"itemStyle"),xGapRef:v,overflowRef:S}),{isSsr:!je,contentEl:p,mergedClsPrefix:o,style:C(()=>e.layoutShiftDisabled?{width:"100%",display:"grid",gridTemplateColumns:`repeat(${e.cols}, minmax(0, 1fr))`,columnGap:X(e.xGap),rowGap:X(e.yGap)}:{width:"100%",display:"grid",gridTemplateColumns:`repeat(${g.value}, minmax(0, 1fr))`,columnGap:X(v.value),rowGap:X($.value)}),isResponsive:r,responsiveQuery:a,responsiveCols:g,handleResize:b,overflow:S}},render(){if(this.layoutShiftDisabled)return n("div",ae({ref:"contentEl",class:`${this.mergedClsPrefix}-grid`,style:this.style},this.$attrs),this.$slots);const e=()=>{var o,s,u,c,l,r,a;this.overflow=!1;const g=Oe(Me(this)),v=[],{collapsed:$,collapsedRows:x,responsiveCols:m,responsiveQuery:S}=this;g.forEach(h=>{var R,k,B,P,M;if(((R=h?.type)===null||R===void 0?void 0:R.__GRID_ITEM__)!==!0)return;if(nt(h)){const A=ce(h);A.props?A.props.privateShow=!1:A.props={privateShow:!1},v.push({child:A,rawChildSpan:0});return}h.dirs=((k=h.dirs)===null||k===void 0?void 0:k.filter(({dir:A})=>A!==ye))||null,((B=h.dirs)===null||B===void 0?void 0:B.length)===0&&(h.dirs=null);const oe=ce(h),le=Number((M=q((P=oe.props)===null||P===void 0?void 0:P.span,S))!==null&&M!==void 0?M:ge);le!==0&&v.push({child:oe,rawChildSpan:le})});let b=0;const i=(o=v[v.length-1])===null||o===void 0?void 0:o.child;if(i?.props){const h=(s=i.props)===null||s===void 0?void 0:s.suffix;h!==void 0&&h!==!1&&(b=Number((c=q((u=i.props)===null||u===void 0?void 0:u.span,S))!==null&&c!==void 0?c:ge),i.props.privateSpan=b,i.props.privateColStart=m+1-b,i.props.privateShow=(l=i.props.privateShow)!==null&&l!==void 0?l:!0)}let p=0,y=!1;for(const{child:h,rawChildSpan:R}of v){if(y&&(this.overflow=!0),!y){const k=Number((a=q((r=h.props)===null||r===void 0?void 0:r.offset,S))!==null&&a!==void 0?a:0),B=Math.min(R+k,m);if(h.props?(h.props.privateSpan=B,h.props.privateOffset=k):h.props={privateSpan:B,privateOffset:k},$){const P=p%m;B+P>m&&(p+=m-P),B+p+b>x*m?y=!0:p+=B}}y&&(h.props?h.props.privateShow!==!0&&(h.props.privateShow=!1):h.props={privateShow:!1})}return n("div",ae({ref:"contentEl",class:`${this.mergedClsPrefix}-grid`,style:this.style,[ie]:this.isSsr||void 0},this.$attrs),v.map(({child:h})=>h))};return this.isResponsive&&this.responsive==="self"?n(Te,{onResize:this.handleResize},{default:e}):e()}}),ut={success:n(ke,null),error:n(Ce,null),warning:n($e,null),info:n(Se,null)},ct=I({name:"ProgressCircle",props:{clsPrefix:{type:String,required:!0},status:{type:String,required:!0},strokeWidth:{type:Number,required:!0},fillColor:[String,Object],railColor:String,railStyle:[String,Object],percentage:{type:Number,default:0},offsetDegree:{type:Number,default:0},showIndicator:{type:Boolean,required:!0},indicatorTextColor:String,unit:String,viewBoxWidth:{type:Number,required:!0},gapDegree:{type:Number,required:!0},gapOffsetDegree:{type:Number,default:0}},setup(e,{slots:o}){const s=C(()=>{const l="gradient",{fillColor:r}=e;return typeof r=="object"?`${l}-${We(JSON.stringify(r))}`:l});function u(l,r,a,g){const{gapDegree:v,viewBoxWidth:$,strokeWidth:x}=e,m=50,S=0,b=m,i=0,p=2*m,y=50+x/2,h=`M ${y},${y} m ${S},${b}
      a ${m},${m} 0 1 1 ${i},${-p}
      a ${m},${m} 0 1 1 ${-i},${p}`,R=Math.PI*2*m,k={stroke:g==="rail"?a:typeof e.fillColor=="object"?`url(#${s.value})`:a,strokeDasharray:`${Math.min(l,100)/100*(R-v)}px ${$*8}px`,strokeDashoffset:`-${v/2}px`,transformOrigin:r?"center":void 0,transform:r?`rotate(${r}deg)`:void 0};return{pathString:h,pathStyle:k}}const c=()=>{const l=typeof e.fillColor=="object",r=l?e.fillColor.stops[0]:"",a=l?e.fillColor.stops[1]:"";return l&&n("defs",null,n("linearGradient",{id:s.value,x1:"0%",y1:"100%",x2:"100%",y2:"0%"},n("stop",{offset:"0%","stop-color":r}),n("stop",{offset:"100%","stop-color":a})))};return()=>{const{fillColor:l,railColor:r,strokeWidth:a,offsetDegree:g,status:v,percentage:$,showIndicator:x,indicatorTextColor:m,unit:S,gapOffsetDegree:b,clsPrefix:i}=e,{pathString:p,pathStyle:y}=u(100,0,r,"rail"),{pathString:h,pathStyle:R}=u($,g,l,"fill"),k=100+a;return n("div",{class:`${i}-progress-content`,role:"none"},n("div",{class:`${i}-progress-graph`,"aria-hidden":!0},n("div",{class:`${i}-progress-graph-circle`,style:{transform:b?`rotate(${b}deg)`:void 0}},n("svg",{viewBox:`0 0 ${k} ${k}`},c(),n("g",null,n("path",{class:`${i}-progress-graph-circle-rail`,d:p,"stroke-width":a,"stroke-linecap":"round",fill:"none",style:y})),n("g",null,n("path",{class:[`${i}-progress-graph-circle-fill`,$===0&&`${i}-progress-graph-circle-fill--empty`],d:h,"stroke-width":a,"stroke-linecap":"round",fill:"none",style:R}))))),x?n("div",null,o.default?n("div",{class:`${i}-progress-custom-content`,role:"none"},o.default()):v!=="default"?n("div",{class:`${i}-progress-icon`,"aria-hidden":!0},n(xe,{clsPrefix:i},{default:()=>ut[v]})):n("div",{class:`${i}-progress-text`,style:{color:m},role:"none"},n("span",{class:`${i}-progress-text__percentage`},$),n("span",{class:`${i}-progress-text__unit`},S))):null)}}}),dt={success:n(ke,null),error:n(Ce,null),warning:n($e,null),info:n(Se,null)},ft=I({name:"ProgressLine",props:{clsPrefix:{type:String,required:!0},percentage:{type:Number,default:0},railColor:String,railStyle:[String,Object],fillColor:[String,Object],status:{type:String,required:!0},indicatorPlacement:{type:String,required:!0},indicatorTextColor:String,unit:{type:String,default:"%"},processing:{type:Boolean,required:!0},showIndicator:{type:Boolean,required:!0},height:[String,Number],railBorderRadius:[String,Number],fillBorderRadius:[String,Number]},setup(e,{slots:o}){const s=C(()=>L(e.height)),u=C(()=>{var r,a;return typeof e.fillColor=="object"?`linear-gradient(to right, ${(r=e.fillColor)===null||r===void 0?void 0:r.stops[0]} , ${(a=e.fillColor)===null||a===void 0?void 0:a.stops[1]})`:e.fillColor}),c=C(()=>e.railBorderRadius!==void 0?L(e.railBorderRadius):e.height!==void 0?L(e.height,{c:.5}):""),l=C(()=>e.fillBorderRadius!==void 0?L(e.fillBorderRadius):e.railBorderRadius!==void 0?L(e.railBorderRadius):e.height!==void 0?L(e.height,{c:.5}):"");return()=>{const{indicatorPlacement:r,railColor:a,railStyle:g,percentage:v,unit:$,indicatorTextColor:x,status:m,showIndicator:S,processing:b,clsPrefix:i}=e;return n("div",{class:`${i}-progress-content`,role:"none"},n("div",{class:`${i}-progress-graph`,"aria-hidden":!0},n("div",{class:[`${i}-progress-graph-line`,{[`${i}-progress-graph-line--indicator-${r}`]:!0}]},n("div",{class:`${i}-progress-graph-line-rail`,style:[{backgroundColor:a,height:s.value,borderRadius:c.value},g]},n("div",{class:[`${i}-progress-graph-line-fill`,b&&`${i}-progress-graph-line-fill--processing`],style:{maxWidth:`${e.percentage}%`,background:u.value,height:s.value,lineHeight:s.value,borderRadius:l.value}},r==="inside"?n("div",{class:`${i}-progress-graph-line-indicator`,style:{color:x}},o.default?o.default():`${v}${$}`):null)))),S&&r==="outside"?n("div",null,o.default?n("div",{class:`${i}-progress-custom-content`,style:{color:x},role:"none"},o.default()):m==="default"?n("div",{role:"none",class:`${i}-progress-icon ${i}-progress-icon--as-text`,style:{color:x}},v,$):n("div",{class:`${i}-progress-icon`,"aria-hidden":!0},n(xe,{clsPrefix:i},{default:()=>dt[m]}))):null)}}});function ve(e,o,s=100){return`m ${s/2} ${s/2-e} a ${e} ${e} 0 1 1 0 ${2*e} a ${e} ${e} 0 1 1 0 -${2*e}`}const pt=I({name:"ProgressMultipleCircle",props:{clsPrefix:{type:String,required:!0},viewBoxWidth:{type:Number,required:!0},percentage:{type:Array,default:[0]},strokeWidth:{type:Number,required:!0},circleGap:{type:Number,required:!0},showIndicator:{type:Boolean,required:!0},fillColor:{type:Array,default:()=>[]},railColor:{type:Array,default:()=>[]},railStyle:{type:Array,default:()=>[]}},setup(e,{slots:o}){const s=C(()=>e.percentage.map((l,r)=>`${Math.PI*l/100*(e.viewBoxWidth/2-e.strokeWidth/2*(1+2*r)-e.circleGap*r)*2}, ${e.viewBoxWidth*8}`)),u=(c,l)=>{const r=e.fillColor[l],a=typeof r=="object"?r.stops[0]:"",g=typeof r=="object"?r.stops[1]:"";return typeof e.fillColor[l]=="object"&&n("linearGradient",{id:`gradient-${l}`,x1:"100%",y1:"0%",x2:"0%",y2:"100%"},n("stop",{offset:"0%","stop-color":a}),n("stop",{offset:"100%","stop-color":g}))};return()=>{const{viewBoxWidth:c,strokeWidth:l,circleGap:r,showIndicator:a,fillColor:g,railColor:v,railStyle:$,percentage:x,clsPrefix:m}=e;return n("div",{class:`${m}-progress-content`,role:"none"},n("div",{class:`${m}-progress-graph`,"aria-hidden":!0},n("div",{class:`${m}-progress-graph-circle`},n("svg",{viewBox:`0 0 ${c} ${c}`},n("defs",null,x.map((S,b)=>u(S,b))),x.map((S,b)=>n("g",{key:b},n("path",{class:`${m}-progress-graph-circle-rail`,d:ve(c/2-l/2*(1+2*b)-r*b,l,c),"stroke-width":l,"stroke-linecap":"round",fill:"none",style:[{strokeDashoffset:0,stroke:v[b]},$[b]]}),n("path",{class:[`${m}-progress-graph-circle-fill`,S===0&&`${m}-progress-graph-circle-fill--empty`],d:ve(c/2-l/2*(1+2*b)-r*b,l,c),"stroke-width":l,"stroke-linecap":"round",fill:"none",style:{strokeDasharray:s.value[b],strokeDashoffset:0,stroke:typeof g[b]=="object"?`url(#gradient-${b})`:g[b]}})))))),a&&o.default?n("div",null,n("div",{class:`${m}-progress-text`},o.default())):null)}}}),gt=U([w("progress",{display:"inline-block"},[w("progress-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 `),j("line",`
 width: 100%;
 display: block;
 `,[w("progress-content",`
 display: flex;
 align-items: center;
 `,[w("progress-graph",{flex:1})]),w("progress-custom-content",{marginLeft:"14px"}),w("progress-icon",`
 width: 30px;
 padding-left: 14px;
 height: var(--n-icon-size-line);
 line-height: var(--n-icon-size-line);
 font-size: var(--n-icon-size-line);
 `,[j("as-text",`
 color: var(--n-text-color-line-outer);
 text-align: center;
 width: 40px;
 font-size: var(--n-font-size);
 padding-left: 4px;
 transition: color .3s var(--n-bezier);
 `)])]),j("circle, dashboard",{width:"120px"},[w("progress-custom-content",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `),w("progress-text",`
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
 `),w("progress-icon",`
 position: absolute;
 left: 50%;
 top: 50%;
 transform: translateX(-50%) translateY(-50%);
 display: flex;
 align-items: center;
 color: var(--n-icon-color);
 font-size: var(--n-icon-size-circle);
 `)]),j("multiple-circle",`
 width: 200px;
 color: inherit;
 `,[w("progress-text",`
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
 `)]),w("progress-content",{position:"relative"}),w("progress-graph",{position:"relative"},[w("progress-graph-circle",[U("svg",{verticalAlign:"bottom"}),w("progress-graph-circle-fill",`
 stroke: var(--n-fill-color);
 transition:
 opacity .3s var(--n-bezier),
 stroke .3s var(--n-bezier),
 stroke-dasharray .3s var(--n-bezier);
 `,[j("empty",{opacity:0})]),w("progress-graph-circle-rail",`
 transition: stroke .3s var(--n-bezier);
 overflow: hidden;
 stroke: var(--n-rail-color);
 `)]),w("progress-graph-line",[j("indicator-inside",[w("progress-graph-line-rail",`
 height: 16px;
 line-height: 16px;
 border-radius: 10px;
 `,[w("progress-graph-line-fill",`
 height: inherit;
 border-radius: 10px;
 `),w("progress-graph-line-indicator",`
 background: #0000;
 white-space: nowrap;
 text-align: right;
 margin-left: 14px;
 margin-right: 14px;
 height: inherit;
 font-size: 12px;
 color: var(--n-text-color-line-inner);
 transition: color .3s var(--n-bezier);
 `)])]),j("indicator-inside-label",`
 height: 16px;
 display: flex;
 align-items: center;
 `,[w("progress-graph-line-rail",`
 flex: 1;
 transition: background-color .3s var(--n-bezier);
 `),w("progress-graph-line-indicator",`
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
 `)]),w("progress-graph-line-rail",`
 position: relative;
 overflow: hidden;
 height: var(--n-rail-height);
 border-radius: 5px;
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 `,[w("progress-graph-line-fill",`
 background: var(--n-fill-color);
 position: relative;
 border-radius: 5px;
 height: inherit;
 width: 100%;
 max-width: 0%;
 transition:
 background-color .3s var(--n-bezier),
 max-width .2s var(--n-bezier);
 `,[j("processing",[U("&::after",`
 content: "";
 background-image: var(--n-line-bg-processing);
 animation: progress-processing-animation 2s var(--n-bezier) infinite;
 `)])])])])])]),U("@keyframes progress-processing-animation",`
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
 `)]),ht=Object.assign(Object.assign({},te.props),{processing:Boolean,type:{type:String,default:"line"},gapDegree:Number,gapOffsetDegree:Number,status:{type:String,default:"default"},railColor:[String,Array],railStyle:[String,Array],color:[String,Array,Object],viewBoxWidth:{type:Number,default:100},strokeWidth:{type:Number,default:7},percentage:[Number,Array],unit:{type:String,default:"%"},showIndicator:{type:Boolean,default:!0},indicatorPosition:{type:String,default:"outside"},indicatorPlacement:{type:String,default:"outside"},indicatorTextColor:String,circleGap:{type:Number,default:1},height:Number,borderRadius:[String,Number],fillBorderRadius:[String,Number],offsetDegree:Number}),vt=I({name:"Progress",props:ht,setup(e){const o=C(()=>e.indicatorPlacement||e.indicatorPosition),s=C(()=>{if(e.gapDegree||e.gapDegree===0)return e.gapDegree;if(e.type==="dashboard")return 75}),{mergedClsPrefixRef:u,inlineThemeDisabled:c}=ne(e),l=te("Progress","-progress",gt,Ae,e,u),r=C(()=>{const{status:g}=e,{common:{cubicBezierEaseInOut:v},self:{fontSize:$,fontSizeCircle:x,railColor:m,railHeight:S,iconSizeCircle:b,iconSizeLine:i,textColorCircle:p,textColorLineInner:y,textColorLineOuter:h,lineBgProcessing:R,fontWeightCircle:k,[de("iconColor",g)]:B,[de("fillColor",g)]:P}}=l.value;return{"--n-bezier":v,"--n-fill-color":P,"--n-font-size":$,"--n-font-size-circle":x,"--n-font-weight-circle":k,"--n-icon-color":B,"--n-icon-size-circle":b,"--n-icon-size-line":i,"--n-line-bg-processing":R,"--n-rail-color":m,"--n-rail-height":S,"--n-text-color-circle":p,"--n-text-color-line-inner":y,"--n-text-color-line-outer":h}}),a=c?we("progress",C(()=>e.status[0]),r,e):void 0;return{mergedClsPrefix:u,mergedIndicatorPlacement:o,gapDeg:s,cssVars:c?void 0:r,themeClass:a?.themeClass,onRender:a?.onRender}},render(){const{type:e,cssVars:o,indicatorTextColor:s,showIndicator:u,status:c,railColor:l,railStyle:r,color:a,percentage:g,viewBoxWidth:v,strokeWidth:$,mergedIndicatorPlacement:x,unit:m,borderRadius:S,fillBorderRadius:b,height:i,processing:p,circleGap:y,mergedClsPrefix:h,gapDeg:R,gapOffsetDegree:k,themeClass:B,$slots:P,onRender:M}=this;return M?.(),n("div",{class:[B,`${h}-progress`,`${h}-progress--${e}`,`${h}-progress--${c}`],style:o,"aria-valuemax":100,"aria-valuemin":0,"aria-valuenow":g,role:e==="circle"||e==="line"||e==="dashboard"?"progressbar":"none"},e==="circle"||e==="dashboard"?n(ct,{clsPrefix:h,status:c,showIndicator:u,indicatorTextColor:s,railColor:l,fillColor:a,railStyle:r,offsetDegree:this.offsetDegree,percentage:g,viewBoxWidth:v,strokeWidth:$,gapDegree:R===void 0?e==="dashboard"?75:0:R,gapOffsetDegree:k,unit:m},P):e==="line"?n(ft,{clsPrefix:h,status:c,showIndicator:u,indicatorTextColor:s,railColor:l,fillColor:a,railStyle:r,percentage:g,processing:p,indicatorPlacement:x,unit:m,fillBorderRadius:b,railBorderRadius:S,height:i},P):e==="multiple-circle"?n(pt,{clsPrefix:h,strokeWidth:$,railColor:l,fillColor:a,railStyle:r,viewBoxWidth:v,percentage:g,showIndicator:u,circleGap:y},P):null)}}),mt=w("statistic",[J("label",`
 font-weight: var(--n-label-font-weight);
 transition: .3s color var(--n-bezier);
 font-size: var(--n-label-font-size);
 color: var(--n-label-text-color);
 `),w("statistic-value",`
 margin-top: 4px;
 font-weight: var(--n-value-font-weight);
 `,[J("prefix",`
 margin: 0 4px 0 0;
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-prefix-text-color);
 `,[w("icon",{verticalAlign:"-0.125em"})]),J("content",`
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-text-color);
 `),J("suffix",`
 margin: 0 0 0 4px;
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-suffix-text-color);
 `,[w("icon",{verticalAlign:"-0.125em"})])])]),yt=Object.assign(Object.assign({},te.props),{tabularNums:Boolean,label:String,value:[String,Number]}),se=I({name:"Statistic",props:yt,slots:Object,setup(e){const{mergedClsPrefixRef:o,inlineThemeDisabled:s,mergedRtlRef:u}=ne(e),c=te("Statistic","-statistic",mt,Le,e,o),l=qe("Statistic",u,o),r=C(()=>{const{self:{labelFontWeight:g,valueFontSize:v,valueFontWeight:$,valuePrefixTextColor:x,labelTextColor:m,valueSuffixTextColor:S,valueTextColor:b,labelFontSize:i},common:{cubicBezierEaseInOut:p}}=c.value;return{"--n-bezier":p,"--n-label-font-size":i,"--n-label-font-weight":g,"--n-label-text-color":m,"--n-value-font-weight":$,"--n-value-font-size":v,"--n-value-prefix-text-color":x,"--n-value-suffix-text-color":S,"--n-value-text-color":b}}),a=s?we("statistic",void 0,r,e):void 0;return{rtlEnabled:l,mergedClsPrefix:o,cssVars:s?void 0:r,themeClass:a?.themeClass,onRender:a?.onRender}},render(){var e;const{mergedClsPrefix:o,$slots:{default:s,label:u,prefix:c,suffix:l}}=this;return(e=this.onRender)===null||e===void 0||e.call(this),n("div",{class:[`${o}-statistic`,this.themeClass,this.rtlEnabled&&`${o}-statistic--rtl`],style:this.cssVars},Z(u,r=>n("div",{class:`${o}-statistic__label`},this.label||r)),n("div",{class:`${o}-statistic-value`,style:{fontVariantNumeric:this.tabularNums?"tabular-nums":""}},Z(c,r=>r&&n("span",{class:`${o}-statistic-value__prefix`},r)),this.value!==void 0?n("span",{class:`${o}-statistic-value__content`},this.value):Z(s,r=>r&&n("span",{class:`${o}-statistic-value__content`},r)),Z(l,r=>r&&n("span",{class:`${o}-statistic-value__suffix`},r))))}}),bt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},xt=I({name:"AlertCircleOutline",render:function(o,s){return N(),T("svg",bt,s[0]||(s[0]=[_("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),_("path",{d:"M250.26 166.05L256 288l5.73-121.95a5.74 5.74 0 0 0-5.79-6h0a5.74 5.74 0 0 0-5.68 6z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),_("path",{d:"M256 367.91a20 20 0 1 1 20-20a20 20 0 0 1-20 20z",fill:"currentColor"},null,-1)]))}}),wt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},me=I({name:"CheckmarkCircleOutline",render:function(o,s){return N(),T("svg",wt,s[0]||(s[0]=[_("path",{d:"M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),_("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 176L217.6 336L160 272"},null,-1)]))}}),St={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},$t=I({name:"TrendingUpOutline",render:function(o,s){return N(),T("svg",St,s[0]||(s[0]=[_("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 144h112v112"},null,-1),_("path",{d:"M48 368l121.37-121.37a32 32 0 0 1 45.26 0l50.74 50.74a32 32 0 0 0 45.26 0L448 160",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Ct={class:"dashboard"},kt={class:"dashboard-header"},_t={class:"stat-value"},Rt={key:0,class:"change-list"},zt={class:"task-name"},Nt={key:0,class:"more-hint"},Bt=I({__name:"Dashboard",setup(e){const o=Xe(),s=Ve(),u=Ue();let c=null;const l=F(!0),r=i=>{if(i<60)return`${Math.floor(i)}秒`;if(i<3600)return`${Math.floor(i/60)}分钟`;if(i<86400){const p=Math.floor(i/3600),y=Math.floor(i%3600/60);return`${p}小时${y}分钟`}else{const p=Math.floor(i/86400),y=Math.floor(i%86400/3600);return`${p}天${y}小时`}},a=i=>{if(!i)return"-";try{return new Date(i).toLocaleString("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})}catch{return i}},g=C(()=>{const i=s.totalExecutions;return i===0?100:Math.round(s.successfulExecutions/i*100)}),v=C(()=>[...u.tasks].filter(i=>i.last_change).sort((i,p)=>{const y=new Date(i.last_change||0).getTime();return new Date(p.last_change||0).getTime()-y}).slice(0,5)),$=[{title:"任务名称",key:"name",ellipsis:{tooltip:!0}},{title:"状态",key:"status",width:100,render:i=>i.enabled?i.error_count>0?n(ee,{type:"error",size:"small"},{default:()=>"错误"}):n(ee,{type:"success",size:"small"},{default:()=>"正常"}):n(ee,{type:"default",size:"small"},{default:()=>"已禁用"})},{title:"最后变化",key:"last_change",width:140,render:i=>a(i.last_change)},{title:"变化次数",key:"change_count",width:90,align:"center"}],x=async()=>{l.value=!0;try{await Promise.all([s.fetchStatus(),u.fetchTasks()])}finally{l.value=!1}},m=async()=>{await x()},S=()=>{o.push("/tasks")},b=()=>{o.push("/history")};return be(async()=>{await x(),c=window.setInterval(x,3e4)}),Fe(()=>{c&&clearInterval(c)}),(i,p)=>(N(),T("div",Ct,[d(t(Je),{show:l.value},{default:f(()=>[_("div",kt,[p[0]||(p[0]=_("h2",{class:"page-title"},"仪表盘",-1)),d(t(Y),{quaternary:"",circle:"",onClick:m},{icon:f(()=>[d(t(E),null,{default:f(()=>[d(t(Ze))]),_:1})]),_:1})]),d(t(he),{cols:24,"x-gap":16,"y-gap":16},{default:f(()=>[d(t(V),{span:6},{default:f(()=>[d(t(W),{class:"stat-card"},{default:f(()=>[d(t(D),{vertical:""},{default:f(()=>[d(t(D),{align:"center",justify:"space-between",style:{width:"100%"}},{default:f(()=>[p[1]||(p[1]=_("span",{class:"stat-label"},"任务总数",-1)),d(t(E),{size:"24",color:"#63e2b7"},{default:f(()=>[d(t(Ke))]),_:1})]),_:1}),d(t(se),{value:t(u).total},null,8,["value"]),d(t(O),{depth:"3"},{default:f(()=>[z("活跃: "+G(t(u).activeCount),1)]),_:1})]),_:1})]),_:1})]),_:1}),d(t(V),{span:6},{default:f(()=>[d(t(W),{class:"stat-card"},{default:f(()=>[d(t(D),{vertical:""},{default:f(()=>[d(t(D),{align:"center",justify:"space-between",style:{width:"100%"}},{default:f(()=>[p[2]||(p[2]=_("span",{class:"stat-label"},"检测到的变化",-1)),d(t(E),{size:"24",color:"#f2c97d"},{default:f(()=>[d(t($t))]),_:1})]),_:1}),d(t(se),{value:t(s).totalChanges},null,8,["value"]),d(t(O),{depth:"3"},{default:f(()=>[z("执行次数: "+G(t(s).totalExecutions),1)]),_:1})]),_:1})]),_:1})]),_:1}),d(t(V),{span:6},{default:f(()=>[d(t(W),{class:"stat-card"},{default:f(()=>[d(t(D),{vertical:""},{default:f(()=>[d(t(D),{align:"center",justify:"space-between",style:{width:"100%"}},{default:f(()=>[p[3]||(p[3]=_("span",{class:"stat-label"},"成功率",-1)),d(t(E),{size:"24",color:"#70c0e8"},{default:f(()=>[d(t(me))]),_:1})]),_:1}),d(t(se),{value:g.value,suffix:"%"},null,8,["value"]),d(t(vt),{type:"line",percentage:g.value,"show-indicator":!1,height:4,color:g.value>=80?"#63e2b7":g.value>=50?"#f2c97d":"#e88080"},null,8,["percentage","color"])]),_:1})]),_:1})]),_:1}),d(t(V),{span:6},{default:f(()=>[d(t(W),{class:"stat-card"},{default:f(()=>[d(t(D),{vertical:""},{default:f(()=>[d(t(D),{align:"center",justify:"space-between",style:{width:"100%"}},{default:f(()=>[p[4]||(p[4]=_("span",{class:"stat-label"},"运行时间",-1)),d(t(E),{size:"24",color:t(s).isRunning?"#63e2b7":"#909399"},{default:f(()=>[d(t(Ye))]),_:1},8,["color"])]),_:1}),_("div",_t,[t(s).isRunning?(N(),T(re,{key:0},[z(G(r(t(s).uptime)),1)],64)):(N(),K(t(O),{key:1,depth:"3"},{default:f(()=>[...p[5]||(p[5]=[z("已停止",-1)])]),_:1}))]),d(t(O),{depth:"3"},{default:f(()=>[p[6]||(p[6]=z(" 状态: ",-1)),d(t(O),{type:t(s).isRunning?"success":"default"},{default:f(()=>[z(G(t(s).isRunning?"运行中":"已停止"),1)]),_:1},8,["type"])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),d(t(he),{cols:24,"x-gap":16,"y-gap":16,style:{"margin-top":"16px"}},{default:f(()=>[d(t(V),{span:12},{default:f(()=>[d(t(W),{title:"最近变化",class:"list-card"},{"header-extra":f(()=>[d(t(Y),{text:"",type:"primary",onClick:b},{default:f(()=>[...p[7]||(p[7]=[z("查看全部",-1)])]),_:1})]),default:f(()=>[v.value.length>0?(N(),T("div",Rt,[(N(!0),T(re,null,He(v.value,y=>(N(),T("div",{key:y.id,class:"change-item"},[d(t(D),{align:"center",justify:"space-between",style:{width:"100%"}},{default:f(()=>[d(t(D),{align:"center"},{default:f(()=>[d(t(E),{color:"#63e2b7"},{default:f(()=>[d(t(me))]),_:1}),_("span",zt,G(y.name),1)]),_:2},1024),d(t(D),{align:"center"},{default:f(()=>[d(t(ee),{size:"small",round:""},{default:f(()=>[z(G(y.change_count)+"次",1)]),_:2},1024),d(t(O),{depth:"3",style:{"font-size":"12px"}},{default:f(()=>[z(G(a(y.last_change)),1)]),_:2},1024)]),_:2},1024)]),_:2},1024)]))),128))])):(N(),K(t(pe),{key:1,description:"暂无变化记录"}))]),_:1})]),_:1}),d(t(V),{span:12},{default:f(()=>[d(t(W),{title:"任务概览",class:"list-card"},{"header-extra":f(()=>[d(t(Y),{text:"",type:"primary",onClick:S},{default:f(()=>[...p[8]||(p[8]=[z("管理任务",-1)])]),_:1})]),default:f(()=>[t(u).tasks.length>0?(N(),T(re,{key:0},[d(t(et),{columns:$,data:t(u).tasks.slice(0,5),bordered:!1,size:"small",pagination:!1},null,8,["data"]),t(u).total>5?(N(),T("div",Nt,[d(t(O),{depth:"3"},{default:f(()=>[z("共 "+G(t(u).total)+" 个任务",1)]),_:1})])):fe("",!0)],64)):(N(),K(t(pe),{key:1,description:"暂无任务"},{extra:f(()=>[d(t(Y),{size:"small",onClick:S},{default:f(()=>[...p[9]||(p[9]=[z("添加任务",-1)])]),_:1})]),_:1}))]),_:1})]),_:1})]),_:1}),t(u).errorCount>0?(N(),K(t(W),{key:0,class:"error-card",style:{"margin-top":"16px"}},{default:f(()=>[d(t(D),{align:"center"},{default:f(()=>[d(t(E),{size:"20",color:"#e88080"},{default:f(()=>[d(t(xt))]),_:1}),d(t(O),{type:"error"},{default:f(()=>[z(G(t(u).errorCount)+" 个任务存在错误，请检查任务配置 ",1)]),_:1}),d(t(Y),{size:"small",text:"",type:"primary",onClick:S},{default:f(()=>[...p[10]||(p[10]=[z(" 查看详情 ",-1)])]),_:1})]),_:1})]),_:1})):fe("",!0)]),_:1},8,["show"])]))}}),Tt=Qe(Bt,[["__scopeId","data-v-2307ecea"]]);export{Tt as default};
