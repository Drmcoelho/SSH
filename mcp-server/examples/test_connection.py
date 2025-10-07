#!/usr/bin/env python3
"""
Exemplo de teste de conexão SSH para demonstração
Parte do curso SSH - MVP 6
"""

import sys
import socket
import subprocess
from pathlib import Path

def test_ssh_connection(host="localhost", port=22, timeout=5):
    """
    Testa uma conexão SSH básica
    """
    print(f"🔌 Testando conexão SSH para {host}:{port}")
    
    try:
        # Teste básico de socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Porta {port} está aberta em {host}")
            return True
        else:
            print(f"❌ Não foi possível conectar em {host}:{port}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def list_local_ssh_keys():
    """
    Lista chaves SSH locais
    """
    print("🔑 Chaves SSH encontradas:")
    
    ssh_dir = Path.home() / ".ssh"
    if not ssh_dir.exists():
        print("❌ Diretório ~/.ssh não encontrado")
        return []
    
    key_files = []
    for key_type in ["id_rsa", "id_ed25519", "id_ecdsa"]:
        private_key = ssh_dir / key_type
        public_key = ssh_dir / f"{key_type}.pub"
        
        if private_key.exists() and public_key.exists():
            print(f"✅ {key_type} (privada e pública)")
            key_files.append(key_type)
        elif public_key.exists():
            print(f"🔸 {key_type}.pub (apenas pública)")
    
    if not key_files:
        print("❌ Nenhuma chave SSH encontrada")
    
    return key_files

def check_ssh_service():
    """
    Verifica se o serviço SSH está rodando localmente
    """
    print("🔍 Verificando serviço SSH local...")
    
    try:
        # Tenta verificar se o sshd está rodando
        result = subprocess.run(
            ["pgrep", "-f", "sshd"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Serviço SSH está rodando")
            return True
        else:
            print("❌ Serviço SSH não está rodando")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar serviço: {e}")
        return False

def main():
    """
    Função principal de teste
    """
    print("🚀 Teste do Servidor MCP SSH")
    print("=" * 40)
    
    # Testes básicos
    test_ssh_connection()
    print()
    
    list_local_ssh_keys()
    print()
    
    check_ssh_service()
    print()
    
    print("✨ Teste concluído!")

if __name__ == "__main__":
    main()