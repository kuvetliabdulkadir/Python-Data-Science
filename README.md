# Ağ Trafiği Anomali Tespiti — Maliyet Odaklı Siber Güvenlik Modeli

Python ile Veri Bilimi dersi final projesi. Wireshark ağ trafiği verisi ile IANA port veritabanı birleştirilerek XGBoost tabanlı bir anomali tespit modeli geliştirilmiş; karar eşiği finansal olarak optimize edilmiştir.

## Proje Özeti

| | |
|---|---|
| Toplam Paket | 64.910 (Normal: %94.4 / Saldırı: %5.6) |
| Model | XGBoost (AUC: 0.825, Accuracy: %86.9) |
| Yöntem | Data Fusion + Özellik Mühendisliği + Eşik Optimizasyonu |
| Net Tasarruf | 88.965 TL (test seti, eşik %50 → %34) |

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `main_final.ipynb` | Ana notebook — veri işleme, model, SHAP, finansal simülasyon |
| `normal_traffic.csv` | Wireshark normal trafik verisi |
| `attack_traffic.csv` | Wireshark saldırı (Nmap) verisi |
| `service-names-port-numbers.csv` | IANA port veritabanı |
| `requirements.txt` | Gerekli kütüphaneler |

## Kurulum

```bash
pip install -r requirements.txt
jupyter notebook main_final.ipynb
```

## Yöntem

1. **Data Fusion** — Wireshark trafiği + IANA tehdit istihbaratı (%71.9 eşleşme)
2. **Özellik Mühendisliği** — 5 yeni davranışsal özellik (Time_Diff, Bytes_Per_Sec vb.)
3. **Model** — XGBoost vs Random Forest karşılaştırması, under-sampling ile denge
4. **Finansal Optimizasyon** — KVKK maliyet modeli ile eşik optimizasyonu
5. **SHAP** — Açıklanabilir YZ analizi (Dst_Port, Length, Protocol_Enc önde)

---

* [Abdulkadir Kuvetli](https://kuvetliabdulkadir.com)
