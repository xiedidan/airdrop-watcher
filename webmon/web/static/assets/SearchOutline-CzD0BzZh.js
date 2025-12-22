import{b4 as ze,bc as V,s as B,aj as F,bd as Te,be as le,O as Q,bf as q,b8 as We,t as Ue,M as W,Y as ae,$ as Fe,a as _,b as z,aY as Ve,a2 as C,e as P,bg as qe,d as L,h as d,a5 as te,N as Ge,af as ve,u as re,ad as Qe,c as $,g as I,bh as Je,i as Ze,bi as et,j as ce,bj as E,F as he,bk as tt,bl as ot,a9 as nt,b9 as it,b6 as st,aO as ne,aJ as lt,bm as at,a4 as Ee,b5 as ge,aQ as rt,al as ie,a6 as D,bn as me,K as G,ai as pe,bo as je,a0 as U,bp as ct,bq as dt,br as ut,bs as ft,aR as vt,bt as ht,bu as gt,aU as mt,bv as pt,ah as Y,aP as bt,bw as Ct,P as wt,ao as oe,I as yt,bx as kt,k as xt,o as Rt,l as be}from"./index-CszZxiYV.js";import{b as Pt,c as Bt,N as St,d as $t}from"./Card-CPXwtuO1.js";import{E as Ot,W as Mt,S as zt,I as Ce,i as Tt}from"./RefreshOutline-Buv_sUGL.js";const A=B(null);function we(e){if(e.clientX>0||e.clientY>0)A.value={x:e.clientX,y:e.clientY};else{const{target:t}=e;if(t instanceof Element){const{left:o,top:l,width:u,height:r}=t.getBoundingClientRect();o>0||l>0?A.value={x:o+u/2,y:l+r/2}:A.value={x:0,y:0}}else A.value=null}}let X=0,ye=!0;function Ft(){if(!ze)return V(B(null));X===0&&F("click",document,we,!0);const e=()=>{X+=1};return ye&&(ye=Te())?(le(e),Q(()=>{X-=1,X===0&&q("click",document,we,!0)})):e(),V(A)}const Et=B(void 0);let K=0;function ke(){Et.value=Date.now()}let xe=!0;function jt(e){if(!ze)return V(B(!1));const t=B(!1);let o=null;function l(){o!==null&&window.clearTimeout(o)}function u(){l(),t.value=!0,o=window.setTimeout(()=>{t.value=!1},e)}K===0&&F("click",window,ke,!0);const r=()=>{K+=1,F("click",window,u,!0)};return xe&&(xe=Te())?(le(r),Q(()=>{K-=1,K===0&&q("click",window,ke,!0),q("click",window,u,!0),l()})):r(),V(t)}const de=B(!1);function Re(){de.value=!0}function Pe(){de.value=!1}let N=0;function It(){return We&&(le(()=>{N||(window.addEventListener("compositionstart",Re),window.addEventListener("compositionend",Pe)),N++}),Q(()=>{N<=1?(window.removeEventListener("compositionstart",Re),window.removeEventListener("compositionend",Pe),N=0):N--})),de}let j=0,Be="",Se="",$e="",Oe="";const Me=B("0px");function Nt(e){if(typeof document>"u")return;const t=document.documentElement;let o,l=!1;const u=()=>{t.style.marginRight=Be,t.style.overflow=Se,t.style.overflowX=$e,t.style.overflowY=Oe,Me.value="0px"};Ue(()=>{o=W(e,r=>{if(r){if(!j){const a=window.innerWidth-t.offsetWidth;a>0&&(Be=t.style.marginRight,t.style.marginRight=`${a}px`,Me.value=`${a}px`),Se=t.style.overflow,$e=t.style.overflowX,Oe=t.style.overflowY,t.style.overflow="hidden",t.style.overflowX="hidden",t.style.overflowY="hidden"}l=!0,j++}else j--,j||u(),l=!1},{immediate:!0})}),Q(()=>{o?.(),l&&(j--,j||u(),l=!1)})}const At=ae("n-dialog-provider"),to=ae("n-dialog-api"),ue={icon:Function,type:{type:String,default:"default"},title:[String,Function],closable:{type:Boolean,default:!0},negativeText:String,positiveText:String,positiveButtonProps:Object,negativeButtonProps:Object,content:[String,Function],action:Function,showIcon:{type:Boolean,default:!0},loading:Boolean,bordered:Boolean,iconPlacement:String,titleClass:[String,Array],titleStyle:[String,Object],contentClass:[String,Array],contentStyle:[String,Object],actionClass:[String,Array],actionStyle:[String,Object],onPositiveClick:Function,onNegativeClick:Function,onClose:Function,closeFocusable:Boolean},_t=Fe(ue),Dt=_([z("dialog",`
 --n-icon-margin: var(--n-icon-margin-top) var(--n-icon-margin-right) var(--n-icon-margin-bottom) var(--n-icon-margin-left);
 word-break: break-word;
 line-height: var(--n-line-height);
 position: relative;
 background: var(--n-color);
 color: var(--n-text-color);
 box-sizing: border-box;
 margin: auto;
 border-radius: var(--n-border-radius);
 padding: var(--n-padding);
 transition: 
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `,[C("icon",`
 color: var(--n-icon-color);
 `),P("bordered",`
 border: var(--n-border);
 `),P("icon-top",[C("close",`
 margin: var(--n-close-margin);
 `),C("icon",`
 margin: var(--n-icon-margin);
 `),C("content",`
 text-align: center;
 `),C("title",`
 justify-content: center;
 `),C("action",`
 justify-content: center;
 `)]),P("icon-left",[C("icon",`
 margin: var(--n-icon-margin);
 `),P("closable",[C("title",`
 padding-right: calc(var(--n-close-size) + 6px);
 `)])]),C("close",`
 position: absolute;
 right: 0;
 top: 0;
 margin: var(--n-close-margin);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 z-index: 1;
 `),C("content",`
 font-size: var(--n-font-size);
 margin: var(--n-content-margin);
 position: relative;
 word-break: break-word;
 `,[P("last","margin-bottom: 0;")]),C("action",`
 display: flex;
 justify-content: flex-end;
 `,[_("> *:not(:last-child)",`
 margin-right: var(--n-action-space);
 `)]),C("icon",`
 font-size: var(--n-icon-size);
 transition: color .3s var(--n-bezier);
 `),C("title",`
 transition: color .3s var(--n-bezier);
 display: flex;
 align-items: center;
 font-size: var(--n-title-font-size);
 font-weight: var(--n-title-font-weight);
 color: var(--n-title-text-color);
 `),z("dialog-icon-container",`
 display: flex;
 justify-content: center;
 `)]),Ve(z("dialog",`
 width: 446px;
 max-width: calc(100vw - 32px);
 `)),z("dialog",[qe(`
 width: 446px;
 max-width: calc(100vw - 32px);
 `)])]),Lt={default:()=>d(Ce,null),info:()=>d(Ce,null),success:()=>d(zt,null),warning:()=>d(Mt,null),error:()=>d(Ot,null)},Ht=L({name:"Dialog",alias:["NimbusConfirmCard","Confirm"],props:Object.assign(Object.assign({},I.props),ue),slots:Object,setup(e){const{mergedComponentPropsRef:t,mergedClsPrefixRef:o,inlineThemeDisabled:l,mergedRtlRef:u}=re(e),r=Qe("Dialog",u,o),a=$(()=>{var g,m;const{iconPlacement:x}=e;return x||((m=(g=t?.value)===null||g===void 0?void 0:g.Dialog)===null||m===void 0?void 0:m.iconPlacement)||"left"});function h(g){const{onPositiveClick:m}=e;m&&m(g)}function c(g){const{onNegativeClick:m}=e;m&&m(g)}function w(){const{onClose:g}=e;g&&g()}const k=I("Dialog","-dialog",Dt,Je,e,o),y=$(()=>{const{type:g}=e,m=a.value,{common:{cubicBezierEaseInOut:x},self:{fontSize:S,lineHeight:O,border:v,titleTextColor:M,textColor:R,color:p,closeBorderRadius:i,closeColorHover:s,closeColorPressed:n,closeIconColor:b,closeIconColorHover:T,closeIconColorPressed:J,closeIconSize:Z,borderRadius:ee,titleFontWeight:Ie,titleFontSize:Ne,padding:Ae,iconSize:_e,actionSpace:De,contentMargin:Le,closeSize:He,[m==="top"?"iconMarginIconTop":"iconMargin"]:Ye,[m==="top"?"closeMarginIconTop":"closeMargin"]:Xe,[Ze("iconColor",g)]:Ke}}=k.value,H=et(Ye);return{"--n-font-size":S,"--n-icon-color":Ke,"--n-bezier":x,"--n-close-margin":Xe,"--n-icon-margin-top":H.top,"--n-icon-margin-right":H.right,"--n-icon-margin-bottom":H.bottom,"--n-icon-margin-left":H.left,"--n-icon-size":_e,"--n-close-size":He,"--n-close-icon-size":Z,"--n-close-border-radius":i,"--n-close-color-hover":s,"--n-close-color-pressed":n,"--n-close-icon-color":b,"--n-close-icon-color-hover":T,"--n-close-icon-color-pressed":J,"--n-color":p,"--n-text-color":R,"--n-border-radius":ee,"--n-padding":Ae,"--n-line-height":O,"--n-border":v,"--n-content-margin":Le,"--n-title-font-size":Ne,"--n-title-font-weight":Ie,"--n-title-text-color":M,"--n-action-space":De}}),f=l?ce("dialog",$(()=>`${e.type[0]}${a.value[0]}`),y,e):void 0;return{mergedClsPrefix:o,rtlEnabled:r,mergedIconPlacement:a,mergedTheme:k,handlePositiveClick:h,handleNegativeClick:c,handleCloseClick:w,cssVars:l?void 0:y,themeClass:f?.themeClass,onRender:f?.onRender}},render(){var e;const{bordered:t,mergedIconPlacement:o,cssVars:l,closable:u,showIcon:r,title:a,content:h,action:c,negativeText:w,positiveText:k,positiveButtonProps:y,negativeButtonProps:f,handlePositiveClick:g,handleNegativeClick:m,mergedTheme:x,loading:S,type:O,mergedClsPrefix:v}=this;(e=this.onRender)===null||e===void 0||e.call(this);const M=r?d(Ge,{clsPrefix:v,class:`${v}-dialog__icon`},{default:()=>te(this.$slots.icon,p=>p||(this.icon?E(this.icon):Lt[this.type]()))}):null,R=te(this.$slots.action,p=>p||k||w||c?d("div",{class:[`${v}-dialog__action`,this.actionClass],style:this.actionStyle},p||(c?[E(c)]:[this.negativeText&&d(he,Object.assign({theme:x.peers.Button,themeOverrides:x.peerOverrides.Button,ghost:!0,size:"small",onClick:m},f),{default:()=>E(this.negativeText)}),this.positiveText&&d(he,Object.assign({theme:x.peers.Button,themeOverrides:x.peerOverrides.Button,size:"small",type:O==="default"?"primary":O,disabled:S,loading:S,onClick:g},y),{default:()=>E(this.positiveText)})])):null);return d("div",{class:[`${v}-dialog`,this.themeClass,this.closable&&`${v}-dialog--closable`,`${v}-dialog--icon-${o}`,t&&`${v}-dialog--bordered`,this.rtlEnabled&&`${v}-dialog--rtl`],style:l,role:"dialog"},u?te(this.$slots.close,p=>{const i=[`${v}-dialog__close`,this.rtlEnabled&&`${v}-dialog--rtl`];return p?d("div",{class:i},p):d(Pt,{focusable:this.closeFocusable,clsPrefix:v,class:i,onClick:this.handleCloseClick})}):null,r&&o==="top"?d("div",{class:`${v}-dialog-icon-container`},M):null,d("div",{class:[`${v}-dialog__title`,this.titleClass],style:this.titleStyle},r&&o==="left"?M:null,ve(this.$slots.header,()=>[E(a)])),d("div",{class:[`${v}-dialog__content`,R?"":`${v}-dialog__content--last`,this.contentClass],style:this.contentStyle},ve(this.$slots.default,()=>[E(h)])),R)}}),se="n-draggable";function Yt(e,t){let o;const l=$(()=>e.value!==!1),u=$(()=>l.value?se:""),r=$(()=>{const c=e.value;return c===!0||c===!1?!0:c?c.bounds!=="none":!0});function a(c){const w=c.querySelector(`.${se}`);if(!w||!u.value)return;let k=0,y=0,f=0,g=0,m=0,x=0,S;function O(R){R.preventDefault(),S=R;const{x:p,y:i,right:s,bottom:n}=c.getBoundingClientRect();y=p,g=i,k=window.innerWidth-s,f=window.innerHeight-n;const{left:b,top:T}=c.style;m=+T.slice(0,-2),x=+b.slice(0,-2)}function v(R){if(!S)return;const{clientX:p,clientY:i}=S;let s=R.clientX-p,n=R.clientY-i;r.value&&(s>k?s=k:-s>y&&(s=-y),n>f?n=f:-n>g&&(n=-g));const b=s+x,T=n+m;c.style.top=`${T}px`,c.style.left=`${b}px`}function M(){S=void 0,t.onEnd(c)}F("mousedown",w,O),F("mousemove",window,v),F("mouseup",window,M),o=()=>{q("mousedown",w,O),F("mousemove",window,v),F("mouseup",window,M)}}function h(){o&&(o(),o=void 0)}return tt(h),{stopDrag:h,startDrag:a,draggableRef:l,draggableClassRef:u}}const fe=Object.assign(Object.assign({},Bt),ue),Xt=Fe(fe),Kt=L({name:"ModalBody",inheritAttrs:!1,slots:Object,props:Object.assign(Object.assign({show:{type:Boolean,required:!0},preset:String,displayDirective:{type:String,required:!0},trapFocus:{type:Boolean,default:!0},autoFocus:{type:Boolean,default:!0},blockScroll:Boolean,draggable:{type:[Boolean,Object],default:!1},maskHidden:Boolean},fe),{renderMask:Function,onClickoutside:Function,onBeforeLeave:{type:Function,required:!0},onAfterLeave:{type:Function,required:!0},onPositiveClick:{type:Function,required:!0},onNegativeClick:{type:Function,required:!0},onClose:{type:Function,required:!0},onAfterEnter:Function,onEsc:Function}),setup(e){const t=B(null),o=B(null),l=B(e.show),u=B(null),r=B(null),a=G(je);let h=null;W(D(e,"show"),n=>{n&&(h=a.getMousePosition())},{immediate:!0});const{stopDrag:c,startDrag:w,draggableRef:k,draggableClassRef:y}=Yt(D(e,"draggable"),{onEnd:n=>{x(n)}}),f=$(()=>me([e.titleClass,y.value])),g=$(()=>me([e.headerClass,y.value]));W(D(e,"show"),n=>{n&&(l.value=!0)}),Nt($(()=>e.blockScroll&&l.value));function m(){if(a.transformOriginRef.value==="center")return"";const{value:n}=u,{value:b}=r;if(n===null||b===null)return"";if(o.value){const T=o.value.containerScrollTop;return`${n}px ${b+T}px`}return""}function x(n){if(a.transformOriginRef.value==="center"||!h||!o.value)return;const b=o.value.containerScrollTop,{offsetLeft:T,offsetTop:J}=n,Z=h.y,ee=h.x;u.value=-(T-ee),r.value=-(J-Z-b),n.style.transformOrigin=m()}function S(n){pe(()=>{x(n)})}function O(n){n.style.transformOrigin=m(),e.onBeforeLeave()}function v(n){const b=n;k.value&&w(b),e.onAfterEnter&&e.onAfterEnter(b)}function M(){l.value=!1,u.value=null,r.value=null,c(),e.onAfterLeave()}function R(){const{onClose:n}=e;n&&n()}function p(){e.onNegativeClick()}function i(){e.onPositiveClick()}const s=B(null);return W(s,n=>{n&&pe(()=>{const b=n.el;b&&t.value!==b&&(t.value=b)})}),U(ct,t),U(dt,null),U(ut,null),{mergedTheme:a.mergedThemeRef,appear:a.appearRef,isMounted:a.isMountedRef,mergedClsPrefix:a.mergedClsPrefixRef,bodyRef:t,scrollbarRef:o,draggableClass:y,displayed:l,childNodeRef:s,cardHeaderClass:g,dialogTitleClass:f,handlePositiveClick:i,handleNegativeClick:p,handleCloseClick:R,handleAfterEnter:v,handleAfterLeave:M,handleBeforeLeave:O,handleEnter:S}},render(){const{$slots:e,$attrs:t,handleEnter:o,handleAfterEnter:l,handleAfterLeave:u,handleBeforeLeave:r,preset:a,mergedClsPrefix:h}=this;let c=null;if(!a){if(c=ot("default",e.default,{draggableClass:this.draggableClass}),!c){nt("modal","default slot is empty");return}c=it(c),c.props=st({class:`${h}-modal`},t,c.props||{})}return this.displayDirective==="show"||this.displayed||this.show?ne(d("div",{role:"none",class:[`${h}-modal-body-wrapper`,this.maskHidden&&`${h}-modal-body-wrapper--mask-hidden`]},d(lt,{ref:"scrollbarRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:`${h}-modal-scroll-content`},{default:()=>{var w;return[(w=this.renderMask)===null||w===void 0?void 0:w.call(this),d(at,{disabled:!this.trapFocus||this.maskHidden,active:this.show,onEsc:this.onEsc,autoFocus:this.autoFocus},{default:()=>{var k;return d(Ee,{name:"fade-in-scale-up-transition",appear:(k=this.appear)!==null&&k!==void 0?k:this.isMounted,onEnter:o,onAfterEnter:l,onAfterLeave:u,onBeforeLeave:r},{default:()=>{const y=[[ge,this.show]],{onClickoutside:f}=this;return f&&y.push([rt,this.onClickoutside,void 0,{capture:!0}]),ne(this.preset==="confirm"||this.preset==="dialog"?d(Ht,Object.assign({},this.$attrs,{class:[`${h}-modal`,this.$attrs.class],ref:"bodyRef",theme:this.mergedTheme.peers.Dialog,themeOverrides:this.mergedTheme.peerOverrides.Dialog},ie(this.$props,_t),{titleClass:this.dialogTitleClass,"aria-modal":"true"}),e):this.preset==="card"?d(St,Object.assign({},this.$attrs,{ref:"bodyRef",class:[`${h}-modal`,this.$attrs.class],theme:this.mergedTheme.peers.Card,themeOverrides:this.mergedTheme.peerOverrides.Card},ie(this.$props,$t),{headerClass:this.cardHeaderClass,"aria-modal":"true",role:"dialog"}),e):this.childNodeRef=c,y)}})}})]}})),[[ge,this.displayDirective==="if"||this.displayed||this.show]]):null}}),Wt=_([z("modal-container",`
 position: fixed;
 left: 0;
 top: 0;
 height: 0;
 width: 0;
 display: flex;
 `),z("modal-mask",`
 position: fixed;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 background-color: rgba(0, 0, 0, .4);
 `,[ft({enterDuration:".25s",leaveDuration:".25s",enterCubicBezier:"var(--n-bezier-ease-out)",leaveCubicBezier:"var(--n-bezier-ease-out)"})]),z("modal-body-wrapper",`
 position: fixed;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 overflow: visible;
 `,[z("modal-scroll-content",`
 min-height: 100%;
 display: flex;
 position: relative;
 `),P("mask-hidden","pointer-events: none;",[z("modal-scroll-content",[_("> *",`
 pointer-events: all;
 `)])])]),z("modal",`
 position: relative;
 align-self: center;
 color: var(--n-text-color);
 margin: auto;
 box-shadow: var(--n-box-shadow);
 `,[vt({duration:".25s",enterScale:".5"}),_(`.${se}`,`
 cursor: move;
 user-select: none;
 `)])]),Ut=Object.assign(Object.assign(Object.assign(Object.assign({},I.props),{show:Boolean,showMask:{type:Boolean,default:!0},maskClosable:{type:Boolean,default:!0},preset:String,to:[String,Object],displayDirective:{type:String,default:"if"},transformOrigin:{type:String,default:"mouse"},zIndex:Number,autoFocus:{type:Boolean,default:!0},trapFocus:{type:Boolean,default:!0},closeOnEsc:{type:Boolean,default:!0},blockScroll:{type:Boolean,default:!0}}),fe),{draggable:[Boolean,Object],onEsc:Function,"onUpdate:show":[Function,Array],onUpdateShow:[Function,Array],onAfterEnter:Function,onBeforeLeave:Function,onAfterLeave:Function,onClose:Function,onPositiveClick:Function,onNegativeClick:Function,onMaskClick:Function,internalDialog:Boolean,internalModal:Boolean,internalAppear:{type:Boolean,default:void 0},overlayStyle:[String,Object],onBeforeHide:Function,onAfterHide:Function,onHide:Function,unstableShowMask:{type:Boolean,default:void 0}}),oo=L({name:"Modal",inheritAttrs:!1,props:Ut,slots:Object,setup(e){const t=B(null),{mergedClsPrefixRef:o,namespaceRef:l,inlineThemeDisabled:u}=re(e),r=I("Modal","-modal",Wt,pt,e,o),a=jt(64),h=Ft(),c=mt(),w=e.internalDialog?G(At,null):null,k=e.internalModal?G(Ct,null):null,y=It();function f(i){const{onUpdateShow:s,"onUpdate:show":n,onHide:b}=e;s&&Y(s,i),n&&Y(n,i),b&&!i&&b(i)}function g(){const{onClose:i}=e;i?Promise.resolve(i()).then(s=>{s!==!1&&f(!1)}):f(!1)}function m(){const{onPositiveClick:i}=e;i?Promise.resolve(i()).then(s=>{s!==!1&&f(!1)}):f(!1)}function x(){const{onNegativeClick:i}=e;i?Promise.resolve(i()).then(s=>{s!==!1&&f(!1)}):f(!1)}function S(){const{onBeforeLeave:i,onBeforeHide:s}=e;i&&Y(i),s&&s()}function O(){const{onAfterLeave:i,onAfterHide:s}=e;i&&Y(i),s&&s()}function v(i){var s;const{onMaskClick:n}=e;n&&n(i),e.maskClosable&&!((s=t.value)===null||s===void 0)&&s.contains(bt(i))&&f(!1)}function M(i){var s;(s=e.onEsc)===null||s===void 0||s.call(e),e.show&&e.closeOnEsc&&Tt(i)&&(y.value||f(!1))}U(je,{getMousePosition:()=>{const i=w||k;if(i){const{clickedRef:s,clickedPositionRef:n}=i;if(s.value&&n.value)return n.value}return a.value?h.value:null},mergedClsPrefixRef:o,mergedThemeRef:r,isMountedRef:c,appearRef:D(e,"internalAppear"),transformOriginRef:D(e,"transformOrigin")});const R=$(()=>{const{common:{cubicBezierEaseOut:i},self:{boxShadow:s,color:n,textColor:b}}=r.value;return{"--n-bezier-ease-out":i,"--n-box-shadow":s,"--n-color":n,"--n-text-color":b}}),p=u?ce("theme-class",void 0,R,e):void 0;return{mergedClsPrefix:o,namespace:l,isMounted:c,containerRef:t,presetProps:$(()=>ie(e,Xt)),handleEsc:M,handleAfterLeave:O,handleClickoutside:v,handleBeforeLeave:S,doUpdateShow:f,handleNegativeClick:x,handlePositiveClick:m,handleCloseClick:g,cssVars:u?void 0:R,themeClass:p?.themeClass,onRender:p?.onRender}},render(){const{mergedClsPrefix:e}=this;return d(gt,{to:this.to,show:this.show},{default:()=>{var t;(t=this.onRender)===null||t===void 0||t.call(this);const{showMask:o}=this;return ne(d("div",{role:"none",ref:"containerRef",class:[`${e}-modal-container`,this.themeClass,this.namespace],style:this.cssVars},d(Kt,Object.assign({style:this.overlayStyle},this.$attrs,{ref:"bodyWrapper",displayDirective:this.displayDirective,show:this.show,preset:this.preset,autoFocus:this.autoFocus,trapFocus:this.trapFocus,draggable:this.draggable,blockScroll:this.blockScroll,maskHidden:!o},this.presetProps,{onEsc:this.handleEsc,onClose:this.handleCloseClick,onNegativeClick:this.handleNegativeClick,onPositiveClick:this.handlePositiveClick,onBeforeLeave:this.handleBeforeLeave,onAfterEnter:this.onAfterEnter,onAfterLeave:this.handleAfterLeave,onClickoutside:o?void 0:this.handleClickoutside,renderMask:o?()=>{var l;return d(Ee,{name:"fade-in-transition",key:"mask",appear:(l=this.internalAppear)!==null&&l!==void 0?l:this.isMounted},{default:()=>this.show?d("div",{"aria-hidden":!0,ref:"containerRef",class:`${e}-modal-mask`,onClick:this.handleClickoutside}):null})}:void 0}),this.$slots)),[[ht,{zIndex:this.zIndex,enabled:this.show}]])}})}}),Vt=ae("n-message-api");function no(){const e=G(Vt,null);return e===null&&wt("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),e}const qt=z("divider",`
 position: relative;
 display: flex;
 width: 100%;
 box-sizing: border-box;
 font-size: 16px;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
`,[oe("vertical",`
 margin-top: 24px;
 margin-bottom: 24px;
 `,[oe("no-title",`
 display: flex;
 align-items: center;
 `)]),C("title",`
 display: flex;
 align-items: center;
 margin-left: 12px;
 margin-right: 12px;
 white-space: nowrap;
 font-weight: var(--n-font-weight);
 `),P("title-position-left",[C("line",[P("left",{width:"28px"})])]),P("title-position-right",[C("line",[P("right",{width:"28px"})])]),P("dashed",[C("line",`
 background-color: #0000;
 height: 0px;
 width: 100%;
 border-style: dashed;
 border-width: 1px 0 0;
 `)]),P("vertical",`
 display: inline-block;
 height: 1em;
 margin: 0 8px;
 vertical-align: middle;
 width: 1px;
 `),C("line",`
 border: none;
 transition: background-color .3s var(--n-bezier), border-color .3s var(--n-bezier);
 height: 1px;
 width: 100%;
 margin: 0;
 `),oe("dashed",[C("line",{backgroundColor:"var(--n-color)"})]),P("dashed",[C("line",{borderColor:"var(--n-color)"})]),P("vertical",{backgroundColor:"var(--n-color)"})]),Gt=Object.assign(Object.assign({},I.props),{titlePlacement:{type:String,default:"center"},dashed:Boolean,vertical:Boolean}),io=L({name:"Divider",props:Gt,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=re(e),l=I("Divider","-divider",qt,kt,e,t),u=$(()=>{const{common:{cubicBezierEaseInOut:a},self:{color:h,textColor:c,fontWeight:w}}=l.value;return{"--n-bezier":a,"--n-color":h,"--n-text-color":c,"--n-font-weight":w}}),r=o?ce("divider",void 0,u,e):void 0;return{mergedClsPrefix:t,cssVars:o?void 0:u,themeClass:r?.themeClass,onRender:r?.onRender}},render(){var e;const{$slots:t,titlePlacement:o,vertical:l,dashed:u,cssVars:r,mergedClsPrefix:a}=this;return(e=this.onRender)===null||e===void 0||e.call(this),d("div",{role:"separator",class:[`${a}-divider`,this.themeClass,{[`${a}-divider--vertical`]:l,[`${a}-divider--no-title`]:!t.default,[`${a}-divider--dashed`]:u,[`${a}-divider--title-position-${o}`]:t.default&&o}],style:r},l?null:d("div",{class:`${a}-divider__line ${a}-divider__line--left`}),!l&&t.default?d(yt,null,d("div",{class:`${a}-divider__title`},this.$slots),d("div",{class:`${a}-divider__line ${a}-divider__line--right`})):null)}}),Qt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},so=L({name:"SearchOutline",render:function(t,o){return Rt(),xt("svg",Qt,o[0]||(o[0]=[be("path",{d:"M221.09 64a157.09 157.09 0 1 0 157.09 157.09A157.1 157.1 0 0 0 221.09 64z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),be("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32",d:"M338.29 338.29L448 448"},null,-1)]))}});export{oo as N,so as S,io as a,to as d,no as u};
