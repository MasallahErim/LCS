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