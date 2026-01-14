import{a as m,b as d,aM as Y,aN as J,aq as j,e as g,ap as w,d as C,b3 as X,h as c,b4 as Z,bi as ee,u as q,g as R,c5 as oe,c as T,i as E,j as H,bP as te,a7 as I,an as _,c6 as ne,c7 as re,c8 as ie,R as se,s as G,c9 as le,aY as ae,O as W,aA as D,ca as de,cb as ce,cc as pe,aT as ue,bU as be,cd as he,ce as ge,cf as ve,cg as fe,x as V,ch as me,ci as we,bn as ye,aD as xe,cj as Ce,ck as Pe,cl as Se,cm as ke,cn as $e,co as ze}from"./index-DeyCeJbE.js";function U(e,t="default",o=[]){const{children:n}=e;if(n!==null&&typeof n=="object"&&!Array.isArray(n)){const a=n[t];if(typeof a=="function")return a()}return o}const Ae=m([d("descriptions",{fontSize:"var(--n-font-size)"},[d("descriptions-separator",`
 display: inline-block;
 margin: 0 8px 0 2px;
 `),d("descriptions-table-wrapper",[d("descriptions-table",[d("descriptions-table-row",[d("descriptions-table-header",{padding:"var(--n-th-padding)"}),d("descriptions-table-content",{padding:"var(--n-td-padding)"})])])]),j("bordered",[d("descriptions-table-wrapper",[d("descriptions-table",[d("descriptions-table-row",[m("&:last-child",[d("descriptions-table-content",{paddingBottom:0})])])])])]),g("left-label-placement",[d("descriptions-table-content",[m("> *",{verticalAlign:"top"})])]),g("left-label-align",[m("th",{textAlign:"left"})]),g("center-label-align",[m("th",{textAlign:"center"})]),g("right-label-align",[m("th",{textAlign:"right"})]),g("bordered",[d("descriptions-table-wrapper",`
 border-radius: var(--n-border-radius);
 overflow: hidden;
 background: var(--n-merged-td-color);
 border: 1px solid var(--n-merged-border-color);
 `,[d("descriptions-table",[d("descriptions-table-row",[m("&:not(:last-child)",[d("descriptions-table-content",{borderBottom:"1px solid var(--n-merged-border-color)"}),d("descriptions-table-header",{borderBottom:"1px solid var(--n-merged-border-color)"})]),d("descriptions-table-header",`
 font-weight: 400;
 background-clip: padding-box;
 background-color: var(--n-merged-th-color);
 `,[m("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})]),d("descriptions-table-content",[m("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})])])])])]),d("descriptions-header",`
 font-weight: var(--n-th-font-weight);
 font-size: 18px;
 transition: color .3s var(--n-bezier);
 line-height: var(--n-line-height);
 margin-bottom: 16px;
 color: var(--n-title-text-color);
 `),d("descriptions-table-wrapper",`
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[d("descriptions-table",`
 width: 100%;
 border-collapse: separate;
 border-spacing: 0;
 box-sizing: border-box;
 `,[d("descriptions-table-row",`
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
 `,[d("descriptions-table-header",`
 font-weight: var(--n-th-font-weight);
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-th-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `),d("descriptions-table-content",`
 vertical-align: top;
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-td-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[w("content",`
 transition: color .3s var(--n-bezier);
 display: inline-block;
 color: var(--n-td-text-color);
 `)]),w("label",`
 font-weight: var(--n-th-font-weight);
 transition: color .3s var(--n-bezier);
 display: inline-block;
 margin-right: 14px;
 color: var(--n-th-text-color);
 `)])])])]),d("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color);
 --n-merged-td-color: var(--n-td-color);
 --n-merged-border-color: var(--n-border-color);
 `),Y(d("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-modal);
 --n-merged-td-color: var(--n-td-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `)),J(d("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-popover);
 --n-merged-td-color: var(--n-td-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `))]),Q="DESCRIPTION_ITEM_FLAG";function je(e){return typeof e=="object"&&e&&!Array.isArray(e)?e.type&&e.type[Q]:!1}const Re=Object.assign(Object.assign({},R.props),{title:String,column:{type:Number,default:3},columns:Number,labelPlacement:{type:String,default:"top"},labelAlign:{type:String,default:"left"},separator:{type:String,default:":"},size:{type:String,default:"medium"},bordered:Boolean,labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]}),He=C({name:"Descriptions",props:Re,slots:Object,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=q(e),n=R("Descriptions","-descriptions",Ae,oe,e,t),a=T(()=>{const{size:i,bordered:l}=e,{common:{cubicBezierEaseInOut:p},self:{titleTextColor:h,thColor:b,thColorModal:s,thColorPopover:v,thTextColor:P,thFontWeight:A,tdTextColor:N,tdColor:K,tdColorModal:O,tdColorPopover:u,borderColor:S,borderColorModal:M,borderColorPopover:f,borderRadius:y,lineHeight:k,[E("fontSize",i)]:$,[E(l?"thPaddingBordered":"thPadding",i)]:x,[E(l?"tdPaddingBordered":"tdPadding",i)]:z}}=n.value;return{"--n-title-text-color":h,"--n-th-padding":x,"--n-td-padding":z,"--n-font-size":$,"--n-bezier":p,"--n-th-font-weight":A,"--n-line-height":k,"--n-th-text-color":P,"--n-td-text-color":N,"--n-th-color":b,"--n-th-color-modal":s,"--n-th-color-popover":v,"--n-td-color":K,"--n-td-color-modal":O,"--n-td-color-popover":u,"--n-border-radius":y,"--n-border-color":S,"--n-border-color-modal":M,"--n-border-color-popover":f}}),r=o?H("descriptions",T(()=>{let i="";const{size:l,bordered:p}=e;return p&&(i+="a"),i+=l[0],i}),a,e):void 0;return{mergedClsPrefix:t,cssVars:o?void 0:a,themeClass:r?.themeClass,onRender:r?.onRender,compitableColumn:te(e,["columns","column"]),inlineThemeDisabled:o}},render(){const e=this.$slots.default,t=e?X(e()):[];t.length;const{contentClass:o,labelClass:n,compitableColumn:a,labelPlacement:r,labelAlign:i,size:l,bordered:p,title:h,cssVars:b,mergedClsPrefix:s,separator:v,onRender:P}=this;P?.();const A=t.filter(u=>je(u)),N={span:0,row:[],secondRow:[],rows:[]},O=A.reduce((u,S,M)=>{const f=S.props||{},y=A.length-1===M,k=["label"in f?f.label:U(S,"label")],$=[U(S)],x=f.span||1,z=u.span;u.span+=x;const L=f.labelStyle||f["label-style"]||this.labelStyle,B=f.contentStyle||f["content-style"]||this.contentStyle;if(r==="left")p?u.row.push(c("th",{class:[`${s}-descriptions-table-header`,n],colspan:1,style:L},k),c("td",{class:[`${s}-descriptions-table-content`,o],colspan:y?(a-z)*2+1:x*2-1,style:B},$)):u.row.push(c("td",{class:`${s}-descriptions-table-content`,colspan:y?(a-z)*2:x*2},c("span",{class:[`${s}-descriptions-table-content__label`,n],style:L},[...k,v&&c("span",{class:`${s}-descriptions-separator`},v)]),c("span",{class:[`${s}-descriptions-table-content__content`,o],style:B},$)));else{const F=y?(a-z)*2:x*2;u.row.push(c("th",{class:[`${s}-descriptions-table-header`,n],colspan:F,style:L},k)),u.secondRow.push(c("td",{class:[`${s}-descriptions-table-content`,o],colspan:F,style:B},$))}return(u.span>=a||y)&&(u.span=0,u.row.length&&(u.rows.push(u.row),u.row=[]),r!=="left"&&u.secondRow.length&&(u.rows.push(u.secondRow),u.secondRow=[])),u},N).rows.map(u=>c("tr",{class:`${s}-descriptions-table-row`},u));return c("div",{style:b,class:[`${s}-descriptions`,this.themeClass,`${s}-descriptions--${r}-label-placement`,`${s}-descriptions--${i}-label-align`,`${s}-descriptions--${l}-size`,p&&`${s}-descriptions--bordered`]},h||this.$slots.header?c("div",{class:`${s}-descriptions-header`},h||Z(this,"header")):null,c("div",{class:`${s}-descriptions-table-wrapper`},c("table",{class:`${s}-descriptions-table`},c("tbody",null,r==="top"&&c("tr",{class:`${s}-descriptions-table-row`,style:{visibility:"collapse"}},ee(a*2,c("td",null))),O))))}}),Ie={label:String,span:{type:Number,default:1},labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]},Ge=C({name:"DescriptionsItem",[Q]:!0,props:Ie,slots:Object,render(){return null}});function _e(){const e=I(ne,null);return e===null&&_("use-dialog","No outer <n-dialog-provider /> founded."),e}function Ne(){const e=I(re,null);return e===null&&_("use-loading-bar","No outer <n-loading-bar-provider /> founded."),e}function Oe(){const e=I(ie,null);return e===null&&_("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),e}const Me=C({name:"ModalEnvironment",props:Object.assign(Object.assign({},le),{internalKey:{type:String,required:!0},onInternalAfterLeave:{type:Function,required:!0}}),setup(e){const t=G(!0);function o(){const{onInternalAfterLeave:b,internalKey:s,onAfterLeave:v}=e;b&&b(s),v&&v()}function n(){const{onPositiveClick:b}=e;b?Promise.resolve(b()).then(s=>{s!==!1&&p()}):p()}function a(){const{onNegativeClick:b}=e;b?Promise.resolve(b()).then(s=>{s!==!1&&p()}):p()}function r(){const{onClose:b}=e;b?Promise.resolve(b()).then(s=>{s!==!1&&p()}):p()}function i(b){const{onMaskClick:s,maskClosable:v}=e;s&&(s(b),v&&p())}function l(){const{onEsc:b}=e;b&&b()}function p(){t.value=!1}function h(b){t.value=b}return{show:t,hide:p,handleUpdateShow:h,handleAfterLeave:o,handleCloseClick:r,handleNegativeClick:a,handlePositiveClick:n,handleMaskClick:i,handleEsc:l}},render(){const{handleUpdateShow:e,handleAfterLeave:t,handleMaskClick:o,handleEsc:n,show:a}=this;return c(se,Object.assign({},this.$props,{show:a,onUpdateShow:e,onMaskClick:o,onEsc:n,onAfterLeave:t,internalAppear:!0,internalModal:!0}),this.$slots)}}),Le={to:[String,Object]},Be=C({name:"ModalProvider",props:Le,setup(){const e=G([]),t={};function o(i={}){const l=ue(),p=be(Object.assign(Object.assign({},i),{key:l,destroy:()=>{var h;(h=t[`n-modal-${l}`])===null||h===void 0||h.hide()}}));return e.value.push(p),p}function n(i){const{value:l}=e;l.splice(l.findIndex(p=>p.key===i),1)}function a(){Object.values(t).forEach(i=>{i?.hide()})}const r={create:o,destroyAll:a};return D(he,r),D(pe,{clickedRef:ce(64),clickedPositionRef:de()}),D(ge,e),Object.assign(Object.assign({},r),{modalList:e,modalInstRefs:t,handleAfterLeave:n})},render(){var e,t;return c(W,null,[this.modalList.map(o=>{var n;return c(Me,ae(o,["destroy","render"],{to:(n=o.to)!==null&&n!==void 0?n:this.to,ref:a=>{a===null?delete this.modalInstRefs[`n-modal-${o.key}`]:this.modalInstRefs[`n-modal-${o.key}`]=a},internalKey:o.key,onInternalAfterLeave:this.handleAfterLeave}),{default:o.render})}),(t=(e=this.$slots).default)===null||t===void 0?void 0:t.call(e)])}});function Ee(){const e=I(ve,null);return e===null&&_("use-notification","No outer `n-notification-provider` found."),e}const De=C({name:"InjectionExtractor",props:{onSetup:Function},setup(e,{slots:t}){var o;return(o=e.onSetup)===null||o===void 0||o.call(e),()=>{var n;return(n=t.default)===null||n===void 0?void 0:n.call(t)}}}),Te={message:Oe,notification:Ee,loadingBar:Ne,dialog:_e,modal:me};function Ke({providersAndProps:e,configProviderProps:t}){let o=fe(a);const n={app:o};function a(){return c(we,V(t),{default:()=>e.map(({type:l,Provider:p,props:h})=>c(p,V(h),{default:()=>c(De,{onSetup:()=>n[l]=Te[l]()})}))})}let r;return ye&&(r=document.createElement("div"),document.body.appendChild(r),o.mount(r)),Object.assign({unmount:()=>{var l;if(o===null||r===null){xe("discrete","unmount call no need because discrete app has been unmounted");return}o.unmount(),(l=r.parentNode)===null||l===void 0||l.removeChild(r),r=null,o=null}},n)}function Fe(e,{configProviderProps:t,messageProviderProps:o,dialogProviderProps:n,notificationProviderProps:a,loadingBarProviderProps:r,modalProviderProps:i}={}){const l=[];return e.forEach(h=>{switch(h){case"message":l.push({type:h,Provider:ke,props:o});break;case"notification":l.push({type:h,Provider:Se,props:a});break;case"dialog":l.push({type:h,Provider:Pe,props:n});break;case"loadingBar":l.push({type:h,Provider:Ce,props:r});break;case"modal":l.push({type:h,Provider:Be,props:i})}}),Ke({providersAndProps:l,configProviderProps:t})}const Ve=d("divider",`
 position: relative;
 display: flex;
 width: 100%;
 box-sizing: border-box;
 font-size: 16px;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
`,[j("vertical",`
 margin-top: 24px;
 margin-bottom: 24px;
 `,[j("no-title",`
 display: flex;
 align-items: center;
 `)]),w("title",`
 display: flex;
 align-items: center;
 margin-left: 12px;
 margin-right: 12px;
 white-space: nowrap;
 font-weight: var(--n-font-weight);
 `),g("title-position-left",[w("line",[g("left",{width:"28px"})])]),g("title-position-right",[w("line",[g("right",{width:"28px"})])]),g("dashed",[w("line",`
 background-color: #0000;
 height: 0px;
 width: 100%;
 border-style: dashed;
 border-width: 1px 0 0;
 `)]),g("vertical",`
 display: inline-block;
 height: 1em;
 margin: 0 8px;
 vertical-align: middle;
 width: 1px;
 `),w("line",`
 border: none;
 transition: background-color .3s var(--n-bezier), border-color .3s var(--n-bezier);
 height: 1px;
 width: 100%;
 margin: 0;
 `),j("dashed",[w("line",{backgroundColor:"var(--n-color)"})]),g("dashed",[w("line",{borderColor:"var(--n-color)"})]),g("vertical",{backgroundColor:"var(--n-color)"})]),Ue=Object.assign(Object.assign({},R.props),{titlePlacement:{type:String,default:"center"},dashed:Boolean,vertical:Boolean}),We=C({name:"Divider",props:Ue,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=q(e),n=R("Divider","-divider",Ve,$e,e,t),a=T(()=>{const{common:{cubicBezierEaseInOut:i},self:{color:l,textColor:p,fontWeight:h}}=n.value;return{"--n-bezier":i,"--n-color":l,"--n-text-color":p,"--n-font-weight":h}}),r=o?H("divider",void 0,a,e):void 0;return{mergedClsPrefix:t,cssVars:o?void 0:a,themeClass:r?.themeClass,onRender:r?.onRender}},render(){var e;const{$slots:t,titlePlacement:o,vertical:n,dashed:a,cssVars:r,mergedClsPrefix:i}=this;return(e=this.onRender)===null||e===void 0||e.call(this),c("div",{role:"separator",class:[`${i}-divider`,this.themeClass,{[`${i}-divider--vertical`]:n,[`${i}-divider--no-title`]:!t.default,[`${i}-divider--dashed`]:a,[`${i}-divider--title-position-${o}`]:t.default&&o}],style:r},n?null:c("div",{class:`${i}-divider__line ${i}-divider__line--left`}),!n&&t.default?c(W,null,c("div",{class:`${i}-divider__title`},this.$slots),c("div",{class:`${i}-divider__line ${i}-divider__line--right`})):null)}}),{message:Qe,notification:Ye,dialog:Je,loadingBar:Xe}=Fe(["message","dialog","notification","loadingBar"],{configProviderProps:{theme:ze}});export{We as N,He as a,Ge as b,Je as d,Qe as m};
