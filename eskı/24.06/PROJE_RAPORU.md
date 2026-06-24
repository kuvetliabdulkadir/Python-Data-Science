# Ağ Trafiği Anomali Tespiti — Maliyet Odaklı Siber Güvenlik Modeli

## Proje Özeti

Bu proje, **makine öğrenmesi** ve **iş analitiği** kullanarak ağ trafiğinden saldırıları otomatik olarak tespit eden bir sistemdir. Projenin amacı, siber güvenlik ekiplerine **gerçek tehditler ile yanlış alarmlar arasında akıllıca ayırım yaparak işletme maliyetlerini optimize etmek**tir.

---

## 1. Veri Seti

### Veri Kaynağı
- **Normal Trafik**: Kendi ağından Wireshark ile yakalanan normal ağ aktiviteleri
- **Agresif Trafik**: Nmap port tarama aracı kullanılarak üretilen agresif/saldırı simülasyonları
- **Format**: CSV dosyaları olarak işlenmiş Wireshark paket verileri

### Veri Zenginleştirmesi
Wireshark paket verilerine, **IANA resmi port/servis veritabanı** entegre edilerek:
- Her porta karşılık gelen hizmet adı eklendi
- Protokol kategorileri belirlendi
- Potansiyel tehdit seviyelerine göre risk skorları atandı

---

## 2. Temel Amaçlar

### 🔗 Veri Birleştirme (Data Fusion)
- Normal ve saldırı trafiği CSV dosyalarını birleştirildi
- IANA resmi port/servis veritabanıyla harmanlama yapıldı
- Tehdit istihbaratı bilgileri entegre edildi

### ⚙️ Özellik Mühendisliği (Feature Engineering)
5 yeni finansal ve güvenlik özelliği oluşturuldu:
1. **Port Kategorisi**: Standart portlar (SSH, HTTP, DNS) vs. anormal portlar
2. **Protokol Risk Skoru**: TCP/UDP/ICMP gibi protokollerin risk değerlendirmesi
3. **Zaman Tabanlı Özellikler**: Paket gönderme sıklığı ve işlem başına ortalama zaman farkları
4. **Veri Hacimleri**: Kaynak-hedef IP ikilisi başına aktarılan toplam byte miktarı
5. **Bağlantı Yoğunluğu**: Belirli bir zaman penceresinde eşzamanlı bağlantı sayısı

### 🤖 Model Eğitimi ve Optimizasyon
- **Modeller**: XGBoost ve Random Forest algoritmaları kullanılarak saldırı tespiti
- **Sınıf Dengesizliği**: SMOTE (Synthetic Minority Over-sampling Technique) ve ağırlıklı sınıf dengeleme uygulandı
- **Hiperparametre Optimizasyonu**: GridSearchCV ile optimal parametreler bulundu
- **Cross-Validation**: StratifiedKFold ile güvenilir performans değerlendirmesi

### 💰 Maliyet-Fayda Analizi (Cost-Sensitive Analytics)
**Bu projede en önemli bileşen:**
- **Yanlış Pozitif Maliyeti**: Hatalı alarm için yapılan gereksiz müdahale ve insan gücü maliyeti
- **Yanlış Negatif Maliyeti**: Gerçek saldırının kaçırılması ve olası veri ihlali maliyeti
- **Finansal Simülasyon**: Farklı karar eşiğinde sistemi analiz ederek en optimal sınıflandırma eşiği belirlenmiş
- **ROI Maksimizasyonu**: İşletmeye maksimum fayda sağlayan model ayarlanmış

### 📊 Açıklanabilir Yapay Zeka (Explainable AI)
- **SHAP (SHapley Additive exPlanations)** kütüphanesi kullanıldı
- Her tahmin için hangi özelliklerin karar üzerinde etkili olduğu görselleştirilmiş
- Siber güvenlik ekibinin modeli güvenmesi ve sonuçları anlaması sağlandı

---

## 3. Çıktılar ve Faydaları

### 📌 Ne İşe Yarar?

1. **Otomatik Anomali Tespiti**
   - Ağ trafiğindeki anormal etkinlikleri gerçek zamanda tanımlar
   - İnsan ekibin manuel izlem yükünü azaltır

2. **Akıllı Tehdit Değerlendirmesi**
   - Siber güvenlik ekiplerine **gerçek tehditler vs. yanlış alarmları** ayırt etmesine yardımcı olur
   - Operasyonel verimliliği artırır

3. **İş Odaklı Karar Alma**
   - Teknik güvenlik metrikleri işletme maliyetleriyle dengelenir
   - Optimum sınıflandırma eşiği belirlerek **ROI maksimize** edilir
   - Güvenlik ve operasyon maliyet dengesinin sağlanması

4. **Şeffaflık ve Güven**
   - SHAP analizleriyle modelin kararları açıklanır
   - Siber güvenlik profesyonelleri algoritmanın mantığını anlayabilir

---

## 4. Metodoloji

### Veri İşleme Adımları
```
Wireshark CSV Dosyaları 
    ↓
Regex ile Port Çıkarma + IANA Mapping
    ↓
Eksik Değer İşleme ve Veri Temizleme
    ↓
Özellik Mühendisliği (5 Yeni Özellik)
    ↓
Sınıf Dengesizliği Çözme (SMOTE)
    ↓
Train/Test Split (Stratified)
```

### Model Eğitimi
```
Eğitim Veri Seti
    ↓
GridSearchCV + StratifiedKFold
    ↓
XGBoost ve Random Forest Modelleri
    ↓
Performans Değerlendirmesi (ROC-AUC, F1, Precision, Recall)
    ↓
Maliyet-Fayda Analizi ile Eşik Optimizasyonu
```

### Değerlendirme Metrikleri
- **Accuracy (Doğruluk)**: Genel sınıflandırma performansı
- **Precision (Hassasiyet)**: Yanlış pozitif alarmı minimize etme
- **Recall (Duyarlılık)**: Gerçek saldırıları yakalama oranı
- **F1-Score**: Precision ve Recall'un dengeli ortalaması
- **ROC-AUC**: Farklı eşiklerde modelin performansı
- **Maliyet Matrisi**: Yanlış pozitif vs. yanlış negatif maliyetler

---

## 5. Beklenen Katkılar

✅ **Akademik Katkı**
- Veri bilimi ve makine öğrenme tekniklerinin siber güvenliğe uygulanması
- Maliyet-duyarlı sınıflandırma (Cost-Sensitive Classification) örneği
- Açıklanabilir yapay zeka (XAI) pratik implementasyonu

✅ **Endüstriyel Katkı**
- Gerçek ağ verisi kullanarak pratik bir anomali tespit sistemi
- İşletmeler için operasyonel olarak uygulanabilir çözüm
- Siber güvenlik ve iş analitikleri arasında köprü kurma

---

## 6. Teknik Stack

| Bileşen | Teknoloji |
|---------|-----------|
| **Veri İşleme** | Pandas, NumPy |
| **Makine Öğrenmesi** | XGBoost, Scikit-learn, Random Forest |
| **Görselleştirme** | Matplotlib, Seaborn |
| **Açıklanabilirlik** | SHAP |
| **Geliştirme Ortamı** | Python, Jupyter Notebook |

---

## 7. Proje Dosyaları

```
Proje1/
├── normal_traffic.csv          # Normal ağ trafiği verisi
├── attack_traffic.csv          # Agresif/saldırı trafiği verisi
├── service-names-port-numbers.csv  # IANA port veritabanı
├── main_final.ipynb            # Ana analiz ve model eğitimi notebook
├── requirements.txt            # Python bağımlılıkları
└── PROJE_RAPORU.md            # Bu dosya
```

---

## Sonuç

Bu proje, **veri bilimi, makine öğrenmesi ve siber güvenlik** nin kesiştiği önemli bir alanda çalışmaktadır. Teknik olarak sofistike bir anomali tespit modeli sunurken, aynı zamanda **işletme maliyetlerini optimize etme** hedefini de taşımaktadır. Böylece, sadece teknik bir çözüm değil, **gerçek dünyada uygulanabilir ve maliyeti hesaplayan bir sistem** ortaya çıkmıştır.

---

**Hazırlayan**: Python ile Veri Bilimi Projesi  
**Tema**: Cost-Sensitive Analitik  
**Tarih**: 2026
