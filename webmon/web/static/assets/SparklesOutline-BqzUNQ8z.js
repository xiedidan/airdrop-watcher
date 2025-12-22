import{a as b,b as e,aX as G,bd as K,as as U,e as C,R as T,d as P,aM as W,h as n,bx as X,aN as q,u as J,g as V,c4 as Q,c as _,i as A,j as Y,bU as Z,k as N,o as F,l as h}from"./index-C0S4fFCR.js";function E(r,d="default",l=[]){const{children:a}=r;if(a!==null&&typeof a=="object"&&!Array.isArray(a)){const s=a[d];if(typeof s=="function")return s()}return l}const ee=b([e("descriptions",{fontSize:"var(--n-font-size)"},[e("descriptions-separator",`
 display: inline-block;
 margin: 0 8px 0 2px;
 `),e("descriptions-table-wrapper",[e("descriptions-table",[e("descriptions-table-row",[e("descriptions-table-header",{padding:"var(--n-th-padding)"}),e("descriptions-table-content",{padding:"var(--n-td-padding)"})])])]),U("bordered",[e("descriptions-table-wrapper",[e("descriptions-table",[e("descriptions-table-row",[b("&:last-child",[e("descriptions-table-content",{paddingBottom:0})])])])])]),C("left-label-placement",[e("descriptions-table-content",[b("> *",{verticalAlign:"top"})])]),C("left-label-align",[b("th",{textAlign:"left"})]),C("center-label-align",[b("th",{textAlign:"center"})]),C("right-label-align",[b("th",{textAlign:"right"})]),C("bordered",[e("descriptions-table-wrapper",`
 border-radius: var(--n-border-radius);
 overflow: hidden;
 background: var(--n-merged-td-color);
 border: 1px solid var(--n-merged-border-color);
 `,[e("descriptions-table",[e("descriptions-table-row",[b("&:not(:last-child)",[e("descriptions-table-content",{borderBottom:"1px solid var(--n-merged-border-color)"}),e("descriptions-table-header",{borderBottom:"1px solid var(--n-merged-border-color)"})]),e("descriptions-table-header",`
 font-weight: 400;
 background-clip: padding-box;
 background-color: var(--n-merged-th-color);
 `,[b("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})]),e("descriptions-table-content",[b("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})])])])])]),e("descriptions-header",`
 font-weight: var(--n-th-font-weight);
 font-size: 18px;
 transition: color .3s var(--n-bezier);
 line-height: var(--n-line-height);
 margin-bottom: 16px;
 color: var(--n-title-text-color);
 `),e("descriptions-table-wrapper",`
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[e("descriptions-table",`
 width: 100%;
 border-collapse: separate;
 border-spacing: 0;
 box-sizing: border-box;
 `,[e("descriptions-table-row",`
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
 `,[e("descriptions-table-header",`
 font-weight: var(--n-th-font-weight);
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-th-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `),e("descriptions-table-content",`
 vertical-align: top;
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-td-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[T("content",`
 transition: color .3s var(--n-bezier);
 display: inline-block;
 color: var(--n-td-text-color);
 `)]),T("label",`
 font-weight: var(--n-th-font-weight);
 transition: color .3s var(--n-bezier);
 display: inline-block;
 margin-right: 14px;
 color: var(--n-th-text-color);
 `)])])])]),e("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color);
 --n-merged-td-color: var(--n-td-color);
 --n-merged-border-color: var(--n-border-color);
 `),G(e("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-modal);
 --n-merged-td-color: var(--n-td-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `)),K(e("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-popover);
 --n-merged-td-color: var(--n-td-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `))]),H="DESCRIPTION_ITEM_FLAG";function oe(r){return typeof r=="object"&&r&&!Array.isArray(r)?r.type&&r.type[H]:!1}const te=Object.assign(Object.assign({},V.props),{title:String,column:{type:Number,default:3},columns:Number,labelPlacement:{type:String,default:"top"},labelAlign:{type:String,default:"left"},separator:{type:String,default:":"},size:{type:String,default:"medium"},bordered:Boolean,labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]}),ie=P({name:"Descriptions",props:te,slots:Object,setup(r){const{mergedClsPrefixRef:d,inlineThemeDisabled:l}=J(r),a=V("Descriptions","-descriptions",ee,Q,r,d),s=_(()=>{const{size:c,bordered:g}=r,{common:{cubicBezierEaseInOut:u},self:{titleTextColor:S,thColor:j,thColorModal:t,thColorPopover:z,thTextColor:v,thFontWeight:$,tdTextColor:R,tdColor:D,tdColorModal:M,tdColorPopover:o,borderColor:w,borderColorModal:O,borderColorPopover:p,borderRadius:m,lineHeight:x,[A("fontSize",c)]:k,[A(g?"thPaddingBordered":"thPadding",c)]:f,[A(g?"tdPaddingBordered":"tdPadding",c)]:y}}=a.value;return{"--n-title-text-color":S,"--n-th-padding":f,"--n-td-padding":y,"--n-font-size":k,"--n-bezier":u,"--n-th-font-weight":$,"--n-line-height":x,"--n-th-text-color":v,"--n-td-text-color":R,"--n-th-color":j,"--n-th-color-modal":t,"--n-th-color-popover":z,"--n-td-color":D,"--n-td-color-modal":M,"--n-td-color-popover":o,"--n-border-radius":m,"--n-border-color":w,"--n-border-color-modal":O,"--n-border-color-popover":p}}),i=l?Y("descriptions",_(()=>{let c="";const{size:g,bordered:u}=r;return u&&(c+="a"),c+=g[0],c}),s,r):void 0;return{mergedClsPrefix:d,cssVars:l?void 0:s,themeClass:i?.themeClass,onRender:i?.onRender,compitableColumn:Z(r,["columns","column"]),inlineThemeDisabled:l}},render(){const r=this.$slots.default,d=r?W(r()):[];d.length;const{contentClass:l,labelClass:a,compitableColumn:s,labelPlacement:i,labelAlign:c,size:g,bordered:u,title:S,cssVars:j,mergedClsPrefix:t,separator:z,onRender:v}=this;v?.();const $=d.filter(o=>oe(o)),R={span:0,row:[],secondRow:[],rows:[]},M=$.reduce((o,w,O)=>{const p=w.props||{},m=$.length-1===O,x=["label"in p?p.label:E(w,"label")],k=[E(w)],f=p.span||1,y=o.span;o.span+=f;const L=p.labelStyle||p["label-style"]||this.labelStyle,B=p.contentStyle||p["content-style"]||this.contentStyle;if(i==="left")u?o.row.push(n("th",{class:[`${t}-descriptions-table-header`,a],colspan:1,style:L},x),n("td",{class:[`${t}-descriptions-table-content`,l],colspan:m?(s-y)*2+1:f*2-1,style:B},k)):o.row.push(n("td",{class:`${t}-descriptions-table-content`,colspan:m?(s-y)*2:f*2},n("span",{class:[`${t}-descriptions-table-content__label`,a],style:L},[...x,z&&n("span",{class:`${t}-descriptions-separator`},z)]),n("span",{class:[`${t}-descriptions-table-content__content`,l],style:B},k)));else{const I=m?(s-y)*2:f*2;o.row.push(n("th",{class:[`${t}-descriptions-table-header`,a],colspan:I,style:L},x)),o.secondRow.push(n("td",{class:[`${t}-descriptions-table-content`,l],colspan:I,style:B},k))}return(o.span>=s||m)&&(o.span=0,o.row.length&&(o.rows.push(o.row),o.row=[]),i!=="left"&&o.secondRow.length&&(o.rows.push(o.secondRow),o.secondRow=[])),o},R).rows.map(o=>n("tr",{class:`${t}-descriptions-table-row`},o));return n("div",{style:j,class:[`${t}-descriptions`,this.themeClass,`${t}-descriptions--${i}-label-placement`,`${t}-descriptions--${c}-label-align`,`${t}-descriptions--${g}-size`,u&&`${t}-descriptions--bordered`]},S||this.$slots.header?n("div",{class:`${t}-descriptions-header`},S||q(this,"header")):null,n("div",{class:`${t}-descriptions-table-wrapper`},n("table",{class:`${t}-descriptions-table`},n("tbody",null,i==="top"&&n("tr",{class:`${t}-descriptions-table-row`,style:{visibility:"collapse"}},X(s*2,n("td",null))),M))))}}),re={label:String,span:{type:Number,default:1},labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]},ae=P({name:"DescriptionsItem",[H]:!0,props:re,slots:Object,render(){return null}}),ne={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},de=P({name:"DocumentTextOutline",render:function(d,l){return F(),N("svg",ne,l[0]||(l[0]=[h("path",{d:"M416 221.25V416a48 48 0 0 1-48 48H144a48 48 0 0 1-48-48V96a48 48 0 0 1 48-48h98.75a32 32 0 0 1 22.62 9.37l141.26 141.26a32 32 0 0 1 9.37 22.62z",fill:"none",stroke:"currentColor","stroke-linejoin":"round","stroke-width":"32"},null,-1),h("path",{d:"M256 56v120a32 32 0 0 0 32 32h120",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),h("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M176 288h160"},null,-1),h("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M176 368h160"},null,-1)]))}}),le={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},ce=P({name:"SparklesOutline",render:function(d,l){return F(),N("svg",le,l[0]||(l[0]=[h("path",{d:"M259.92 262.91L216.4 149.77a9 9 0 0 0-16.8 0l-43.52 113.14a9 9 0 0 1-5.17 5.17L37.77 311.6a9 9 0 0 0 0 16.8l113.14 43.52a9 9 0 0 1 5.17 5.17l43.52 113.14a9 9 0 0 0 16.8 0l43.52-113.14a9 9 0 0 1 5.17-5.17l113.14-43.52a9 9 0 0 0 0-16.8l-113.14-43.52a9 9 0 0 1-5.17-5.17z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"},null,-1),h("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M108 68L88 16L68 68L16 88l52 20l20 52l20-52l52-20l-52-20z"},null,-1),h("path",{fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32",d:"M426.67 117.33L400 48l-26.67 69.33L304 144l69.33 26.67L400 240l26.67-69.33L496 144l-69.33-26.67z"},null,-1)]))}});export{de as D,ie as N,ce as S,ae as a};
