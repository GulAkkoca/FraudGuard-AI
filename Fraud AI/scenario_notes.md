# FraudGuard AI Scenario Notes

Bu dosya, `data/products.json` icindeki mock urunlerin hangi demo amacina hizmet ettigini aciklar. Her urun rastgele degil, FraudGuard AI ajaninin farkli risk sinyallerini gostermek icin tasarlanmistir.

## Genel Analiz Katmanlari

- **Review analysis:** Yorum metinlerinde tekrar, benzer kaliplar, ayni gun yogunlugu, rating-metin uyumsuzlugu.
- **Price analysis:** Gecmis fiyatlara gore anormal indirim, yapay yukseltilmis original price, ani fiyat kirilmalari.
- **Seller analysis:** Satici puani, hesap yasi, verified durumu, iade orani.
- **Product consistency:** Urun aciklamasi ve yorumlar arasindaki celiski.
- **Final risk decision:** Dusuk, orta, sinirda veya yuksek risk kararinin birden fazla sinyalle birlestirilmesi.

## p001 - Everyday Cotton T-Shirt

**Scenario:** `low_risk`

Bu urun, sistemin guvenilir ve normal davranan urunleri de ayirt edebildigini gostermek icin hazirlandi.

Beklenen sinyaller:

- Satici dogrulanmis ve uzun sureli.
- Return rate dusuk.
- Fiyat gecmisi kademeli ve makul.
- Yorumlar cesitli, dogal ve urunle uyumlu.
- Aciklama ile yorumlar arasinda celiski yok.

Beklenen karar: **Low risk / guvenilir urun**

## p002 - Wireless Earbuds Pro X

**Scenario:** `fake_review`

Bu urun, Gemini veya LLM tabanli yorum metni analizinin gucunu gostermek icin hazirlandi.

Beklenen sinyaller:

- Birden fazla yorum ayni tarihte girilmis.
- Yorum metinleri cok benzer kaliplardan olusuyor.
- "Amazing product", "very good quality", "fast delivery" gibi tekrar eden ifadeler var.
- 5 yildizli yorumlar ile daha gercekci dusuk puanli yorum arasinda kalite farki bulunuyor.

Beklenen karar: **Fake review suspicion**

## p003 - Smart Air Fryer 6L

**Scenario:** `fake_discount`

Bu urun, rule-based fiyat anomalisi analizini gostermek icin hazirlandi.

Beklenen sinyaller:

- Fiyat gecmisi once 1500-1700 bandinda seyrederken original price aniden 4999 olarak gorunuyor.
- Current price 1299 oldugu icin indirim cok buyuk gorunuyor.
- Satici ve yorumlar genel olarak normal, bu nedenle ana risk fiyat katmanindan gelmeli.

Beklenen karar: **Fake discount suspicion**

## p004 - Luxury Leather Wallet

**Scenario:** `suspicious_seller`

Bu urun, satici kaynakli risk sinyallerini gostermek icin hazirlandi.

Beklenen sinyaller:

- Satici hesabi cok yeni.
- Verified degil.
- Rating dusuk.
- Return rate yuksek.
- Yorumlar tek basina cok sahte gorunmese de satici profili guven sorunu yaratiyor.

Beklenen karar: **Seller risk**

## p005 - Waterproof Hiking Jacket

**Scenario:** `product_inconsistency`

Bu urun, aciklama ve yorumlar arasindaki celiskiyi gostermek icin hazirlandi.

Beklenen sinyaller:

- Urun aciklamasi "fully waterproof", "sealed seams", "storm hood" iddialarini tasiyor.
- Yorumlarda su gecirme, omuz dikislerinden islanma ve kapuson sorunu belirtiliyor.
- Satici kotu degil, fiyat da cok anormal degil; risk urun iddiasi ile deneyim arasindaki farktan geliyor.

Beklenen karar: **Product inconsistency**

## p006 - Flagship Phone 15 Ultra Replica

**Scenario:** `very_high_risk`

Bu urun, tum risklerin birlestigi guclu demo senaryosu olarak hazirlandi.

Beklenen sinyaller:

- Original price ile current price arasinda asiri fark var.
- Satici cok yeni, verified degil, rating cok dusuk ve return rate cok yuksek.
- Bazi yorumlar sahte gibi tekrar eden olumlu kaliplar tasiyor.
- Diger yorumlarda IMEI, garanti, kutu ve kamera kalitesiyle ilgili ciddi supheler var.
- Urun aciklamasindaki "official warranty" ve "authentic serial number" iddialari yorumlarla celisiyor.

Beklenen karar: **Very high risk / avoid**

## p007 - Robot Vacuum Lite

**Scenario:** `medium_risk`

Bu urun, sistemin ara seviye risk kararini gostermek icin hazirlandi.

Beklenen sinyaller:

- Satici dogrulanmis ama rating ve return rate mukemmel degil.
- Fiyat indirimi makul fakat yine de izlenebilir.
- Yorumlar karisik: bazi kullanicilar memnun, bazilari navigasyon ve mop performansindan sikayetci.
- Sahte yorum sinyali baskin degil; urun performansi konusunda orta seviye risk var.

Beklenen karar: **Medium risk**

## p008 - Noise Cancelling Headphones S2

**Scenario:** `borderline`

Bu urun, Gemini'ye veya LLM analizine gonderilip gonderilmeme esigini gostermek icin hazirlandi.

Beklenen sinyaller:

- Satici yeni sayilabilir ama verified.
- Rating orta seviyede.
- Return rate biraz yuksek ama alarm seviyesinde degil.
- Iki yorum birbirine benzer, fakat tum yorum seti tamamen sahte gorunmuyor.
- Fiyat indirimi makul aralikta.

Beklenen karar: **Borderline / secondary AI review needed**

## Demo Akisi Onerisi

Demo sirasinda urunleri su sirayla gostermek anlasilir bir hikaye kurar:

1. `p001` ile sistemin her seyi riskli isaretlemedigi gosterilir.
2. `p002` ile yorum metni analizi one cikarilir.
3. `p003` ile fiyat anomalisi rule-based olarak anlatilir.
4. `p004` ile satici sinyalleri gosterilir.
5. `p005` ile aciklama-yorum celiskisi anlatilir.
6. `p007` ile orta risk karari gosterilir.
7. `p008` ile borderline/esik mantigi anlatilir.
8. `p006` ile tum risklerin birlestigi final demo yapilir.

## Beklenen Kullanici Ciktisi

Her urun icin ajan su tipte bir cevap uretmelidir:

- Guven skoru veya risk seviyesi.
- Risk nedenlerinin kisa ozeti.
- Hangi sinyallerin karari etkiledigi.
- Kullaniciya aksiyon onerisi: satin alinabilir, dikkatli olunmali, ek kontrol gerekli veya uzak durulmali.
