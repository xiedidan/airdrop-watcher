import{c as m,a7 as W,bj as F,bv as D,a as w,b as q,e as y,ap as K,d as g,h as $,u as U,s as z,t as A,aa as v,au as L,g as k,j as G,ab as J,k as p,o as x,l as a}from"./index-DeyCeJbE.js";function Q(n,e){const o=W(F,null);return m(()=>n.hljs||o?.mergedHljsRef.value)}function X(n){const{textColor2:e,fontSize:o,fontWeightStrong:l,textColor3:c}=n;return{textColor:e,fontSize:o,fontWeightStrong:l,"mono-3":"#a0a1a7","hue-1":"#0184bb","hue-2":"#4078f2","hue-3":"#a626a4","hue-4":"#50a14f","hue-5":"#e45649","hue-5-2":"#c91243","hue-6":"#986801","hue-6-2":"#c18401",lineNumberTextColor:c}}const Y={common:D,self:X},Z=w([q("code",`
 font-size: var(--n-font-size);
 font-family: var(--n-font-family);
 `,[y("show-line-numbers",`
 display: flex;
 `),K("line-numbers",`
 user-select: none;
 padding-right: 12px;
 text-align: right;
 transition: color .3s var(--n-bezier);
 color: var(--n-line-number-text-color);
 `),y("word-wrap",[w("pre",`
 white-space: pre-wrap;
 word-break: break-all;
 `)]),w("pre",`
 margin: 0;
 line-height: inherit;
 font-size: inherit;
 font-family: inherit;
 `),w("[class^=hljs]",`
 color: var(--n-text-color);
 transition: 
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `)]),({props:n})=>{const e=`${n.bPrefix}code`;return[`${e} .hljs-comment,
 ${e} .hljs-quote {
 color: var(--n-mono-3);
 font-style: italic;
 }`,`${e} .hljs-doctag,
 ${e} .hljs-keyword,
 ${e} .hljs-formula {
 color: var(--n-hue-3);
 }`,`${e} .hljs-section,
 ${e} .hljs-name,
 ${e} .hljs-selector-tag,
 ${e} .hljs-deletion,
 ${e} .hljs-subst {
 color: var(--n-hue-5);
 }`,`${e} .hljs-literal {
 color: var(--n-hue-1);
 }`,`${e} .hljs-string,
 ${e} .hljs-regexp,
 ${e} .hljs-addition,
 ${e} .hljs-attribute,
 ${e} .hljs-meta-string {
 color: var(--n-hue-4);
 }`,`${e} .hljs-built_in,
 ${e} .hljs-class .hljs-title {
 color: var(--n-hue-6-2);
 }`,`${e} .hljs-attr,
 ${e} .hljs-variable,
 ${e} .hljs-template-variable,
 ${e} .hljs-type,
 ${e} .hljs-selector-class,
 ${e} .hljs-selector-attr,
 ${e} .hljs-selector-pseudo,
 ${e} .hljs-number {
 color: var(--n-hue-6);
 }`,`${e} .hljs-symbol,
 ${e} .hljs-bullet,
 ${e} .hljs-link,
 ${e} .hljs-meta,
 ${e} .hljs-selector-id,
 ${e} .hljs-title {
 color: var(--n-hue-2);
 }`,`${e} .hljs-emphasis {
 font-style: italic;
 }`,`${e} .hljs-strong {
 font-weight: var(--n-font-weight-strong);
 }`,`${e} .hljs-link {
 text-decoration: underline;
 }`]}]),ee=Object.assign(Object.assign({},k.props),{language:String,code:{type:String,default:""},trim:{type:Boolean,default:!0},hljs:Object,uri:Boolean,inline:Boolean,wordWrap:Boolean,showLineNumbers:Boolean,internalFontSize:Number,internalNoHighlight:Boolean}),se=g({name:"Code",props:ee,setup(n,{slots:e}){const{internalNoHighlight:o}=n,{mergedClsPrefixRef:l,inlineThemeDisabled:c}=U(),h=z(null),C=o?{value:void 0}:Q(n),N=(t,s,r)=>{const{value:i}=C;return!i||!(t&&i.getLanguage(t))?null:i.highlight(r?s.trim():s,{language:t}).value},M=m(()=>n.inline||n.wordWrap?!1:n.showLineNumbers),j=()=>{if(e.default)return;const{value:t}=h;if(!t)return;const{language:s}=n,r=n.uri?window.decodeURIComponent(n.code):n.code;if(s){const u=N(s,r,n.trim);if(u!==null){if(n.inline)t.innerHTML=u;else{const b=t.querySelector(".__code__");b&&t.removeChild(b);const f=document.createElement("pre");f.className="__code__",f.innerHTML=u,t.appendChild(f)}return}}if(n.inline){t.textContent=r;return}const i=t.querySelector(".__code__");if(i)i.textContent=r;else{const u=document.createElement("pre");u.className="__code__",u.textContent=r,t.innerHTML="",t.appendChild(u)}};A(j),v(L(n,"language"),j),v(L(n,"code"),j),o||v(C,j);const B=k("Code","-code",Z,Y,n,l),S=m(()=>{const{common:{cubicBezierEaseInOut:t,fontFamilyMono:s},self:{textColor:r,fontSize:i,fontWeightStrong:u,lineNumberTextColor:b,"mono-3":f,"hue-1":O,"hue-2":R,"hue-3":P,"hue-4":T,"hue-5":H,"hue-5-2":E,"hue-6":I,"hue-6-2":V}}=B.value,{internalFontSize:_}=n;return{"--n-font-size":_?`${_}px`:i,"--n-font-family":s,"--n-font-weight-strong":u,"--n-bezier":t,"--n-text-color":r,"--n-mono-3":f,"--n-hue-1":O,"--n-hue-2":R,"--n-hue-3":P,"--n-hue-4":T,"--n-hue-5":H,"--n-hue-5-2":E,"--n-hue-6":I,"--n-hue-6-2":V,"--n-line-number-text-color":b}}),d=c?G("code",m(()=>`${n.internalFontSize||"a"}`),S,n):void 0;return{mergedClsPrefix:l,codeRef:h,mergedShowLineNumbers:M,lineNumbers:m(()=>{let t=1;const s=[];let r=!1;for(const i of n.code)i===`
`?(r=!0,s.push(t++)):r=!1;return r||s.push(t++),s.join(`
`)}),cssVars:c?void 0:S,themeClass:d?.themeClass,onRender:d?.onRender}},render(){var n,e;const{mergedClsPrefix:o,wordWrap:l,mergedShowLineNumbers:c,onRender:h}=this;return h?.(),$("code",{class:[`${o}-code`,this.themeClass,l&&`${o}-code--word-wrap`,c&&`${o}-code--show-line-numbers`],style:this.cssVars,ref:"codeRef"},c?$("pre",{class:`${o}-code__line-numbers`},this.lineNumbers):null,(e=(n=this.$slots).default)===null||e===void 0?void 0:e.call(n))}}),ne=Object.assign(Object.assign({},k.props),{trigger:String,xScrollable:Boolean,onScroll:Function,contentClass:String,contentStyle:[Object,String],size:Number,yPlacement:{type:String,default:"right"},xPlacement:{type:String,default:"bottom"}}),ie=g({name:"Scrollbar",props:ne,setup(){const n=z(null);return Object.assign(Object.assign({},{scrollTo:(...o)=>{var l;(l=n.value)===null||l===void 0||l.scrollTo(o[0],o[1])},scrollBy:(...o)=>{var l;(l=n.value)===null||l===void 0||l.scrollBy(o[0],o[1])}}),{scrollbarInstRef:n})},render(){return $(J,Object.assign({ref:"scrollbarInstRef"},this.$props),this.$slots)}}),oe={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ae=g({name:"CodeSlashOutline",render:function(e,o){return x(),p("svg",oe,o[0]||(o[0]=[a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M160 368L32 256l128-112"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M352 368l128-112l-128-112"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M304 96l-96 320"},null,-1)]))}}),te={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ue=g({name:"DocumentTextOutline",render:function(e,o){return x(),p("svg",te,o[0]||(o[0]=[a("path",{d:"M416 221.25V416a48 48 0 0 1-48 48H144a48 48 0 0 1-48-48V96a48 48 0 0 1 48-48h98.75a32 32 0 0 1 22.62 9.37l141.26 141.26a32 32 0 0 1 9.37 22.62z",fill:"none",stroke:"currentColor","stroke-linejoin":"round","stroke-width":"32"},null,-1),a("path",{d:"M256 56v120a32 32 0 0 0 32 32h120",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M176 288h160"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M176 368h160"},null,-1)]))}}),le={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ce=g({name:"SparklesOutline",render:function(e,o){return x(),p("svg",le,o[0]||(o[0]=[a("path",{d:"M259.92 262.91L216.4 149.77a9 9 0 0 0-16.8 0l-43.52 113.14a9 9 0 0 1-5.17 5.17L37.77 311.6a9 9 0 0 0 0 16.8l113.14 43.52a9 9 0 0 1 5.17 5.17l43.52 113.14a9 9 0 0 0 16.8 0l43.52-113.14a9 9 0 0 1 5.17-5.17l113.14-43.52a9 9 0 0 0 0-16.8l-113.14-43.52a9 9 0 0 1-5.17-5.17z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M108 68L88 16L68 68L16 88l52 20l20 52l20-52l52-20l-52-20z"},null,-1),a("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M426.67 117.33L400 48l-26.67 69.33L304 144l69.33 26.67L400 240l26.67-69.33L496 144l-69.33-26.67z"},null,-1)]))}});export{ae as C,ue as D,se as N,ce as S,ie as a};
