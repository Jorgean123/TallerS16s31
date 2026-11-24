'use strict';
const $ = id => document.getElementById(id);
let token = '', selected = null;
function notice(message, error = false) { $('notice').textContent = message; $('notice').className = error ? 'error' : ''; $('notice').hidden = !message; }
function session(active) { $('login-panel').hidden = active; $('dashboard').hidden = !active; $('logout').hidden = !active; $('account').textContent = active ? 'Administrador · Sesión activa' : 'Sin sesión'; }
async function api(path, options = {}) {
  const res = await fetch('api/' + path, { ...options, headers: { 'Content-Type': 'application/json', ...(token ? {Authorization: 'Bearer ' + token} : {}), ...options.headers } });
  const data = await res.json();
  if (!res.ok) {
    if(res.status === 401 && token) { token = ''; session(false); $('edit-dialog').close(); }
    throw new Error(data.detail || data.message || 'No se pudo completar la operación.');
  }
  return data;
}
async function busy(button, action) { button.disabled = true; try { await action(); } finally { button.disabled = false; } }
function cell(text, cls) { const el = document.createElement('td'); el.textContent = text; if(cls) el.className = cls; return el; }
async function load() {
  const q = new URLSearchParams({sort:$('sort').value}); if($('ciclo').value) q.set('ciclo',$('ciclo').value);
  const data = await api('v1/cursos?' + q);
  $('courses').replaceChildren();
  data.forEach(c => {
    const row = document.createElement('tr'), name = cell(''), title = document.createElement('b'), code = document.createElement('small');
    title.textContent = c.nombre; code.textContent = c.codigo + ' · ID ' + c.id; name.append(title,code);
    const cycle = cell(''), cycleLabel = document.createElement('span'); cycleLabel.className = 'cycle'; cycleLabel.textContent = 'Ciclo ' + c.ciclo; cycle.append(cycleLabel);
    const state = cell(''), badge = document.createElement('span'); badge.className = 'badge' + (c.vacantes ? '' : ' full'); badge.textContent = c.vacantes ? 'Disponible' : 'Sin vacantes'; state.append(badge);
    const action = cell(''), button = document.createElement('button'); button.className = 'edit'; button.textContent = 'Editar vacantes'; button.setAttribute('aria-label','Editar vacantes de ' + c.nombre); button.onclick = () => { selected = c.id; $('edit-name').textContent = c.nombre; $('new-vacantes').value = c.vacantes; $('edit-error').hidden = true; $('edit-dialog').showModal(); }; action.append(button);
    row.append(name,cycle,cell(c.vacantes),state,action); $('courses').append(row);
  });
  $('total').textContent = data.length; $('vacantes').textContent = data.reduce((a,c) => a+c.vacantes,0); $('disponibles').textContent = data.filter(c => c.vacantes>0).length;
  $('count').textContent = data.length + ' cursos encontrados'; $('empty').hidden = data.length !== 0;
}
$('login-form').onsubmit = e => { e.preventDefault(); busy(e.submitter, async () => { try { const result = await api('auth/login',{method:'POST',body:JSON.stringify({usuario:$('usuario').value,clave:$('clave').value})}); token = result.access_token; $('clave').value = ''; session(true); notice(''); await load(); } catch(err) { notice(err.message,true); } }); };
$('filters').onsubmit = e => { e.preventDefault(); busy(e.submitter,async () => { try { await load(); notice(''); } catch(err) { notice(err.message,true); } }); };
$('logout').onclick = () => { token = ''; session(false); notice(''); $('courses').replaceChildren(); };
$('close-dialog').onclick = $('cancel').onclick = () => $('edit-dialog').close();
$('edit-form').onsubmit = e => { e.preventDefault(); busy(e.submitter,async () => { try { const n = Number($('new-vacantes').value); if(!Number.isInteger(n) || n<0 || n>2147483647) throw new Error('Ingrese un entero válido mayor o igual a cero.'); await api('v1/cursos/'+selected,{method:'PATCH',body:JSON.stringify({vacantes:n})}); $('edit-dialog').close(); notice('Vacantes actualizadas correctamente.'); await load(); } catch(err) { $('edit-error').textContent = err.message; $('edit-error').hidden = false; if(!$('edit-dialog').open) notice(err.message,true); } }); };
