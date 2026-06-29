"""
Near Tools - Discord Multi-Tool
By Near | pas abuser !
"""
import os, sys, json, time, random, string
from pathlib import Path

try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
    from rich.live import Live
    from rich import box
except ImportError:
    print("[!] Il manque des dépendances. Lance NearTools-Setup.bat pour tout installer.")
    sys.exit(1)

console = Console()

# === Stockage local ===
STORAGE = Path(os.environ.get("APPDATA", os.path.expanduser("~"))) / "NearTools"
STORAGE.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = STORAGE / "token.dat"
WH_FILE = STORAGE / "webhook.dat"

# === Palette de couleurs (mauve/rose) ===
C = {
    "p1": "#ffb6d9", "p2": "#f0a0dc", "p3": "#dc8ce1",
    "p4": "#c878e6", "p5": "#b464e1", "p6": "#a050d7",
    "pink": "#ff6dc4", "purple": "#c864e6",
    "wh": "#ffffff", "gr": "#aaaabe", "dg": "#6e6e82",
    "rd": "#ff5a78", "gn": "#82e6a0", "yl": "#ffdc82",
}

BANNER = r"""
    ███╗   ██╗███████╗ █████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ████╗  ██║██╔════╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██╔██╗ ██║█████╗  ███████║██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
    ██║╚██╗██║██╔══╝  ██╔══██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║ ╚████║███████╗██║  ██║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""


def gradient_text(text: str, colors: list[str]) -> Text:
    """Applique un dégradé multi-couleur ligne par ligne."""
    t = Text()
    lines = text.splitlines()
    n = len(colors)
    non_empty = [l for l in lines if l.strip()]
    for line in lines:
        if not line.strip():
            t.append(line + "\n")
            continue
        idx = non_empty.index(line) if line in non_empty else 0
        color = colors[min(idx * n // max(len(non_empty), 1), n - 1)]
        t.append(line + "\n", style=color)
    return t


def banner():
    console.clear()
    grad_colors = [C["p1"], C["p2"], C["p3"], C["p4"], C["p5"], C["p6"]]
    console.print(gradient_text(BANNER, grad_colors))
    sub = Text()
    sub.append("  ────────────────  ", style=C["p3"])
    sub.append("Discord GRANT-tools", style="bold white")
    sub.append("  ", style=C["wh"])
    sub.append("(prochain upgrades a venir)", style=C["p4"])
    sub.append("  ────────────────", style=C["p3"])
    console.print(Align.center(sub))
    foot = Text()
    foot.append("made with ", style=C["gr"])
    foot.append("♥", style=C["rd"])
    foot.append(" by ", style=C["gr"])
    foot.append("Near", style=f"bold {C['p2']}")
    foot.append("  ·  ", style=C["gr"])
    foot.append("abuse pas du tools", style=C["dg"])
    console.print(Align.center(foot))
    console.print()


def loading_intro():
    console.clear()
    console.print()
    console.print()
    console.print(Align.center(Text("chargement en cours..", style=f"bold {C['p2']}")))
    console.print()
    with Progress(
        SpinnerColumn(style=C["p3"]),
        BarColumn(bar_width=40, complete_style=C["p4"], finished_style=C["pink"]),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style=C["p2"]),
        console=console,
        transient=True,
    ) as prog:
        task = prog.add_task("[mauve]chargement", total=30)
        for _ in range(30):
            prog.advance(task)
            time.sleep(0.03)


def load_token() -> str | None:
    return TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else None


def load_webhook() -> str | None:
    return WH_FILE.read_text().strip() if WH_FILE.exists() else None


def pause():
    console.print(f"\n[dim]Appuie sur Entrée pour revenir au menu...[/]")
    input()


def section_title(title: str):
    banner()
    console.print(f"  [bold {C['p2']}]▸[/] [bold white]{title}[/]")
    console.print(f"  [{C['dg']}]{'─' * 70}[/]\n")


# === MENU ===
def menu():
    banner()
    status_tk = f"[{C['gn']}]configuré[/]" if TOKEN_FILE.exists() else f"[{C['rd']}]non configuré[/]"
    status_wh = f"[{C['gn']}]configuré[/]" if WH_FILE.exists() else f"[{C['rd']}]non configuré[/]"

    items_l = [
        ("01", "DM All Friends"), ("02", "Webhook Sender"),
        ("03", "Webhook Deleter"), ("04", "Webhook Info"),
        ("05", "Token Checker / Mon Compte"), ("06", "Spam Message (via token)"),
    ]
    items_r = [
        ("07", "Server Info (via invite)"), ("08", "User Lookup (via ID)"),
        ("09", "Nitro Generator (format)"), ("10", "Nitro Checker"),
        ("11", "Configurer / Effacer Token"), ("12", "À propos"),
    ]

    table = Table(show_header=False, box=box.ROUNDED, border_style=C["p4"], padding=(0, 2), expand=False)
    table.add_column(justify="left")
    table.add_column(justify="left")

    for (n1, l1), (n2, l2) in zip(items_l, items_r):
        # FIX: séparer les balises de couleur pour éviter la fusion "[#color01#color]"
        left  = Text()
        left.append("[", style=C["p2"])
        left.append(n1, style=C["p1"])
        left.append("]", style=C["p2"])
        left.append(f"  {l1}", style="white")

        right = Text()
        right.append("[", style=C["p2"])
        right.append(n2, style=C["p1"])
        right.append("]", style=C["p2"])
        right.append(f"  {l2}", style="white")

        table.add_row(left, right)

    table.add_row("", "")

    quit_row = Text()
    quit_row.append("[", style=C["p2"])
    quit_row.append("00", style=C["rd"])
    quit_row.append("]", style=C["p2"])
    quit_row.append("  Quitter", style="white")
    table.add_row(quit_row, "")

    console.print(Align.center(table))
    console.print(f"\n     [{C['gr']}]Token   :[/] {status_tk}      [{C['gr']}]Webhook :[/] {status_wh}\n")

    choice = Prompt.ask(
        f"  [{C['p3']}]┌─[/] [white]Near[/] [{C['p3']}]─[[/][{C['p1']}]choix[/][{C['p3']}]]─►[/]",
        default="0"
    ).strip().zfill(2)

    actions = {
        "01": dm_all, "02": wh_send, "03": wh_del, "04": wh_info,
        "05": tk_check, "06": spam_channel, "07": srv_info, "08": user_lookup,
        "09": nitro_gen, "10": nitro_check, "11": tk_config, "12": about,
        "00": lambda: sys.exit(0),
    }
    fn = actions.get(choice)
    if fn:
        try:
            fn()
        except KeyboardInterrupt:
            console.print(f"\n[{C['yl']}][!] Annulé[/]")
            pause()
        except Exception as e:
            console.print(f"\n[{C['rd']}][X] Une erreur est survenue : {e}[/]")
            pause()
    else:
        console.print(f"\n  [{C['rd']}][X] Choix invalide, réessaie[/]")
        time.sleep(1)


# === Helpers HTTP ===
def api_get(url, token=None):
    h = {"Authorization": token} if token else {}
    return requests.get(url, headers=h, timeout=15)


def api_post(url, token=None, json_data=None):
    h = {"Authorization": token, "Content-Type": "application/json"} if token else {"Content-Type": "application/json"}
    return requests.post(url, headers=h, json=json_data, timeout=15)


# === FONCTIONNALITÉS ===
def dm_all():
    section_title("DM All Friends")
    token = load_token()
    if not token:
        console.print(f"  [{C['rd']}][X] Aucun token configuré — va dans l'option 11 d'abord[/]")
        pause()
        return
    console.print(f"  [{C['yl']}][!] Rappel : le selfbot viole les CGU Discord. Ton compte risque un ban.[/]\n")
    msg = Prompt.ask(f"  [{C['p2']}]Message à envoyer[/]")
    delay = IntPrompt.ask(f"  [{C['p2']}]Délai entre chaque DM (secondes)[/]", default=3)
    if not msg:
        pause()
        return

    console.print(f"\n  [{C['p2']}][i][/] Récupération de ta liste d'amis...")
    r = api_get("https://discord.com/api/v9/users/@me/relationships", token)
    if r.status_code != 200:
        console.print(f"  [{C['rd']}][X] Token invalide ou expiré ({r.status_code})[/]")
        pause()
        return
    friends = [u["id"] for u in r.json() if u.get("type") == 1]
    console.print(f"  [{C['p2']}][i][/] [white]{len(friends)}[/] ami(s) trouvé(s)\n")
    if not friends or not Confirm.ask(
        f"  [{C['yl']}]Tu vas envoyer le message à {len(friends)} personne(s). C'est bon ?[/]",
        default=False
    ):
        pause()
        return

    sent, fail = 0, 0
    for fid in friends:
        try:
            r2 = api_post("https://discord.com/api/v9/users/@me/channels", token, {"recipient_id": fid})
            ch_id = r2.json().get("id")
            if ch_id:
                api_post(f"https://discord.com/api/v9/channels/{ch_id}/messages", token, {"content": msg})
                console.print(f"  [{C['gn']}][✓][/] {fid}")
                sent += 1
            else:
                console.print(f"  [{C['rd']}][✗][/] {fid}")
                fail += 1
        except Exception:
            fail += 1
        time.sleep(delay)
    console.print(f"\n  [{C['gn']}][OK][/] {sent} envoyé(s), {fail} échec(s)")
    pause()


def wh_send():
    section_title("Webhook Sender")
    wh = load_webhook() or Prompt.ask(f"  [{C['p2']}]URL du Webhook[/]")
    if not wh:
        pause()
        return
    msg = Prompt.ask(f"  [{C['p2']}]Message à envoyer[/]")
    name = Prompt.ask(f"  [{C['p2']}]Pseudo affiché (laisse vide pour garder celui du webhook)[/]", default="")
    n = IntPrompt.ask(f"  [{C['p2']}]Nombre d'envois[/]", default=1)
    payload = {"content": msg}
    if name:
        payload["username"] = name
    ok, ko = 0, 0
    for i in range(1, n + 1):
        r = requests.post(wh, json=payload, timeout=15)
        if r.status_code == 204:
            console.print(f"  [{C['gn']}][{i}/{n}] ✓[/]")
            ok += 1
        else:
            console.print(f"  [{C['rd']}][{i}/{n}] erreur {r.status_code}[/]")
            ko += 1
        time.sleep(1)
    console.print(f"\n  [{C['gn']}][OK][/] {ok} envoyé(s), {ko} échec(s)")
    pause()


def wh_del():
    section_title("Webhook Deleter")
    wh = Prompt.ask(f"  [{C['p2']}]URL du Webhook à supprimer[/]")
    if not wh:
        pause()
        return
    r = requests.delete(wh, timeout=15)
    if r.status_code == 204:
        console.print(f"\n  [{C['gn']}][✓] Webhook supprimé avec succès[/]")
    else:
        console.print(f"\n  [{C['rd']}][✗] Échec (code {r.status_code})[/]")
    pause()


def wh_info():
    section_title("Webhook Info")
    wh = Prompt.ask(f"  [{C['p2']}]URL du Webhook[/]")
    if not wh:
        pause()
        return
    r = requests.get(wh, timeout=15)
    if r.status_code != 200:
        console.print(f"  [{C['rd']}][X] Impossible de récupérer les infos ({r.status_code})[/]")
        pause()
        return
    d = r.json()
    for k, label in [("name", "Nom"), ("id", "ID"), ("channel_id", "Channel ID"),
                     ("guild_id", "Guild ID"), ("token", "Token"), ("avatar", "Avatar")]:
        console.print(f"  [{C['p2']}]{label:<13}[/] : [white]{d.get(k, '—')}[/]")
    pause()


def tk_check():
    section_title("Token Checker / Mon Compte")
    token = load_token() or Prompt.ask(f"  [{C['p2']}]Ton token Discord[/]")
    if not token:
        pause()
        return
    r = api_get("https://discord.com/api/v9/users/@me", token)
    if r.status_code != 200:
        console.print(f"  [{C['rd']}][X] Token invalide ou expiré ({r.status_code})[/]")
        pause()
        return
    d = r.json()
    info = [
        ("Pseudo",      f"{d.get('username')}#{d.get('discriminator')}"),
        ("Global Name", d.get("global_name")),
        ("ID",          d.get("id")),
        ("Email",       d.get("email")),
        ("Téléphone",   d.get("phone")),
        ("2FA actif",   d.get("mfa_enabled")),
        ("Vérifié",     d.get("verified")),
        ("Nitro",       d.get("premium_type")),
        ("Langue",      d.get("locale")),
    ]
    for label, val in info:
        console.print(f"  [{C['p2']}]{label:<13}[/] : [white]{val}[/]")
    pause()


def spam_channel():
    section_title("Spam Message (via Token)")
    token = load_token()
    if not token:
        console.print(f"  [{C['rd']}][X] Aucun token configuré — va dans l'option 11 d'abord[/]")
        pause()
        return
    ch = Prompt.ask(f"  [{C['p2']}]ID du channel[/]")
    msg = Prompt.ask(f"  [{C['p2']}]Message à envoyer[/]")
    n = IntPrompt.ask(f"  [{C['p2']}]Combien de fois ?[/]", default=1)
    delay = IntPrompt.ask(f"  [{C['p2']}]Délai entre chaque envoi (s)[/]", default=2)
    for i in range(1, n + 1):
        r = api_post(f"https://discord.com/api/v9/channels/{ch}/messages", token, {"content": msg})
        color = C["gn"] if r.status_code == 200 else C["rd"]
        console.print(f"  [{color}][{i}/{n}] {r.status_code}[/]")
        time.sleep(delay)
    pause()


def srv_info():
    section_title("Server Info (via Invite)")
    inv = Prompt.ask(f"  [{C['p2']}]Lien ou code d'invitation[/]")
    inv = inv.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").strip()
    if not inv:
        pause()
        return
    r = requests.get(
        f"https://discord.com/api/v9/invites/{inv}?with_counts=true&with_expiration=true",
        timeout=15
    )
    if r.status_code != 200:
        console.print(f"  [{C['rd']}][X] {r.json().get('message', 'Invitation invalide')}[/]")
        pause()
        return
    d = r.json()
    g = d.get("guild", {})
    info = [
        ("Serveur",    g.get("name")),
        ("ID",         g.get("id")),
        ("Description",g.get("description")),
        ("Membres",    d.get("approximate_member_count")),
        ("En ligne",   d.get("approximate_presence_count")),
        ("Boosts",     g.get("premium_subscription_count")),
        ("Channel inv",d.get("channel", {}).get("name")),
        ("Inviteur",   d.get("inviter", {}).get("username")),
        ("Expiration", d.get("expires_at")),
    ]
    for label, val in info:
        console.print(f"  [{C['p2']}]{label:<13}[/] : [white]{val}[/]")
    pause()


def user_lookup():
    section_title("User Lookup (via ID)")
    token = load_token()
    if not token:
        console.print(f"  [{C['rd']}][X] Aucun token configuré — va dans l'option 11 d'abord[/]")
        pause()
        return
    uid = Prompt.ask(f"  [{C['p2']}]ID de l'utilisateur[/]")
    if not uid:
        pause()
        return
    r = api_get(f"https://discord.com/api/v9/users/{uid}", token)
    if r.status_code != 200:
        console.print(f"  [{C['rd']}][X] {r.json().get('message', 'Utilisateur introuvable')}[/]")
        pause()
        return
    d = r.json()
    info = [
        ("Pseudo",     f"{d.get('username')}#{d.get('discriminator')}"),
        ("Global Name",d.get("global_name")),
        ("ID",         d.get("id")),
        ("Bot",        d.get("bot", False)),
        ("Avatar",     f"https://cdn.discordapp.com/avatars/{d.get('id')}/{d.get('avatar')}.png"),
        ("Flags",      d.get("public_flags")),
    ]
    for label, val in info:
        console.print(f"  [{C['p2']}]{label:<13}[/] : [white]{val}[/]")
    pause()


def nitro_gen():
    section_title("Nitro Code Generator (format)")
    console.print(f"  [{C['yl']}][i] Ces codes sont générés aléatoirement — ils ne sont pas valides.[/]\n")
    n = IntPrompt.ask(f"  [{C['p2']}]Combien de codes tu veux ?[/]", default=10)
    out = STORAGE / f"nitro_{random.randint(1000, 9999)}.txt"
    with out.open("w") as f:
        for _ in range(n):
            code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
            url = f"https://discord.gift/{code}"
            console.print(f"  [{C['p2']}]{url}[/]")
            f.write(url + "\n")
    console.print(f"\n  [{C['gn']}][OK] Sauvegardé ici : {out}[/]")
    pause()


def nitro_check():
    section_title("Nitro Checker")
    console.print(
        f"  [{C['p2']}][[/][white]1[/][{C['p2']}]][/] [white]Code unique[/]   "
        f"[{C['p2']}][[/][white]2[/][{C['p2']}]][/] [white]Fichier .txt[/]   "
        f"[{C['p2']}][[/][white]0[/][{C['p2']}]][/] [white]Retour[/]"
    )
    c = Prompt.ask(f"  [{C['p3']}]►[/]")
    if c == "1":
        code = Prompt.ask(f"  [{C['p2']}]Code ou lien Nitro[/]").replace("https://discord.gift/", "").strip()
        r = requests.get(
            f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_subscription_plan=true",
            timeout=15
        )
        if r.status_code == 200:
            console.print(f"  [{C['gn']}][✓ VALIDE] {r.json().get('subscription_plan', {}).get('name')}[/]")
        else:
            console.print(f"  [{C['rd']}][✗] {r.json().get('message', 'Code invalide')}[/]")
    elif c == "2":
        path = Prompt.ask(f"  [{C['p2']}]Chemin vers le fichier .txt[/]")
        if not Path(path).exists():
            console.print(f"  [{C['rd']}][X] Fichier introuvable[/]")
            pause()
            return
        for line in Path(path).read_text().splitlines():
            code = line.replace("https://discord.gift/", "").strip()
            if not code:
                continue
            r = requests.get(
                f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_subscription_plan=true",
                timeout=15
            )
            if r.status_code == 200:
                console.print(f"  [{C['gn']}][✓ VALIDE][/] {code}")
            else:
                console.print(f"  [{C['dg']}][✗] {code}[/]")
            time.sleep(0.8)
    pause()


def tk_config():
    while True:
        section_title("Gestion du Token & Webhook")
        console.print(
            f"  [{'green' if TOKEN_FILE.exists() else 'red'}]"
            f"● Token : {'configuré ✓' if TOKEN_FILE.exists() else 'non configuré'}[/]"
        )
        console.print(
            f"  [{'green' if WH_FILE.exists() else 'red'}]"
            f"● Webhook : {'configuré ✓' if WH_FILE.exists() else 'non configuré'}[/]\n"
        )
        options = [
            ("1", "Définir / remplacer le token"),
            ("2", "Définir / remplacer le webhook"),
            ("3", "Effacer le token"),
            ("4", "Effacer le webhook"),
            ("0", "Retour au menu"),
        ]
        for n, l in options:
            t = Text()
            t.append("[", style=C["p2"])
            t.append(n, style=C["p1"])
            t.append("]", style=C["p2"])
            t.append(f"  {l}", style="white")
            console.print("  ", t)
        c = Prompt.ask(f"\n  [{C['p3']}]►[/]")
        if c == "1":
            t = Prompt.ask(f"  [{C['p2']}]Colle ton token ici[/]", password=True)
            if t:
                TOKEN_FILE.write_text(t)
                console.print(f"  [{C['gn']}][OK] Token sauvegardé[/]")
                time.sleep(1)
        elif c == "2":
            w = Prompt.ask(f"  [{C['p2']}]URL du webhook[/]")
            if w:
                WH_FILE.write_text(w)
                console.print(f"  [{C['gn']}][OK] Webhook sauvegardé[/]")
                time.sleep(1)
        elif c == "3":
            TOKEN_FILE.unlink(missing_ok=True)
            console.print(f"  [{C['gn']}][OK] Token effacé[/]")
            time.sleep(1)
        elif c == "4":
            WH_FILE.unlink(missing_ok=True)
            console.print(f"  [{C['gn']}][OK] Webhook effacé[/]")
            time.sleep(1)
        elif c == "0":
            return


def about():
    section_title("À propos de Near Tools")
    console.print(Panel.fit(
        f"[bold {C['p2']}]Near Tools[/] — multi-tool Discord fait maison en Python + Rich.\n\n"
        f"[{C['gr']}]Données stockées localement :[/] [white]{STORAGE}[/]\n\n"
        f"[bold {C['p3']}]Ce que tu peux faire :[/]\n"
        f"  [{C['p2']}]●[/] DM All Friends, Spam canal, infos token\n"
        f"  [{C['p2']}]●[/] Webhook : envoyer / supprimer / inspecter\n"
        f"  [{C['p2']}]●[/] Infos serveur, lookup user, génération/vérif Nitro\n\n"
        f"[{C['yl']}][!] Disclaimer :[/] outil à but éducatif uniquement.\n"
        f"Le selfbot viole les CGU Discord — utilise ça avec ta tête.\n\n"
        f"Fait avec [{C['rd']}]♥[/] par [{C['p2']}]Near[/]",
        border_style=C["p4"], box=box.ROUNDED, padding=(1, 2)
    ))
    pause()


def main():
    try:
        loading_intro()
        while True:
            menu()
    except KeyboardInterrupt:
        console.clear()
        console.print()
        console.print(Align.center(Text("Merci d'avoir utilisé Near Tools  ✨", style=f"bold {C['p2']}")))
        console.print(Align.center(Text("à la prochaine !", style=C["gr"])))
        time.sleep(1)


if __name__ == "__main__":
    main()
