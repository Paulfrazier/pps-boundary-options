/* Trade-offs at a glance: the models' green / yellow / red table (TRADEOFFS_MATRIX.json via site_data "matrix").
   renderMatrix(el, D, base, keep): el = container, D = SITE_DATA, base = path prefix to the kit root ("" or "../"),
   keep = optional function(planName) -> bool; plans it rejects are left out (options.html plan picker). */
function renderMatrix(el, D, base, keep){
  var M = D && D.matrix; if(!el) return;
  if(!M){ el.innerHTML = '<p class="muted">The trade-offs table is not in the data yet.</p>'; return; }
  var esc = function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var by = {}; D.options.forEach(function(o){by[o.name]=o});
  var P = keep ? M.plans.filter(function(p){return keep(p.name);}) : M.plans;
  if(!P.length){ el.innerHTML = '<p class="muted">No plans picked. Choose at least one plan above.</p>'; return; }
  var word = {green:'better', yellow:'middle', red:'worse'};
  var head = '<tr><th scope="col">Measure</th>'+P.map(function(p){var o=by[p.name]||{};
    return '<th scope="col"'+(p.name==='status_quo'?' class="ref"':'')+'>'+esc(o.short||p.name).replace(/K-8/g,'K&#8209;8')
      +(o.what_if?'<span class="mx-tag">what-if</span>':o.kind==='pps'||o.kind==='reference'?'<span class="mx-tag">'+(p.name==='status_quo'?'baseline':'PPS')+'</span>':'')+'</th>'}).join('')+'</tr>';
  // one table, all measures, colored boxes; no Key / All switch
  // site wording for rows whose models label reads awkwardly ("going to a farther school")
  var LABEL = {'K-5_past_closer':'K-5 kids assigned to a farther school, past a closer one','6-8_past_closer':'6-8 kids assigned to a farther school, past a closer one'};
  var rowsM = M.measures.slice();
  // K-5 within 1 mile is the 3rd row
  // ... and K-5 kids going past a closer school sits right below it
  var mv = function(key, at){ var r = rowsM.filter(function(m){return m.key===key;}); if (r.length) { rowsM = rowsM.filter(function(m){return m.key!==key;}); rowsM.splice(at, 0, r[0]); } };
  mv('K-5_within1', 2); mv('K-5_past_closer', 3);
  // small "vs PPS A" line under each value: the difference from PPS A's cell in the same row
  var pA = M.plans.filter(function(p){return p.name==='scenario_A';})[0];
  var parse = function(t){ t = String(t==null?'':t).replace(/,/g,'').trim(); var f = t.match(/^(-?\d+)\/(\d+)$/);
    if (f) return {v:+f[1], den:+f[2], dp:0, pct:false};
    var n = t.match(/^(-?\d+(?:\.(\d+))?)(%?)$/); return n ? {v:+n[1], den:null, dp:(n[2]||'').length, pct:!!n[3]} : null; };
  var vsA = function(p, m){ if (!pA || p.name==='scenario_A' || p.name==='status_quo') return '';
    var a = parse((pA.cells[m.key]||{}).text), b = parse((p.cells[m.key]||{}).text);
    if (!a || !b || a.den!==b.den || a.pct!==b.pct) return '';
    var d = +(b.v - a.v).toFixed(Math.max(a.dp, b.dp));
    var s = d===0 ? 'same as A' : (d>0?'+':'&minus;')+Math.abs(d).toLocaleString('en-US',{minimumFractionDigits:Math.max(a.dp,b.dp),maximumFractionDigits:Math.max(a.dp,b.dp)})+(a.pct?' pts':'')+' vs A';
    return '<span class="mx-vsA">'+s+'</span>'; };
  var body = rowsM.map(function(m){
    var st = m.key==='K-5_in_range_minus9';   // our stress test, not a PPS measure: bottom row, uncolored
    return '<tr'+(st?' class="mx-stress"':'')+'><th scope="row">'+esc(LABEL[m.key]||m.label)+'</th>'+P.map(function(p){var c=p.cells[m.key]||{};var r=st?'':(c.rating||'');
      return '<td class="mx-'+(r||'none')+'"'+(r?' title="'+word[r]+'"':'')+'>'+(r?'<span class="mx-dot" aria-hidden="true"></span><span class="vh">'+word[r]+': </span>':'')+esc(c.text)+vsA(p, m)+'</td>'}).join('')+'</tr>'}).join('');
  // footnote text
  var note = ''
    +'&mdash; compared among the plans that close schools (everything but PPS Status Quo, the uncolored baseline): each row&rsquo;s range from best to worst value is split into thirds. '
    +'The two &ldquo;at target every year&rdquo; rows are absolute instead: green when every school is at target in every year 2027-28 to 2031-32, yellow at 80% or more, red below. '
    +'Colors are relative to these plans, not a PPS standard. For PPS Status Quo, A and B, the &ldquo;at target every year&rdquo; rows use PPS&rsquo;s own Family Guide projections; every other number is our model, 2031-32 unless noted. Within 1 mile: share of neighborhood kids within a 1-mile walking route of their school. PPS&rsquo;s Family Guides report a &ldquo;within 1 mile&rdquo; figure per school but don&rsquo;t say how it is measured, so the two may not match exactly. '
    +'Past the bus line: kids whose walk is over the distance at which Oregon law (ORS 327.043) and PPS&rsquo;s transportation guidelines provide a bus, more than 1 mile for K-5 and 1.5 miles for 6-8 (<a href="'+base+'pages/sources.html#def-past-busing-distance">definition</a>). '
    +'Small gray lines: the difference from PPS A in the same row (&ldquo;pts&rdquo; = percentage points; for the &ldquo;at target every year&rdquo; rows, PPS A&rsquo;s count is PPS&rsquo;s own projection). '
    // a plan solved with a lower minimum (site_data PPS_FLOOR_RECOUNT) is counted here at PPS's: say so beside the table
    +P.map(function(p){var o=by[p.name]||{},sf=o.solved_floor||{};return Object.keys(sf).map(function(lv){
      return '<b>'+esc(o.short)+'</b> is solved with a '+lv+' minimum of '+sf[lv]+', below PPS&rsquo;s '+o.pps_floor[lv]+'; this table counts it at PPS&rsquo;s '+o.pps_floor[lv]
        +', so its '+lv+' schools below '+o.pps_floor[lv]+' in any year are not at target (<a href="'+base+'pages/options.html#opt-'+esc(p.name)+'">call-out</a>). '}).join('')}).join('')
    +(P.length<M.plans.length?'Some plans are hidden; colors still compare all '+M.plans.length+' plans. ':'')
    +'Source: <a href="'+base+esc(M.source)+'">TRADEOFFS_MATRIX.json</a>, built from each plan&rsquo;s scorecard.</p>';
  el.innerHTML = '<div class="tbl mx-wrap"><table class="mx"><thead>'+head+'</thead><tbody>'+body+'</tbody></table></div>'
    +'<p class="small muted mx-key"><span class="mx-k mx-green"><span class="mx-dot"></span>better</span> <span class="mx-k mx-yellow"><span class="mx-dot"></span>middle</span> <span class="mx-k mx-red"><span class="mx-dot"></span>worse</span> '
    + note;
}
