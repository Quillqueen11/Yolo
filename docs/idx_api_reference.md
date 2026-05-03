# IDX API Reference

## Working Endpoints (confirmed 200 OK)

| Endpoint | Method | Params | Description |
|----------|--------|--------|-------------|
| `/primary/home/content` | GET | - | Home banners & content |
| `/primary/TradingSummary/GetIndexSummary` | GET | `length=N&start=N&DateFrom=YYYY-MM-DD&DateTo=YYYY-MM-DD&IndexCode=CODE` | Index summary (45 indices) |
| `/primary/TradingSummary/GetStockSummary` | GET | `length=N&start=N` | All stock daily summaries (959 stocks, DataTables format) |
| `/primary/TradingSummary/GetBrokerSummary` | GET | `length=N&start=N` | Broker trading summary (88 brokers) |
| `/primary/NewsAnnouncement/GetAllAnnouncement` | GET | `pageSize=N&pageNumber=N&kodeEmiten=CODE` | All disclosures (245K+ items, camelCase) |
| `/primary/newsannouncement/getAllAnnouncement` | GET | `pageSize=N&pageNumber=N&kodeEmiten=CODE` | Same endpoint, lowercase (alias) |
| `/primary/ListedCompany/GetCompanyProfiles` | GET | `start=N&length=N` | All listed companies |
| `/primary/ListedCompany/GetCompanyProfilesDetail` | GET | `KodeEmiten=CODE&language=id-id` | Company profile detail (direksi, komisaris, dividen, etc) |
| `/primary/ListedCompany/GetAnnouncement` | GET | `start=N&length=N&kodeEmiten=CODE` | Company-specific announcements (currently returns 0) |

## Response Formats

### DataTables Format (Index/Summary/Broker)
```json
{"draw": 0, "recordsTotal": N, "recordsFiltered": N, "data": [...]}
```

### Pagination Format (NewsAnnouncement)
```json
{"Items": [...], "ItemCount": N, "PageSize": N, "PageNumber": N, "PageCount": N}
```

### Company Profile Detail Format
```json
{"ResultCount": 1, "Profiles": [...], "Sekretaris": [...], "Direktur": [...], "Komisaris": [...], "PemegangSaham": [...], "Dividen": [...], "BondsAndSukuk": [...]}
```

## Always 503 Endpoints (broken)
- `/primary/news/getNews`
- `/primary/News/GetNews`
- `/primary/NewsAnnouncement/GetNews`
- `/primary/announcement/GetAnnouncementStock`
- `/primary/Announcement/GetAnnouncementStock`
- `/primary/CorporateAction/GetAnnouncementStock`
- `/primary/keterbukaan/GetKeterbukaanInformasi`
- `/primary/Stock/GetStockHistory`
- `/primary/StockHistory/GetHistory`
- `/primary/broker/searchBroker`
- `/primary/Sector/*`
- `/primary/IPO/*`
- `/primary/Market/*`

## Key Discoveries
- `kodeEmiten=` (empty) returns ALL items
- `pageSize` + `pageNumber` required for NewsAnnouncement pagination
- `length` + `start` required for DataTables format (IndexSummary, StockSummary)
- `curl_cffi` with `impersonate="chrome"` bypasses Cloudflare for all working endpoints
- No browser needed for all working endpoints
