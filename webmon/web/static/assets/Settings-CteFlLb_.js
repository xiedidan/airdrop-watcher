import{d as ie,h as c,s as N,bp as Jt,bq as Fa,br as Ua,bs as Wa,bt as yt,bu as Va,bv as Kt,bw as Ka,bx as Me,by as Le,b as s,ap as T,e as z,bz as wa,a as U,aO as Ca,bA as ka,am as _a,ac as Ut,bB as Sa,u as Ve,g as he,aF as bt,c as te,bC as ft,i as de,j as We,N as wt,E as qa,W as Xa,I as Ga,S as Ya,aq as za,av as Ct,bD as Ja,a6 as qt,aA as Xt,az as ge,aj as Ra,bE as Qa,au as pe,aL as $a,ae as Qt,bi as Za,bF as en,b0 as tn,aQ as an,a7 as kt,an as Gt,ay as Zt,bG as nn,bH as rn,bI as ln,bJ as on,H as Z,B as G,as as Ta,a9 as Je,bK as sn,aW as Ia,aX as Pa,bL as dn,ao as ea,bM as un,af as cn,ag as fn,ah as vn,ar as Wt,ai as bn,aa as vt,aK as pn,aw as gn,aZ as pt,bj as gt,bN as mn,O as Pe,b5 as hn,aS as Ht,aP as Bt,bO as xn,bP as ta,t as Aa,bQ as yn,aB as wn,ba as Cn,bR as kn,aU as _n,bS as Sn,k as ue,o as q,l as Q,bT as zn,bU as Ae,v as t,w as r,x as e,R as aa,aH as Fe,bV as Ie,bW as Rn,L as ut,M as se,D as C,J as X,F as ee,bX as $n,Q as ct,C as mt,T as Tn,z as be,A as Xe,bY as In,bZ as Pn,_ as An}from"./index-tAneExlJ.js";import{m as J,N as _e,d as na}from"./discrete-T1T4YqhK.js";import{f as Oa,N as Ge,a as P,b as oe,c as Ue,A as On,P as En,d as jn,C as Hn,e as Bn,T as Nn}from"./TrashOutline-Bpbq1DvO.js";import{t as Dn,a as ze,c as me,u as Mn,s as Ln,i as Fn,N as Nt,d as ht,R as ra,b as Un,F as Wn}from"./RefreshOutline-njQl8I8M.js";import{D as la,S as Vn,C as oa,N as Dt,a as Se,b as ia,c as sa}from"./SparklesOutline-DlScG-K3.js";const Kn=Jt(".v-x-scroll",{overflow:"auto",scrollbarWidth:"none"},[Jt("&::-webkit-scrollbar",{width:0,height:0})]),qn=ie({name:"XScroll",props:{disabled:Boolean,onScroll:Function},setup(){const n=N(null);function o(v){!(v.currentTarget.offsetWidth<v.currentTarget.scrollWidth)||v.deltaY===0||(v.currentTarget.scrollLeft+=v.deltaY+v.deltaX,v.preventDefault())}const i=Fa();return Kn.mount({id:"vueuc/x-scroll",head:!0,anchorMetaName:Ua,ssr:i}),Object.assign({selfRef:n,handleWheel:o},{scrollTo(...v){var g;(g=n.value)===null||g===void 0||g.scrollTo(...v)}})},render(){return c("div",{ref:"selfRef",onScroll:this.onScroll,onWheel:this.disabled?void 0:this.handleWheel,class:"v-x-scroll"},this.$slots)}});var Xn=/\s/;function Gn(n){for(var o=n.length;o--&&Xn.test(n.charAt(o)););return o}var Yn=/^\s+/;function Jn(n){return n&&n.slice(0,Gn(n)+1).replace(Yn,"")}var da=NaN,Qn=/^[-+]0x[0-9a-f]+$/i,Zn=/^0b[01]+$/i,er=/^0o[0-7]+$/i,tr=parseInt;function ua(n){if(typeof n=="number")return n;if(Wa(n))return da;if(yt(n)){var o=typeof n.valueOf=="function"?n.valueOf():n;n=yt(o)?o+"":o}if(typeof n!="string")return n===0?n:+n;n=Jn(n);var i=Zn.test(n);return i||er.test(n)?tr(n.slice(2),i?2:8):Qn.test(n)?da:+n}var Mt=function(){return Va.Date.now()},ar="Expected a function",nr=Math.max,rr=Math.min;function lr(n,o,i){var p,v,g,$,h,x,_=0,y=!1,m=!1,O=!0;if(typeof n!="function")throw new TypeError(ar);o=ua(o)||0,yt(i)&&(y=!!i.leading,m="maxWait"in i,g=m?nr(ua(i.maxWait)||0,o):g,O="trailing"in i?!!i.trailing:O);function w(E){var M=p,V=v;return p=v=void 0,_=E,$=n.apply(V,M),$}function S(E){return _=E,h=setTimeout(I,o),y?w(E):$}function D(E){var M=E-x,V=E-_,W=o-M;return m?rr(W,g-V):W}function j(E){var M=E-x,V=E-_;return x===void 0||M>=o||M<0||m&&V>=g}function I(){var E=Mt();if(j(E))return F(E);h=setTimeout(I,D(E))}function F(E){return h=void 0,O&&p?w(E):(p=v=void 0,$)}function ae(){h!==void 0&&clearTimeout(h),_=0,p=x=v=h=void 0}function L(){return h===void 0?$:F(Mt())}function A(){var E=Mt(),M=j(E);if(p=arguments,v=this,x=E,M){if(h===void 0)return S(x);if(m)return clearTimeout(h),h=setTimeout(I,o),w(x)}return h===void 0&&(h=setTimeout(I,o)),$}return A.cancel=ae,A.flush=L,A}var or="Expected a function";function ir(n,o,i){var p=!0,v=!0;if(typeof n!="function")throw new TypeError(or);return yt(i)&&(p="leading"in i?!!i.leading:p,v="trailing"in i?!!i.trailing:v),lr(n,o,{leading:p,maxWait:o,trailing:v})}const sr=ie({name:"ChevronLeft",render(){return c("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg"},c("path",{d:"M10.3536 3.14645C10.5488 3.34171 10.5488 3.65829 10.3536 3.85355L6.20711 8L10.3536 12.1464C10.5488 12.3417 10.5488 12.6583 10.3536 12.8536C10.1583 13.0488 9.84171 13.0488 9.64645 12.8536L5.14645 8.35355C4.95118 8.15829 4.95118 7.84171 5.14645 7.64645L9.64645 3.14645C9.84171 2.95118 10.1583 2.95118 10.3536 3.14645Z",fill:"currentColor"}))}});function dr(n){const{lineHeight:o,borderRadius:i,fontWeightStrong:p,baseColor:v,dividerColor:g,actionColor:$,textColor1:h,textColor2:x,closeColorHover:_,closeColorPressed:y,closeIconColor:m,closeIconColorHover:O,closeIconColorPressed:w,infoColor:S,successColor:D,warningColor:j,errorColor:I,fontSize:F}=n;return Object.assign(Object.assign({},Ka),{fontSize:F,lineHeight:o,titleFontWeight:p,borderRadius:i,border:`1px solid ${g}`,color:$,titleTextColor:h,iconColor:x,contentTextColor:x,closeBorderRadius:i,closeColorHover:_,closeColorPressed:y,closeIconColor:m,closeIconColorHover:O,closeIconColorPressed:w,borderInfo:`1px solid ${Me(v,Le(S,{alpha:.25}))}`,colorInfo:Me(v,Le(S,{alpha:.08})),titleTextColorInfo:h,iconColorInfo:S,contentTextColorInfo:x,closeColorHoverInfo:_,closeColorPressedInfo:y,closeIconColorInfo:m,closeIconColorHoverInfo:O,closeIconColorPressedInfo:w,borderSuccess:`1px solid ${Me(v,Le(D,{alpha:.25}))}`,colorSuccess:Me(v,Le(D,{alpha:.08})),titleTextColorSuccess:h,iconColorSuccess:D,contentTextColorSuccess:x,closeColorHoverSuccess:_,closeColorPressedSuccess:y,closeIconColorSuccess:m,closeIconColorHoverSuccess:O,closeIconColorPressedSuccess:w,borderWarning:`1px solid ${Me(v,Le(j,{alpha:.33}))}`,colorWarning:Me(v,Le(j,{alpha:.08})),titleTextColorWarning:h,iconColorWarning:j,contentTextColorWarning:x,closeColorHoverWarning:_,closeColorPressedWarning:y,closeIconColorWarning:m,closeIconColorHoverWarning:O,closeIconColorPressedWarning:w,borderError:`1px solid ${Me(v,Le(I,{alpha:.25}))}`,colorError:Me(v,Le(I,{alpha:.08})),titleTextColorError:h,iconColorError:I,contentTextColorError:x,closeColorHoverError:_,closeColorPressedError:y,closeIconColorError:m,closeIconColorHoverError:O,closeIconColorPressedError:w})}const ur={common:Kt,self:dr},cr=s("alert",`
 line-height: var(--n-line-height);
 border-radius: var(--n-border-radius);
 position: relative;
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-color);
 text-align: start;
 word-break: break-word;
`,[T("border",`
 border-radius: inherit;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 transition: border-color .3s var(--n-bezier);
 border: var(--n-border);
 pointer-events: none;
 `),z("closable",[s("alert-body",[T("title",`
 padding-right: 24px;
 `)])]),T("icon",{color:"var(--n-icon-color)"}),s("alert-body",{padding:"var(--n-padding)"},[T("title",{color:"var(--n-title-text-color)"}),T("content",{color:"var(--n-content-text-color)"})]),wa({originalTransition:"transform .3s var(--n-bezier)",enterToProps:{transform:"scale(1)"},leaveToProps:{transform:"scale(0.9)"}}),T("icon",`
 position: absolute;
 left: 0;
 top: 0;
 align-items: center;
 justify-content: center;
 display: flex;
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 font-size: var(--n-icon-size);
 margin: var(--n-icon-margin);
 `),T("close",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 right: 0;
 top: 0;
 margin: var(--n-close-margin);
 `),z("show-icon",[s("alert-body",{paddingLeft:"calc(var(--n-icon-margin-left) + var(--n-icon-size) + var(--n-icon-margin-right))"})]),z("right-adjust",[s("alert-body",{paddingRight:"calc(var(--n-close-size) + var(--n-padding) + 2px)"})]),s("alert-body",`
 border-radius: var(--n-border-radius);
 transition: border-color .3s var(--n-bezier);
 `,[T("title",`
 transition: color .3s var(--n-bezier);
 font-size: 16px;
 line-height: 19px;
 font-weight: var(--n-title-font-weight);
 `,[U("& +",[T("content",{marginTop:"9px"})])]),T("content",{transition:"color .3s var(--n-bezier)",fontSize:"var(--n-font-size)"})]),T("icon",{transition:"color .3s var(--n-bezier)"})]),fr=Object.assign(Object.assign({},he.props),{title:String,showIcon:{type:Boolean,default:!0},type:{type:String,default:"default"},bordered:{type:Boolean,default:!0},closable:Boolean,onClose:Function,onAfterLeave:Function,onAfterHide:Function}),xt=ie({name:"Alert",inheritAttrs:!1,props:fr,slots:Object,setup(n){const{mergedClsPrefixRef:o,mergedBorderedRef:i,inlineThemeDisabled:p,mergedRtlRef:v}=Ve(n),g=he("Alert","-alert",cr,ur,n,o),$=bt("Alert",v,o),h=te(()=>{const{common:{cubicBezierEaseInOut:w},self:S}=g.value,{fontSize:D,borderRadius:j,titleFontWeight:I,lineHeight:F,iconSize:ae,iconMargin:L,iconMarginRtl:A,closeIconSize:E,closeBorderRadius:M,closeSize:V,closeMargin:W,closeMarginRtl:ne,padding:re}=S,{type:K}=n,{left:H,right:xe}=ft(L);return{"--n-bezier":w,"--n-color":S[de("color",K)],"--n-close-icon-size":E,"--n-close-border-radius":M,"--n-close-color-hover":S[de("closeColorHover",K)],"--n-close-color-pressed":S[de("closeColorPressed",K)],"--n-close-icon-color":S[de("closeIconColor",K)],"--n-close-icon-color-hover":S[de("closeIconColorHover",K)],"--n-close-icon-color-pressed":S[de("closeIconColorPressed",K)],"--n-icon-color":S[de("iconColor",K)],"--n-border":S[de("border",K)],"--n-title-text-color":S[de("titleTextColor",K)],"--n-content-text-color":S[de("contentTextColor",K)],"--n-line-height":F,"--n-border-radius":j,"--n-font-size":D,"--n-title-font-weight":I,"--n-icon-size":ae,"--n-icon-margin":L,"--n-icon-margin-rtl":A,"--n-close-size":V,"--n-close-margin":W,"--n-close-margin-rtl":ne,"--n-padding":re,"--n-icon-margin-left":H,"--n-icon-margin-right":xe}}),x=p?We("alert",te(()=>n.type[0]),h,n):void 0,_=N(!0),y=()=>{const{onAfterLeave:w,onAfterHide:S}=n;w&&w(),S&&S()};return{rtlEnabled:$,mergedClsPrefix:o,mergedBordered:i,visible:_,handleCloseClick:()=>{var w;Promise.resolve((w=n.onClose)===null||w===void 0?void 0:w.call(n)).then(S=>{S!==!1&&(_.value=!1)})},handleAfterLeave:()=>{y()},mergedTheme:g,cssVars:p?void 0:h,themeClass:x?.themeClass,onRender:x?.onRender}},render(){var n;return(n=this.onRender)===null||n===void 0||n.call(this),c(Sa,{onAfterLeave:this.handleAfterLeave},{default:()=>{const{mergedClsPrefix:o,$slots:i}=this,p={class:[`${o}-alert`,this.themeClass,this.closable&&`${o}-alert--closable`,this.showIcon&&`${o}-alert--show-icon`,!this.title&&this.closable&&`${o}-alert--right-adjust`,this.rtlEnabled&&`${o}-alert--rtl`],style:this.cssVars,role:"alert"};return this.visible?c("div",Object.assign({},Ca(this.$attrs,p)),this.closable&&c(ka,{clsPrefix:o,class:`${o}-alert__close`,onClick:this.handleCloseClick}),this.bordered&&c("div",{class:`${o}-alert__border`}),this.showIcon&&c("div",{class:`${o}-alert__icon`,"aria-hidden":"true"},_a(i.icon,()=>[c(wt,{clsPrefix:o},{default:()=>{switch(this.type){case"success":return c(Ya,null);case"info":return c(Ga,null);case"warning":return c(Xa,null);case"error":return c(qa,null);default:return null}}})])),c("div",{class:[`${o}-alert-body`,this.mergedBordered&&`${o}-alert-body--bordered`]},Ut(i.header,v=>{const g=v||this.title;return g?c("div",{class:`${o}-alert-body__title`},g):null}),i.default&&c("div",{class:`${o}-alert-body__content`},i))):null}})}}),vr=s("collapse","width: 100%;",[s("collapse-item",`
 font-size: var(--n-font-size);
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 margin: var(--n-item-margin);
 `,[z("disabled",[T("header","cursor: not-allowed;",[T("header-main",`
 color: var(--n-title-text-color-disabled);
 `),s("collapse-item-arrow",`
 color: var(--n-arrow-color-disabled);
 `)])]),s("collapse-item","margin-left: 32px;"),U("&:first-child","margin-top: 0;"),U("&:first-child >",[T("header","padding-top: 0;")]),z("left-arrow-placement",[T("header",[s("collapse-item-arrow","margin-right: 4px;")])]),z("right-arrow-placement",[T("header",[s("collapse-item-arrow","margin-left: 4px;")])]),T("content-wrapper",[T("content-inner","padding-top: 16px;"),wa({duration:"0.15s"})]),z("active",[T("header",[z("active",[s("collapse-item-arrow","transform: rotate(90deg);")])])]),U("&:not(:first-child)","border-top: 1px solid var(--n-divider-color);"),za("disabled",[z("trigger-area-main",[T("header",[T("header-main","cursor: pointer;"),s("collapse-item-arrow","cursor: default;")])]),z("trigger-area-arrow",[T("header",[s("collapse-item-arrow","cursor: pointer;")])]),z("trigger-area-extra",[T("header",[T("header-extra","cursor: pointer;")])])]),T("header",`
 font-size: var(--n-title-font-size);
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 transition: color .3s var(--n-bezier);
 position: relative;
 padding: var(--n-title-padding);
 color: var(--n-title-text-color);
 `,[T("header-main",`
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 color: var(--n-title-text-color);
 `),T("header-extra",`
 display: flex;
 align-items: center;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),s("collapse-item-arrow",`
 display: flex;
 transition:
 transform .15s var(--n-bezier),
 color .3s var(--n-bezier);
 font-size: 18px;
 color: var(--n-arrow-color);
 `)])])]),br=Object.assign(Object.assign({},he.props),{defaultExpandedNames:{type:[Array,String],default:null},expandedNames:[Array,String],arrowPlacement:{type:String,default:"left"},accordion:{type:Boolean,default:!1},displayDirective:{type:String,default:"if"},triggerAreas:{type:Array,default:()=>["main","extra","arrow"]},onItemHeaderClick:[Function,Array],"onUpdate:expandedNames":[Function,Array],onUpdateExpandedNames:[Function,Array],onExpandedNamesChange:{type:[Function,Array],validator:()=>!0,default:void 0}}),Ea=qt("n-collapse"),pr=ie({name:"Collapse",props:br,slots:Object,setup(n,{slots:o}){const{mergedClsPrefixRef:i,inlineThemeDisabled:p,mergedRtlRef:v}=Ve(n),g=N(n.defaultExpandedNames),$=te(()=>n.expandedNames),h=Ct($,g),x=he("Collapse","-collapse",vr,Ja,n,i);function _(D){const{"onUpdate:expandedNames":j,onUpdateExpandedNames:I,onExpandedNamesChange:F}=n;I&&ge(I,D),j&&ge(j,D),F&&ge(F,D),g.value=D}function y(D){const{onItemHeaderClick:j}=n;j&&ge(j,D)}function m(D,j,I){const{accordion:F}=n,{value:ae}=h;if(F)D?(_([j]),y({name:j,expanded:!0,event:I})):(_([]),y({name:j,expanded:!1,event:I}));else if(!Array.isArray(ae))_([j]),y({name:j,expanded:!0,event:I});else{const L=ae.slice(),A=L.findIndex(E=>j===E);~A?(L.splice(A,1),_(L),y({name:j,expanded:!1,event:I})):(L.push(j),_(L),y({name:j,expanded:!0,event:I}))}}Xt(Ea,{props:n,mergedClsPrefixRef:i,expandedNamesRef:h,slots:o,toggleItem:m});const O=bt("Collapse",v,i),w=te(()=>{const{common:{cubicBezierEaseInOut:D},self:{titleFontWeight:j,dividerColor:I,titlePadding:F,titleTextColor:ae,titleTextColorDisabled:L,textColor:A,arrowColor:E,fontSize:M,titleFontSize:V,arrowColorDisabled:W,itemMargin:ne}}=x.value;return{"--n-font-size":M,"--n-bezier":D,"--n-text-color":A,"--n-divider-color":I,"--n-title-padding":F,"--n-title-font-size":V,"--n-title-text-color":ae,"--n-title-text-color-disabled":L,"--n-title-font-weight":j,"--n-arrow-color":E,"--n-arrow-color-disabled":W,"--n-item-margin":ne}}),S=p?We("collapse",void 0,w,n):void 0;return{rtlEnabled:O,mergedTheme:x,mergedClsPrefix:i,cssVars:p?void 0:w,themeClass:S?.themeClass,onRender:S?.onRender}},render(){var n;return(n=this.onRender)===null||n===void 0||n.call(this),c("div",{class:[`${this.mergedClsPrefix}-collapse`,this.rtlEnabled&&`${this.mergedClsPrefix}-collapse--rtl`,this.themeClass],style:this.cssVars},this.$slots)}}),gr=ie({name:"CollapseItemContent",props:{displayDirective:{type:String,required:!0},show:Boolean,clsPrefix:{type:String,required:!0}},setup(n){return{onceTrue:Qa(pe(n,"show"))}},render(){return c(Sa,null,{default:()=>{const{show:n,displayDirective:o,onceTrue:i,clsPrefix:p}=this,v=o==="show"&&i,g=c("div",{class:`${p}-collapse-item__content-wrapper`},c("div",{class:`${p}-collapse-item__content-inner`},this.$slots));return v?Ra(g,[[$a,n]]):n?g:null}})}}),mr={title:String,name:[String,Number],disabled:Boolean,displayDirective:String},hr=ie({name:"CollapseItem",props:mr,setup(n){const{mergedRtlRef:o}=Ve(n),i=tn(),p=an(()=>{var m;return(m=n.name)!==null&&m!==void 0?m:i}),v=kt(Ea);v||Gt("collapse-item","`n-collapse-item` must be placed inside `n-collapse`.");const{expandedNamesRef:g,props:$,mergedClsPrefixRef:h,slots:x}=v,_=te(()=>{const{value:m}=g;if(Array.isArray(m)){const{value:O}=p;return!~m.findIndex(w=>w===O)}else if(m){const{value:O}=p;return O!==m}return!0});return{rtlEnabled:bt("Collapse",o,h),collapseSlots:x,randomName:i,mergedClsPrefix:h,collapsed:_,triggerAreas:pe($,"triggerAreas"),mergedDisplayDirective:te(()=>{const{displayDirective:m}=n;return m||$.displayDirective}),arrowPlacement:te(()=>$.arrowPlacement),handleClick(m){let O="main";Zt(m,"arrow")&&(O="arrow"),Zt(m,"extra")&&(O="extra"),$.triggerAreas.includes(O)&&v&&!n.disabled&&v.toggleItem(_.value,p.value,m)}}},render(){const{collapseSlots:n,$slots:o,arrowPlacement:i,collapsed:p,mergedDisplayDirective:v,mergedClsPrefix:g,disabled:$,triggerAreas:h}=this,x=Qt(o.header,{collapsed:p},()=>[this.title]),_=o["header-extra"]||n["header-extra"],y=o.arrow||n.arrow;return c("div",{class:[`${g}-collapse-item`,`${g}-collapse-item--${i}-arrow-placement`,$&&`${g}-collapse-item--disabled`,!p&&`${g}-collapse-item--active`,h.map(m=>`${g}-collapse-item--trigger-area-${m}`)]},c("div",{class:[`${g}-collapse-item__header`,!p&&`${g}-collapse-item__header--active`]},c("div",{class:`${g}-collapse-item__header-main`,onClick:this.handleClick},i==="right"&&x,c("div",{class:`${g}-collapse-item-arrow`,key:this.rtlEnabled?0:1,"data-arrow":!0},Qt(y,{collapsed:p},()=>[c(wt,{clsPrefix:g},{default:()=>this.rtlEnabled?c(sr,null):c(Za,null)})])),i==="left"&&x),en(_,{collapsed:p},m=>c("div",{class:`${g}-collapse-item__header-extra`,onClick:this.handleClick,"data-extra":!0},m))),c(gr,{clsPrefix:g,displayDirective:v,show:!p},o))}}),xr=nn({name:"DynamicTags",common:Kt,peers:{Input:on,Button:ln,Tag:Dn,Space:rn},self(){return{inputWidth:"64px"}}}),yr=s("dynamic-tags",[s("input",{minWidth:"var(--n-input-width)"})]),wr=Object.assign(Object.assign(Object.assign({},he.props),Fn),{size:{type:String,default:"medium"},closable:{type:Boolean,default:!0},defaultValue:{type:Array,default:()=>[]},value:Array,inputClass:String,inputStyle:[String,Object],inputProps:Object,max:Number,tagClass:String,tagStyle:[String,Object],renderTag:Function,onCreate:{type:Function,default:n=>n},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onChange:[Function,Array]}),Cr=ie({name:"DynamicTags",props:wr,slots:Object,setup(n){const{mergedClsPrefixRef:o,inlineThemeDisabled:i}=Ve(n),{localeRef:p}=Mn("DynamicTags"),v=Ta(n),{mergedDisabledRef:g}=v,$=N(""),h=N(!1),x=N(!0),_=N(null),y=he("DynamicTags","-dynamic-tags",yr,xr,n,o),m=N(n.defaultValue),O=pe(n,"value"),w=Ct(O,m),S=te(()=>p.value.add),D=te(()=>Ln(n.size)),j=te(()=>g.value||!!n.max&&w.value.length>=n.max);function I(W){const{onChange:ne,"onUpdate:value":re,onUpdateValue:K}=n,{nTriggerFormInput:H,nTriggerFormChange:xe}=v;ne&&ge(ne,W),K&&ge(K,W),re&&ge(re,W),m.value=W,H(),xe()}function F(W){const ne=w.value.slice(0);ne.splice(W,1),I(ne)}function ae(W){W.key==="Enter"&&L()}function L(W){const ne=W??$.value;if(ne){const re=w.value.slice(0);re.push(n.onCreate(ne)),I(re)}h.value=!1,x.value=!0,$.value=""}function A(){L()}function E(){h.value=!0,Je(()=>{var W;(W=_.value)===null||W===void 0||W.focus(),x.value=!1})}const M=te(()=>{const{self:{inputWidth:W}}=y.value;return{"--n-input-width":W}}),V=i?We("dynamic-tags",void 0,M,n):void 0;return{mergedClsPrefix:o,inputInstRef:_,localizedAdd:S,inputSize:D,inputValue:$,showInput:h,inputForceFocused:x,mergedValue:w,mergedDisabled:g,triggerDisabled:j,handleInputKeyDown:ae,handleAddClick:E,handleInputBlur:A,handleCloseClick:F,handleInputConfirm:L,mergedTheme:y,cssVars:i?void 0:M,themeClass:V?.themeClass,onRender:V?.onRender}},render(){const{mergedTheme:n,cssVars:o,mergedClsPrefix:i,onRender:p,renderTag:v}=this;return p?.(),c(G,{class:[`${i}-dynamic-tags`,this.themeClass],size:"small",style:o,theme:n.peers.Space,themeOverrides:n.peerOverrides.Space,itemStyle:"display: flex;"},{default:()=>{const{mergedTheme:g,tagClass:$,tagStyle:h,type:x,round:_,size:y,color:m,closable:O,mergedDisabled:w,showInput:S,inputValue:D,inputClass:j,inputStyle:I,inputSize:F,inputForceFocused:ae,triggerDisabled:L,handleInputKeyDown:A,handleInputBlur:E,handleAddClick:M,handleCloseClick:V,handleInputConfirm:W,$slots:ne}=this;return this.mergedValue.map((re,K)=>v?v(re,K):c(ze,{key:K,theme:g.peers.Tag,themeOverrides:g.peerOverrides.Tag,class:$,style:h,type:x,round:_,size:y,color:m,closable:O,disabled:w,onClose:()=>{V(K)}},{default:()=>typeof re=="string"?re:re.label})).concat(S?ne.input?ne.input({submit:W,deactivate:E}):c(me,Object.assign({placeholder:"",size:F,style:I,class:j,autosize:!0},this.inputProps,{ref:"inputInstRef",value:D,onUpdateValue:re=>{this.inputValue=re},theme:g.peers.Input,themeOverrides:g.peerOverrides.Input,onKeydown:A,onBlur:E,internalForceFocus:ae})):ne.trigger?ne.trigger({activate:M,disabled:L}):c(Z,{dashed:!0,disabled:L,theme:g.peers.Button,themeOverrides:g.peerOverrides.Button,size:F,onClick:M},{icon:()=>c(wt,{clsPrefix:i},{default:()=>c(Oa,null)})}))}})}});function kr(n){const o="rgba(0, 0, 0, .85)",i="0 2px 8px 0 rgba(0, 0, 0, 0.12)",{railColor:p,primaryColor:v,baseColor:g,cardColor:$,modalColor:h,popoverColor:x,borderRadius:_,fontSize:y,opacityDisabled:m}=n;return Object.assign(Object.assign({},sn),{fontSize:y,markFontSize:y,railColor:p,railColorHover:p,fillColor:v,fillColorHover:v,opacityDisabled:m,handleColor:"#FFF",dotColor:$,dotColorModal:h,dotColorPopover:x,handleBoxShadow:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowHover:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowActive:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowFocus:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",indicatorColor:o,indicatorBoxShadow:i,indicatorTextColor:g,indicatorBorderRadius:_,dotBorder:`2px solid ${p}`,dotBorderActive:`2px solid ${v}`,dotBoxShadow:""})}const _r={common:Kt,self:kr},Sr=U([s("list",`
 --n-merged-border-color: var(--n-border-color);
 --n-merged-color: var(--n-color);
 --n-merged-color-hover: var(--n-color-hover);
 margin: 0;
 font-size: var(--n-font-size);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 padding: 0;
 list-style-type: none;
 color: var(--n-text-color);
 background-color: var(--n-merged-color);
 `,[z("show-divider",[s("list-item",[U("&:not(:last-child)",[T("divider",`
 background-color: var(--n-merged-border-color);
 `)])])]),z("clickable",[s("list-item",`
 cursor: pointer;
 `)]),z("bordered",`
 border: 1px solid var(--n-merged-border-color);
 border-radius: var(--n-border-radius);
 `),z("hoverable",[s("list-item",`
 border-radius: var(--n-border-radius);
 `,[U("&:hover",`
 background-color: var(--n-merged-color-hover);
 `,[T("divider",`
 background-color: transparent;
 `)])])]),z("bordered, hoverable",[s("list-item",`
 padding: 12px 20px;
 `),T("header, footer",`
 padding: 12px 20px;
 `)]),T("header, footer",`
 padding: 12px 0;
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
 `,[U("&:not(:last-child)",`
 border-bottom: 1px solid var(--n-merged-border-color);
 `)]),s("list-item",`
 position: relative;
 padding: 12px 0; 
 box-sizing: border-box;
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[T("prefix",`
 margin-right: 20px;
 flex: 0;
 `),T("suffix",`
 margin-left: 20px;
 flex: 0;
 `),T("main",`
 flex: 1;
 `),T("divider",`
 height: 1px;
 position: absolute;
 bottom: 0;
 left: 0;
 right: 0;
 background-color: transparent;
 transition: background-color .3s var(--n-bezier);
 pointer-events: none;
 `)])]),Ia(s("list",`
 --n-merged-color-hover: var(--n-color-hover-modal);
 --n-merged-color: var(--n-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `)),Pa(s("list",`
 --n-merged-color-hover: var(--n-color-hover-popover);
 --n-merged-color: var(--n-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `))]),zr=Object.assign(Object.assign({},he.props),{size:{type:String,default:"medium"},bordered:Boolean,clickable:Boolean,hoverable:Boolean,showDivider:{type:Boolean,default:!0}}),ja=qt("n-list"),ca=ie({name:"List",props:zr,slots:Object,setup(n){const{mergedClsPrefixRef:o,inlineThemeDisabled:i,mergedRtlRef:p}=Ve(n),v=bt("List",p,o),g=he("List","-list",Sr,dn,n,o);Xt(ja,{showDividerRef:pe(n,"showDivider"),mergedClsPrefixRef:o});const $=te(()=>{const{common:{cubicBezierEaseInOut:x},self:{fontSize:_,textColor:y,color:m,colorModal:O,colorPopover:w,borderColor:S,borderColorModal:D,borderColorPopover:j,borderRadius:I,colorHover:F,colorHoverModal:ae,colorHoverPopover:L}}=g.value;return{"--n-font-size":_,"--n-bezier":x,"--n-text-color":y,"--n-color":m,"--n-border-radius":I,"--n-border-color":S,"--n-border-color-modal":D,"--n-border-color-popover":j,"--n-color-modal":O,"--n-color-popover":w,"--n-color-hover":F,"--n-color-hover-modal":ae,"--n-color-hover-popover":L}}),h=i?We("list",void 0,$,n):void 0;return{mergedClsPrefix:o,rtlEnabled:v,cssVars:i?void 0:$,themeClass:h?.themeClass,onRender:h?.onRender}},render(){var n;const{$slots:o,mergedClsPrefix:i,onRender:p}=this;return p?.(),c("ul",{class:[`${i}-list`,this.rtlEnabled&&`${i}-list--rtl`,this.bordered&&`${i}-list--bordered`,this.showDivider&&`${i}-list--show-divider`,this.hoverable&&`${i}-list--hoverable`,this.clickable&&`${i}-list--clickable`,this.themeClass],style:this.cssVars},o.header?c("div",{class:`${i}-list__header`},o.header()):null,(n=o.default)===null||n===void 0?void 0:n.call(o),o.footer?c("div",{class:`${i}-list__footer`},o.footer()):null)}}),fa=ie({name:"ListItem",slots:Object,setup(){const n=kt(ja,null);return n||Gt("list-item","`n-list-item` must be placed in `n-list`."),{showDivider:n.showDividerRef,mergedClsPrefix:n.mergedClsPrefixRef}},render(){const{$slots:n,mergedClsPrefix:o}=this;return c("li",{class:`${o}-list-item`},n.prefix?c("div",{class:`${o}-list-item__prefix`},n.prefix()):null,n.default?c("div",{class:`${o}-list-item__main`},n):null,n.suffix?c("div",{class:`${o}-list-item__suffix`},n.suffix()):null,this.showDivider&&c("div",{class:`${o}-list-item__divider`}))}}),Rr=U([s("slider",`
 display: block;
 padding: calc((var(--n-handle-size) - var(--n-rail-height)) / 2) 0;
 position: relative;
 z-index: 0;
 width: 100%;
 cursor: pointer;
 user-select: none;
 -webkit-user-select: none;
 `,[z("reverse",[s("slider-handles",[s("slider-handle-wrapper",`
 transform: translate(50%, -50%);
 `)]),s("slider-dots",[s("slider-dot",`
 transform: translateX(50%, -50%);
 `)]),z("vertical",[s("slider-handles",[s("slider-handle-wrapper",`
 transform: translate(-50%, -50%);
 `)]),s("slider-marks",[s("slider-mark",`
 transform: translateY(calc(-50% + var(--n-dot-height) / 2));
 `)]),s("slider-dots",[s("slider-dot",`
 transform: translateX(-50%) translateY(0);
 `)])])]),z("vertical",`
 box-sizing: content-box;
 padding: 0 calc((var(--n-handle-size) - var(--n-rail-height)) / 2);
 width: var(--n-rail-width-vertical);
 height: 100%;
 `,[s("slider-handles",`
 top: calc(var(--n-handle-size) / 2);
 right: 0;
 bottom: calc(var(--n-handle-size) / 2);
 left: 0;
 `,[s("slider-handle-wrapper",`
 top: unset;
 left: 50%;
 transform: translate(-50%, 50%);
 `)]),s("slider-rail",`
 height: 100%;
 `,[T("fill",`
 top: unset;
 right: 0;
 bottom: unset;
 left: 0;
 `)]),z("with-mark",`
 width: var(--n-rail-width-vertical);
 margin: 0 32px 0 8px;
 `),s("slider-marks",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 22px;
 font-size: var(--n-mark-font-size);
 `,[s("slider-mark",`
 transform: translateY(50%);
 white-space: nowrap;
 `)]),s("slider-dots",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 50%;
 `,[s("slider-dot",`
 transform: translateX(-50%) translateY(50%);
 `)])]),z("disabled",`
 cursor: not-allowed;
 opacity: var(--n-opacity-disabled);
 `,[s("slider-handle",`
 cursor: not-allowed;
 `)]),z("with-mark",`
 width: 100%;
 margin: 8px 0 32px 0;
 `),U("&:hover",[s("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[T("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),s("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),z("active",[s("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[T("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),s("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),s("slider-marks",`
 position: absolute;
 top: 18px;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[s("slider-mark",`
 position: absolute;
 transform: translateX(-50%);
 white-space: nowrap;
 `)]),s("slider-rail",`
 width: 100%;
 position: relative;
 height: var(--n-rail-height);
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 border-radius: calc(var(--n-rail-height) / 2);
 `,[T("fill",`
 position: absolute;
 top: 0;
 bottom: 0;
 border-radius: calc(var(--n-rail-height) / 2);
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-fill-color);
 `)]),s("slider-handles",`
 position: absolute;
 top: 0;
 right: calc(var(--n-handle-size) / 2);
 bottom: 0;
 left: calc(var(--n-handle-size) / 2);
 `,[s("slider-handle-wrapper",`
 outline: none;
 position: absolute;
 top: 50%;
 transform: translate(-50%, -50%);
 cursor: pointer;
 display: flex;
 `,[s("slider-handle",`
 height: var(--n-handle-size);
 width: var(--n-handle-size);
 border-radius: 50%;
 overflow: hidden;
 transition: box-shadow .2s var(--n-bezier), background-color .3s var(--n-bezier);
 background-color: var(--n-handle-color);
 box-shadow: var(--n-handle-box-shadow);
 `,[U("&:hover",`
 box-shadow: var(--n-handle-box-shadow-hover);
 `)]),U("&:focus",[s("slider-handle",`
 box-shadow: var(--n-handle-box-shadow-focus);
 `,[U("&:hover",`
 box-shadow: var(--n-handle-box-shadow-active);
 `)])])])]),s("slider-dots",`
 position: absolute;
 top: 50%;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[z("transition-disabled",[s("slider-dot","transition: none;")]),s("slider-dot",`
 transition:
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 transform: translate(-50%, -50%);
 height: var(--n-dot-height);
 width: var(--n-dot-width);
 border-radius: var(--n-dot-border-radius);
 overflow: hidden;
 box-sizing: border-box;
 border: var(--n-dot-border);
 background-color: var(--n-dot-color);
 `,[z("active","border: var(--n-dot-border-active);")])])]),s("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[ea()]),s("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[z("top",`
 margin-bottom: 12px;
 `),z("right",`
 margin-left: 12px;
 `),z("bottom",`
 margin-top: 12px;
 `),z("left",`
 margin-right: 12px;
 `),ea()]),Ia(s("slider",[s("slider-dot","background-color: var(--n-dot-color-modal);")])),Pa(s("slider",[s("slider-dot","background-color: var(--n-dot-color-popover);")]))]);function va(n){return window.TouchEvent&&n instanceof window.TouchEvent}function ba(){const n=new Map,o=i=>p=>{n.set(i,p)};return un(()=>{n.clear()}),[n,o]}const $r=0,Tr=Object.assign(Object.assign({},he.props),{to:Wt.propTo,defaultValue:{type:[Number,Array],default:0},marks:Object,disabled:{type:Boolean,default:void 0},formatTooltip:Function,keyboard:{type:Boolean,default:!0},min:{type:Number,default:0},max:{type:Number,default:100},step:{type:[Number,String],default:1},range:Boolean,value:[Number,Array],placement:String,showTooltip:{type:Boolean,default:void 0},tooltip:{type:Boolean,default:!0},vertical:Boolean,reverse:Boolean,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onDragstart:[Function],onDragend:[Function]}),pa=ie({name:"Slider",props:Tr,slots:Object,setup(n){const{mergedClsPrefixRef:o,namespaceRef:i,inlineThemeDisabled:p}=Ve(n),v=he("Slider","-slider",Rr,_r,n,o),g=N(null),[$,h]=ba(),[x,_]=ba(),y=N(new Set),m=Ta(n),{mergedDisabledRef:O}=m,w=te(()=>{const{step:d}=n;if(Number(d)<=0||d==="mark")return 0;const f=d.toString();let k=0;return f.includes(".")&&(k=f.length-f.indexOf(".")-1),k}),S=N(n.defaultValue),D=pe(n,"value"),j=Ct(D,S),I=te(()=>{const{value:d}=j;return(n.range?d:[d]).map(et)}),F=te(()=>I.value.length>2),ae=te(()=>n.placement===void 0?n.vertical?"right":"top":n.placement),L=te(()=>{const{marks:d}=n;return d?Object.keys(d).map(Number.parseFloat):null}),A=N(-1),E=N(-1),M=N(-1),V=N(!1),W=N(!1),ne=te(()=>{const{vertical:d,reverse:f}=n;return d?f?"top":"bottom":f?"right":"left"}),re=te(()=>{if(F.value)return;const d=I.value,f=He(n.range?Math.min(...d):n.min),k=He(n.range?Math.max(...d):d[0]),{value:B}=ne;return n.vertical?{[B]:`${f}%`,height:`${k-f}%`}:{[B]:`${f}%`,width:`${k-f}%`}}),K=te(()=>{const d=[],{marks:f}=n;if(f){const k=I.value.slice();k.sort((fe,ce)=>fe-ce);const{value:B}=ne,{value:Y}=F,{range:le}=n,ye=Y?()=>!1:fe=>le?fe>=k[0]&&fe<=k[k.length-1]:fe<=k[0];for(const fe of Object.keys(f)){const ce=Number(fe);d.push({active:ye(ce),key:ce,label:f[fe],style:{[B]:`${He(ce)}%`}})}}return d});function H(d,f){const k=He(d),{value:B}=ne;return{[B]:`${k}%`,zIndex:f===A.value?1:0}}function xe(d){return n.showTooltip||M.value===d||A.value===d&&V.value}function ve(d){return V.value?!(A.value===d&&E.value===d):!0}function nt(d){var f;~d&&(A.value=d,(f=$.get(d))===null||f===void 0||f.focus())}function Qe(){x.forEach((d,f)=>{xe(f)&&d.syncPosition()})}function Ze(d){const{"onUpdate:value":f,onUpdateValue:k}=n,{nTriggerFormInput:B,nTriggerFormChange:Y}=m;k&&ge(k,d),f&&ge(f,d),S.value=d,B(),Y()}function Ee(d){const{range:f}=n;if(f){if(Array.isArray(d)){const{value:k}=I;d.join()!==k.join()&&Ze(d)}}else Array.isArray(d)||I.value[0]!==d&&Ze(d)}function je(d,f){if(n.range){const k=I.value.slice();k.splice(f,1,d),Ee(k)}else Ee(d)}function Ke(d,f,k){const B=k!==void 0;k||(k=d-f>0?1:-1);const Y=L.value||[],{step:le}=n;if(le==="mark"){const ce=we(d,Y.concat(f),B?k:void 0);return ce?ce.value:f}if(le<=0)return f;const{value:ye}=w;let fe;if(B){const ce=Number((f/le).toFixed(ye)),Te=Math.floor(ce),st=ce>Te?Te:Te-1,dt=ce<Te?Te:Te+1;fe=we(f,[Number((st*le).toFixed(ye)),Number((dt*le).toFixed(ye)),...Y],k)}else{const ce=Re(d);fe=we(d,[...Y,ce])}return fe?et(fe.value):f}function et(d){return Math.min(n.max,Math.max(n.min,d))}function He(d){const{max:f,min:k}=n;return(d-k)/(f-k)*100}function tt(d){const{max:f,min:k}=n;return k+(f-k)*d}function Re(d){const{step:f,min:k}=n;if(Number(f)<=0||f==="mark")return d;const B=Math.round((d-k)/f)*f+k;return Number(B.toFixed(w.value))}function we(d,f=L.value,k){if(!f?.length)return null;let B=null,Y=-1;for(;++Y<f.length;){const le=f[Y]-d,ye=Math.abs(le);(k===void 0||le*k>0)&&(B===null||ye<B.distance)&&(B={index:Y,distance:ye,value:f[Y]})}return B}function qe(d){const f=g.value;if(!f)return;const k=va(d)?d.touches[0]:d,B=f.getBoundingClientRect();let Y;return n.vertical?Y=(B.bottom-k.clientY)/B.height:Y=(k.clientX-B.left)/B.width,n.reverse&&(Y=1-Y),tt(Y)}function rt(d){if(O.value||!n.keyboard)return;const{vertical:f,reverse:k}=n;switch(d.key){case"ArrowUp":d.preventDefault(),Be(f&&k?-1:1);break;case"ArrowRight":d.preventDefault(),Be(!f&&k?-1:1);break;case"ArrowDown":d.preventDefault(),Be(f&&k?1:-1);break;case"ArrowLeft":d.preventDefault(),Be(!f&&k?1:-1);break}}function Be(d){const f=A.value;if(f===-1)return;const{step:k}=n,B=I.value[f],Y=Number(k)<=0||k==="mark"?B:B+k*d;je(Ke(Y,B,d>0?1:-1),f)}function Ce(d){var f,k;if(O.value||!va(d)&&d.button!==$r)return;const B=qe(d);if(B===void 0)return;const Y=I.value.slice(),le=n.range?(k=(f=we(B,Y))===null||f===void 0?void 0:f.index)!==null&&k!==void 0?k:-1:0;le!==-1&&(d.preventDefault(),nt(le),lt(),je(Ke(B,I.value[le]),le))}function lt(){V.value||(V.value=!0,n.onDragstart&&ge(n.onDragstart),pt("touchend",document,$e),pt("mouseup",document,$e),pt("touchmove",document,De),pt("mousemove",document,De))}function Ne(){V.value&&(V.value=!1,n.onDragend&&ge(n.onDragend),gt("touchend",document,$e),gt("mouseup",document,$e),gt("touchmove",document,De),gt("mousemove",document,De))}function De(d){const{value:f}=A;if(!V.value||f===-1){Ne();return}const k=qe(d);k!==void 0&&je(Ke(k,I.value[f]),f)}function $e(){Ne()}function ke(d){A.value=d,O.value||(M.value=d)}function ot(d){A.value===d&&(A.value=-1,Ne()),M.value===d&&(M.value=-1)}function it(d){M.value=d}function b(d){M.value===d&&(M.value=-1)}vt(A,(d,f)=>{Je(()=>E.value=f)}),vt(j,()=>{if(n.marks){if(W.value)return;W.value=!0,Je(()=>{W.value=!1})}Je(Qe)}),pn(()=>{Ne()});const a=te(()=>{const{self:{markFontSize:d,railColor:f,railColorHover:k,fillColor:B,fillColorHover:Y,handleColor:le,opacityDisabled:ye,dotColor:fe,dotColorModal:ce,handleBoxShadow:Te,handleBoxShadowHover:st,handleBoxShadowActive:dt,handleBoxShadowFocus:_t,dotBorder:St,dotBoxShadow:zt,railHeight:Rt,railWidthVertical:$t,handleSize:Tt,dotHeight:It,dotWidth:at,dotBorderRadius:Pt,fontSize:At,dotBorderActive:Ot,dotColorPopover:Et},common:{cubicBezierEaseInOut:jt}}=v.value;return{"--n-bezier":jt,"--n-dot-border":St,"--n-dot-border-active":Ot,"--n-dot-border-radius":Pt,"--n-dot-box-shadow":zt,"--n-dot-color":fe,"--n-dot-color-modal":ce,"--n-dot-color-popover":Et,"--n-dot-height":It,"--n-dot-width":at,"--n-fill-color":B,"--n-fill-color-hover":Y,"--n-font-size":At,"--n-handle-box-shadow":Te,"--n-handle-box-shadow-active":dt,"--n-handle-box-shadow-focus":_t,"--n-handle-box-shadow-hover":st,"--n-handle-color":le,"--n-handle-size":Tt,"--n-opacity-disabled":ye,"--n-rail-color":f,"--n-rail-color-hover":k,"--n-rail-height":Rt,"--n-rail-width-vertical":$t,"--n-mark-font-size":d}}),l=p?We("slider",void 0,a,n):void 0,u=te(()=>{const{self:{fontSize:d,indicatorColor:f,indicatorBoxShadow:k,indicatorTextColor:B,indicatorBorderRadius:Y}}=v.value;return{"--n-font-size":d,"--n-indicator-border-radius":Y,"--n-indicator-box-shadow":k,"--n-indicator-color":f,"--n-indicator-text-color":B}}),R=p?We("slider-indicator",void 0,u,n):void 0;return{mergedClsPrefix:o,namespace:i,uncontrolledValue:S,mergedValue:j,mergedDisabled:O,mergedPlacement:ae,isMounted:gn(),adjustedTo:Wt(n),dotTransitionDisabled:W,markInfos:K,isShowTooltip:xe,shouldKeepTooltipTransition:ve,handleRailRef:g,setHandleRefs:h,setFollowerRefs:_,fillStyle:re,getHandleStyle:H,activeIndex:A,arrifiedValues:I,followerEnabledIndexSet:y,handleRailMouseDown:Ce,handleHandleFocus:ke,handleHandleBlur:ot,handleHandleMouseEnter:it,handleHandleMouseLeave:b,handleRailKeyDown:rt,indicatorCssVars:p?void 0:u,indicatorThemeClass:R?.themeClass,indicatorOnRender:R?.onRender,cssVars:p?void 0:a,themeClass:l?.themeClass,onRender:l?.onRender}},render(){var n;const{mergedClsPrefix:o,themeClass:i,formatTooltip:p}=this;return(n=this.onRender)===null||n===void 0||n.call(this),c("div",{class:[`${o}-slider`,i,{[`${o}-slider--disabled`]:this.mergedDisabled,[`${o}-slider--active`]:this.activeIndex!==-1,[`${o}-slider--with-mark`]:this.marks,[`${o}-slider--vertical`]:this.vertical,[`${o}-slider--reverse`]:this.reverse}],style:this.cssVars,onKeydown:this.handleRailKeyDown,onMousedown:this.handleRailMouseDown,onTouchstart:this.handleRailMouseDown},c("div",{class:`${o}-slider-rail`},c("div",{class:`${o}-slider-rail__fill`,style:this.fillStyle}),this.marks?c("div",{class:[`${o}-slider-dots`,this.dotTransitionDisabled&&`${o}-slider-dots--transition-disabled`]},this.markInfos.map(v=>c("div",{key:v.key,class:[`${o}-slider-dot`,{[`${o}-slider-dot--active`]:v.active}],style:v.style}))):null,c("div",{ref:"handleRailRef",class:`${o}-slider-handles`},this.arrifiedValues.map((v,g)=>{const $=this.isShowTooltip(g);return c(cn,null,{default:()=>[c(fn,null,{default:()=>c("div",{ref:this.setHandleRefs(g),class:`${o}-slider-handle-wrapper`,tabindex:this.mergedDisabled?-1:0,role:"slider","aria-valuenow":v,"aria-valuemin":this.min,"aria-valuemax":this.max,"aria-orientation":this.vertical?"vertical":"horizontal","aria-disabled":this.disabled,style:this.getHandleStyle(v,g),onFocus:()=>{this.handleHandleFocus(g)},onBlur:()=>{this.handleHandleBlur(g)},onMouseenter:()=>{this.handleHandleMouseEnter(g)},onMouseleave:()=>{this.handleHandleMouseLeave(g)}},_a(this.$slots.thumb,()=>[c("div",{class:`${o}-slider-handle`})]))}),this.tooltip&&c(vn,{ref:this.setFollowerRefs(g),show:$,to:this.adjustedTo,enabled:this.showTooltip&&!this.range||this.followerEnabledIndexSet.has(g),teleportDisabled:this.adjustedTo===Wt.tdkey,placement:this.mergedPlacement,containerClass:this.namespace},{default:()=>c(bn,{name:"fade-in-scale-up-transition",appear:this.isMounted,css:this.shouldKeepTooltipTransition(g),onEnter:()=>{this.followerEnabledIndexSet.add(g)},onAfterLeave:()=>{this.followerEnabledIndexSet.delete(g)}},{default:()=>{var h;return $?((h=this.indicatorOnRender)===null||h===void 0||h.call(this),c("div",{class:[`${o}-slider-handle-indicator`,this.indicatorThemeClass,`${o}-slider-handle-indicator--${this.mergedPlacement}`],style:this.indicatorCssVars},typeof p=="function"?p(v):v)):null}})})]})})),this.marks?c("div",{class:`${o}-slider-marks`},this.markInfos.map(v=>c("div",{key:v.key,class:`${o}-slider-mark`,style:v.style},typeof v.label=="function"?v.label():v.label))):null))}}),Yt=qt("n-tabs"),Ha={tab:[String,Number,Object,Function],name:{type:[String,Number],required:!0},disabled:Boolean,displayDirective:{type:String,default:"if"},closable:{type:Boolean,default:void 0},tabProps:Object,label:[String,Number,Object,Function]},Oe=ie({__TAB_PANE__:!0,name:"TabPane",alias:["TabPanel"],props:Ha,slots:Object,setup(n){const o=kt(Yt,null);return o||Gt("tab-pane","`n-tab-pane` must be placed inside `n-tabs`."),{style:o.paneStyleRef,class:o.paneClassRef,mergedClsPrefix:o.mergedClsPrefixRef}},render(){return c("div",{class:[`${this.mergedClsPrefix}-tab-pane`,this.class],style:this.style},this.$slots)}}),Ir=Object.assign({internalLeftPadded:Boolean,internalAddable:Boolean,internalCreatedByPane:Boolean},hn(Ha,["displayDirective"])),Vt=ie({__TAB__:!0,inheritAttrs:!1,name:"Tab",props:Ir,setup(n){const{mergedClsPrefixRef:o,valueRef:i,typeRef:p,closableRef:v,tabStyleRef:g,addTabStyleRef:$,tabClassRef:h,addTabClassRef:x,tabChangeIdRef:_,onBeforeLeaveRef:y,triggerRef:m,handleAdd:O,activateTab:w,handleClose:S}=kt(Yt);return{trigger:m,mergedClosable:te(()=>{if(n.internalAddable)return!1;const{closable:D}=n;return D===void 0?v.value:D}),style:g,addStyle:$,tabClass:h,addTabClass:x,clsPrefix:o,value:i,type:p,handleClose(D){D.stopPropagation(),!n.disabled&&S(n.name)},activateTab(){if(n.disabled)return;if(n.internalAddable){O();return}const{name:D}=n,j=++_.id;if(D!==i.value){const{value:I}=y;I?Promise.resolve(I(n.name,i.value)).then(F=>{F&&_.id===j&&w(D)}):w(D)}}}},render(){const{internalAddable:n,clsPrefix:o,name:i,disabled:p,label:v,tab:g,value:$,mergedClosable:h,trigger:x,$slots:{default:_}}=this,y=v??g;return c("div",{class:`${o}-tabs-tab-wrapper`},this.internalLeftPadded?c("div",{class:`${o}-tabs-tab-pad`}):null,c("div",Object.assign({key:i,"data-name":i,"data-disabled":p?!0:void 0},Ca({class:[`${o}-tabs-tab`,$===i&&`${o}-tabs-tab--active`,p&&`${o}-tabs-tab--disabled`,h&&`${o}-tabs-tab--closable`,n&&`${o}-tabs-tab--addable`,n?this.addTabClass:this.tabClass],onClick:x==="click"?this.activateTab:void 0,onMouseenter:x==="hover"?this.activateTab:void 0,style:n?this.addStyle:this.style},this.internalCreatedByPane?this.tabProps||{}:this.$attrs)),c("span",{class:`${o}-tabs-tab__label`},n?c(Pe,null,c("div",{class:`${o}-tabs-tab__height-placeholder`}," "),c(wt,{clsPrefix:o},{default:()=>c(Oa,null)})):_?_():typeof y=="object"?y:mn(y??i)),h&&this.type==="card"?c(ka,{clsPrefix:o,class:`${o}-tabs-tab__close`,onClick:this.handleClose,disabled:p}):null))}}),Pr=s("tabs",`
 box-sizing: border-box;
 width: 100%;
 display: flex;
 flex-direction: column;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
`,[z("segment-type",[s("tabs-rail",[U("&.transition-disabled",[s("tabs-capsule",`
 transition: none;
 `)])])]),z("top",[s("tab-pane",`
 padding: var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left);
 `)]),z("left",[s("tab-pane",`
 padding: var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left) var(--n-pane-padding-top);
 `)]),z("left, right",`
 flex-direction: row;
 `,[s("tabs-bar",`
 width: 2px;
 right: 0;
 transition:
 top .2s var(--n-bezier),
 max-height .2s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `),s("tabs-tab",`
 padding: var(--n-tab-padding-vertical); 
 `)]),z("right",`
 flex-direction: row-reverse;
 `,[s("tab-pane",`
 padding: var(--n-pane-padding-left) var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom);
 `),s("tabs-bar",`
 left: 0;
 `)]),z("bottom",`
 flex-direction: column-reverse;
 justify-content: flex-end;
 `,[s("tab-pane",`
 padding: var(--n-pane-padding-bottom) var(--n-pane-padding-right) var(--n-pane-padding-top) var(--n-pane-padding-left);
 `),s("tabs-bar",`
 top: 0;
 `)]),s("tabs-rail",`
 position: relative;
 padding: 3px;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 background-color: var(--n-color-segment);
 transition: background-color .3s var(--n-bezier);
 display: flex;
 align-items: center;
 `,[s("tabs-capsule",`
 border-radius: var(--n-tab-border-radius);
 position: absolute;
 pointer-events: none;
 background-color: var(--n-tab-color-segment);
 box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .08);
 transition: transform 0.3s var(--n-bezier);
 `),s("tabs-tab-wrapper",`
 flex-basis: 0;
 flex-grow: 1;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[s("tabs-tab",`
 overflow: hidden;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[z("active",`
 font-weight: var(--n-font-weight-strong);
 color: var(--n-tab-text-color-active);
 `),U("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])])]),z("flex",[s("tabs-nav",`
 width: 100%;
 position: relative;
 `,[s("tabs-wrapper",`
 width: 100%;
 `,[s("tabs-tab",`
 margin-right: 0;
 `)])])]),s("tabs-nav",`
 box-sizing: border-box;
 line-height: 1.5;
 display: flex;
 transition: border-color .3s var(--n-bezier);
 `,[T("prefix, suffix",`
 display: flex;
 align-items: center;
 `),T("prefix","padding-right: 16px;"),T("suffix","padding-left: 16px;")]),z("top, bottom",[U(">",[s("tabs-nav",[s("tabs-nav-scroll-wrapper",[U("&::before",`
 top: 0;
 bottom: 0;
 left: 0;
 width: 20px;
 `),U("&::after",`
 top: 0;
 bottom: 0;
 right: 0;
 width: 20px;
 `),z("shadow-start",[U("&::before",`
 box-shadow: inset 10px 0 8px -8px rgba(0, 0, 0, .12);
 `)]),z("shadow-end",[U("&::after",`
 box-shadow: inset -10px 0 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),z("left, right",[s("tabs-nav-scroll-content",`
 flex-direction: column;
 `),U(">",[s("tabs-nav",[s("tabs-nav-scroll-wrapper",[U("&::before",`
 top: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),U("&::after",`
 bottom: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),z("shadow-start",[U("&::before",`
 box-shadow: inset 0 10px 8px -8px rgba(0, 0, 0, .12);
 `)]),z("shadow-end",[U("&::after",`
 box-shadow: inset 0 -10px 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),s("tabs-nav-scroll-wrapper",`
 flex: 1;
 position: relative;
 overflow: hidden;
 `,[s("tabs-nav-y-scroll",`
 height: 100%;
 width: 100%;
 overflow-y: auto; 
 scrollbar-width: none;
 `,[U("&::-webkit-scrollbar, &::-webkit-scrollbar-track-piece, &::-webkit-scrollbar-thumb",`
 width: 0;
 height: 0;
 display: none;
 `)]),U("&::before, &::after",`
 transition: box-shadow .3s var(--n-bezier);
 pointer-events: none;
 content: "";
 position: absolute;
 z-index: 1;
 `)]),s("tabs-nav-scroll-content",`
 display: flex;
 position: relative;
 min-width: 100%;
 min-height: 100%;
 width: fit-content;
 box-sizing: border-box;
 `),s("tabs-wrapper",`
 display: inline-flex;
 flex-wrap: nowrap;
 position: relative;
 `),s("tabs-tab-wrapper",`
 display: flex;
 flex-wrap: nowrap;
 flex-shrink: 0;
 flex-grow: 0;
 `),s("tabs-tab",`
 cursor: pointer;
 white-space: nowrap;
 flex-wrap: nowrap;
 display: inline-flex;
 align-items: center;
 color: var(--n-tab-text-color);
 font-size: var(--n-tab-font-size);
 background-clip: padding-box;
 padding: var(--n-tab-padding);
 transition:
 box-shadow .3s var(--n-bezier),
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[z("disabled",{cursor:"not-allowed"}),T("close",`
 margin-left: 6px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `),T("label",`
 display: flex;
 align-items: center;
 z-index: 1;
 `)]),s("tabs-bar",`
 position: absolute;
 bottom: 0;
 height: 2px;
 border-radius: 1px;
 background-color: var(--n-bar-color);
 transition:
 left .2s var(--n-bezier),
 max-width .2s var(--n-bezier),
 opacity .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `,[U("&.transition-disabled",`
 transition: none;
 `),z("disabled",`
 background-color: var(--n-tab-text-color-disabled)
 `)]),s("tabs-pane-wrapper",`
 position: relative;
 overflow: hidden;
 transition: max-height .2s var(--n-bezier);
 `),s("tab-pane",`
 color: var(--n-pane-text-color);
 width: 100%;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 opacity .2s var(--n-bezier);
 left: 0;
 right: 0;
 top: 0;
 `,[U("&.next-transition-leave-active, &.prev-transition-leave-active, &.next-transition-enter-active, &.prev-transition-enter-active",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 transform .2s var(--n-bezier),
 opacity .2s var(--n-bezier);
 `),U("&.next-transition-leave-active, &.prev-transition-leave-active",`
 position: absolute;
 `),U("&.next-transition-enter-from, &.prev-transition-leave-to",`
 transform: translateX(32px);
 opacity: 0;
 `),U("&.next-transition-leave-to, &.prev-transition-enter-from",`
 transform: translateX(-32px);
 opacity: 0;
 `),U("&.next-transition-leave-from, &.next-transition-enter-to, &.prev-transition-leave-from, &.prev-transition-enter-to",`
 transform: translateX(0);
 opacity: 1;
 `)]),s("tabs-tab-pad",`
 box-sizing: border-box;
 width: var(--n-tab-gap);
 flex-grow: 0;
 flex-shrink: 0;
 `),z("line-type, bar-type",[s("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 box-sizing: border-box;
 vertical-align: bottom;
 `,[U("&:hover",{color:"var(--n-tab-text-color-hover)"}),z("active",`
 color: var(--n-tab-text-color-active);
 font-weight: var(--n-tab-font-weight-active);
 `),z("disabled",{color:"var(--n-tab-text-color-disabled)"})])]),s("tabs-nav",[z("line-type",[z("top",[T("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),s("tabs-nav-scroll-content",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),s("tabs-bar",`
 bottom: -1px;
 `)]),z("left",[T("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),s("tabs-nav-scroll-content",`
 border-right: 1px solid var(--n-tab-border-color);
 `),s("tabs-bar",`
 right: -1px;
 `)]),z("right",[T("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),s("tabs-nav-scroll-content",`
 border-left: 1px solid var(--n-tab-border-color);
 `),s("tabs-bar",`
 left: -1px;
 `)]),z("bottom",[T("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),s("tabs-nav-scroll-content",`
 border-top: 1px solid var(--n-tab-border-color);
 `),s("tabs-bar",`
 top: -1px;
 `)]),T("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),s("tabs-nav-scroll-content",`
 transition: border-color .3s var(--n-bezier);
 `),s("tabs-bar",`
 border-radius: 0;
 `)]),z("card-type",[T("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),s("tabs-pad",`
 flex-grow: 1;
 transition: border-color .3s var(--n-bezier);
 `),s("tabs-tab-pad",`
 transition: border-color .3s var(--n-bezier);
 `),s("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 border: 1px solid var(--n-tab-border-color);
 background-color: var(--n-tab-color);
 box-sizing: border-box;
 position: relative;
 vertical-align: bottom;
 display: flex;
 justify-content: space-between;
 font-size: var(--n-tab-font-size);
 color: var(--n-tab-text-color);
 `,[z("addable",`
 padding-left: 8px;
 padding-right: 8px;
 font-size: 16px;
 justify-content: center;
 `,[T("height-placeholder",`
 width: 0;
 font-size: var(--n-tab-font-size);
 `),za("disabled",[U("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])]),z("closable","padding-right: 8px;"),z("active",`
 background-color: #0000;
 font-weight: var(--n-tab-font-weight-active);
 color: var(--n-tab-text-color-active);
 `),z("disabled","color: var(--n-tab-text-color-disabled);")])]),z("left, right",`
 flex-direction: column; 
 `,[T("prefix, suffix",`
 padding: var(--n-tab-padding-vertical);
 `),s("tabs-wrapper",`
 flex-direction: column;
 `),s("tabs-tab-wrapper",`
 flex-direction: column;
 `,[s("tabs-tab-pad",`
 height: var(--n-tab-gap-vertical);
 width: 100%;
 `)])]),z("top",[z("card-type",[s("tabs-scroll-padding","border-bottom: 1px solid var(--n-tab-border-color);"),T("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),s("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-top-right-radius: var(--n-tab-border-radius);
 `,[z("active",`
 border-bottom: 1px solid #0000;
 `)]),s("tabs-tab-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),s("tabs-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `)])]),z("left",[z("card-type",[s("tabs-scroll-padding","border-right: 1px solid var(--n-tab-border-color);"),T("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),s("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-bottom-left-radius: var(--n-tab-border-radius);
 `,[z("active",`
 border-right: 1px solid #0000;
 `)]),s("tabs-tab-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `),s("tabs-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `)])]),z("right",[z("card-type",[s("tabs-scroll-padding","border-left: 1px solid var(--n-tab-border-color);"),T("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),s("tabs-tab",`
 border-top-right-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[z("active",`
 border-left: 1px solid #0000;
 `)]),s("tabs-tab-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `),s("tabs-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `)])]),z("bottom",[z("card-type",[s("tabs-scroll-padding","border-top: 1px solid var(--n-tab-border-color);"),T("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),s("tabs-tab",`
 border-bottom-left-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[z("active",`
 border-top: 1px solid #0000;
 `)]),s("tabs-tab-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `),s("tabs-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `)])])])]),Lt=ir,Ar=Object.assign(Object.assign({},he.props),{value:[String,Number],defaultValue:[String,Number],trigger:{type:String,default:"click"},type:{type:String,default:"bar"},closable:Boolean,justifyContent:String,size:{type:String,default:"medium"},placement:{type:String,default:"top"},tabStyle:[String,Object],tabClass:String,addTabStyle:[String,Object],addTabClass:String,barWidth:Number,paneClass:String,paneStyle:[String,Object],paneWrapperClass:String,paneWrapperStyle:[String,Object],addable:[Boolean,Object],tabsPadding:{type:Number,default:0},animated:Boolean,onBeforeLeave:Function,onAdd:Function,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onClose:[Function,Array],labelSize:String,activeName:[String,Number],onActiveNameChange:[Function,Array]}),Or=ie({name:"Tabs",props:Ar,slots:Object,setup(n,{slots:o}){var i,p,v,g;const{mergedClsPrefixRef:$,inlineThemeDisabled:h}=Ve(n),x=he("Tabs","-tabs",Pr,xn,n,$),_=N(null),y=N(null),m=N(null),O=N(null),w=N(null),S=N(null),D=N(!0),j=N(!0),I=ta(n,["labelSize","size"]),F=ta(n,["activeName","value"]),ae=N((p=(i=F.value)!==null&&i!==void 0?i:n.defaultValue)!==null&&p!==void 0?p:o.default?(g=(v=Ht(o.default())[0])===null||v===void 0?void 0:v.props)===null||g===void 0?void 0:g.name:null),L=Ct(F,ae),A={id:0},E=te(()=>{if(!(!n.justifyContent||n.type==="card"))return{display:"flex",justifyContent:n.justifyContent}});vt(L,()=>{A.id=0,re(),K()});function M(){var l;const{value:u}=L;return u===null?null:(l=_.value)===null||l===void 0?void 0:l.querySelector(`[data-name="${u}"]`)}function V(l){if(n.type==="card")return;const{value:u}=y;if(!u)return;const R=u.style.opacity==="0";if(l){const d=`${$.value}-tabs-bar--disabled`,{barWidth:f,placement:k}=n;if(l.dataset.disabled==="true"?u.classList.add(d):u.classList.remove(d),["top","bottom"].includes(k)){if(ne(["top","maxHeight","height"]),typeof f=="number"&&l.offsetWidth>=f){const B=Math.floor((l.offsetWidth-f)/2)+l.offsetLeft;u.style.left=`${B}px`,u.style.maxWidth=`${f}px`}else u.style.left=`${l.offsetLeft}px`,u.style.maxWidth=`${l.offsetWidth}px`;u.style.width="8192px",R&&(u.style.transition="none"),u.offsetWidth,R&&(u.style.transition="",u.style.opacity="1")}else{if(ne(["left","maxWidth","width"]),typeof f=="number"&&l.offsetHeight>=f){const B=Math.floor((l.offsetHeight-f)/2)+l.offsetTop;u.style.top=`${B}px`,u.style.maxHeight=`${f}px`}else u.style.top=`${l.offsetTop}px`,u.style.maxHeight=`${l.offsetHeight}px`;u.style.height="8192px",R&&(u.style.transition="none"),u.offsetHeight,R&&(u.style.transition="",u.style.opacity="1")}}}function W(){if(n.type==="card")return;const{value:l}=y;l&&(l.style.opacity="0")}function ne(l){const{value:u}=y;if(u)for(const R of l)u.style[R]=""}function re(){if(n.type==="card")return;const l=M();l?V(l):W()}function K(){var l;const u=(l=w.value)===null||l===void 0?void 0:l.$el;if(!u)return;const R=M();if(!R)return;const{scrollLeft:d,offsetWidth:f}=u,{offsetLeft:k,offsetWidth:B}=R;d>k?u.scrollTo({top:0,left:k,behavior:"smooth"}):k+B>d+f&&u.scrollTo({top:0,left:k+B-f,behavior:"smooth"})}const H=N(null);let xe=0,ve=null;function nt(l){const u=H.value;if(u){xe=l.getBoundingClientRect().height;const R=`${xe}px`,d=()=>{u.style.height=R,u.style.maxHeight=R};ve?(d(),ve(),ve=null):ve=d}}function Qe(l){const u=H.value;if(u){const R=l.getBoundingClientRect().height,d=()=>{document.body.offsetHeight,u.style.maxHeight=`${R}px`,u.style.height=`${Math.max(xe,R)}px`};ve?(ve(),ve=null,d()):ve=d}}function Ze(){const l=H.value;if(l){l.style.maxHeight="",l.style.height="";const{paneWrapperStyle:u}=n;if(typeof u=="string")l.style.cssText=u;else if(u){const{maxHeight:R,height:d}=u;R!==void 0&&(l.style.maxHeight=R),d!==void 0&&(l.style.height=d)}}}const Ee={value:[]},je=N("next");function Ke(l){const u=L.value;let R="next";for(const d of Ee.value){if(d===u)break;if(d===l){R="prev";break}}je.value=R,et(l)}function et(l){const{onActiveNameChange:u,onUpdateValue:R,"onUpdate:value":d}=n;u&&ge(u,l),R&&ge(R,l),d&&ge(d,l),ae.value=l}function He(l){const{onClose:u}=n;u&&ge(u,l)}function tt(){const{value:l}=y;if(!l)return;const u="transition-disabled";l.classList.add(u),re(),l.classList.remove(u)}const Re=N(null);function we({transitionDisabled:l}){const u=_.value;if(!u)return;l&&u.classList.add("transition-disabled");const R=M();R&&Re.value&&(Re.value.style.width=`${R.offsetWidth}px`,Re.value.style.height=`${R.offsetHeight}px`,Re.value.style.transform=`translateX(${R.offsetLeft-Cn(getComputedStyle(u).paddingLeft)}px)`,l&&Re.value.offsetWidth),l&&u.classList.remove("transition-disabled")}vt([L],()=>{n.type==="segment"&&Je(()=>{we({transitionDisabled:!1})})}),Aa(()=>{n.type==="segment"&&we({transitionDisabled:!0})});let qe=0;function rt(l){var u;if(l.contentRect.width===0&&l.contentRect.height===0||qe===l.contentRect.width)return;qe=l.contentRect.width;const{type:R}=n;if((R==="line"||R==="bar")&&tt(),R!=="segment"){const{placement:d}=n;$e((d==="top"||d==="bottom"?(u=w.value)===null||u===void 0?void 0:u.$el:S.value)||null)}}const Be=Lt(rt,64);vt([()=>n.justifyContent,()=>n.size],()=>{Je(()=>{const{type:l}=n;(l==="line"||l==="bar")&&tt()})});const Ce=N(!1);function lt(l){var u;const{target:R,contentRect:{width:d,height:f}}=l,k=R.parentElement.parentElement.offsetWidth,B=R.parentElement.parentElement.offsetHeight,{placement:Y}=n;if(!Ce.value)Y==="top"||Y==="bottom"?k<d&&(Ce.value=!0):B<f&&(Ce.value=!0);else{const{value:le}=O;if(!le)return;Y==="top"||Y==="bottom"?k-d>le.$el.offsetWidth&&(Ce.value=!1):B-f>le.$el.offsetHeight&&(Ce.value=!1)}$e(((u=w.value)===null||u===void 0?void 0:u.$el)||null)}const Ne=Lt(lt,64);function De(){const{onAdd:l}=n;l&&l(),Je(()=>{const u=M(),{value:R}=w;!u||!R||R.scrollTo({left:u.offsetLeft,top:0,behavior:"smooth"})})}function $e(l){if(!l)return;const{placement:u}=n;if(u==="top"||u==="bottom"){const{scrollLeft:R,scrollWidth:d,offsetWidth:f}=l;D.value=R<=0,j.value=R+f>=d}else{const{scrollTop:R,scrollHeight:d,offsetHeight:f}=l;D.value=R<=0,j.value=R+f>=d}}const ke=Lt(l=>{$e(l.target)},64);Xt(Yt,{triggerRef:pe(n,"trigger"),tabStyleRef:pe(n,"tabStyle"),tabClassRef:pe(n,"tabClass"),addTabStyleRef:pe(n,"addTabStyle"),addTabClassRef:pe(n,"addTabClass"),paneClassRef:pe(n,"paneClass"),paneStyleRef:pe(n,"paneStyle"),mergedClsPrefixRef:$,typeRef:pe(n,"type"),closableRef:pe(n,"closable"),valueRef:L,tabChangeIdRef:A,onBeforeLeaveRef:pe(n,"onBeforeLeave"),activateTab:Ke,handleClose:He,handleAdd:De}),yn(()=>{re(),K()}),wn(()=>{const{value:l}=m;if(!l)return;const{value:u}=$,R=`${u}-tabs-nav-scroll-wrapper--shadow-start`,d=`${u}-tabs-nav-scroll-wrapper--shadow-end`;D.value?l.classList.remove(R):l.classList.add(R),j.value?l.classList.remove(d):l.classList.add(d)});const ot={syncBarPosition:()=>{re()}},it=()=>{we({transitionDisabled:!0})},b=te(()=>{const{value:l}=I,{type:u}=n,R={card:"Card",bar:"Bar",line:"Line",segment:"Segment"}[u],d=`${l}${R}`,{self:{barColor:f,closeIconColor:k,closeIconColorHover:B,closeIconColorPressed:Y,tabColor:le,tabBorderColor:ye,paneTextColor:fe,tabFontWeight:ce,tabBorderRadius:Te,tabFontWeightActive:st,colorSegment:dt,fontWeightStrong:_t,tabColorSegment:St,closeSize:zt,closeIconSize:Rt,closeColorHover:$t,closeColorPressed:Tt,closeBorderRadius:It,[de("panePadding",l)]:at,[de("tabPadding",d)]:Pt,[de("tabPaddingVertical",d)]:At,[de("tabGap",d)]:Ot,[de("tabGap",`${d}Vertical`)]:Et,[de("tabTextColor",u)]:jt,[de("tabTextColorActive",u)]:Ba,[de("tabTextColorHover",u)]:Na,[de("tabTextColorDisabled",u)]:Da,[de("tabFontSize",l)]:Ma},common:{cubicBezierEaseInOut:La}}=x.value;return{"--n-bezier":La,"--n-color-segment":dt,"--n-bar-color":f,"--n-tab-font-size":Ma,"--n-tab-text-color":jt,"--n-tab-text-color-active":Ba,"--n-tab-text-color-disabled":Da,"--n-tab-text-color-hover":Na,"--n-pane-text-color":fe,"--n-tab-border-color":ye,"--n-tab-border-radius":Te,"--n-close-size":zt,"--n-close-icon-size":Rt,"--n-close-color-hover":$t,"--n-close-color-pressed":Tt,"--n-close-border-radius":It,"--n-close-icon-color":k,"--n-close-icon-color-hover":B,"--n-close-icon-color-pressed":Y,"--n-tab-color":le,"--n-tab-font-weight":ce,"--n-tab-font-weight-active":st,"--n-tab-padding":Pt,"--n-tab-padding-vertical":At,"--n-tab-gap":Ot,"--n-tab-gap-vertical":Et,"--n-pane-padding-left":ft(at,"left"),"--n-pane-padding-right":ft(at,"right"),"--n-pane-padding-top":ft(at,"top"),"--n-pane-padding-bottom":ft(at,"bottom"),"--n-font-weight-strong":_t,"--n-tab-color-segment":St}}),a=h?We("tabs",te(()=>`${I.value[0]}${n.type[0]}`),b,n):void 0;return Object.assign({mergedClsPrefix:$,mergedValue:L,renderedNames:new Set,segmentCapsuleElRef:Re,tabsPaneWrapperRef:H,tabsElRef:_,barElRef:y,addTabInstRef:O,xScrollInstRef:w,scrollWrapperElRef:m,addTabFixed:Ce,tabWrapperStyle:E,handleNavResize:Be,mergedSize:I,handleScroll:ke,handleTabsResize:Ne,cssVars:h?void 0:b,themeClass:a?.themeClass,animationDirection:je,renderNameListRef:Ee,yScrollElRef:S,handleSegmentResize:it,onAnimationBeforeLeave:nt,onAnimationEnter:Qe,onAnimationAfterEnter:Ze,onRender:a?.onRender},ot)},render(){const{mergedClsPrefix:n,type:o,placement:i,addTabFixed:p,addable:v,mergedSize:g,renderNameListRef:$,onRender:h,paneWrapperClass:x,paneWrapperStyle:_,$slots:{default:y,prefix:m,suffix:O}}=this;h?.();const w=y?Ht(y()).filter(A=>A.type.__TAB_PANE__===!0):[],S=y?Ht(y()).filter(A=>A.type.__TAB__===!0):[],D=!S.length,j=o==="card",I=o==="segment",F=!j&&!I&&this.justifyContent;$.value=[];const ae=()=>{const A=c("div",{style:this.tabWrapperStyle,class:`${n}-tabs-wrapper`},F?null:c("div",{class:`${n}-tabs-scroll-padding`,style:i==="top"||i==="bottom"?{width:`${this.tabsPadding}px`}:{height:`${this.tabsPadding}px`}}),D?w.map((E,M)=>($.value.push(E.props.name),Ft(c(Vt,Object.assign({},E.props,{internalCreatedByPane:!0,internalLeftPadded:M!==0&&(!F||F==="center"||F==="start"||F==="end")}),E.children?{default:E.children.tab}:void 0)))):S.map((E,M)=>($.value.push(E.props.name),Ft(M!==0&&!F?ha(E):E))),!p&&v&&j?ma(v,(D?w.length:S.length)!==0):null,F?null:c("div",{class:`${n}-tabs-scroll-padding`,style:{width:`${this.tabsPadding}px`}}));return c("div",{ref:"tabsElRef",class:`${n}-tabs-nav-scroll-content`},j&&v?c(Bt,{onResize:this.handleTabsResize},{default:()=>A}):A,j?c("div",{class:`${n}-tabs-pad`}):null,j?null:c("div",{ref:"barElRef",class:`${n}-tabs-bar`}))},L=I?"top":i;return c("div",{class:[`${n}-tabs`,this.themeClass,`${n}-tabs--${o}-type`,`${n}-tabs--${g}-size`,F&&`${n}-tabs--flex`,`${n}-tabs--${L}`],style:this.cssVars},c("div",{class:[`${n}-tabs-nav--${o}-type`,`${n}-tabs-nav--${L}`,`${n}-tabs-nav`]},Ut(m,A=>A&&c("div",{class:`${n}-tabs-nav__prefix`},A)),I?c(Bt,{onResize:this.handleSegmentResize},{default:()=>c("div",{class:`${n}-tabs-rail`,ref:"tabsElRef"},c("div",{class:`${n}-tabs-capsule`,ref:"segmentCapsuleElRef"},c("div",{class:`${n}-tabs-wrapper`},c("div",{class:`${n}-tabs-tab`}))),D?w.map((A,E)=>($.value.push(A.props.name),c(Vt,Object.assign({},A.props,{internalCreatedByPane:!0,internalLeftPadded:E!==0}),A.children?{default:A.children.tab}:void 0))):S.map((A,E)=>($.value.push(A.props.name),E===0?A:ha(A))))}):c(Bt,{onResize:this.handleNavResize},{default:()=>c("div",{class:`${n}-tabs-nav-scroll-wrapper`,ref:"scrollWrapperElRef"},["top","bottom"].includes(L)?c(qn,{ref:"xScrollInstRef",onScroll:this.handleScroll},{default:ae}):c("div",{class:`${n}-tabs-nav-y-scroll`,onScroll:this.handleScroll,ref:"yScrollElRef"},ae()))}),p&&v&&j?ma(v,!0):null,Ut(O,A=>A&&c("div",{class:`${n}-tabs-nav__suffix`},A))),D&&(this.animated&&(L==="top"||L==="bottom")?c("div",{ref:"tabsPaneWrapperRef",style:_,class:[`${n}-tabs-pane-wrapper`,x]},ga(w,this.mergedValue,this.renderedNames,this.onAnimationBeforeLeave,this.onAnimationEnter,this.onAnimationAfterEnter,this.animationDirection)):ga(w,this.mergedValue,this.renderedNames)))}});function ga(n,o,i,p,v,g,$){const h=[];return n.forEach(x=>{const{name:_,displayDirective:y,"display-directive":m}=x.props,O=S=>y===S||m===S,w=o===_;if(x.key!==void 0&&(x.key=_),w||O("show")||O("show:lazy")&&i.has(_)){i.has(_)||i.add(_);const S=!O("if");h.push(S?Ra(x,[[$a,w]]):x)}}),$?c(kn,{name:`${$}-transition`,onBeforeLeave:p,onEnter:v,onAfterEnter:g},{default:()=>h}):h}function ma(n,o){return c(Vt,{ref:"addTabInstRef",key:"__addable",name:"__addable",internalCreatedByPane:!0,internalAddable:!0,internalLeftPadded:o,disabled:typeof n=="object"&&n.disabled})}function ha(n){const o=_n(n);return o.props?o.props.internalLeftPadded=!0:o.props={internalLeftPadded:!0},o}function Ft(n){return Array.isArray(n.dynamicProps)?n.dynamicProps.includes("internalLeftPadded")||n.dynamicProps.push("internalLeftPadded"):n.dynamicProps=["internalLeftPadded"],n}const Er=s("thing",`
 display: flex;
 transition: color .3s var(--n-bezier);
 font-size: var(--n-font-size);
 color: var(--n-text-color);
`,[s("thing-avatar",`
 margin-right: 12px;
 margin-top: 2px;
 `),s("thing-avatar-header-wrapper",`
 display: flex;
 flex-wrap: nowrap;
 `,[s("thing-header-wrapper",`
 flex: 1;
 `)]),s("thing-main",`
 flex-grow: 1;
 `,[s("thing-header",`
 display: flex;
 margin-bottom: 4px;
 justify-content: space-between;
 align-items: center;
 `,[T("title",`
 font-size: 16px;
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 color: var(--n-title-text-color);
 `)]),T("description",[U("&:not(:last-child)",`
 margin-bottom: 4px;
 `)]),T("content",[U("&:not(:first-child)",`
 margin-top: 12px;
 `)]),T("footer",[U("&:not(:first-child)",`
 margin-top: 12px;
 `)]),T("action",[U("&:not(:first-child)",`
 margin-top: 12px;
 `)])])]),jr=Object.assign(Object.assign({},he.props),{title:String,titleExtra:String,description:String,descriptionClass:String,descriptionStyle:[String,Object],content:String,contentClass:String,contentStyle:[String,Object],contentIndented:Boolean}),xa=ie({name:"Thing",props:jr,slots:Object,setup(n,{slots:o}){const{mergedClsPrefixRef:i,inlineThemeDisabled:p,mergedRtlRef:v}=Ve(n),g=he("Thing","-thing",Er,Sn,n,i),$=bt("Thing",v,i),h=te(()=>{const{self:{titleTextColor:_,textColor:y,titleFontWeight:m,fontSize:O},common:{cubicBezierEaseInOut:w}}=g.value;return{"--n-bezier":w,"--n-font-size":O,"--n-text-color":y,"--n-title-font-weight":m,"--n-title-text-color":_}}),x=p?We("thing",void 0,h,n):void 0;return()=>{var _;const{value:y}=i,m=$?$.value:!1;return(_=x?.onRender)===null||_===void 0||_.call(x),c("div",{class:[`${y}-thing`,x?.themeClass,m&&`${y}-thing--rtl`],style:p?void 0:h.value},o.avatar&&n.contentIndented?c("div",{class:`${y}-thing-avatar`},o.avatar()):null,c("div",{class:`${y}-thing-main`},!n.contentIndented&&(o.header||n.title||o["header-extra"]||n.titleExtra||o.avatar)?c("div",{class:`${y}-thing-avatar-header-wrapper`},o.avatar?c("div",{class:`${y}-thing-avatar`},o.avatar()):null,o.header||n.title||o["header-extra"]||n.titleExtra?c("div",{class:`${y}-thing-header-wrapper`},c("div",{class:`${y}-thing-header`},o.header||n.title?c("div",{class:`${y}-thing-header__title`},o.header?o.header():n.title):null,o["header-extra"]||n.titleExtra?c("div",{class:`${y}-thing-header__extra`},o["header-extra"]?o["header-extra"]():n.titleExtra):null),o.description||n.description?c("div",{class:[`${y}-thing-main__description`,n.descriptionClass],style:n.descriptionStyle},o.description?o.description():n.description):null):null):c(Pe,null,o.header||n.title||o["header-extra"]||n.titleExtra?c("div",{class:`${y}-thing-header`},o.header||n.title?c("div",{class:`${y}-thing-header__title`},o.header?o.header():n.title):null,o["header-extra"]||n.titleExtra?c("div",{class:`${y}-thing-header__extra`},o["header-extra"]?o["header-extra"]():n.titleExtra):null):null,o.description||n.description?c("div",{class:[`${y}-thing-main__description`,n.descriptionClass],style:n.descriptionStyle},o.description?o.description():n.description):null),o.default||n.content?c("div",{class:[`${y}-thing-main__content`,n.contentClass],style:n.contentStyle},o.default?o.default():n.content):null,o.footer?c("div",{class:`${y}-thing-main__footer`},o.footer()):null,o.action?c("div",{class:`${y}-thing-main__action`},o.action()):null))}}}),Hr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Br=ie({name:"BookOutline",render:function(o,i){return q(),ue("svg",Hr,i[0]||(i[0]=[Q("path",{d:"M256 160c16-63.16 76.43-95.41 208-96a15.94 15.94 0 0 1 16 16v288a16 16 0 0 1-16 16c-128 0-177.45 25.81-208 64c-30.37-38-80-64-208-64c-9.88 0-16-8.05-16-17.93V80a15.94 15.94 0 0 1 16-16c131.57.59 192 32.84 208 96z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),Q("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M256 160v288"},null,-1)]))}}),Nr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Dr=ie({name:"BugOutline",render:function(o,i){return q(),ue("svg",Nr,i[0]||(i[0]=[zn('<path d="M370 378c28.89 23.52 46 46.07 46 86" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path><path d="M142 378c-28.89 23.52-46 46.06-46 86" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path><path d="M384 208c28.89-23.52 32-56.07 32-96" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path><path d="M128 206c-28.89-23.52-32-54.06-32-94" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M464 288.13h-80"></path><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M128 288.13H48"></path><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M256 192v256"></path><path d="M256 448h0c-70.4 0-128-57.6-128-128v-96.07c0-65.07 57.6-96 128-96h0c70.4 0 128 25.6 128 96V320c0 70.4-57.6 128-128 128z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path><path d="M179.43 143.52a49.08 49.08 0 0 1-3.43-15.73A80 80 0 0 1 255.79 48h.42A80 80 0 0 1 336 127.79a41.91 41.91 0 0 1-3.12 14.3" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path>',9)]))}}),Mr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Lr=ie({name:"HeartOutline",render:function(o,i){return q(),ue("svg",Mr,i[0]||(i[0]=[Q("path",{d:"M352.92 80C288 80 256 144 256 144s-32-64-96.92-64c-52.76 0-94.54 44.14-95.08 96.81c-1.1 109.33 86.73 187.08 183 252.42a16 16 0 0 0 18 0c96.26-65.34 184.09-143.09 183-252.42c-.54-52.67-42.32-96.81-95.08-96.81z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Fr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ya=ie({name:"InformationCircleOutline",render:function(o,i){return q(),ue("svg",Fr,i[0]||(i[0]=[Q("path",{d:"M248 64C146.39 64 64 146.39 64 248s82.39 184 184 184s184-82.39 184-184S349.61 64 248 64z",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"},null,-1),Q("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M220 220h32v116"},null,-1),Q("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32",d:"M208 340h88"},null,-1),Q("path",{d:"M248 130a26 26 0 1 0 26 26a26 26 0 0 0-26-26z",fill:"currentColor"},null,-1)]))}}),Ur={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Wr=ie({name:"LogoGithub",render:function(o,i){return q(),ue("svg",Ur,i[0]||(i[0]=[Q("path",{d:"M256 32C132.3 32 32 134.9 32 261.7c0 101.5 64.2 187.5 153.2 217.9a17.56 17.56 0 0 0 3.8.4c8.3 0 11.5-6.1 11.5-11.4c0-5.5-.2-19.9-.3-39.1a102.4 102.4 0 0 1-22.6 2.7c-43.1 0-52.9-33.5-52.9-33.5c-10.2-26.5-24.9-33.6-24.9-33.6c-19.5-13.7-.1-14.1 1.4-14.1h.1c22.5 2 34.3 23.8 34.3 23.8c11.2 19.6 26.2 25.1 39.6 25.1a63 63 0 0 0 25.6-6c2-14.8 7.8-24.9 14.2-30.7c-49.7-5.8-102-25.5-102-113.5c0-25.1 8.7-45.6 23-61.6c-2.3-5.8-10-29.2 2.2-60.8a18.64 18.64 0 0 1 5-.5c8.1 0 26.4 3.1 56.6 24.1a208.21 208.21 0 0 1 112.2 0c30.2-21 48.5-24.1 56.6-24.1a18.64 18.64 0 0 1 5 .5c12.2 31.6 4.5 55 2.2 60.8c14.3 16.1 23 36.6 23 61.6c0 88.2-52.4 107.6-102.3 113.3c8 7.1 15.2 21.1 15.2 42.5c0 30.7-.3 55.5-.3 63c0 5.4 3.1 11.5 11.4 11.5a19.35 19.35 0 0 0 4-.4C415.9 449.2 480 363.1 480 261.7C480 134.9 379.7 32 256 32z",fill:"currentColor"},null,-1)]))}}),Vr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Kr=ie({name:"NotificationsOutline",render:function(o,i){return q(),ue("svg",Vr,i[0]||(i[0]=[Q("path",{d:"M427.68 351.43C402 320 383.87 304 383.87 217.35C383.87 138 343.35 109.73 310 96c-4.43-1.82-8.6-6-9.95-10.55C294.2 65.54 277.8 48 256 48s-38.21 17.55-44 37.47c-1.35 4.6-5.52 8.71-9.95 10.53c-33.39 13.75-73.87 41.92-73.87 121.35C128.13 304 110 320 84.32 351.43C73.68 364.45 83 384 101.61 384h308.88c18.51 0 27.77-19.61 17.19-32.57z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),Q("path",{d:"M320 384v16a64 64 0 0 1-128 0v-16",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),qr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Ye=ie({name:"SaveOutline",render:function(o,i){return q(),ue("svg",qr,i[0]||(i[0]=[Q("path",{d:"M380.93 57.37A32 32 0 0 0 358.3 48H94.22A46.21 46.21 0 0 0 48 94.22v323.56A46.21 46.21 0 0 0 94.22 464h323.56A46.36 46.36 0 0 0 464 417.78V153.7a32 32 0 0 0-9.37-22.63zM256 416a64 64 0 1 1 64-64a63.92 63.92 0 0 1-64 64zm48-224H112a16 16 0 0 1-16-16v-64a16 16 0 0 1 16-16h192a16 16 0 0 1 16 16v64a16 16 0 0 1-16 16z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1)]))}}),Xr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Gr=ie({name:"ServerOutline",render:function(o,i){return q(),ue("svg",Xr,i[0]||(i[0]=[Q("ellipse",{cx:"256",cy:"128",rx:"192",ry:"80",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32"},null,-1),Q("path",{d:"M448 214c0 44.18-86 80-192 80S64 258.18 64 214",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32"},null,-1),Q("path",{d:"M448 300c0 44.18-86 80-192 80S64 344.18 64 300",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32"},null,-1),Q("path",{d:"M64 127.24v257.52C64 428.52 150 464 256 464s192-35.48 192-79.24V127.24",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-miterlimit":"10","stroke-width":"32"},null,-1)]))}}),Yr={class:"settings"},Jr={style:{"text-transform":"capitalize"}},Qr={key:1},Zr={class:"hook-name"},el={key:0,class:"about-content"},tl={class:"project-header"},al={class:"project-name"},nl={class:"project-description"},rl={class:"project-links"},ll={class:"dep-name"},ol=ie({__name:"Settings",setup(n){const o=N(!0),i=N(!1),p=N(!1),v=N("monitoring"),g=Ae({}),$=N([]),h=N(null),x=Ae({rate_limit:{requests_per_minute:30,retry_delay:60}}),_=Ae({ignore_selectors:[]}),y=Ae({enabled_platforms:[]}),m=Ae({}),O=Ae({}),w=Ae({rotation:{type:"time",interval:7,retention_days:30,max_size:10485760,backup_count:5}}),S=Ae({performance:{max_concurrent_tasks:15,max_browser_resources:8,scheduler_loop_interval:.2},retry:{retry_attempts:5,retry_delay:120}}),D=[{name:"{task_name}",description:"任务名称"},{name:"{url}",description:"监控的 URL 地址"},{name:"{description}",description:"任务描述"},{name:"{changes}",description:"变化内容"},{name:"{old_content}",description:"旧内容"},{name:"{new_content}",description:"新内容"}],j=[{label:"DEBUG",value:"DEBUG"},{label:"INFO",value:"INFO"},{label:"WARNING",value:"WARNING"},{label:"ERROR",value:"ERROR"},{label:"CRITICAL",value:"CRITICAL"}],I=N(!1),F=N({}),ae=N({}),L=N([]),A=N(!1),E=N(null),M=N(!1),V=N("add"),W=N(null),ne=N(""),re=N(!1),K=N(null),H=Ae({name:"",type:"shell",script:"",trigger:"on_change_detected",enabled:!0,timeout:30,async:!0,args:"",env:"",condition:"",working_dir:"",max_retries:0}),xe=[{label:"Shell",value:"shell"},{label:"Python",value:"python"}];async function ve(){A.value=!0;try{const b=await Fe.list();F.value=b.hooks,I.value=b.enabled,ae.value=b.defaults,L.value=await Fe.getTriggers()}catch(b){console.error("加载 Hook 配置失败:",b),J.error("加载 Hook 配置失败")}finally{A.value=!1}}const nt=te(()=>L.value.map(b=>({label:`${b.name} - ${b.description}`,value:b.name}))),Qe=te(()=>{const b=[];for(const[a,l]of Object.entries(F.value))for(const u of l)b.push({trigger:a,hook:u});return b});async function Ze(){try{const b=await Fe.toggleGlobal();I.value=b,J.success(b?"Hook 功能已启用":"Hook 功能已禁用")}catch(b){console.error("切换 Hook 状态失败:",b),J.error("操作失败")}}function Ee(){V.value="add",W.value=null,ne.value="",Object.assign(H,{name:"",type:"shell",script:"",trigger:"on_change_detected",enabled:!0,timeout:ae.value.timeout||30,async:ae.value.async!==!1,args:"",env:"",condition:"",working_dir:"",max_retries:ae.value.max_retries||0}),M.value=!0}function je(b,a){V.value="edit",W.value=a,ne.value=b,Object.assign(H,{name:a.name,type:a.type,script:a.script,trigger:b,enabled:a.enabled,timeout:a.timeout,async:a.async,args:a.args.join(", "),env:Object.entries(a.env).map(([l,u])=>`${l}=${u}`).join(`
`),condition:a.condition||"",working_dir:a.working_dir||"",max_retries:a.max_retries}),M.value=!0}async function Ke(){i.value=!0;try{const b={name:H.name,type:H.type,script:H.script,enabled:H.enabled,timeout:H.timeout,async:H.async,args:H.args?H.args.split(",").map(a=>a.trim()).filter(Boolean):[],env:H.env?Object.fromEntries(H.env.split(`
`).map(a=>a.trim()).filter(Boolean).map(a=>{const l=a.indexOf("=");return l>0?[a.slice(0,l),a.slice(l+1)]:[a,""]})):{},condition:H.condition||void 0,working_dir:H.working_dir||void 0,max_retries:H.max_retries};V.value==="add"?(await Fe.create({trigger:H.trigger,hook:b}),J.success("Hook 已添加")):(await Fe.update(W.value.name,b),J.success("Hook 已更新")),M.value=!1,await ve()}catch(b){console.error("保存 Hook 失败:",b),J.error(b.response?.data?.detail||"保存失败")}finally{i.value=!1}}async function et(b){try{await Fe.delete(b),J.success("Hook 已删除"),await ve()}catch(a){console.error("删除 Hook 失败:",a),J.error("删除失败")}}async function He(b){try{const a=await Fe.toggle(b);J.success(a?"Hook 已启用":"Hook 已禁用"),await ve()}catch(a){console.error("切换 Hook 状态失败:",a),J.error("操作失败")}}async function tt(b){E.value=b;try{const a=await Fe.test(b);a.result&&(K.value=a.result,re.value=!0),a.success?J.success("测试成功"):J.warning(a.message)}catch(a){console.error("测试 Hook 失败:",a),J.error(a.response?.data?.detail||"测试失败")}finally{E.value=null}}function Re(b){return L.value.find(l=>l.name===b)?.description||b}async function we(){o.value=!0;try{const b=await Ie.getAll();Object.assign(g,b),b.monitoring&&Object.assign(x,b.monitoring),b.detection&&Object.assign(_,b.detection),b.notification&&Object.assign(y,b.notification),b.ai&&Object.assign(m,b.ai),b.storage&&Object.assign(O,b.storage),b.logging&&Object.assign(w,b.logging),b.scheduler&&Object.assign(S,b.scheduler),$.value=await Ie.getNotificationPlatforms(),h.value=await Rn.getInfo()}catch(b){console.error("加载配置失败:",b),J.error("加载配置失败")}finally{o.value=!1}}async function qe(){i.value=!0;try{await Ie.updateMonitoring(x),J.success("监控配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function rt(){i.value=!0;try{await Ie.updateDetection(_),J.success("检测配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function Be(){i.value=!0;try{await Ie.updateNotification(y),J.success("通知配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function Ce(b){p.value=!0;try{const a=await In.test(b);if(a.success?J.success(a.message):J.warning(a.message),a.results&&a.results.length>0){const l=a.results.map(u=>`${u.platform}: ${u.success?"成功":"失败"}${u.error?` - ${u.error}`:""}`).join(`
`);na.info({title:"通知测试结果",content:l,positiveText:"确定"})}}catch(a){console.error("测试失败:",a),J.error("测试通知失败")}finally{p.value=!1}}async function lt(){i.value=!0;try{await Ie.updateAI(m),J.success("AI 配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function Ne(){i.value=!0;try{await Ie.updateStorage(O),J.success("存储配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function De(){i.value=!0;try{await Ie.updateLogging(w),J.success("日志配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function $e(){i.value=!0;try{await Ie.updateScheduler(S),J.success("调度器配置已保存")}catch(b){console.error("保存失败:",b),J.error("保存失败")}finally{i.value=!1}}async function ke(b){na.warning({title:"确认重置",content:`确定要将 ${ot(b)} 重置为默认值吗？`,positiveText:"确定",negativeText:"取消",onPositiveClick:async()=>{try{const a=await Ie.resetSection(b);switch(b){case"monitoring":Object.assign(x,a);break;case"detection":Object.assign(_,a);break;case"notification":Object.assign(y,a);break;case"ai":Object.assign(m,a);break;case"storage":Object.assign(O,a);break;case"logging":Object.assign(w,a);break;case"scheduler":Object.assign(S,a);break}J.success("配置已重置为默认值")}catch(a){console.error("重置失败:",a),J.error("重置失败")}}})}function ot(b){return{monitoring:"监控配置",detection:"检测配置",notification:"通知配置",ai:"AI 配置",storage:"存储配置",logging:"日志配置",scheduler:"调度器配置"}[b]||b}function it(b){return b<60?`${b} 秒`:b<3600?`${Math.floor(b/60)} 分钟`:`${Math.floor(b/3600)} 小时`}return Aa(()=>{we(),ve()}),(b,a)=>(q(),ue("div",Yr,[t(e(Nt),{show:o.value},{default:r(()=>[t(e(ut),{title:"系统设置",bordered:!1},{"header-extra":r(()=>[t(e(Z),{text:"",onClick:we},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(ra))]),_:1})]),default:r(()=>[a[62]||(a[62]=C(" 刷新 ",-1))]),_:1})]),default:r(()=>[t(e(Or),{value:v.value,"onUpdate:value":a[46]||(a[46]=l=>v.value=l),type:"line",animated:""},{default:r(()=>[t(e(Oe),{name:"monitoring",tab:"监控配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e($n))]),_:1}),a[63]||(a[63]=Q("span",null,"监控配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"140px","show-feedback":!1},{default:r(()=>[t(e(P),{label:"默认检测间隔"},{default:r(()=>[t(e(oe),{value:x.default_interval,"onUpdate:value":a[0]||(a[0]=l=>x.default_interval=l),min:10,max:86400,step:60,style:{width:"200px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[C(X(it(x.default_interval||300)),1)]),_:1})]),_:1}),t(e(P),{label:"默认超时时间"},{default:r(()=>[t(e(oe),{value:x.default_timeout,"onUpdate:value":a[1]||(a[1]=l=>x.default_timeout=l),min:1e3,max:12e4,step:1e3,style:{width:"200px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[...a[64]||(a[64]=[C("毫秒",-1)])]),_:1})]),_:1}),t(e(P),{label:"最大重试次数"},{default:r(()=>[t(e(oe),{value:x.max_retries,"onUpdate:value":a[2]||(a[2]=l=>x.max_retries=l),min:0,max:10,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"并发任务数"},{default:r(()=>[t(e(oe),{value:x.concurrent_tasks,"onUpdate:value":a[3]||(a[3]=l=>x.concurrent_tasks=l),min:1,max:50,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"浏览器无头模式"},{default:r(()=>[t(e(Ue),{value:x.browser_headless,"onUpdate:value":a[4]||(a[4]=l=>x.browser_headless=l)},null,8,["value"])]),_:1}),t(e(_e)),t(e(P),{label:"速率限制"},{default:r(()=>[t(e(G),{vertical:""},{default:r(()=>[t(e(G),{align:"center"},{default:r(()=>[t(e(se),null,{default:r(()=>[...a[65]||(a[65]=[C("每分钟请求数:",-1)])]),_:1}),t(e(oe),{value:x.rate_limit.requests_per_minute,"onUpdate:value":a[5]||(a[5]=l=>x.rate_limit.requests_per_minute=l),min:1,max:1e3,style:{width:"120px"}},null,8,["value"])]),_:1}),t(e(G),{align:"center"},{default:r(()=>[t(e(se),null,{default:r(()=>[...a[66]||(a[66]=[C("重试延迟 (秒):",-1)])]),_:1}),t(e(oe),{value:x.rate_limit.retry_delay,"onUpdate:value":a[6]||(a[6]=l=>x.rate_limit.retry_delay=l),min:1,max:3600,style:{width:"120px"}},null,8,["value"])]),_:1})]),_:1})]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:qe},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[67]||(a[67]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[7]||(a[7]=l=>ke("monitoring"))},{default:r(()=>[...a[68]||(a[68]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"detection",tab:"检测配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(la))]),_:1}),a[69]||(a[69]=Q("span",null,"检测配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"140px","show-feedback":!1},{default:r(()=>[t(e(P),{label:"启用智能检测"},{default:r(()=>[t(e(Ue),{value:_.enable_smart_detection,"onUpdate:value":a[8]||(a[8]=l=>_.enable_smart_detection=l)},null,8,["value"])]),_:1}),t(e(P),{label:"相似度阈值"},{default:r(()=>[t(e(pa),{value:_.similarity_threshold,"onUpdate:value":a[9]||(a[9]=l=>_.similarity_threshold=l),min:0,max:1,step:.01,"format-tooltip":l=>`${(l*100).toFixed(0)}%`,style:{width:"300px"}},null,8,["value","format-tooltip"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[C(X(((_.similarity_threshold||.85)*100).toFixed(0))+"% ",1)]),_:1})]),_:1}),t(e(P),{label:"最小变化长度"},{default:r(()=>[t(e(oe),{value:_.min_change_length,"onUpdate:value":a[10]||(a[10]=l=>_.min_change_length=l),min:1,max:1e3,style:{width:"200px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[...a[70]||(a[70]=[C("字符",-1)])]),_:1})]),_:1}),t(e(P),{label:"忽略的选择器"},{default:r(()=>[t(e(Cr),{value:_.ignore_selectors,"onUpdate:value":a[11]||(a[11]=l=>_.ignore_selectors=l)},null,8,["value"])]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:rt},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[71]||(a[71]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[12]||(a[12]=l=>ke("detection"))},{default:r(()=>[...a[72]||(a[72]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"notification",tab:"通知配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Kr))]),_:1}),a[73]||(a[73]=Q("span",null,"通知配置",-1))]),_:1})]),default:r(()=>[t(e(xt),{type:"info",title:"通知平台配置",style:{"margin-bottom":"16px"}},{default:r(()=>[...a[74]||(a[74]=[C(" 请在 config.json 或环境变量中配置各平台的 Token/Webhook。支持的占位符格式：${VAR_NAME} ",-1)])]),_:1}),t(e(pr),null,{default:r(()=>[(q(!0),ue(Pe,null,ct($.value,l=>(q(),be(e(hr),{key:l.name,title:l.name,name:l.name},{header:r(()=>[t(e(G),{align:"center"},{default:r(()=>[Q("span",Jr,X(l.name),1),l.enabled?(q(),be(e(ze),{key:0,type:"success",size:"small"},{default:r(()=>[...a[75]||(a[75]=[C("已启用",-1)])]),_:1})):(q(),be(e(ze),{key:1,type:"default",size:"small"},{default:r(()=>[...a[76]||(a[76]=[C("未启用",-1)])]),_:1}))]),_:2},1024)]),"header-extra":r(()=>[t(e(Z),{size:"small",type:"primary",ghost:"",loading:p.value,onClick:Pn(u=>Ce(l.name),["stop"])},{default:r(()=>[...a[77]||(a[77]=[C(" 测试 ",-1)])]),_:1},8,["loading","onClick"])]),default:r(()=>[t(e(Dt),{column:1,bordered:""},{default:r(()=>[t(e(Se),{label:"启用状态"},{default:r(()=>[C(X(l.enabled?"已启用":"未启用"),1)]),_:2},1024),(q(!0),ue(Pe,null,ct(l.config,(u,R)=>(q(),be(e(Se),{key:R,label:String(R)},{default:r(()=>[String(R).includes("token")||String(R).includes("webhook")||String(R).includes("key")?(q(),be(e(se),{key:0},{default:r(()=>[C(X(u||"(未配置)"),1)]),_:2},1024)):(q(),ue("span",Qr,X(u),1))]),_:2},1032,["label"]))),128))]),_:2},1024)]),_:2},1032,["title","name"]))),128))]),_:1}),t(e(_e)),t(e(P),{label:"已启用的平台"},{default:r(()=>[t(e(ht),{value:y.enabled_platforms,"onUpdate:value":a[13]||(a[13]=l=>y.enabled_platforms=l),multiple:"",options:$.value.map(l=>({label:l.name,value:l.name})),placeholder:"选择要启用的通知平台"},null,8,["value","options"])]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:Be},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[78]||(a[78]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{type:"info",loading:p.value,onClick:a[14]||(a[14]=l=>Ce())},{default:r(()=>[...a[79]||(a[79]=[C(" 测试所有平台 ",-1)])]),_:1},8,["loading"]),t(e(Z),{onClick:a[15]||(a[15]=l=>ke("notification"))},{default:r(()=>[...a[80]||(a[80]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"ai",tab:"AI 配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Vn))]),_:1}),a[81]||(a[81]=Q("span",null,"AI 配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"140px","show-feedback":!1},{default:r(()=>[t(e(P),{label:"启用 AI 分析"},{default:r(()=>[t(e(Ue),{value:m.enabled,"onUpdate:value":a[16]||(a[16]=l=>m.enabled=l)},null,8,["value"])]),_:1}),t(e(P),{label:"API 地址"},{default:r(()=>[t(e(me),{value:m.api_url,"onUpdate:value":a[17]||(a[17]=l=>m.api_url=l),placeholder:"https://api.deepseek.com/v1",style:{width:"400px"}},null,8,["value"])]),_:1}),t(e(P),{label:"API Key"},{default:r(()=>[t(e(me),{value:m.api_key,"onUpdate:value":a[18]||(a[18]=l=>m.api_key=l),type:"password","show-password-on":"click",placeholder:"${AI_API_KEY}",style:{width:"400px"}},null,8,["value"]),t(e(mt),null,{trigger:r(()=>[t(e(ee),{style:{"margin-left":"8px",cursor:"help"}},{default:r(()=>[t(e(ya))]),_:1})]),default:r(()=>[a[82]||(a[82]=C(" 可使用环境变量占位符 ${AI_API_KEY} ",-1))]),_:1})]),_:1}),t(e(P),{label:"模型"},{default:r(()=>[t(e(me),{value:m.model,"onUpdate:value":a[19]||(a[19]=l=>m.model=l),placeholder:"deepseek-reasoner",style:{width:"300px"}},null,8,["value"])]),_:1}),t(e(P),{label:"最大 Token 数"},{default:r(()=>[t(e(oe),{value:m.max_tokens,"onUpdate:value":a[20]||(a[20]=l=>m.max_tokens=l),min:100,max:32e3,step:100,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"温度参数"},{default:r(()=>[t(e(pa),{value:m.temperature,"onUpdate:value":a[21]||(a[21]=l=>m.temperature=l),min:0,max:2,step:.1,style:{width:"300px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[C(X(m.temperature),1)]),_:1})]),_:1}),t(e(P),{label:"请求超时 (秒)"},{default:r(()=>[t(e(oe),{value:m.timeout,"onUpdate:value":a[22]||(a[22]=l=>m.timeout=l),min:10,max:600,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"重试次数"},{default:r(()=>[t(e(oe),{value:m.retry_attempts,"onUpdate:value":a[23]||(a[23]=l=>m.retry_attempts=l),min:0,max:10,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(_e)),t(e(xt),{type:"info",style:{"margin-bottom":"16px"}},{header:r(()=>[...a[83]||(a[83]=[C("提示词占位符说明",-1)])]),default:r(()=>[t(e(G),{wrap:""},{default:r(()=>[(q(),ue(Pe,null,ct(D,l=>t(e(ze),{key:l.name,type:"info"},{default:r(()=>[C(X(l.name)+" - "+X(l.description),1)]),_:2},1024)),64))]),_:1})]),_:1}),t(e(P),{label:"系统提示词"},{default:r(()=>[t(e(me),{value:m.system_prompt,"onUpdate:value":a[24]||(a[24]=l=>m.system_prompt=l),type:"textarea",rows:4,placeholder:"你是一个网页变化分析助手...",style:{width:"100%"}},null,8,["value"])]),_:1}),t(e(P),{label:"用户提示词模板"},{default:r(()=>[t(e(me),{value:m.user_prompt_template,"onUpdate:value":a[25]||(a[25]=l=>m.user_prompt_template=l),type:"textarea",rows:6,placeholder:`请分析以下网页变化：
任务：{task_name}
URL：{url}
描述：{description}
变化内容：{changes}`,style:{width:"100%"}},null,8,["value"])]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:lt},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[84]||(a[84]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[26]||(a[26]=l=>ke("ai"))},{default:r(()=>[...a[85]||(a[85]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"storage",tab:"存储配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Gr))]),_:1}),a[86]||(a[86]=Q("span",null,"存储配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"140px","show-feedback":!1},{default:r(()=>[t(e(P),{label:"历史记录文件"},{default:r(()=>[t(e(me),{value:O.history_file,"onUpdate:value":a[27]||(a[27]=l=>O.history_file=l),placeholder:"data/history.json",style:{width:"400px"}},null,8,["value"])]),_:1}),t(e(P),{label:"最大记录数"},{default:r(()=>[t(e(oe),{value:O.max_history_entries,"onUpdate:value":a[28]||(a[28]=l=>O.max_history_entries=l),min:100,max:1e5,step:100,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"自动清理天数"},{default:r(()=>[t(e(oe),{value:O.auto_cleanup_days,"onUpdate:value":a[29]||(a[29]=l=>O.auto_cleanup_days=l),min:1,max:365,style:{width:"200px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[...a[87]||(a[87]=[C("天",-1)])]),_:1})]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:Ne},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[88]||(a[88]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[30]||(a[30]=l=>ke("storage"))},{default:r(()=>[...a[89]||(a[89]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"logging",tab:"日志配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(la))]),_:1}),a[90]||(a[90]=Q("span",null,"日志配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"140px","show-feedback":!1},{default:r(()=>[t(e(P),{label:"日志级别"},{default:r(()=>[t(e(ht),{value:w.level,"onUpdate:value":a[31]||(a[31]=l=>w.level=l),options:j,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(P),{label:"日志目录"},{default:r(()=>[t(e(me),{value:w.log_dir,"onUpdate:value":a[32]||(a[32]=l=>w.log_dir=l),placeholder:"./logs",style:{width:"300px"}},null,8,["value"])]),_:1}),t(e(P),{label:"日志压缩"},{default:r(()=>[t(e(Ue),{value:w.compression,"onUpdate:value":a[33]||(a[33]=l=>w.compression=l)},null,8,["value"])]),_:1}),t(e(P),{label:"异步模式"},{default:r(()=>[t(e(Ue),{value:w.async_mode,"onUpdate:value":a[34]||(a[34]=l=>w.async_mode=l)},null,8,["value"])]),_:1}),t(e(P),{label:"缓冲区大小"},{default:r(()=>[t(e(oe),{value:w.buffer_size,"onUpdate:value":a[35]||(a[35]=l=>w.buffer_size=l),min:100,max:1e4,step:100,style:{width:"200px"}},null,8,["value"])]),_:1}),t(e(_e),null,{default:r(()=>[...a[91]||(a[91]=[C("轮转配置",-1)])]),_:1}),t(e(P),{label:"轮转间隔 (天)"},{default:r(()=>[t(e(oe),{value:w.rotation.interval,"onUpdate:value":a[36]||(a[36]=l=>w.rotation.interval=l),min:1,max:365,style:{width:"200px"},disabled:!w.rotation},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"保留天数"},{default:r(()=>[t(e(oe),{value:w.rotation.retention_days,"onUpdate:value":a[37]||(a[37]=l=>w.rotation.retention_days=l),min:1,max:365,style:{width:"200px"},disabled:!w.rotation},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"备份文件数"},{default:r(()=>[t(e(oe),{value:w.rotation.backup_count,"onUpdate:value":a[38]||(a[38]=l=>w.rotation.backup_count=l),min:1,max:100,style:{width:"200px"},disabled:!w.rotation},null,8,["value","disabled"])]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:De},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[92]||(a[92]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[39]||(a[39]=l=>ke("logging"))},{default:r(()=>[...a[93]||(a[93]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"scheduler",tab:"调度器配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Tn))]),_:1}),a[94]||(a[94]=Q("span",null,"调度器配置",-1))]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"180px","show-feedback":!1},{default:r(()=>[t(e(_e),null,{default:r(()=>[...a[95]||(a[95]=[C("性能配置",-1)])]),_:1}),t(e(P),{label:"最大并发任务数"},{default:r(()=>[t(e(oe),{value:S.performance.max_concurrent_tasks,"onUpdate:value":a[40]||(a[40]=l=>S.performance.max_concurrent_tasks=l),min:1,max:100,style:{width:"200px"},disabled:!S.performance},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"最大浏览器资源数"},{default:r(()=>[t(e(oe),{value:S.performance.max_browser_resources,"onUpdate:value":a[41]||(a[41]=l=>S.performance.max_browser_resources=l),min:1,max:50,style:{width:"200px"},disabled:!S.performance},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"调度循环间隔 (秒)"},{default:r(()=>[t(e(oe),{value:S.performance.scheduler_loop_interval,"onUpdate:value":a[42]||(a[42]=l=>S.performance.scheduler_loop_interval=l),min:.1,max:5,step:.1,style:{width:"200px"},disabled:!S.performance},null,8,["value","disabled"])]),_:1}),t(e(_e),null,{default:r(()=>[...a[96]||(a[96]=[C("重试配置",-1)])]),_:1}),t(e(P),{label:"重试次数"},{default:r(()=>[t(e(oe),{value:S.retry.retry_attempts,"onUpdate:value":a[43]||(a[43]=l=>S.retry.retry_attempts=l),min:0,max:20,style:{width:"200px"},disabled:!S.retry},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"重试延迟 (秒)"},{default:r(()=>[t(e(oe),{value:S.retry.retry_delay,"onUpdate:value":a[44]||(a[44]=l=>S.retry.retry_delay=l),min:10,max:3600,style:{width:"200px"},disabled:!S.retry},null,8,["value","disabled"])]),_:1}),t(e(P),null,{default:r(()=>[t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",loading:i.value,onClick:$e},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Ye))]),_:1})]),default:r(()=>[a[97]||(a[97]=C(" 保存 ",-1))]),_:1},8,["loading"]),t(e(Z),{onClick:a[45]||(a[45]=l=>ke("scheduler"))},{default:r(()=>[...a[98]||(a[98]=[C("重置为默认值",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1}),t(e(Oe),{name:"hooks",tab:"Hook 配置"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(oa))]),_:1}),a[99]||(a[99]=Q("span",null,"Hook 配置",-1))]),_:1})]),default:r(()=>[t(e(Nt),{show:A.value},{default:r(()=>[t(e(G),{align:"center",justify:"space-between",style:{"margin-bottom":"16px"}},{default:r(()=>[t(e(G),{align:"center"},{default:r(()=>[t(e(se),null,{default:r(()=>[...a[100]||(a[100]=[C("Hook 功能",-1)])]),_:1}),t(e(Ue),{value:I.value,"onUpdate:value":Ze},null,8,["value"]),t(e(ze),{type:I.value?"success":"default",size:"small"},{default:r(()=>[C(X(I.value?"已启用":"已禁用"),1)]),_:1},8,["type"])]),_:1}),t(e(G),null,{default:r(()=>[t(e(Z),{type:"primary",onClick:Ee,disabled:!I.value},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(On))]),_:1})]),default:r(()=>[a[101]||(a[101]=C(" 添加 Hook ",-1))]),_:1},8,["disabled"]),t(e(Z),{onClick:ve},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(ra))]),_:1})]),default:r(()=>[a[102]||(a[102]=C(" 刷新 ",-1))]),_:1})]),_:1})]),_:1}),I.value?Xe("",!0):(q(),be(e(xt),{key:0,type:"info",style:{"margin-bottom":"16px"}},{default:r(()=>[...a[103]||(a[103]=[C(" Hook 功能当前已禁用。启用后可以在页面变化检测时自动执行自定义脚本。 ",-1)])]),_:1})),Qe.value.length===0?(q(),be(e(Un),{key:1,description:"暂无 Hook 配置"},{extra:r(()=>[t(e(Z),{size:"small",onClick:Ee,disabled:!I.value},{default:r(()=>[...a[104]||(a[104]=[C(" 添加第一个 Hook ",-1)])]),_:1},8,["disabled"])]),_:1})):(q(),be(e(ca),{key:2,bordered:""},{default:r(()=>[(q(!0),ue(Pe,null,ct(Qe.value,({trigger:l,hook:u})=>(q(),be(e(fa),{key:u.name},{default:r(()=>[t(e(xa),null,{header:r(()=>[t(e(G),{align:"center"},{default:r(()=>[Q("span",Zr,X(u.name),1),t(e(ze),{type:u.enabled?"success":"default",size:"small"},{default:r(()=>[C(X(u.enabled?"启用":"禁用"),1)]),_:2},1032,["type"]),t(e(ze),{type:"info",size:"small"},{default:r(()=>[C(X(u.type),1)]),_:2},1024),u.async?(q(),be(e(ze),{key:0,type:"warning",size:"small"},{default:r(()=>[...a[105]||(a[105]=[C("异步",-1)])]),_:1})):Xe("",!0)]),_:2},1024)]),"header-extra":r(()=>[t(e(G),null,{default:r(()=>[t(e(mt),null,{trigger:r(()=>[t(e(Z),{size:"small",quaternary:"",type:"info",loading:E.value===u.name,onClick:R=>tt(u.name)},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Wn))]),_:1})]),_:1},8,["loading","onClick"])]),default:r(()=>[a[106]||(a[106]=C(" 测试 ",-1))]),_:2},1024),t(e(mt),null,{trigger:r(()=>[t(e(Z),{size:"small",quaternary:"",type:u.enabled?"warning":"success",onClick:R=>He(u.name)},{icon:r(()=>[t(e(ee),null,{default:r(()=>[u.enabled?(q(),be(e(En),{key:0})):(q(),be(e(jn),{key:1}))]),_:2},1024)]),_:2},1032,["type","onClick"])]),default:r(()=>[C(" "+X(u.enabled?"禁用":"启用"),1)]),_:2},1024),t(e(mt),null,{trigger:r(()=>[t(e(Z),{size:"small",quaternary:"",type:"primary",onClick:R=>je(l,u)},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Hn))]),_:1})]),_:1},8,["onClick"])]),default:r(()=>[a[107]||(a[107]=C(" 编辑 ",-1))]),_:2},1024),t(e(Bn),{onPositiveClick:R=>et(u.name)},{trigger:r(()=>[t(e(Z),{size:"small",quaternary:"",type:"error"},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Nn))]),_:1})]),_:1})]),default:r(()=>[C(' 确定要删除 Hook "'+X(u.name)+'" 吗？ ',1)]),_:2},1032,["onPositiveClick"])]),_:2},1024)]),description:r(()=>[t(e(G),{vertical:"",size:4},{default:r(()=>[t(e(se),{depth:"3"},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(oa))]),_:1}),C(" "+X(u.script),1)]),_:2},1024),t(e(se),{depth:"3"},{default:r(()=>[C(" 触发点: "+X(Re(l)),1)]),_:2},1024),u.condition?(q(),be(e(G),{key:0},{default:r(()=>[t(e(se),{depth:"3"},{default:r(()=>[C("条件: "+X(u.condition),1)]),_:2},1024)]),_:2},1024)):Xe("",!0)]),_:2},1024)]),_:2},1024)]),_:2},1024))),128))]),_:1})),t(e(_e)),t(e(xt),{type:"info",title:"Hook 使用说明"},{default:r(()=>[t(e(G),{vertical:"",size:4},{default:r(()=>[t(e(se),null,{default:r(()=>[...a[108]||(a[108]=[C("Hook 是在特定事件发生时自动执行的脚本，支持 Shell 和 Python。",-1)])]),_:1}),t(e(se),null,{default:r(()=>[...a[109]||(a[109]=[C("脚本会通过环境变量和 stdin 接收上下文数据（JSON 格式）。",-1)])]),_:1}),t(e(se),null,{default:r(()=>[...a[110]||(a[110]=[C("脚本路径支持绝对路径或相对于项目 hooks/ 目录的路径。",-1)])]),_:1})]),_:1})]),_:1})]),_:1},8,["show"])]),_:1}),t(e(Oe),{name:"about",tab:"关于"},{tab:r(()=>[t(e(G),{align:"center",size:4},{default:r(()=>[t(e(ee),null,{default:r(()=>[t(e(ya))]),_:1}),a[111]||(a[111]=Q("span",null,"关于",-1))]),_:1})]),default:r(()=>[h.value?(q(),ue("div",el,[t(e(ut),{class:"about-card",bordered:!1},{default:r(()=>[Q("div",tl,[Q("h1",al,X(h.value.name),1),t(e(ze),{type:"primary",size:"large"},{default:r(()=>[C("v"+X(h.value.version),1)]),_:1})]),Q("p",nl,X(h.value.description),1),t(e(_e)),Q("div",rl,[t(e(G),{size:16},{default:r(()=>[t(e(Z),{tag:"a",href:h.value.links.repository,target:"_blank",type:"default",secondary:""},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Wr))]),_:1})]),default:r(()=>[a[112]||(a[112]=C(" GitHub ",-1))]),_:1},8,["href"]),t(e(Z),{tag:"a",href:h.value.links.documentation,target:"_blank",type:"default",secondary:""},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Br))]),_:1})]),default:r(()=>[a[113]||(a[113]=C(" 文档 ",-1))]),_:1},8,["href"]),t(e(Z),{tag:"a",href:h.value.links.issues,target:"_blank",type:"default",secondary:""},{icon:r(()=>[t(e(ee),null,{default:r(()=>[t(e(Dr))]),_:1})]),default:r(()=>[a[114]||(a[114]=C(" 反馈问题 ",-1))]),_:1},8,["href"])]),_:1})])]),_:1}),t(e(ut),{title:"系统信息",class:"about-card",bordered:!1},{default:r(()=>[t(e(Dt),{column:2,"label-placement":"left",bordered:""},{default:r(()=>[t(e(Se),{label:"Python 版本"},{default:r(()=>[C(X(h.value.system.python_version),1)]),_:1}),t(e(Se),{label:"操作系统"},{default:r(()=>[C(X(h.value.system.platform),1)]),_:1}),t(e(Se),{label:"系统版本"},{default:r(()=>[C(X(h.value.system.platform_version),1)]),_:1}),t(e(Se),{label:"许可证"},{default:r(()=>[C(X(h.value.license),1)]),_:1})]),_:1})]),_:1}),t(e(ut),{title:"核心依赖",class:"about-card",bordered:!1},{default:r(()=>[t(e(ca),{bordered:""},{default:r(()=>[(q(!0),ue(Pe,null,ct(h.value.dependencies,l=>(q(),be(e(fa),{key:l.name},{default:r(()=>[t(e(xa),null,{header:r(()=>[t(e(G),{align:"center"},{default:r(()=>[Q("span",ll,X(l.name),1),t(e(ze),{type:"info",size:"small"},{default:r(()=>[C(X(l.version),1)]),_:2},1024)]),_:2},1024)]),description:r(()=>[t(e(se),{depth:"3"},{default:r(()=>[C(X(l.description),1)]),_:2},1024)]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1}),t(e(ut),{class:"about-card",bordered:!1},{default:r(()=>[t(e(G),{align:"center",justify:"center",class:"thanks"},{default:r(()=>[t(e(ee),{color:"#f5222d",size:"18"},{default:r(()=>[t(e(Lr))]),_:1}),t(e(se),{depth:"2"},{default:r(()=>[...a[115]||(a[115]=[C("感谢所有开源项目贡献者",-1)])]),_:1})]),_:1})]),_:1})])):(q(),be(e(Nt),{key:1,show:o.value},{default:r(()=>[...a[116]||(a[116]=[Q("div",{style:{height:"200px"}},null,-1)])]),_:1},8,["show"]))]),_:1})]),_:1},8,["value"])]),_:1})]),_:1},8,["show"]),t(e(aa),{show:M.value,"onUpdate:show":a[60]||(a[60]=l=>M.value=l),title:V.value==="add"?"添加 Hook":"编辑 Hook",preset:"card",style:{width:"650px"},"mask-closable":!1},{footer:r(()=>[t(e(G),{justify:"end"},{default:r(()=>[t(e(Z),{onClick:a[59]||(a[59]=l=>M.value=!1)},{default:r(()=>[...a[120]||(a[120]=[C("取消",-1)])]),_:1}),t(e(Z),{type:"primary",loading:i.value,onClick:Ke},{default:r(()=>[C(X(V.value==="add"?"添加":"保存"),1)]),_:1},8,["loading"])]),_:1})]),default:r(()=>[t(e(Ge),{"label-placement":"left","label-width":"100"},{default:r(()=>[t(e(P),{label:"Hook 名称",required:""},{default:r(()=>[t(e(me),{value:H.name,"onUpdate:value":a[47]||(a[47]=l=>H.name=l),placeholder:"输入 Hook 名称",disabled:V.value==="edit"},null,8,["value","disabled"])]),_:1}),t(e(P),{label:"触发点",required:""},{default:r(()=>[t(e(ht),{value:H.trigger,"onUpdate:value":a[48]||(a[48]=l=>H.trigger=l),options:nt.value,placeholder:"选择触发点",disabled:V.value==="edit"},null,8,["value","options","disabled"])]),_:1}),t(e(P),{label:"脚本类型",required:""},{default:r(()=>[t(e(ht),{value:H.type,"onUpdate:value":a[49]||(a[49]=l=>H.type=l),options:xe,placeholder:"选择脚本类型"},null,8,["value"])]),_:1}),t(e(P),{label:"脚本路径",required:""},{default:r(()=>[t(e(me),{value:H.script,"onUpdate:value":a[50]||(a[50]=l=>H.script=l),placeholder:"hooks/my_script.sh 或绝对路径"},null,8,["value"])]),_:1}),t(e(P),{label:"启用状态"},{default:r(()=>[t(e(Ue),{value:H.enabled,"onUpdate:value":a[51]||(a[51]=l=>H.enabled=l)},null,8,["value"])]),_:1}),t(e(P),{label:"异步执行"},{default:r(()=>[t(e(Ue),{value:H.async,"onUpdate:value":a[52]||(a[52]=l=>H.async=l)},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[...a[117]||(a[117]=[C(" 异步执行不会阻塞后续流程 ",-1)])]),_:1})]),_:1}),t(e(P),{label:"超时时间"},{default:r(()=>[t(e(oe),{value:H.timeout,"onUpdate:value":a[53]||(a[53]=l=>H.timeout=l),min:1,max:300,style:{width:"150px"}},null,8,["value"]),t(e(se),{depth:"3",style:{"margin-left":"12px"}},{default:r(()=>[...a[118]||(a[118]=[C("秒",-1)])]),_:1})]),_:1}),t(e(P),{label:"重试次数"},{default:r(()=>[t(e(oe),{value:H.max_retries,"onUpdate:value":a[54]||(a[54]=l=>H.max_retries=l),min:0,max:5,style:{width:"150px"}},null,8,["value"])]),_:1}),t(e(_e),{style:{margin:"16px 0"}},{default:r(()=>[...a[119]||(a[119]=[C("高级选项",-1)])]),_:1}),t(e(P),{label:"命令行参数"},{default:r(()=>[t(e(me),{value:H.args,"onUpdate:value":a[55]||(a[55]=l=>H.args=l),placeholder:"多个参数用逗号分隔"},null,8,["value"])]),_:1}),t(e(P),{label:"环境变量"},{default:r(()=>[t(e(me),{value:H.env,"onUpdate:value":a[56]||(a[56]=l=>H.env=l),type:"textarea",rows:3,placeholder:"每行一个，格式: KEY=VALUE"},null,8,["value"])]),_:1}),t(e(P),{label:"执行条件"},{default:r(()=>[t(e(me),{value:H.condition,"onUpdate:value":a[57]||(a[57]=l=>H.condition=l),placeholder:"例如: change_type == 'content_change'"},null,8,["value"])]),_:1}),t(e(P),{label:"工作目录"},{default:r(()=>[t(e(me),{value:H.working_dir,"onUpdate:value":a[58]||(a[58]=l=>H.working_dir=l),placeholder:"留空使用项目根目录"},null,8,["value"])]),_:1})]),_:1})]),_:1},8,["show","title"]),t(e(aa),{show:re.value,"onUpdate:show":a[61]||(a[61]=l=>re.value=l),title:"Hook 测试结果",preset:"card",style:{width:"700px"}},{default:r(()=>[K.value?(q(),ue(Pe,{key:0},[t(e(Dt),{column:2,"label-placement":"left",bordered:""},{default:r(()=>[t(e(Se),{label:"Hook 名称"},{default:r(()=>[C(X(K.value.hook_name),1)]),_:1}),t(e(Se),{label:"执行状态"},{default:r(()=>[t(e(ze),{type:K.value.success?"success":"error",size:"small"},{default:r(()=>[C(X(K.value.success?"成功":"失败"),1)]),_:1},8,["type"])]),_:1}),t(e(Se),{label:"退出码"},{default:r(()=>[C(X(K.value.exit_code??"-"),1)]),_:1}),t(e(Se),{label:"执行耗时"},{default:r(()=>[C(X(K.value.execution_time.toFixed(2))+"s ",1)]),_:1}),K.value.error_message?(q(),be(e(Se),{key:0,label:"错误信息",span:2},{default:r(()=>[t(e(se),{type:"error"},{default:r(()=>[C(X(K.value.error_message),1)]),_:1})]),_:1})):Xe("",!0)]),_:1}),K.value.stdout?(q(),ue(Pe,{key:0},[t(e(_e),null,{default:r(()=>[...a[121]||(a[121]=[C("标准输出",-1)])]),_:1}),t(e(ia),{style:{"max-height":"200px"}},{default:r(()=>[t(e(sa),{code:K.value.stdout,language:"text"},null,8,["code"])]),_:1})],64)):Xe("",!0),K.value.stderr?(q(),ue(Pe,{key:1},[t(e(_e),null,{default:r(()=>[...a[122]||(a[122]=[C("标准错误",-1)])]),_:1}),t(e(ia),{style:{"max-height":"200px"}},{default:r(()=>[t(e(sa),{code:K.value.stderr,language:"text"},null,8,["code"])]),_:1})],64)):Xe("",!0)],64)):Xe("",!0)]),_:1},8,["show"])]))}}),fl=An(ol,[["__scopeId","data-v-024b1ab1"]]);export{fl as default};
