// Optional Node-only UI behavior checks. No DOM/browser packages required.
// API/SQLite integration is independently covered by validate.py.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'scripts/classroom.html'), 'utf8');
const source = html.split('<script>')[1].split('</script>')[0];
const course = {exercises: JSON.parse(fs.readFileSync(path.join(root,'exercises/catalog.json'))), lessons: JSON.parse(fs.readFileSync(path.join(root,'exercises/lessons.json')))};
const notes = Object.fromEntries([['Learning plan','CURRICULUM.md'],['Final briefing','capstone.md'],['Glossary','glossary.md']].map(([label,file])=>[label,fs.readFileSync(path.join(root,file),'utf8')]));
const sourceTables=Object.fromEntries([['clients',20],['projects',100],['markets',10],['project_markets',180],['invoices',300],['survey_waves',200]].map(([name,count])=>[name,{columns:['id','example'],rows:Array.from({length:count},(_,i)=>[i+1,i===0?null:`Example ${i+1}`]),grain:`one ${name} record`} ]));

// Minimal DOM adapter: the test validates state transitions, not browser rendering.
class Element {
  constructor(tag) {this.tagName=tag;this.children=[];this._text='';this.className='';this.value='';this.dataset={};this.style={};this.attributes={};this.events={};this.disabled=false;this.open=false;}
  set textContent(value) {this._text=String(value);this.children=[];}
  get textContent() {return this._text+this.children.map(c=>c.textContent).join('');}
  get firstChild() {return this.children[0];}
  append(...nodes) {this.children.push(...nodes);}
  replaceChildren(...nodes) {this._text='';this.children=[...nodes];}
  setAttribute(key,value) {this.attributes[key]=value;}
  get classList() {return {remove:(name)=>{this.className=this.className.split(' ').filter(v=>v!==name).join(' ');},add:(name)=>{if(!this.className.split(' ').includes(name))this.className+=' '+name;}};}
  addEventListener(name,callback) {this.events[name]=callback;}
  dispatchEvent(event) {this.events[event.type]?.(event);}
  click() {if(!this.disabled)return this.onclick?.();}
  showModal() {this.open=true;}
  close() {this.open=false;}
}
const pause = () => new Promise(resolve=>setTimeout(resolve,5));
function classroom(store=new Map(),storageFails=false,sourceFails=false) {
  const ids={};
  for(const match of html.matchAll(/id="([^"]+)"/g))ids[match[1]]=new Element('div');
  const document={getElementById:id=>ids[id],createElement:tag=>new Element(tag),querySelectorAll:selector=>{
    const nodes=[];
    function visit(el){if(el.className.split(' ').includes(selector.slice(1)))nodes.push(el);el.children.forEach(visit);}
    Object.values(ids).forEach(visit);return nodes;
  }};
  let mode='success';
  const sandbox={document,console,setTimeout,Blob,URL,Event:class {constructor(type){this.type=type;}},localStorage:{
    getItem:key=>{if(storageFails)throw Error('Storage disabled');return store.get(key)||null;},
    setItem:(key,value)=>{if(storageFails)throw Error('Storage disabled');store.set(key,value);}
  },fetch:async(route,opts)=>{
    if(route==='/api/tables'&&sourceFails)throw Error('Source data unavailable');
    if(mode==='offline'&&opts)throw Error('Server unavailable');
    const result=route==='/api/tables'?sourceTables:route==='/api/course'?course:route==='/api/notes'?notes:route==='/api/schema'?{rows:[['projects','CREATE TABLE projects (project_id INTEGER PRIMARY KEY)']]}:route==='/api/run'?{columns:['n','unknown'],rows:[[100,null]]}:{passed:mode!=='fail',tests:[{passed:mode!=='fail',dataset:'Practice',detail:'Example feedback.'},{passed:mode!=='fail',dataset:'Variation',detail:'Example feedback.'}],note:'Explain your reasoning.'};
    return {ok:true,json:async()=>result};
  }};
  vm.createContext(sandbox);vm.runInContext(source,sandbox);
  return {ids,store,setMode:value=>{mode=value;},allowSources:()=>{sourceFails=false;},evaluate:code=>vm.runInContext(code,sandbox)};
}
(async()=>{
  const app=classroom();await pause();const {ids}=app;
  assert.equal(ids.title.textContent,'Meet the clients');
  assert.equal(ids['exercise-list'].children.length,10);
  assert.equal(ids['source-title'].textContent,'clients');
  assert.ok(ids['source-status'].textContent.includes('All 20 rows'));
  assert.equal(ids['source-data'].firstChild.children[1].children.length,20);
  assert.ok(ids['source-data'].textContent.includes('NULL'));
  const initialSource=ids['source-data'].textContent;
  assert.ok(ids['lesson-body'].textContent.includes('primary')||ids['lesson-body'].textContent.includes('database'));
  ids.sql.value='SELECT client_id, client_name, sector FROM clients ORDER BY client_id LIMIT 5;';
  ids.sql.dispatchEvent({type:'input'});
  await app.evaluate('execute(false)');
  assert.ok(ids['result-title'].textContent.includes('1 rows'));
  assert.ok(ids['result-table'].textContent.includes('NULL'));
  assert.equal(ids['source-data'].textContent,initialSource);
  await app.evaluate('execute(true)');
  assert.equal(ids.progress.value,1);
  assert.ok(ids.feedback.textContent.includes('both datasets match'));
  ids.sql.value+=' ';ids.sql.dispatchEvent({type:'input'});
  assert.equal(ids.progress.value,0);
  await app.evaluate('execute(true)');
  ids.next.click();assert.equal(ids.title.textContent,'Project grain');
  assert.equal(ids['source-title'].textContent,'projects');
  assert.equal(ids['source-data'].firstChild.children[1].children.length,100);
  ids.sql.value='SELECT project_id FROM projects;';ids.sql.dispatchEvent({type:'input'});
  const restored=classroom(app.store);await pause();
  assert.equal(restored.ids.title.textContent,'Project grain');
  assert.equal(restored.ids.sql.value,'SELECT project_id FROM projects;');
  assert.equal(restored.ids.progress.value,1);
  ids.week.value='3';ids.week.onchange();ids['exercise-list'].children[9].click();
  assert.deepEqual(ids['source-buttons'].children.map(button=>button.textContent),['clients','projects','invoices','project_markets']);
  ids['source-buttons'].children[2].click();
  assert.equal(ids['source-title'].textContent,'invoices');
  assert.equal(ids['source-data'].firstChild.children[1].children.length,300);
  assert.equal(ids['source-buttons'].children[2].attributes['aria-pressed'],'true');
  ids.week.value='6';ids.week.onchange();
  assert.equal(ids.title.textContent,'Verify the bridge grain');
  await ids['schema-button'].click();assert.equal(ids.schema.open,true);
  ids['close-schema'].click();assert.equal(ids.schema.open,false);
  await ids['notes-button'].click();assert.equal(ids.notes.open,true);
  assert.ok(ids['notes-body'].textContent.includes('Six-week SQL curriculum'));
  ids['notes-select'].value='Final briefing';ids['notes-select'].onchange();
  assert.ok(ids['notes-body'].textContent.includes('Scoring rubric'));
  ids['close-notes'].click();assert.equal(ids.notes.open,false);
  app.setMode('fail');await app.evaluate('execute(true)');
  assert.ok(ids.feedback.textContent.includes('needs attention'));
  app.setMode('offline');await app.evaluate('execute(false)');
  assert.ok(ids.feedback.textContent.includes('Server unavailable'));
  assert.equal(ids.check.disabled,false);assert.equal(ids.sql.disabled,false);
  const noStorage=classroom(new Map(),true);await pause();
  assert.equal(noStorage.ids.title.textContent,'Meet the clients');
  assert.ok(!noStorage.ids['storage-warning'].className.split(' ').includes('hidden'));
  const unavailable=classroom(new Map(),false,true);await pause();
  assert.equal(unavailable.ids.title.textContent,'Meet the clients');
  assert.ok(unavailable.ids['source-status'].textContent.includes('Source data unavailable'));
  unavailable.allowSources();await unavailable.ids['source-status'].children[1].click();
  assert.equal(unavailable.ids['source-data'].firstChild.children[1].children.length,20);
  console.log('PASS: full source tables, table switching, independent query results, preview recovery, navigation, answer checks and saved progress.');
})().catch(error=>{console.error(error);process.exitCode=1;});
