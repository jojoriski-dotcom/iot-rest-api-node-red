# Flow import
Import `flows.json` ke Node-RED. Flow memuat node MQTT, HTTP REST, SQLite, dan WebSocket. Pastikan package `better-sqlite3` dan `ws` di-install pada `~/.node-red` sebelum Deploy. Node function menggunakan `require()`; aktifkan `functionExternalModules` pada `settings.js` bila instalasi Node-RED Anda membatasinya, atau pindahkan modul ke konfigurasi external modules Node-RED.
