// Shared KinAlert checker widget for content pages. Mount: <div data-kinalert-checker data-example="..."></div>
(function () {
  var API = 'https://kinalert-checker.checker-worker.workers.dev/check';
  var TITLE = { SCAM: 'This looks like a scam', SAFE: 'This looks genuine', UNSURE: 'Not sure, so be careful' };
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  document.querySelectorAll('[data-kinalert-checker]').forEach(function (root) {
    root.innerHTML =
      '<form class="kc" novalidate><label class="kc-l" for="kc-msg">Paste the message you got</label>' +
      '<textarea id="kc-msg" maxlength="2500" placeholder="Paste the text, email or WhatsApp here"></textarea>' +
      '<div class="kc-row"><label class="kc-file">Add a screenshot<input type="file" accept="image/*" hidden></label>' +
      '<span class="kc-pv"></span><button class="kc-go" type="submit">Check it free</button></div>' +
      (root.dataset.example ? '<button type="button" class="kc-ex">Try the example</button>' : '') +
      '<div class="kc-out" aria-live="polite"></div></form>';
    var form = root.querySelector('form'), ta = root.querySelector('textarea'), go = root.querySelector('.kc-go');
    var out = root.querySelector('.kc-out'), fileIn = root.querySelector('input[type=file]'), pv = root.querySelector('.kc-pv');
    var image = null;
    fileIn.addEventListener('change', function () {
      var f = fileIn.files && fileIn.files[0]; if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        var img = new Image();
        img.onload = function () {
          var k = Math.min(1, 1600 / Math.max(img.width, img.height)), c = document.createElement('canvas');
          c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
          c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
          image = c.toDataURL('image/jpeg', 0.85); pv.textContent = 'Screenshot added';
        };
        img.src = r.result;
      };
      r.readAsDataURL(f);
    });
    var ex = root.querySelector('.kc-ex');
    if (ex) ex.addEventListener('click', function () { ta.value = root.dataset.example; form.requestSubmit(); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = ta.value.trim();
      if (!image && text.length < 5) { out.innerHTML = '<p class="kc-err">Paste the message, or add a screenshot.</p>'; return; }
      go.disabled = true; go.textContent = 'Checking…'; out.innerHTML = '';
      var body = { text: text }; if (image) body.image = image;
      fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.success) { out.innerHTML = '<p class="kc-err">' + esc(j.error || 'Something went wrong. Try again.') + '</p>'; return; }
          var d = j.data, v = TITLE[d.verdict] ? d.verdict : 'UNSURE';
          var steps = (d.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('');
          out.innerHTML = '<div class="kc-v ' + v + '"><strong>' + TITLE[v] + '</strong><p>' + esc(d.reason) + '</p>' +
            (steps ? '<ol>' + steps + '</ol>' : '') + '<p class="kc-fam">Want to know when your mum or dad gets one? <a href="/#family">Join the KinAlert waitlist</a>.</p></div>';
        })
        .catch(function (err) { console.error('check failed', err); out.innerHTML = '<p class="kc-err">No connection. Try again.</p>'; })
        .finally(function () { go.disabled = false; go.textContent = 'Check it free'; image = null; pv.textContent = ''; fileIn.value = ''; });
    });
  });
})();
