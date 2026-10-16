(() => {
  'use strict';
  const form = document.querySelector('#income-form');
  if (!form) return;
  const rates = JSON.parse(document.querySelector('#calculator-data').textContent);
  const number = new Intl.NumberFormat('ru-RU');
  function plural(n, forms) { const x=n%100, y=n%10; return forms[x>10&&x<20 ? 2 : y===1 ? 0 : y>1&&y<5 ? 1 : 2]; }
  function update() {
    const city = rates[form.elements.city.value];
    const hours = Number(form.elements.hours.value), days = Number(form.elements.days.value);
    const base = Number(city[form.elements.transport.value]);
    const month = Math.round(base / 30 / 12 * hours * days);
    document.querySelector('#month-income').textContent = number.format(month);
    document.querySelector('#week-income').textContent = number.format(Math.round(month / 4));
    document.querySelector('#daily-hero').textContent = number.format(Math.round(base / 30));
    document.querySelector('#hours-value').textContent = `${hours} ${plural(hours, ['час','часа','часов'])}`;
    document.querySelector('#days-value').textContent = `${days} ${plural(days, ['день','дня','дней'])}`;
    for (const input of form.querySelectorAll('[type=range]')) input.style.setProperty('--progress', `${(input.value-input.min)/(input.max-input.min)*100}%`);
  }
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('submit', event => event.preventDefault());
  update();
})();
