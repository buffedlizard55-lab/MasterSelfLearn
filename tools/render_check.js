#!/usr/bin/env node
/* Render every page of the site headlessly and fail if any of them is blank or
 * throws.  A syntax check proves app.js parses; it does not prove that a page
 * draws.  This does: it supplies the slice of the DOM app.js touches, fires the
 * DOMContentLoaded handler the way a browser would, and asserts that #main has
 * children and no "Render error on" note for each route.
 *
 * Usage:  node tools/render_check.js
 * Exit 0 = every page rendered, 1 = something did not.
 */
'use strict';
var fs = require('fs');
var path = require('path');
var ROOT = path.resolve(__dirname, '..');

function Node(tag) {
  this.tagName = (tag || '').toUpperCase();
  this.children = []; this.attributes = {}; this._text = ''; this._html = '';
  this.parentNode = null; this.style = {}; this.className = ''; this.open = false;
}
Node.prototype.setAttribute = function (k, v) { this.attributes[k] = String(v); };
Node.prototype.getAttribute = function (k) { return k in this.attributes ? this.attributes[k] : null; };
Node.prototype.appendChild = function (c) { c.parentNode = this; this.children.push(c); return c; };
Node.prototype.removeChild = function (c) {
  var i = this.children.indexOf(c); if (i >= 0) this.children.splice(i, 1); return c;
};
Node.prototype.insertBefore = function (c, ref) {
  c.parentNode = this; var i = this.children.indexOf(ref);
  if (i < 0) this.children.push(c); else this.children.splice(i, 0, c); return c;
};
Node.prototype.remove = function () { if (this.parentNode) this.parentNode.removeChild(this); };
Node.prototype.addEventListener = function (t, f) { (this._ev = this._ev || {})[t] = f; };
Node.prototype.dispatch = function (t, ev) {
  if (this._ev && this._ev[t]) return this._ev[t](ev || { preventDefault: function () {}, target: this, key: '' });
};
Node.prototype.querySelectorAll = function () { return []; };
Node.prototype.querySelector = function () { return null; };
Node.prototype.scrollIntoView = function () {};
Node.prototype.focus = function () {};
Node.prototype.classList = null;
Object.defineProperty(Node.prototype, 'classList', { get: function () {
  var s = this;
  return { add: function (c) { s.className = (s.className + ' ' + c).trim(); },
           remove: function (c) { s.className = s.className.split(/\s+/).filter(function (x) { return x && x !== c; }).join(' '); },
           toggle: function (c, f) { f ? this.add(c) : this.remove(c); },
           contains: function (c) { return s.className.split(/\s+/).indexOf(c) >= 0; } };
} });
Object.defineProperty(Node.prototype, 'innerHTML', {
  get: function () { return this._html; },
  set: function (v) { this._html = String(v); this._text = String(v).replace(/<[^>]*>/g, ''); } });
Object.defineProperty(Node.prototype, 'textContent', {
  get: function () { return this._text + this.children.map(function (c) { return c.textContent; }).join(''); },
  set: function (v) { this._text = String(v); this.children = []; } });
Object.defineProperty(Node.prototype, 'value', {
  get: function () { return this._value || ''; }, set: function (v) { this._value = v; } });
Object.defineProperty(Node.prototype, 'firstChild', { get: function () { return this.children[0] || null; } });

var els = {}, docReady = null;
global.document = {
  createElement: function (t) { return new Node(t); },
  createTextNode: function (t) { var n = new Node('#text'); n._text = String(t); return n; },
  createDocumentFragment: function () { return new Node('#fragment'); },
  getElementById: function (id) { return (els[id] = els[id] || new Node('div')); },
  querySelector: function () { return null; },
  querySelectorAll: function () { return []; },
  addEventListener: function (t, f) { if (t === 'DOMContentLoaded') docReady = f; },
  title: '', body: new Node('body'),
};
global.window = global;
global.location = { pathname: '/index.html', hash: '', search: '', replace: function () {} };
global.history = { pushState: function () {}, replaceState: function () {} };
global.requestAnimationFrame = function (f) { return f(); };
global.setTimeout = function (f) { return f(); };
global.matchMedia = function () { return { matches: false, addEventListener: function () {}, addListener: function () {} }; };

var sitePath = path.join(ROOT, 'data', 'site.js');
if (!fs.existsSync(sitePath)) {
  console.log('SKIP: data/site.js is not generated yet (run: python3 -m msl.cli cycle --offline)');
  process.exit(0);
}
eval(fs.readFileSync(sitePath, 'utf8'));
if (!global.MSLDATA) { console.log('FAIL: data/site.js did not define window.MSLDATA'); process.exit(1); }
eval(fs.readFileSync(path.join(ROOT, 'app.js'), 'utf8'));

var pages = Object.keys(global.MSLDATA.meta ? {} : {});
pages = fs.readdirSync(ROOT).filter(function (f) { return /\.html$/.test(f); }).sort();
var bad = 0;
pages.forEach(function (p) {
  var main;
  global.document.body.setAttribute('data-page', p);
  els['main'] = new Node('div');
  delete els['nav']; delete els['hdr'];
  try {
    if (!docReady) { throw new Error('app.js never registered a DOMContentLoaded handler'); }
    docReady();
    main = els['main'];
  } catch (e) {
    bad++; console.log('THREW  ' + p + ': ' + (e && e.message ? e.message : e)); return;
  }
  var txt = main.textContent.replace(/\s+/g, ' ').trim();
  if (txt.indexOf('Render error on') >= 0) {
    bad++; console.log('ERROR  ' + p + ': ' + txt.slice(0, 220)); return;
  }
  if (main.children.length === 0) {
    bad++; console.log('BLANK  ' + p + ': #main has no children'); return;
  }
  console.log('ok     ' + p.padEnd(22) + String(main.children.length).padStart(4) + ' nodes ' +
              String(txt.length).padStart(8) + ' chars');
});
console.log(bad ? 'RENDER CHECK FAILED: ' + bad + ' page(s)' : 'RENDER CHECK PASSED: ' + pages.length + ' pages');
process.exit(bad ? 1 : 0);
