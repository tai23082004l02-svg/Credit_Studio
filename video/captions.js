// Supplement saved drafts only when the English cues and their timings match exactly.
// Never replace a user's translation, timeline, audio or other project content.
export function mergeCaptionTranslation(project,bundle){
 if(!bundle||bundle.version!==1||bundle.language!=='vi'||typeof bundle.revision!=='string'||!bundle.revision||bundle.revision!==project.revision||!Array.isArray(bundle.captions)||!project.captions?.length||bundle.captions.length!==project.captions.length)return project;
 if(bundle.captions.some((c,i)=>!c||c.start!==project.captions[i].start||c.end!==project.captions[i].end||c.text!==project.captions[i].text||typeof c.textVi!=='string'||!c.textVi.trim()||c.textVi.length>500))return project;
 if(project.captions.every(c=>typeof c.textVi==='string'&&c.textVi.trim()))return project;
 const next=JSON.parse(JSON.stringify(project));
 next.captions.forEach((c,i)=>{if(!c.textVi?.trim())c.textVi=bundle.captions[i].textVi;});
 return next;
}
export const hasVietnameseCaptions=project=>!!project.captions?.length&&project.captions.every(c=>typeof c.textVi==='string'&&!!c.textVi.trim());
