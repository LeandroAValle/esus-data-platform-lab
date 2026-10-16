const $ = selector => document.querySelector(selector);
const el = (tag, text, className) => { const item = document.createElement(tag); if (text !== undefined) item.textContent = text; if (className) item.className = className; return item; };
let data;
function selectLayer(layer) {
  document.querySelectorAll('.layer').forEach(card => card.classList.toggle('selected', card.dataset.id === layer.id));
  const detail = $('#layer-detail'); detail.replaceChildren();
  const heading = el('div', undefined, 'detail-heading'); heading.append(el('span', `CAMADA ${layer.number}`, 'kicker'), el('h3', layer.name), el('span', layer.state, 'state-badge'));
  detail.append(heading, el('p', layer.description));
  const columns = el('div', undefined, 'detail-columns'), decision = el('div'), files = el('div');
  decision.append(el('b', 'DECISÃO DE ARQUITETURA'), el('p', layer.design));
  files.append(el('b', 'ARQUIVOS NO REPOSITÓRIO'));
  const list = el('ul');
  for (const path of layer.files) { const line = el('li'), link = el('a', `${path} ↗`); link.href = `https://github.com/LeandroAValle/esus-data-platform-lab/blob/main/${path}`; link.target = '_blank'; link.rel = 'noopener'; line.append(link); list.append(line); }
  files.append(list); columns.append(decision, files); detail.append(columns);
}
async function init() {
  try {
    const response = await fetch('layers.json'); if (!response.ok) throw new Error(`HTTP ${response.status}`); data = await response.json();
    const pipeline = $('#pipeline');
    for (const layer of data.layers) { const button = el('button', undefined, 'layer'); button.type = 'button'; button.dataset.id = layer.id; button.append(el('span', layer.number, 'layer-number'), el('strong', layer.name), el('small', layer.tech), el('em', layer.state)); button.addEventListener('click', () => selectLayer(layer)); pipeline.append(button); }
    selectLayer(data.layers[0]);
    const tasks = $('#tasks'); for (const [index, task] of data.orchestration.tasks.entries()) { const box = el('div', undefined, 'task'); box.append(el('span', `0${index + 1}`), el('strong', task.replaceAll('_', ' '))); tasks.append(box); }
    const roadmap = $('#roadmap'); for (const item of data.roadmap) roadmap.append(el('li', item));
  } catch (error) { $('#pipeline').textContent = 'Não foi possível carregar o mapa da arquitetura.'; console.error(error); }
}
init();
