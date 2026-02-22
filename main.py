import concurrent.futures, shutil, tls_client, threading, colorama, os, sys, random, ctypes, toml, time, json, datetime 

def clear_console():
    os.system("clear||cls")
def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'
class bcolors:
    BLACK = '\033[30m'
    TIME = rgb(128, 128, 128)  
    OKBLUE = '\033[94m'
    DEEPBLUE = rgb(61, 255, 210) 
    PURPLE = rgb(255, 61, 158)  
    FAIL = rgb(255, 0, 0) 
    SUCCESS = rgb(94, 255, 0)  
    YELLOW = rgb(252, 247, 134)  
    ENDC = '\033[0m'
    HEADER = '\033[95m'
    OKGREEN = rgb(94, 255, 0)  
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARKGREEN = '\033[32m'
    CYAN = rgb(61, 255, 210) 
    LIGHTBLUE = rgb(227, 229, 255) 
    ERRORBLUE = rgb(61, 36, 255)  
    BANNER = rgb(241, 255, 201)  
    USER = rgb(255, 215, 194)  
    ID = rgb(255, 51, 78)  
    GUILD = rgb(234, 163, 255)  


colorama.init()


def timeShit():
    return f"{bcolors.TIME}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.ENDC}"


config = toml.load("data/config.toml")
settings = json.loads(open("data/settings.json", "r").read())

with open("data/tokens.txt", "r") as f:
    tokens = f.readlines()

with open("data/proxies.txt", "r") as f:
    proxies = f.readlines()

tokens = list(set(tokens))

LOCK = threading.Lock()
valid = 0
invalid = 0
locked = 0
nitro = 0
flagged = 0
total = len(tokens)
current = 0
done = False


clear_console()

output_folder = f"output/{time.strftime('%Y-%m-%d %H-%M-%S')}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start = time.time()


class Checker:
    def __init__(self) -> None:
        self.session = tls_client.Session(
            client_identifier="chrome_104"
        )
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.update_proxy()
    
    def update_proxy(self):
        if not config["main"]["proxyless"]:
            self.session.proxies = f"http://{random.choice(proxies).strip()}"
       
    
    def check(self) -> None:
        global current, total, valid, locked, nitro, invalid, flagged

        while True:
            if len(tokens) == 0:
                break
            token = tokens.pop().strip()
            try:
                token_only = token.split(":")[-1]
                tkv = token_only.split(".")[0]
                self.session.headers["Authorization"] = token_only

                r = self.session.get(f"https://discord.com/api/v9/users/@me/guilds")
                if r.status_code == 429:
                    print(f"{timeShit()} → {bcolors.FAIL}[RATE LIMITED]{bcolors.ENDC} → {bcolors.PURPLE}[Too Many Requests]{bcolors.ENDC} token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC}")
                    self.update_proxy()
                    tokens.append(token)
                    continue

                current += 1

                if r.status_code == 401:
                    invalid += 1
                    print(f"{timeShit()} → {bcolors.FAIL}[INVALID]{bcolors.ENDC} → {bcolors.PURPLE}[Unauthorized]{bcolors.ENDC} token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC}")
                    LOCK.acquire()
                    with open(f"{output_folder}/invalid.txt", "a") as f:
                        f.write(token + "\n")
                    LOCK.release()
                    continue

                if r.status_code == 403:
                    locked += 1
                    print(f"{timeShit()} → {bcolors.FAIL}[LOCKED]{bcolors.ENDC} → {bcolors.PURPLE}[Account Locked]{bcolors.ENDC} token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC}")
                    LOCK.acquire()
                    with open(f"{output_folder}/locked.txt", "a") as f:
                        f.write(token + "\n")
                    LOCK.release()

                if r.status_code == 200:
                    guilds_count = len(r.json()) 
                    r = self.session.get(f"https://discord.com/api/v9/users/@me")
                    user_data = r.json()
                    
                    args = {
                        "token": tkv,
                        "username": user_data.get("username", "Unknown"),
                        "user_id": user_data.get("id", "Unknown"),
                        "guilds": guilds_count
                    }

                    if settings["flagged"]:
                        if r.json()["flags"] & 1048576 == 1048576:
                            flagged += 1
                            print(f"{timeShit()} → {bcolors.YELLOW}[FLAGGED]{bcolors.ENDC} → {bcolors.PURPLE}[Account Flagged]{bcolors.ENDC} token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC}")
                            LOCK.acquire()
                            with open(f"{output_folder}/flagged.txt", "a") as f:
                                f.write(token + "\n")
                            LOCK.release()
                            continue

                    if settings["type"]:
                        LOCK.acquire()
                        type = "unclaimed"
                        if r.json()["email"] != None:
                            type = "email verified"
                        if r.json()["phone"] != None:
                            if type == "email verified":
                                type = "fully verified"
                            else:
                                type = "phone verified"
                    else:
                        type = "valid"

                    args["type"] = type
                    LOCK.release()

                    if settings["age"]:
                        created_at = ((int(r.json()["id"]) >> 22) + 1420070400000) / 1000
                        age = (time.time() - created_at) / 86400 / 30
                        if age > 12:
                            args["age"] = f"{age/12:.0f} years"
                        else:
                            args["age"] = f"{age:.0f} months"

                        if not os.path.exists(f"{output_folder}/age/{args['age']}"):
                            os.makedirs(f"{output_folder}/age/{args['age']}")
                        
                        with open(f"{output_folder}/age/{args['age']}/{type}.txt", "a") as f:
                            f.write(token + "\n")

                    if settings["nitro"]:
                        r = self.session.get(f"https://discord.com/api/v9/users/@me/billing/subscriptions")
                        for sub in r.json():
                            days_left = (time.mktime(time.strptime(sub["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z")) - time.time()) / 86400
                            args["nitro"] = f"{days_left:.0f}d"
                            nitro += 1

                            r = self.session.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots")
                            available = 0
                            
                            for sub in r.json():
                                if sub["cooldown_ends_at"] == None:
                                    available += 1
                            
                            args["boosts"] = available

                            if not os.path.exists(f"{output_folder}/boosts/{days_left:.0f} days"):
                                os.makedirs(f"{output_folder}/boosts/{days_left:.0f} days")
                            
                            with open(f"{output_folder}/boosts/{days_left:.0f} days/{available} boosts.txt", "a") as f:
                                f.write(token + "\n")

                    log_parts = [f"{timeShit()} → {bcolors.SUCCESS}[VALID]{bcolors.ENDC}"]
                    log_parts.append(f"{bcolors.PURPLE}[{type.upper()}]{bcolors.ENDC}")
                    log_parts.append(f"token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC}")
                    log_parts.append(f"user: {bcolors.USER}[{args['username']}]{bcolors.ENDC}")
                    log_parts.append(f"id: {bcolors.ID}[{args['user_id']}]{bcolors.ENDC}")
                    log_parts.append(f"guilds: {bcolors.GUILD}[{args['guilds']}]{bcolors.ENDC}")
                    
                    if "age" in args:
                        log_parts.append(f"age: {bcolors.LIGHTBLUE}[{args['age']}]{bcolors.ENDC}")
                    if "nitro" in args:
                        log_parts.append(f"nitro: {bcolors.YELLOW}[{args['nitro']}]{bcolors.ENDC}")
                    if "boosts" in args:
                        log_parts.append(f"boosts: {bcolors.SUCCESS}[{args['boosts']}]{bcolors.ENDC}")
                    
                    print(" → ".join(log_parts))
                    
                    valid += 1
                    with open(f"{output_folder}/{type}.txt", "a") as f:
                        f.write(token + "\n")
                        
            except Exception as e:
                print(f"{timeShit()} → {bcolors.FAIL}[ERROR]{bcolors.ENDC} → {bcolors.PURPLE}[Exception]{bcolors.ENDC} token: {bcolors.CYAN}[{tkv}]{bcolors.ENDC} | error: {bcolors.ERRORBLUE}[{str(e)}]{bcolors.ENDC}")
                self.update_proxy()
                tokens.append(token)
                continue


def update_title():
    try:
        while not done:
            time.sleep(0.03)
            cps = current / (time.time() - start) if (time.time() - start) > 0 else 0
            cpm = round(cps * 60)
            if hasattr(ctypes, 'windll'):
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Token Checker - Valid: {valid} | Invalid: {invalid} | Locked: {locked} | Flagged: {flagged} | Remaining: {len(tokens)} | Progress: {current/total*100:.2f}% | CPM: {cpm} | tg :  @swllette - karenhoyoshi.asia - dc : fufuyaunn"
                )
    except:
        pass


columns = shutil.get_terminal_size().columns


def print_banner():
    """Print banner with token count"""
    info_text = f"Tokens Loaded: {total}             Powered by fufuyaunn"
    
    banner = f"""{bcolors.BANNER}
                                        ██╗  ██╗ █████╗ ██████╗ ███████╗███╗   ██╗██╗███████╗███╗   ███╗███████╗
                                        ██║ ██╔╝██╔══██╗██╔══██╗██╔════╝████╗  ██║██║██╔════╝████╗ ████║██╔════╝
                                        █████╔╝ ███████║██████╔╝█████╗  ██╔██╗ ██║██║███████╗██╔████╔██║█████╗  
                                        ██╔═██╗ ██╔══██║██╔══██╗██╔══╝  ██║╚██╗██║██║╚════██║██║╚██╔╝██║██╔══╝  
                                        ██║  ██╗██║  ██║██║  ██║███████╗██║ ╚████║██║███████║██║ ╚═╝ ██║███████╗
                                        ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
                                                                        
                                                                                                                  
                                                 {info_text}
{bcolors.ENDC}"""
    print(banner)


if __name__ == '__main__':
    time.sleep(0.1)
    update = threading.Thread(target=update_title)
    update.start()

    print_banner()
    print()

    with concurrent.futures.ThreadPoolExecutor(max_workers=config["main"]["threads"]) as executor:
        for i in range(config["main"]["threads"]):
            executor.submit(Checker().check)
    
    done = True
    update.join()
    
    print()
    elapsed = time.time() - start
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print(f"{timeShit()} → {bcolors.SUCCESS}[COMPLETE]{bcolors.ENDC} → {bcolors.LIGHTBLUE}Duration: [{minutes}m {seconds}s]{bcolors.ENDC}")
    print(f"{timeShit()} → {bcolors.SUCCESS}[$] Results:{bcolors.ENDC} {bcolors.LIGHTBLUE}Total: {current}{bcolors.ENDC} | {bcolors.SUCCESS}Valid: {valid}{bcolors.ENDC} | {bcolors.FAIL}Invalid: {invalid}{bcolors.ENDC} | {bcolors.YELLOW}Nitro: {nitro}{bcolors.ENDC} | {bcolors.PURPLE}Locked: {locked}{bcolors.ENDC} | {bcolors.ERRORBLUE}Flagged: {flagged}{bcolors.ENDC}")
    print(f"{timeShit()} → {bcolors.SUCCESS}[$] Press Enter to exit{bcolors.ENDC}")
    input()
    sys.exit(0)
