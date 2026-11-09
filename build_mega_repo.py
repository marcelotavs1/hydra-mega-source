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
            source_name = "Unknown"
            
            if isinstance(data, dict):
                source_name = data.get("name", url.split("/")[-1])
                if "downloads" in data and isinstance(data["downloads"], list):
                    downloads = data["downloads"]
                elif "games" in data and isinstance(data["games"], list):
                    downloads = data["games"]
                else:
                    # Check if there is any list of items
                    for val in data.values():
                        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict) and ("title" in val[0] or "uris" in val[0]):
                            downloads = val
                            break
            elif isinstance(data, list):
                source_name = url.split("/")[-1]
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
    print(f"Iniciando download de {len(SOURCES)} fontes...")
    results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_source, url): url for url in SOURCES}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res["status"] == "success":
                print(f"[OK] {res['name']} ({res['count']} itens) - {res['url']}")
            else:
                print(f"[ERRO] {res['url']} -> {res['error']}")
                
    # Consolidar
    all_downloads = []
    seen_signatures = set()
    total_raw = 0
    
    for res in results:
        total_raw += res["count"]
        source_label = res["name"]
        for item in res["downloads"]:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title", "")).strip()
            uris = item.get("uris", [])
            
            # Garantir formato de uris como lista de strings
            if isinstance(uris, str):
                uris = [uris]
            elif not isinstance(uris, list):
                uris = []
                
            # Assinatura de desduplicação exata (mesmo título + primeiras URIs)
            uris_sig = tuple(sorted([str(u) for u in uris]))
            item_sig = (title.lower(), uris_sig)
            
            if item_sig in seen_signatures:
                continue
            seen_signatures.add(item_sig)
            
            # Anotar ou manter campos
            cleaned_item = dict(item)
            cleaned_item["uris"] = uris
            if "title" not in cleaned_item or not cleaned_item["title"]:
                cleaned_item["title"] = title or "Unknown Game"
                
            all_downloads.append(cleaned_item)
            
    print("\n" + "="*50)
    print(f"Fontes processadas: {len(results)}")
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    print(f"Sucessos: {len(successful)} | Falhas: {len(failed)}")
    print(f"Total bruto de downloads encontrados: {total_raw}")
    print(f"Total apos deduplicacao: {len(all_downloads)}")
    print("="*50)
    
    mega_repo = {
        "name": "Mega Hydra Source (Unificada)",
        "description": f"Mega repositorio unificado com {len(successful)} fontes do Hydra Launcher.",
        "updatedAt": datetime.utcnow().isoformat() + "Z",
        "sourcesCount": len(successful),
        "downloadsCount": len(all_downloads),
        "sources": [
            {
                "name": r["name"],
                "url": r["url"],
                "count": r["count"]
            } for r in successful
        ],
        "downloads": all_downloads
    }
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, "mega_source.json")
    min_json_path = os.path.join(output_dir, "mega_source.min.json")
    summary_path = os.path.join(output_dir, "summary.json")
    
    print(f"Salvando {json_path}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(mega_repo, f, ensure_ascii=False, indent=2)
        
    print(f"Salvando {min_json_path} (compacto)...")
    with open(min_json_path, "w", encoding="utf-8") as f:
        json.dump(mega_repo, f, ensure_ascii=False, separators=(',', ':'))
        
    # Salvar resumo de status
    with open(summary_path, "w", encoding="utf-8") as f:
        summary = {
            "total_sources": len(SOURCES),
            "successful_sources": len(successful),
            "failed_sources": len(failed),
            "total_items_raw": total_raw,
            "total_items_dedup": len(all_downloads),
            "successful": [
                {"name": r["name"], "url": r["url"], "count": r["count"]}
                for r in successful
            ],
            "failed": [
                {"url": r["url"], "error": r["error"]}
                for r in failed
            ]
        }
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Concluido com sucesso!")

if __name__ == "__main__":
    main()
