import json
import urllib.request
import urllib.error
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os

SOURCES = [
    "https://hydralinks.cloud/sources/gamebounty.json",
    "https://hydralinks.cloud/sources/tinyrepacks.json",
    "https://wkeynhk.online/ankergames.json",
    "https://hydrasources.su/freetp_games.json",
    "https://hydrasources.su/nnmclub.json",
    "https://hydralinks.cloud/sources/dyren.json",
    "https://raw.githubusercontent.com/Altansar69/Hydra-Library/refs/heads/main/hydra-skidrowreloaded/skidrow_cleaned.json",
    "https://raw.githubusercontent.com/irisihrz/json/refs/heads/main/irishub.json",
    "https://stupidlysimpletextshare.quest/77ae94fb09/pcgames.json",
    "https://raw.githubusercontent.com/Merabet4mine/merabet4mine.github.io/refs/heads/master/assets/skidrow.json",
    "https://raw.githubusercontent.com/blaidq-a/rutracker-only-portable/refs/heads/main/source.json",
    "https://raw.githubusercontent.com/sotik11/hydra-download-sources/main/data/repack-igruha.json",
    "https://raw.githubusercontent.com/vinikjkkj/game-links-collection/refs/heads/master/jsons/steamrip.json",
    "https://raw.githubusercontent.com/Smealm/hydra-launcher-stuff/refs/heads/main/hydra%20sources/FMHY/world%20of%20pc%20games/worldofpcgames.json",
    "https://raw.githubusercontent.com/BITO21/BITO_sources/refs/heads/master/GameBounty.json",
    "https://raw.githubusercontent.com/Smealm/hydra-launcher-stuff/refs/heads/main/hydra%20sources/FMHY/steam%20undergound/steamunderground.json",
    "https://cesio-138.github.io/dauphong-hydra/sources/dauphong.json",
    "https://fuck-steam.netlify.app/FONTE.json",
    "https://ggvv13.github.io/Linux-Games.json",
    "https://hydrasources.su/thelastgame.json",
    "https://raw.githubusercontent.com/sotik11/hydra-download-sources/main/data/itorrents-igruha.json",
    "https://raw.githubusercontent.com/vinikjkkj/game-links-collection/refs/heads/master/jsons/fitgirl.json",
    "https://raw.githubusercontent.com/sotik11/hydra-download-sources/main/data/rutor.json",
    "https://raw.githubusercontent.com/Gabihhz/ddlc-ptbr-fonte/main/fonte.json?v=55",
    "https://gist.githubusercontent.com/SawwyReis/8ec9011acc87b101c355636a320f4172/raw/690950e58ed51ee9d1ad077467a26c810da77b40/SukiH.json",
    "https://raw.githubusercontent.com/L1MSpace/hydra-sources-byrutgame/refs/heads/main/games_500pages_byrutgame.json",
    "https://vxvulgooficial.github.io/vxvulgooficial/vxvulgo.json",
    "https://gitlab.com/BadKiko/freetp-hydra-link/-/raw/main/games.json",
    "https://raw.githubusercontent.com/Altansar69/Hydra-Library/refs/heads/main/hydra-gamestorrents/gamestorrents.json",
    "https://gitlab.com/h4rq/linuxrulez-hydra-h4rqqqq11/-/raw/main/linuxrulez_hydra.json",
    "https://nexusbuildcompany.github.io/nexus.json",
    "https://gist.githubusercontent.com/sebastian-morgan/a1e9d5db55bb8646d0278384f3dd3a2f/raw/fbc5b6f2aa92e1067d067ae2e49faadec5f68964/backup.json",
    "https://raw.githubusercontent.com/BITO21/BITO_sources/refs/heads/master/Updates.json",
    "https://hydralinks.pages.dev/sources/atop-games.json",
    "https://gist.githubusercontent.com/sebastian-morgan/4b7bedd9fe5290715d2d95be4283740d/raw/46e621a48ab73be2203ea60977635f5f73a462b9/hub.json",
    "https://raw.githubusercontent.com/BITO21/BITO_sources/refs/heads/master/GameDrive.json"
]

def fetch_source(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            raw_data = response.read().decode('utf-8', errors='ignore')
            data = json.loads(raw_data)
            
            downloads = []
            source_name = url.split("/")[-1]
            
            if isinstance(data, dict):
                source_name = data.get("name", source_name)
                if "downloads" in data and isinstance(data["downloads"], list):
                    downloads = data["downloads"]
                elif "games" in data and isinstance(data["games"], list):
                    downloads = data["games"]
                else:
                    for val in data.values():
                        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict) and ("title" in val[0] or "uris" in val[0]):
                            downloads = val
                            break
            elif isinstance(data, list):
                downloads = data
                
            return {
                "url": url,
                "status": "success",
                "name": source_name,
                "count": len(downloads),
                "downloads": downloads,
                "error": None
            }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "name": url.split("/")[-1],
            "count": 0,
            "downloads": [],
            "error": str(e)
        }

def main():
    print(f"Buscando atualizacoes de {len(SOURCES)} fontes...")
    results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_source, url): url for url in SOURCES}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res["status"] == "success":
                print(f"[OK] {res['name']} ({res['count']} itens)")
            else:
                print(f"[FAIL] {res['url']} -> {res['error']}")
                
    all_clean = []
    seen = set()
    total_raw = 0
    
    for res in results:
        total_raw += res["count"]
        for item in res["downloads"]:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title", "")).strip()
            raw_uris = item.get("uris", [])
            if isinstance(raw_uris, str):
                raw_uris = [raw_uris]
            elif not isinstance(raw_uris, list):
                raw_uris = []
                
            uris = [str(u).strip() for u in raw_uris if str(u).strip() and (str(u).startswith("http") or str(u).startswith("magnet:"))]
            if not title or not uris:
                continue
                
            sig = (title.lower(), tuple(sorted(uris)))
            if sig in seen:
                continue
            seen.add(sig)
            
            upload_date = str(item.get("uploadDate") or "2024-01-01T00:00:00.000Z")
            file_size = str(item.get("fileSize") or "N/A")
            
            all_clean.append({
                "title": title,
                "uris": uris,
                "uploadDate": upload_date,
                "fileSize": file_size
            })
            
    print(f"Total bruto: {total_raw} | Limpos e desduplicados: {len(all_clean)}")
    
    # Ordenar pelos mais recentes para garantir que jogos novos fiquem priorizados
    all_clean.sort(key=lambda x: x.get("uploadDate", ""), reverse=True)
    
    # Limitar aos 80.000 títulos para respeitar o limite de tamanho e timeout da API do Hydra (~28 MB)
    max_games = 80000
    curated = all_clean[:max_games]
    
    payload = {
        "name": "Mega Hydra Source (Auto-Updated)",
        "downloads": curated
    }
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "mega_source.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(',', ':'), ensure_ascii=False)
        
    print(f"Salvo com sucesso em {out_file}: {len(curated)} jogos ({os.path.getsize(out_file)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()
