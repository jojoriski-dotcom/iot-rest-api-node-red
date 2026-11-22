# IoT REST API & Web Dashboard (Node-RED)

Proyek praktikum Pertemuan 9: ESP32/MQTT → Node-RED REST API → custom dashboard.

## Fitur pengembangan
- `GET /api/suhu`, `GET /api/history`, `POST /api/kontrol`
- `PUT /api/threshold` untuk batas suhu dan notifikasi browser/WebSocket
- Grafik real-time Chart.js
- API key melalui `X-API-Key`
- WebSocket push update (tanpa polling)
- SQLite untuk history permanen
- Simulator ESP32 Python untuk pengujian tanpa perangkat fisik

## Persyaratan
- Node.js 18+ dan Node-RED
- Mosquitto (atau broker MQTT kompatibel) pada `localhost:1883`
- Python 3.10+ untuk simulator

## Instalasi
1. Pasang dependensi di folder Node-RED user directory:
   ```bash
   cd ~/.node-red
   npm install better-sqlite3 ws
   ```
   `ws` sudah menjadi dependency di Node-RED pada instalasi umum; pasang bila diperlukan.
2. Salin `settings.js.example` sebagai referensi konfigurasi. Untuk WebSocket, tambahkan instance HTTP server Node-RED ke functionGlobalContext (lihat bagian WebSocket di bawah). Aktifkan `httpStatic` ke folder `public` pada settings.js Node-RED, misalnya:
   ```js
   httpStatic: '/absolute/path/to/iot-rest-api-node-red/public',
   ```
3. Atur environment variable `IOT_API_KEY` pada proses Node-RED. Contoh Windows PowerShell:
   ```powershell
   $env:IOT_API_KEY='ganti-dengan-kunci-rahasia'
   node-red
   ```
   Linux/macOS:
   ```bash
   export IOT_API_KEY='ganti-dengan-kunci-rahasia'
   node-red
   ```
4. Import `flows/flows.json` ke Node-RED (Menu → Import).
5. Pastikan konfigurasi MQTT `localhost:1883`, lalu Deploy.
6. Buka `http://localhost:1880/dashboard/`.
7. Masukkan API key yang sama pada kolom dashboard. API key disimpan di `sessionStorage` selama tab terbuka.
8. Jalankan simulator:
   ```bash
   cd simulator
   python -m pip install -r requirements.txt
   python simulator.py
   ```

## Endpoint
Semua endpoint `/api/*` memerlukan header `X-API-Key`.

| Method | Endpoint | Kegunaan |
|---|---|---|
| GET | `/api/suhu` | Data sensor terbaru |
| GET | `/api/history?limit=50` | Riwayat dari SQLite |
| POST | `/api/kontrol` | Publish kontrol MQTT; body `{"device":"lamp","action":"on"}` |
| PUT | `/api/threshold` | Set batas suhu; body `{"temperature":30}` |
| GET | `/api/threshold` | Baca batas suhu aktif |

WebSocket tersedia di `ws://localhost:1880/ws/sensor?apiKey=...`. API key via query string khusus handshake WebSocket karena browser WebSocket API tidak mendukung custom header. Untuk deployment publik gunakan HTTPS/WSS dan reverse proxy; hindari menyimpan API key dalam source code.

## Topik MQTT
- Sensor: `iot/sensor` dengan JSON `{"suhu":28.5,"kelembaban":65.2,"timestamp":"..."}`
- Kontrol: `iot/kontrol`

## Notifikasi batas suhu
Ketika pembacaan suhu lebih besar dari threshold, backend mengirim event `threshold_exceeded` melalui WebSocket. Dashboard menampilkan notifikasi browser (setelah izin diberikan) dan pesan peringatan pada panel.

## Catatan konfigurasi Node-RED
Flow menggunakan `better-sqlite3` dan `ws` yang dimuat dari Node-RED user directory (`~/.node-red/node_modules`). Bila Node-RED dijalankan sebagai service, pastikan environment variable dan hak akses folder database tersedia. Database dibuat otomatis di `~/.node-red/iot-history.sqlite`.

## Uji cepat API
```bash
curl -H "X-API-Key: ganti-dengan-kunci-rahasia" http://localhost:1880/api/suhu
curl -X PUT http://localhost:1880/api/threshold -H "X-API-Key: ganti-dengan-kunci-rahasia" -H "Content-Type: application/json" -d '{"temperature":30}'
```

## Struktur
- `flows/flows.json` — flow Node-RED untuk MQTT, SQLite, REST, WebSocket
- `public/index.html` — dashboard Chart.js
- `simulator/` — simulator publisher MQTT
- `settings.js.example` — contoh konfigurasi static directory
