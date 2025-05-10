# Lounge Comment System 🗨️

Gerçek zamanlı müşteri yorumlarını Kafka, Redis, gRPC ve PostgreSQL kullanarak işleyen, analiz eden ve sunan bir mikroservis mimarisi.

---


## 🎯 Genel Bakış

Lounge Restoran için günlük yüzlerce müşteri yorumu gerçek zamanlı olarak işlenir. Bu sistem, aşağıdaki işlevleri üstlenir:

- Hugging Face modeli ile yorum üretir  
- Kafka ile `raw-comments` topic’ine gönderir  
- `Consumer` tarafından alınan yorumlar:
  - Duplicate & cache kontrolünden geçer  
  - gRPC üzerinden duygu analizi yapılır  
  - `processed-comments` topic’ine publish edilir  
  - PostgreSQL’e kalıcı olarak kaydedilir  
- Redis ile iki katmanlı cache uygulanır  
- Flask tabanlı REST API ile sorgulama yapılabilir  

---

## ⚙️ Özellikler

- **Domain-Driven Design**: `domains/`, `application/`, `infrastructure/`, `presentation/`
- **Kafka**:
  - `raw-comments`: Ham yorumlar  
  - `processed-comments`: Analiz edilmiş yorumlar  
- **gRPC**:
  - Duygu analizi servisi 
- **Redis Cache**:
  - Text-bazlı sentiment önbelleği  
  - Yorum-ID ile duplicate kontrolü  
- **PostgreSQL**: Kalıcı veri kaydı  
- **Flask REST API**: `/comments` endpoint'i  
- **Docker & Compose**: Servislerin tam konteynerleşmesi  
- **Logging**: Console + dosya loglama  

---

## 🔄 Mimari Akış

[Producer]
│
▼
Kafka (raw-comments topic)
│
▼
[Consumer] ──> Redis (text & ID cache)
│
▼
[gRPC Sentiment Service]
│
├──> Kafka (processed-comments topic)
└──> PostgreSQL (kalıcı veri)
│
▼

----
## 🗂️ Dosya Yapısı



```plaintext
lounge-comment-system/
├── docker-compose.yml        # Tüm altyapı servisi tanımları
├── .env                      # Ortam değişkenleri
├── requirements.txt          # Python bağımlılıkları
├── src/
│   ├── presentation/
│   │   ├── cli/              # Producer & Consumer CLI
│   │   └── api/              # Flask REST API
│   ├── application/          # Use-case’ler ve DTO'lar
│   ├── domains/              # Entity ve servis arayüzleri
│   ├── infrastructure/
│   │   ├── kafka/            # Kafka adapter’ları
│   │   ├── grpc/             # gRPC client/server
│   │   ├── db/               # PostgreSQL repository
│   │   ├── cache/            # Redis adapter
│   │   ├── logging/          # Ortak loglama sistemi
│   │   └── comment_generation/  # HuggingFace yorum üretimi
│   └── config.py             # Konfigürasyon sınıfı


| Servis      | Açıklama                                    |
| ----------- | ------------------------------------------- |
| `zookeeper` | Kafka koordinasyon hizmeti                  |
| `kafka`     | Mesajlaşma altyapısı                        |
| `postgres`  | Kalıcı veri deposu                          |
| `redis`     | Hızlı önbellek                              |
| `sentiment` | gRPC servisi üzerinden analiz               |
| `producer`  | Yorum üretip `raw-comments` topic'ine yazar |
| `consumer`  | Kafka → analiz → PostgreSQL + Kafka         |
| `api`       | Flask ile REST API sunar                    |


---

## ⚙️ Docker ile Başlatma

Tüm servisleri başlatmak için:

```bash
docker-compose up -d --build
docker-compose up -d

## 🌐 REST API Kullanımı

Flask tabanlı REST API ile işlenmiş yorumları sorgulayabilirsiniz.

### 1. Tüm yorumları çekmek

**GET** `http://localhost:8000/comments?limit=10`



### 2. Sadece `POSITIVE` yorumları çekmek

**GET** `http://localhost:8000/comments?sentiment=POSITIVE`

- `sentiment` parametresi `POSITIVE`, `NEGATIVE` veya `NEUTRAL` olabilir.
- Belirtilen duygu etiketine sahip yorumları döner.
 
### Örnek Çıktılar 
[
    {
        "commentId": "044b472c-9ead-4b77-8826-5b93cdf50d57",
        "sentiment": "NEUTRAL",
        "text": "Thitable.\"\n\nThe issue first surfaced last month when then-premie \"",
        "timestamp": "Sat, 10 May 2025 14:02:43 GMT"
    },
    {
        "commentId": "5ad1dee1-ed3a-4b88-8080-05b94f70887d",
        "sentiment": "POSITIVE",
        "text": "The federal NDP promised tement saying, \"",
        "timestamp": "Sat, 10 May 2025 14:02:45 GMT"
    }
]
