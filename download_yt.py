
"""
Ferramenta de download do YouTube com yt-dlp - versão turbinada.
Requer: pip install yt-dlp
Opcional: FFmpeg (recomendado)
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

import yt_dlp
from yt_dlp.utils import DownloadError


# ============================================================
#  Cores para terminal (porque o dragão gosta de estilo)
# ============================================================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    print(Colors.HEADER + "=" * 50)
    print("     YouTube Downloader - Edição Dragão")
    print("=" * 50 + Colors.ENDC)


def progress_hook(d):
    """Barra de progresso colorida com informações detalhadas."""
    if d['status'] == 'downloading':
        # Limpa a linha anterior
        pct = d.get('_percent_str', '?').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        fragment = d.get('fragment_index', '')
        if fragment:
            frag_info = f" | Fragmento: {fragment}/{d.get('fragment_count', '?')}"
        else:
            frag_info = ""
        # Barra simples
        try:
            percent_float = float(pct.strip('%'))
            bar_len = 30
            filled = int(bar_len * percent_float / 100)
            bar = '█' * filled + '░' * (bar_len - filled)
        except:
            bar = '?' * 30
            percent_float = 0

        print(f"\r{Colors.OKCYAN}⬇ {bar} {pct}{Colors.ENDC} | "
              f"Vel: {speed} | ETA: {eta}{frag_info}", end='')
    elif d['status'] == 'finished':
        print(f"\n{Colors.OKGREEN}✓ Download concluído, mesclando...{Colors.ENDC}")


def post_process_hook(d):
    """Hook para pós-processamento."""
    if d['status'] == 'started':
        print(f"\n{Colors.WARNING}⚙ Processando: {d['postprocessor']}{Colors.ENDC}")
    elif d['status'] == 'finished':
        print(f"{Colors.OKGREEN}✓ Pós-processamento finalizado.{Colors.ENDC}")


def get_ydl_opts(args):
    """Constrói as opções do yt-dlp com base nos argumentos."""
    # Template de nome do arquivo
    if args.output_template:
        outtmpl = args.output_template
    else:
        outtmpl = os.path.join(args.output_dir, '%(title).100s [%(id)s].%(ext)s')

    ydl_opts = {
        'outtmpl': outtmpl,
        'progress_hooks': [progress_hook],
        'postprocessor_hooks': [post_process_hook],
        'quiet': args.quiet,
        'no_warnings': args.no_warnings,
        'ignoreerrors': args.ignore_errors,
        'nooverwrites': args.no_overwrite,
        'writethumbnail': args.thumbnail,
        'writesubtitles': args.subtitles,
        'writeautomaticsub': args.auto_subs,
        'subtitleslangs': args.sub_langs.split(',') if args.sub_langs else None,
        'extract_flat': args.extract_flat,
        'playliststart': args.playlist_start,
        'playlistend': args.playlist_end,
        'concurrent_fragment_downloads': args.concurrent_fragments,
        'retries': args.retries,
        'fragment_retries': args.retries,
        'socket_timeout': args.timeout,
    }

    # Qualidade / formato
    if args.audio_only:
        # Extrair apenas áudio
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': args.audio_format,
            'preferredquality': args.audio_quality,
        }]
    elif args.format:
        ydl_opts['format'] = args.format
    else:
        # Melhor vídeo+áudio, mesclando em mp4
        ydl_opts['format'] = 'bestvideo[height<=?1080]+bestaudio/best[height<=?1080]'
        ydl_opts['merge_output_format'] = args.merge_format

    # Cookies
    if args.cookies_from_browser:
        ydl_opts['cookiesfrombrowser'] = (args.cookies_from_browser,)
    elif args.cookies_file:
        ydl_opts['cookiefile'] = args.cookies_file

    # Proxy
    if args.proxy:
        ydl_opts['proxy'] = args.proxy

    # Intervalo de downloads (para não sobrecarregar)
    if args.sleep_interval > 0:
        ydl_opts['sleep_interval'] = args.sleep_interval

    # Limite de taxa
    if args.limit_rate:
        ydl_opts['ratelimit'] = args.limit_rate * 1024  # KB para bytes

    # Metadados
    if args.add_metadata:
        ydl_opts['embedmetadata'] = True

    # Simulação (não baixa, só mostra o que seria baixado)
    if args.simulate:
        ydl_opts['simulate'] = True
        ydl_opts['quiet'] = False

    return ydl_opts


def download(url, opts):
    """Executa o download com tratamento de erros."""
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            print(f"{Colors.OKBLUE}🔍 Analisando: {url}{Colors.ENDC}")
            info = ydl.extract_info(url, download=not opts.get('simulate', False))
            if info and not opts.get('simulate', False):
                print(f"\n{Colors.OKGREEN}✅ Download(s) finalizado(s) com sucesso!{Colors.ENDC}")
            return True
    except DownloadError as e:
        print(f"\n{Colors.FAIL}❌ Erro no download: {e}{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Erro inesperado: {e}{Colors.ENDC}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description=f"{Colors.BOLD}YouTube Downloader Dragão{Colors.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Exemplos:\n"
               "  %(prog)s 'URL'\n"
               "  %(prog)s 'URL' -f bestvideo+bestaudio --merge-format mkv\n"
               "  %(prog)s 'URL' --audio-only --audio-format mp3\n"
               "  %(prog)s 'PLAYLIST_URL' --playlist-start 1 --playlist-end 5\n"
               "  %(prog)s 'URL' --cookies-from-browser chrome"
    )

    # Argumentos essenciais
    parser.add_argument('url', nargs='+', help='URL(s) do vídeo ou playlist')
    parser.add_argument('-o', '--output-dir', default='.', help='Diretório de saída (padrão: atual)')
    parser.add_argument('--output-template', help='Template do nome do arquivo (ex: "%%(title)s.%%(ext)s")')

    # Formato e qualidade
    parser.add_argument('-f', '--format', help='Formato desejado (ex: bestvideo+bestaudio, worst, 720p)')
    parser.add_argument('--merge-format', default='mp4', help='Formato final do container (padrão: mp4)')
    parser.add_argument('--audio-only', action='store_true', help='Extrair apenas áudio')
    parser.add_argument('--audio-format', default='mp3', help='Codec de áudio (padrão: mp3)')
    parser.add_argument('--audio-quality', default='192', help='Qualidade do áudio (padrão: 192)')

    # Playlist
    parser.add_argument('--playlist-start', type=int, default=1, help='Início da playlist (número)')
    parser.add_argument('--playlist-end', type=int, help='Fim da playlist (número)')
    parser.add_argument('--extract-flat', action='store_true', help='Apenas listar itens da playlist, sem baixar')

    # Cookies e autenticação
    parser.add_argument('--cookies-from-browser', help='Navegador para extrair cookies (chrome, firefox, edge, etc.)')
    parser.add_argument('--cookies-file', help='Arquivo de cookies no formato Netscape')

    # Rede
    parser.add_argument('--proxy', help='Proxy (ex: socks5://127.0.0.1:9050)')
    parser.add_argument('--limit-rate', type=float, help='Limitar taxa de download (KB/s)')
    parser.add_argument('--retries', type=int, default=10, help='Número de tentativas (padrão: 10)')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout de socket (padrão: 30s)')
    parser.add_argument('--sleep-interval', type=float, default=0, help='Intervalo entre downloads (segundos)')

    # Extras
    parser.add_argument('--thumbnail', action='store_true', help='Baixar thumbnail')
    parser.add_argument('--subtitles', action='store_true', help='Baixar legendas manuais')
    parser.add_argument('--auto-subs', action='store_true', help='Baixar legendas automáticas')
    parser.add_argument('--sub-langs', default='pt,en', help='Idiomas das legendas (padrão: pt,en)')
    parser.add_argument('--add-metadata', action='store_true', help='Incorporar metadados no arquivo')
    parser.add_argument('--concurrent-fragments', type=int, default=4, help='Downloads paralelos de fragmentos (padrão: 4)')

    # Comportamento
    parser.add_argument('--simulate', action='store_true', help='Simular, sem baixar')
    parser.add_argument('--no-overwrite', action='store_true', help='Não sobrescrever arquivos existentes')
    parser.add_argument('--ignore-errors', action='store_true', help='Ignorar erros e continuar (playlists)')
    parser.add_argument('--quiet', action='store_true', help='Modo silencioso')
    parser.add_argument('--no-warnings', action='store_true', help='Suprimir avisos')

    args = parser.parse_args()

    print_banner()

    # Cria diretório de saída
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = get_ydl_opts(args)

    # Processa cada URL
    success_count = 0
    fail_count = 0
    for url in args.url:
        print(f"\n{Colors.BOLD}🎯 Alvo: {url}{Colors.ENDC}")
        if download(url, ydl_opts):
            success_count += 1
        else:
            fail_count += 1

    # Resumo final
    total = success_count + fail_count
    if total > 1:
        print(f"\n{Colors.BOLD}📊 Resumo: {Colors.OKGREEN}{success_count} sucesso(s){Colors.ENDC}, "
              f"{Colors.FAIL}{fail_count} falha(s){Colors.ENDC} de {total} total.")


if __name__ == '__main__':
    main()