# YÖNETİCİ ÖZETİ — Ağ Trafiği Anomali Tespiti (Maksimum 5 sayfa)

## 1. Proje Kısa Özeti

Bu çalışma, kurumsal ağ trafiğinden anormallikleri tespit ederek işletme maliyetlerini minimize etmeyi amaçlayan maliyet‑duyarlı bir makine öğrenmesi çözümüdür. Projede gerçekçi normal trafik verisi (`normal_traffic.csv`) ile simüle saldırı trafiği (`attack_traffic.csv`) birleştirilmiş, IANA port/servis veritabanı ile zenginleştirme yapılmıştır. Model kararları SHAP ile açıklanabilir hâle getirilmiş; farklı karar eşiği senaryoları üzerinden maliyet‑fayda analizleri ile işletme için en uygun politika belirlenmiştir.

---

## 2. Problem ve İş Hedefi (1 paragraf)

Artan otomatik saldırılar ortamında, güvenlik operasyonlarının iki temel maliyet kalemi vardır: (i) yanlış pozitif alarmlar nedeniyle ortaya çıkan operasyonel müdahale maliyetleri; (ii) yanlış negatifler nedeniyle kaçırılan saldırıların yol açtığı olay ve veri kaybı maliyetleri. Hedefimiz, bu iki maliyeti dengeleyerek kurum için net faydayı maksimize eden bir tespit sistemi sunmaktır.

---

## 3. Veri Kaynakları ve Veri Harmanlama (Kısa, 1/2 sayfa)

- `normal_traffic.csv`: Wireshark ile kaydedilmiş normal paket akışları
- `attack_traffic.csv`: Nmap ile üretilmiş agresif tarama/saldırı simülasyonları
- `service-names-port-numbers.csv`: IANA port → servis eşlemeleri

Veri işleme adımları:
- Zaman etiketleri ve paket bilgi sütunları normalize edildi
- Regex ile hedef port çıkarıldı ve IANA ile eşlendi
- Eksik veriler temizlendi; outlier'lar incelendi
- Veri kaynakları mantıksal anahtarlara göre birleştirilip tek bir analiz seti üretildi

---

## 4. İş Mantığına Dayalı Özellik Mühendisliği (1/2 sayfa)

Bu projede ham paket sütunlarının ötesinde aşağıdaki 5 iş‑odaklı özellik üretildi (kod `main_final.ipynb` içinde):

1. **Port Kategorisi** — Hizmet sınıfı (standart, popüler, nadir) — işletme için risk önceliği sağlar.
2. **Protokol Risk Skoru** — TCP/UDP/ICMP gibi protokollerin tarihsel kötü kullanım frekansına göre ağırlıklandırılmış skor.
3. **Zaman Tabanlı Özetler** — Bir kaynak IP'nin son 1/5/15 dakikadaki paket sayısı ve ortalama inter‑packet zaman farkı.
4. **Veri Hacmi (Bytes)** — Kaynak-hedef çiftine göre taşınan toplam bayt.
5. **Bağlantı Yoğunluğu** — Aynı anda açılan bağlantı sayısı (pencere tabanlı).

Her özellik, hem modellerde açıklayıcı (predictive) hem de maliyet analizi için kullanılabilecek şekilde tasarlandı.

![Keşifçi Veri Analizi — Paket Sınıfı Dağılımı, Paket Boyutu, Zaman Farkı, Veri Yoğunluğu](file:///c:/PythonVeriBilimi/Proje/Proje1/eda_analizi.png)

---

## 5. Modelleme ve Değerlendirme (1/2 sayfa)

- Kullanılan algoritmalar: XGBoost (öncelikli), Random Forest (ikincil kontrol)
- Dengesizlik çözümü: SMOTE + sınıf ağırlıkları
- Hiper‑parametre optimizasyonu: GridSearchCV + StratifiedKFold
- Performans ölçüleri: ROC‑AUC, Precision, Recall, F1, ayrıca eşik bazlı beklenen maliyet

Modelin operasyonel seçimi, standart metriklerin ötesinde "beklenen maliyet" minimizasyonu ile yapıldı (eşik ayarı maliyet fonksiyonunu minimize edecek şekilde seçildi).

![Model Performans — Karmaşıklık Matrisi, ROC Eğrisi, Özellik Önem Derecesi](file:///c:/PythonVeriBilimi/Proje/Proje1/model_performans.png)

---

## 6. Maliyet‑Fayda Analizi (En kritik bölüm — 1 sayfa)

Yaklaşıma genel bakış:

Beklenen toplam maliyet, bir eşiğe (threshold) bağlı olarak aşağıdaki şekilde hesaplanır:

$$
E[C](t) = P_{FP}(t)\times C_{FP} + P_{FN}(t)\times C_{FN}
$$

Burada $P_{FP}(t)$ ve $P_{FN}(t)$ modelin verdiği eşikteki olasılıklardır; $C_{FP}$ = tek bir yanlış pozitif olayının maliyeti; $C_{FN}$ = tek bir yanlış negatif olayının maliyeti.

Uygulamada yapılanlar:
- Farklı $t$ değerleri için $P_{FP}$ ve $P_{FN}$ test kümesi üzerinden hesaplandı
- Kurumsal senaryolar için örnek maliyet aralıkları (parametreleştirilebilir) bırakıldı; raporda birden fazla senaryo sunuldu (konservatif, orta, agresif)
- Optimal eşiğin seçimi: en düşük $E[C](t)$ veren $t^*$ seçildi

Raporun sayısal çıktıları:
- (Tablo A) Senaryo bazlı beklenen maliyetler ve model vs. baseline karşılaştırmaları — `main_final.ipynb` içindeki "Cost-Benefit" hücreleri

Not: Akademik proje olması nedeniyle bazı gerçek işletme maliyetleri özetlenmiş ve parametreleştirilebilir bırakılmıştır. Gerçek TL değerleri kurum verileriyle kolayca güncellenebilir.

![SOC Finansal Maliyet Optimizasyonu — Eşik Bazlı Maliyet Minimizasyonu ve Precision/Recall Dengesi](file:///c:/PythonVeriBilimi/Proje/Proje1/maliyet_optimizasyonu.png)

---

## 7. Açıklanabilirlik (XAI) ve Operasyonel Güven (1/2 sayfa)

SHAP analizleri, operasyon ekibine modelin hangi feature'lara dayanarak alarm ürettiğini gösterir. Bu, aşağıdaki faydaları sağlar:

- Alarm incelemede insan güveni artışı
- Yanlış pozitiflerin kaynak özelliklerine göre hızlı politika düzeltmesi
- Sürekli izleme ile modelde drift tespitine yardımcı olur

![SHAP Açıklanabilir Yapay Zeka — Özellik Kontribüsyon Analizi ve Ortalama SHAP Değerleri](file:///c:/PythonVeriBilimi/Proje/Proje1/shap_ozeti.png)

---

## 8. Operasyonel Öneriler ve Uygulama Adımları (Kısa)

1. Pilot uygulama: Önerilen eşikte 3 aylık pilot (küçük alt ağ veya SIEM entegrasyonu)
2. İnsan+Model Hibrit Akış: Kritik alarmlar için otomatik sınıflandırma + insan onayı
3. Parametre Güncellemesi: 3 aylık canlı verilerle $C_{FP}$ / $C_{FN}$ değerlerinin revizyonu
4. İzleme: SHAP tabanlı haftalık/aylık raporlar

---

## 9. Hızlı Sonuç ve Teslimat Listesi (Kısa)

Bu proje işletmeye gerçek fayda sağlayacak şekilde tasarlanmıştır; teknik ve finansal sonuçların bulunduğu ana teslimatlar şunlardır:

- `main_final.ipynb` — tamamlanmış notebook (veri işleme, model, SHAP, maliyet analizi hücreleri)
- `normal_traffic.csv`, `attack_traffic.csv`, `service-names-port-numbers.csv` — veri kaynakları
- `PROJE_RAPORU.md` — detaylı proje raporu
- `PROJE_YONETICI_OZETI.md` — bu yönetici özeti

---

## Ek Notlar (Kullanım ve Özelleştirme)

- PDF üretimi için bu dosyayı direkt olarak Markdown → PDF araçlarıyla (ör. Pandoc, VSCode Markdown PDF eklentisi) veya Jupyter Notebook içine gömülü hücrelerle rahatça dönüştürebilirsiniz.
- Rakamlar/parametreler (ör. $C_{FP}$, $C_{FN}$) kurum verisiyle güncellenebilir; `main_final.ipynb` içinde parametre hücreleri bulunmaktadır.

---

_Hazırlayan:_ Python ile Veri Bilimi Projesi — Ağ Trafiği Anomali Tespiti (Maliyet Odaklı)

_Tarih:_ 2026

