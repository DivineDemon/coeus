# Cloudflare Infrastructure & Domain Management

> **DNS Provider**: Cloudflare
> **Primary Domain**: `mushoodhanif.com`

---

## Registered Subdomains & Status

### Active / Working
- `mushoodhanif.com` — Personal Portfolio Website
- `haga.mushoodhanif.com` — Haga Main Site (`haga-web.pages.dev`)
- `dataroom.mushoodhanif.com` — Haga Dataroom (`haga-dataroom.pages.dev`)
- `sv.mushoodhanif.com` — Hostinger VPS IP (`195.35.25.162`) *(DNS Only)*
- `cool.sv.mushoodhanif.com` — Coolify Server on Hostinger VPS *(DNS Only)*
- `cockpit.sv.mushoodhanif.com` — Rocky Linux Cockpit Panel *(DNS Only)*
- `self8n.sv.mushoodhanif.com` — Self-hosted n8n *(DNS Only)*

---

## Zone Export Summary (`mushoodhanif.com`)

```dns
;; SOA Record
mushoodhanif.com.	3600	IN	SOA	dawn.ns.cloudflare.com. dns.cloudflare.com. 2053716757 10000 2400 604800 3600

;; NS Records
mushoodhanif.com.	86400	IN	NS	dawn.ns.cloudflare.com.
mushoodhanif.com.	86400	IN	NS	owen.ns.cloudflare.com.

;; A Records
cockpit.sv.mushoodhanif.com.	1	IN	A	195.35.25.162 ; cf_tags=cf-proxied:false
cool.sv.mushoodhanif.com.	1	IN	A	195.35.25.162 ; cf_tags=cf-proxied:false
self8n.sv.mushoodhanif.com.	1	IN	A	195.35.25.162 ; cf_tags=cf-proxied:false
sv.mushoodhanif.com.	1	IN	A	195.35.25.162 ; cf_tags=cf-proxied:false

;; CAA Records
mushoodhanif.com.	1	IN	CAA	0 issue "sectigo.com"
mushoodhanif.com.	1	IN	CAA	0 issue "pki.goog"
mushoodhanif.com.	1	IN	CAA	0 issue "letsencrypt.org"

;; CNAME Records
dataroom.mushoodhanif.com.	1	IN	CNAME	haga-dataroom.pages.dev. ; cf_tags=cf-proxied:true
haga.mushoodhanif.com.	1	IN	CNAME	haga-web.pages.dev. ; cf_tags=cf-proxied:true

;; MX Records
mushoodhanif.com.	1	IN	MX	10 inbound-smtp.ap-northeast-1.amazonaws.com.
send.mushoodhanif.com.	1	IN	MX	10 feedback-smtp.ap-northeast-1.amazonses.com.

;; TXT Records
_dmarc.mushoodhanif.com.	1	IN	TXT	"v=DMARC1; p=none;"
mushoodhanif.com.	1	IN	TXT	"google-site-verification=2QBV9ctO2_bdoJfLUchgPXIjtkdcKof8SaOJYmSRh1U"
resend._domainkey.mushoodhanif.com.	1	IN	TXT	"p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+zL3q5dkAc52bJ/kHIPSLctSqv96BBDN7CgjEf1099imnuocr4DKudnCRl08qRNMaNL8CYDnur8F6GaCVFXy3umb89tbQ/H44Y+E8lee6j5xAfjcUG3wvcs9PJ1+zih2pAH2cmE2ldPUaeehRycbF93eSivSRTOKv+/OC43d6gwIDAQAB"
send.mushoodhanif.com.	1	IN	TXT	"v=spf1 include:amazonses.com ~all"
```
