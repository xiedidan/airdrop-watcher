import{K as v,aq as p,O as f,b,as as c,R as n,e as s,d as x,h as l,I as w,u as C,g as h,c5 as y,c as $,j as _}from"./index-C0S4fFCR.js";const P=v("n-dialog-provider"),R=v("n-dialog-api"),z=v("n-message-api");function K(){const i=f(z,null);return i===null&&p("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),i}const j=b("divider",`
 position: relative;
 display: flex;
 width: 100%;
 box-sizing: border-box;
 font-size: 16px;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
`,[c("vertical",`
 margin-top: 24px;
 margin-bottom: 24px;
 `,[c("no-title",`
 display: flex;
 align-items: center;
 `)]),n("title",`
 display: flex;
 align-items: center;
 margin-left: 12px;
 margin-right: 12px;
 white-space: nowrap;
 font-weight: var(--n-font-weight);
 `),s("title-position-left",[n("line",[s("left",{width:"28px"})])]),s("title-position-right",[n("line",[s("right",{width:"28px"})])]),s("dashed",[n("line",`
 background-color: #0000;
 height: 0px;
 width: 100%;
 border-style: dashed;
 border-width: 1px 0 0;
 `)]),s("vertical",`
 display: inline-block;
 height: 1em;
 margin: 0 8px;
 vertical-align: middle;
 width: 1px;
 `),n("line",`
 border: none;
 transition: background-color .3s var(--n-bezier), border-color .3s var(--n-bezier);
 height: 1px;
 width: 100%;
 margin: 0;
 `),c("dashed",[n("line",{backgroundColor:"var(--n-color)"})]),s("dashed",[n("line",{borderColor:"var(--n-color)"})]),s("vertical",{backgroundColor:"var(--n-color)"})]),k=Object.assign(Object.assign({},h.props),{titlePlacement:{type:String,default:"center"},dashed:Boolean,vertical:Boolean}),N=x({name:"Divider",props:k,setup(i){const{mergedClsPrefixRef:o,inlineThemeDisabled:r}=C(i),a=h("Divider","-divider",j,y,i,o),d=$(()=>{const{common:{cubicBezierEaseInOut:e},self:{color:g,textColor:u,fontWeight:m}}=a.value;return{"--n-bezier":e,"--n-color":g,"--n-text-color":u,"--n-font-weight":m}}),t=r?_("divider",void 0,d,i):void 0;return{mergedClsPrefix:o,cssVars:r?void 0:d,themeClass:t?.themeClass,onRender:t?.onRender}},render(){var i;const{$slots:o,titlePlacement:r,vertical:a,dashed:d,cssVars:t,mergedClsPrefix:e}=this;return(i=this.onRender)===null||i===void 0||i.call(this),l("div",{role:"separator",class:[`${e}-divider`,this.themeClass,{[`${e}-divider--vertical`]:a,[`${e}-divider--no-title`]:!o.default,[`${e}-divider--dashed`]:d,[`${e}-divider--title-position-${r}`]:o.default&&r}],style:t},a?null:l("div",{class:`${e}-divider__line ${e}-divider__line--left`}),!a&&o.default?l(w,null,l("div",{class:`${e}-divider__title`},this.$slots),l("div",{class:`${e}-divider__line ${e}-divider__line--right`})):null)}});export{N,R as a,P as d,K as u};
