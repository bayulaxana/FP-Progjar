# FP-Progjar

## How to Run

Jalankan saja file **load_balancer.py**. Secara default akan aktif pada port 45100 atau menggunakan argumen

```
$ python3 load_balancer.py [port]
```

Terdapat satu worker yang bekerja pada port 8887. Worker akan bertambah secara otomatis secara incremental.

## Testing

Buka browser dan akses `http://127.0.0.1/test.html`, lalu lihat pada konsol anda.

> **NOTE**: Program ini ditujukan untuk OS **Linux** bukan Windows :)