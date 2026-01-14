import{a7 as m,an as g,c6 as j,c7 as y,c8 as N,d as b,h as u,R as $,s as w,c9 as _,b5 as I,O as x,aA as k,ca as L,cb as M,cc as E,b0 as R,bU as O,cd as B,ce as S,cf as K,cg as z,x as P,ch as D,ci as U,aR as q,aD as F,cj as T,ck as V,cl as H,cm as Q,b as W,aq as C,ap as h,e as f,u as G,g as A,cn as J,c as X,j as Y,co as Z}from"./index-tAneExlJ.js";function ee(){const e=m(j,null);return e===null&&g("use-dialog","No outer <n-dialog-provider /> founded."),e}function ie(){const e=m(y,null);return e===null&&g("use-loading-bar","No outer <n-loading-bar-provider /> founded."),e}function ne(){const e=m(N,null);return e===null&&g("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),e}const oe=b({name:"ModalEnvironment",props:Object.assign(Object.assign({},_),{internalKey:{type:String,required:!0},onInternalAfterLeave:{type:Function,required:!0}}),setup(e){const n=w(!0);function i(){const{onInternalAfterLeave:l,internalKey:v,onAfterLeave:p}=e;l&&l(v),p&&p()}function t(){const{onPositiveClick:l}=e;l?Promise.resolve(l()).then(v=>{v!==!1&&s()}):s()}function d(){const{onNegativeClick:l}=e;l?Promise.resolve(l()).then(v=>{v!==!1&&s()}):s()}function a(){const{onClose:l}=e;l?Promise.resolve(l()).then(v=>{v!==!1&&s()}):s()}function o(l){const{onMaskClick:v,maskClosable:p}=e;v&&(v(l),p&&s())}function r(){const{onEsc:l}=e;l&&l()}function s(){n.value=!1}function c(l){n.value=l}return{show:n,hide:s,handleUpdateShow:c,handleAfterLeave:i,handleCloseClick:a,handleNegativeClick:d,handlePositiveClick:t,handleMaskClick:o,handleEsc:r}},render(){const{handleUpdateShow:e,handleAfterLeave:n,handleMaskClick:i,handleEsc:t,show:d}=this;return u($,Object.assign({},this.$props,{show:d,onUpdateShow:e,onMaskClick:i,onEsc:t,onAfterLeave:n,internalAppear:!0,internalModal:!0}),this.$slots)}}),te={to:[String,Object]},ae=b({name:"ModalProvider",props:te,setup(){const e=w([]),n={};function i(o={}){const r=R(),s=O(Object.assign(Object.assign({},o),{key:r,destroy:()=>{var c;(c=n[`n-modal-${r}`])===null||c===void 0||c.hide()}}));return e.value.push(s),s}function t(o){const{value:r}=e;r.splice(r.findIndex(s=>s.key===o),1)}function d(){Object.values(n).forEach(o=>{o?.hide()})}const a={create:i,destroyAll:d};return k(B,a),k(E,{clickedRef:M(64),clickedPositionRef:L()}),k(S,e),Object.assign(Object.assign({},a),{modalList:e,modalInstRefs:n,handleAfterLeave:t})},render(){var e,n;return u(x,null,[this.modalList.map(i=>{var t;return u(oe,I(i,["destroy","render"],{to:(t=i.to)!==null&&t!==void 0?t:this.to,ref:d=>{d===null?delete this.modalInstRefs[`n-modal-${i.key}`]:this.modalInstRefs[`n-modal-${i.key}`]=d},internalKey:i.key,onInternalAfterLeave:this.handleAfterLeave}),{default:i.render})}),(n=(e=this.$slots).default)===null||n===void 0?void 0:n.call(e)])}});function re(){const e=m(K,null);return e===null&&g("use-notification","No outer `n-notification-provider` found."),e}const se=b({name:"InjectionExtractor",props:{onSetup:Function},setup(e,{slots:n}){var i;return(i=e.onSetup)===null||i===void 0||i.call(e),()=>{var t;return(t=n.default)===null||t===void 0?void 0:t.call(n)}}}),le={message:ne,notification:re,loadingBar:ie,dialog:ee,modal:D};function de({providersAndProps:e,configProviderProps:n}){let i=z(d);const t={app:i};function d(){return u(U,P(n),{default:()=>e.map(({type:r,Provider:s,props:c})=>u(s,P(c),{default:()=>u(se,{onSetup:()=>t[r]=le[r]()})}))})}let a;return q&&(a=document.createElement("div"),document.body.appendChild(a),i.mount(a)),Object.assign({unmount:()=>{var r;if(i===null||a===null){F("discrete","unmount call no need because discrete app has been unmounted");return}i.unmount(),(r=a.parentNode)===null||r===void 0||r.removeChild(a),a=null,i=null}},t)}function ce(e,{configProviderProps:n,messageProviderProps:i,dialogProviderProps:t,notificationProviderProps:d,loadingBarProviderProps:a,modalProviderProps:o}={}){const r=[];return e.forEach(c=>{switch(c){case"message":r.push({type:c,Provider:Q,props:i});break;case"notification":r.push({type:c,Provider:H,props:d});break;case"dialog":r.push({type:c,Provider:V,props:t});break;case"loadingBar":r.push({type:c,Provider:T,props:a});break;case"modal":r.push({type:c,Provider:ae,props:o})}}),de({providersAndProps:r,configProviderProps:n})}const ue=W("divider",`
 position: relative;
 display: flex;
 width: 100%;
 box-sizing: border-box;
 font-size: 16px;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
`,[C("vertical",`
 margin-top: 24px;
 margin-bottom: 24px;
 `,[C("no-title",`
 display: flex;
 align-items: center;
 `)]),h("title",`
 display: flex;
 align-items: center;
 margin-left: 12px;
 margin-right: 12px;
 white-space: nowrap;
 font-weight: var(--n-font-weight);
 `),f("title-position-left",[h("line",[f("left",{width:"28px"})])]),f("title-position-right",[h("line",[f("right",{width:"28px"})])]),f("dashed",[h("line",`
 background-color: #0000;
 height: 0px;
 width: 100%;
 border-style: dashed;
 border-width: 1px 0 0;
 `)]),f("vertical",`
 display: inline-block;
 height: 1em;
 margin: 0 8px;
 vertical-align: middle;
 width: 1px;
 `),h("line",`
 border: none;
 transition: background-color .3s var(--n-bezier), border-color .3s var(--n-bezier);
 height: 1px;
 width: 100%;
 margin: 0;
 `),C("dashed",[h("line",{backgroundColor:"var(--n-color)"})]),f("dashed",[h("line",{borderColor:"var(--n-color)"})]),f("vertical",{backgroundColor:"var(--n-color)"})]),ve=Object.assign(Object.assign({},A.props),{titlePlacement:{type:String,default:"center"},dashed:Boolean,vertical:Boolean}),he=b({name:"Divider",props:ve,setup(e){const{mergedClsPrefixRef:n,inlineThemeDisabled:i}=G(e),t=A("Divider","-divider",ue,J,e,n),d=X(()=>{const{common:{cubicBezierEaseInOut:o},self:{color:r,textColor:s,fontWeight:c}}=t.value;return{"--n-bezier":o,"--n-color":r,"--n-text-color":s,"--n-font-weight":c}}),a=i?Y("divider",void 0,d,e):void 0;return{mergedClsPrefix:n,cssVars:i?void 0:d,themeClass:a?.themeClass,onRender:a?.onRender}},render(){var e;const{$slots:n,titlePlacement:i,vertical:t,dashed:d,cssVars:a,mergedClsPrefix:o}=this;return(e=this.onRender)===null||e===void 0||e.call(this),u("div",{role:"separator",class:[`${o}-divider`,this.themeClass,{[`${o}-divider--vertical`]:t,[`${o}-divider--no-title`]:!n.default,[`${o}-divider--dashed`]:d,[`${o}-divider--title-position-${i}`]:n.default&&i}],style:a},t?null:u("div",{class:`${o}-divider__line ${o}-divider__line--left`}),!t&&n.default?u(x,null,u("div",{class:`${o}-divider__title`},this.$slots),u("div",{class:`${o}-divider__line ${o}-divider__line--right`})):null)}}),{message:pe,notification:me,dialog:ge,loadingBar:be}=ce(["message","dialog","notification","loadingBar"],{configProviderProps:{theme:Z}});export{he as N,ge as d,pe as m};
