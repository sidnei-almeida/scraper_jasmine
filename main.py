#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 SCRAPER JASMINE ALIMENTOS - Interface de Coleta de Dados Nutricionais
============================================================
Sistema completo para coleta de dados nutricionais dos produtos da Jasmine Alimentos
do site FatSecret com interface interativa e amigável.

COMO USAR:
1. Execute: python main.py
2. Escolha uma das opções do menu
3. Aguarde o processamento
4. Visualize os resultados na pasta dados/
"""

import os
import sys
import time
import glob
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                🥣 SCRAPER JASMINE ALIMENTOS                  ║
║                                                              ║
║        Coleta de Dados Nutricionais v1.0                    ║
║                                                              ║
║  🔍 Coleta URLs dos produtos da Jasmine Alimentos           ║
║  📊 Extrai dados nutricionais do FatSecret                  ║
║  💾 Gera relatórios em CSV e JSON                           ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES PRINCIPAIS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🔍 {Cores.BRANCO}Coletar URLs{Cores.RESET} - Extrai URLs dos produtos da Jasmine Alimentos
  {Cores.AMARELO}2.{Cores.RESET} 📊 {Cores.BRANCO}Coletar Dados{Cores.RESET} - Extrai dados nutricionais
  {Cores.AMARELO}3.{Cores.RESET} ⚡ {Cores.BRANCO}Coleta Completa{Cores.RESET} - URLs + Dados (automático)

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}6.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}7.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-7): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ============================================================================
# 🎯 FUNÇÕES ESPECÍFICAS DO SCRAPER BOB'S
# ============================================================================

def executar_coleta_urls():
    """Executa a coleta de URLs dos produtos da Jasmine Alimentos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🔍 COLETANDO URLs DOS PRODUTOS DA JASMINE ALIMENTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   🔍 Fonte: {Cores.AMARELO}FatSecret Brasil{Cores.RESET}")
    print(f"   🥣 Produtos: {Cores.AMARELO}Jasmine Alimentos{Cores.RESET}")
    print(f"   📁 Saída: {Cores.AMARELO}dados/jasmine_urls.json{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Iniciando coleta de URLs", 1.5)
            
            # Executa o coletor de URLs
            resultado = subprocess.run([
                sys.executable, "config/url_collector.py"
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"{Cores.VERDE}✅ URLs coletadas com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📁 Arquivo salvo em: dados/jasmine_urls.json{Cores.RESET}")
            else:
                print(f"{Cores.VERMELHO}❌ Erro durante a coleta: {resultado.stderr}{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_coleta_dados():
    """Executa a coleta de dados nutricionais"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📊 COLETANDO DADOS NUTRICIONAIS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verifica se existe o arquivo de URLs
    if not os.path.exists("dados/jasmine_urls.json"):
        print(f"{Cores.VERMELHO}❌ Arquivo de URLs não encontrado!{Cores.RESET}")
        print(f"{Cores.AMARELO}💡 Execute primeiro a opção 'Coletar URLs'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📋 Fonte: {Cores.AMARELO}dados/jasmine_urls.json{Cores.RESET}")
    print(f"   📊 Saída: {Cores.AMARELO}dados/jasmine_nutricional.csv{Cores.RESET}")
    print(f"   ⏱️  Tempo estimado: {Cores.AMARELO}2-5 minutos{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Iniciando coleta de dados nutricionais", 1.5)
            
            # Executa o scraper
            resultado = subprocess.run([
                sys.executable, "config/scraper.py"
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"{Cores.VERDE}✅ Dados nutricionais coletados com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📁 Arquivo salvo em: dados/jasmine_nutricional.csv{Cores.RESET}")
            else:
                print(f"{Cores.VERMELHO}❌ Erro durante a coleta: {resultado.stderr}{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_coleta_completa():
    """Executa a coleta completa (URLs + Dados)"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}⚡ COLETA COMPLETA - URLs + DADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Esta operação pode demorar {Cores.VERMELHO}5-10 minutos{Cores.RESET}")
    print(f"   • Serão executadas duas etapas automaticamente")
    print(f"   • 1ª: Coleta de URLs dos produtos")
    print(f"   • 2ª: Coleta de dados nutricionais")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            # Etapa 1: Coleta de URLs
            print(f"\n{Cores.VERDE}🔄 ETAPA 1: Coletando URLs...{Cores.RESET}")
            mostrar_barra_progresso("Coletando URLs dos produtos", 2.0)
            
            resultado_urls = subprocess.run([
                sys.executable, "config/url_collector.py"
            ], capture_output=True, text=True)
            
            if resultado_urls.returncode != 0:
                print(f"{Cores.VERMELHO}❌ Erro na coleta de URLs: {resultado_urls.stderr}{Cores.RESET}")
                return
            
            print(f"{Cores.VERDE}✅ URLs coletadas com sucesso!{Cores.RESET}")
            
            # Etapa 2: Coleta de dados
            print(f"\n{Cores.VERDE}🔄 ETAPA 2: Coletando dados nutricionais...{Cores.RESET}")
            mostrar_barra_progresso("Coletando dados nutricionais", 2.0)
            
            resultado_dados = subprocess.run([
                sys.executable, "config/scraper.py"
            ], capture_output=True, text=True)
            
            if resultado_dados.returncode == 0:
                print(f"{Cores.VERDE}✅ Coleta completa finalizada com sucesso!{Cores.RESET}")
                print(f"{Cores.CIANO}📁 Arquivos gerados:{Cores.RESET}")
                print(f"   • dados/jasmine_urls.json")
                print(f"   • dados/jasmine_nutricional.csv")
            else:
                print(f"{Cores.VERMELHO}❌ Erro na coleta de dados: {resultado_dados.stderr}{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    extensoes = ["*.json", "*.csv"]
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = []
    for extensao in extensoes:
        arquivos.extend(glob.glob(f"{pasta_dados}/{extensao}"))
    
    if not arquivos:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo encontrado em '{pasta_dados}'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}📊 Total de arquivos: {len(arquivos)}{Cores.RESET}\n")
    
    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
        
        # Calcula o tamanho em formato legível
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
        
        # Ícone baseado na extensão
        if arquivo.endswith('.json'):
            icone = "📄"
        elif arquivo.endswith('.csv'):
            icone = "📊"
        else:
            icone = "📁"
        
        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {icone} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
        print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove arquivos antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    extensoes = ["*.json", "*.csv"]
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = []
    for extensao in extensoes:
        arquivos.extend(glob.glob(f"{pasta_dados}/{extensao}"))
    
    if not arquivos:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{len(arquivos)} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_sobre():
    """Exibe informações sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O SCRAPER JASMINE ALIMENTOS{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   Sistema completo para coleta automatizada de dados nutricionais 
   dos produtos da Jasmine Alimentos disponíveis no site FatSecret Brasil.

{Cores.VERDE}📊 FUNCIONALIDADES:{Cores.RESET}
   • 🔍 Coleta URLs dos produtos da Jasmine Alimentos
   • 📊 Extrai dados nutricionais completos
   • 💾 Gera relatórios em CSV e JSON
   • ⚡ Processamento automatizado

{Cores.VERDE}🛠️  TECNOLOGIAS:{Cores.RESET}
   • Python 3.8+
   • Requests (requisições HTTP)
   • BeautifulSoup (parsing HTML)
   • Pandas (manipulação de dados)

{Cores.VERDE}📂 ARQUIVOS GERADOS:{Cores.RESET}
   • JSON: dados/jasmine_urls.json (URLs coletadas)
   • CSV: dados/jasmine_nutricional.csv (dados nutricionais)
   • Localização: pasta dados/

{Cores.VERDE}⚡ CARACTERÍSTICAS:{Cores.RESET}
   • Interface interativa e amigável
   • Coleta automática com paginação
   • Tratamento de erros robusto
   • Pausas entre requisições

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • Scraper Jasmine Alimentos Team
   • Versão: 1.0
   • Data: {datetime.now().strftime('%B %Y')}

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

# ============================================================================
# 🚀 FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()
            
            escolha = obter_escolha()
            
            if escolha == "1":
                executar_coleta_urls()
                pausar()
                
            elif escolha == "2":
                executar_coleta_dados()
                pausar()
                
            elif escolha == "3":
                executar_coleta_completa()
                pausar()
                
            elif escolha == "4":
                listar_arquivos_gerados()
                pausar()
                
            elif escolha == "5":
                limpar_dados_antigos()
                pausar()
                
            elif escolha == "6":
                mostrar_sobre()
                pausar()
                
            elif escolha == "7":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o Scraper Jasmine Alimentos!{Cores.RESET}")
                print(f"{Cores.CIANO}🥣 Até a próxima!{Cores.RESET}\n")
                break
                
            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 1-7{Cores.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")

if __name__ == "__main__":
    main() 