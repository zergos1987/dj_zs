"use strict";

let app_settings = JSON.parse(document.getElementById('app').getAttribute('app_settings').replaceAll(`'`, `"`));
console.log("app_settings", app_settings);

document.querySelector('head > title').textContent = app_settings.app.name;
