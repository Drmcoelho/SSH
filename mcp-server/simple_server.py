#!/usr/bin/env python3
"""
Servidor MCP SSH - Versão Simplificada para Teste
Este é um servidor MCP funcional para demonstração do curso SSH
"""

import subprocess
import socket
import os
from pathlib import Path
import json

class SSHMCPServer:
    """Servidor MCP para ferramentas SSH"""
    
    def __init__(self):
        """Inicializa o servidor com as ferramentas disponíveis"""
        self.tools = {
            "check_ssh_connection": self.check_ssh_connection,
            "generate_ssh_config": self.generate_ssh_config, 
            "list_ssh_keys": self.list_ssh_keys,
            "ssh_security_audit": self.ssh_security_audit,
            "port_scanner": self.port_scanner
        }
        
    def check_ssh_connection(self, host="localhost", port=22, username=None):
        """Verifica se uma conexão SSH está disponível"""
        try:
            # Teste básico de socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return f"✅ Conexão SSH disponível em {host}:{port}"
            else:
                return f"❌ Porta {port} fechada ou inacessível em {host}"
                
        except Exception as e:
            return f"❌ Erro na verificação: {str(e)}"
    
    def list_ssh_keys(self):
        """Lista as chaves SSH disponíveis no sistema"""
        ssh_dir = Path.home() / ".ssh"
        
        if not ssh_dir.exists():
            return "❌ Diretório ~/.ssh não encontrado"
            
        keys_found = []
        key_types = ["id_rsa", "id_ed25519", "id_ecdsa", "id_dsa"]
        
        for key_type in key_types:
            private_key = ssh_dir / key_type
            public_key = ssh_dir / f"{key_type}.pub"
            
            if private_key.exists() and public_key.exists():
                keys_found.append(f"✅ {key_type} (completa)")
            elif public_key.exists():
                keys_found.append(f"🔸 {key_type}.pub (apenas pública)")
                
        if keys_found:
            return f"🔑 Chaves SSH encontradas:\\n" + "\\n".join(keys_found)
        else:
            return "❌ Nenhuma chave SSH encontrada em ~/.ssh/"
    
    def generate_ssh_config(self, host, hostname, user, port=22, key_file=None):
        """Gera uma configuração SSH para o arquivo ~/.ssh/config"""
        config_entry = f"""
Host {host}
    HostName {hostname}
    User {user}
    Port {port}"""
        
        if key_file:
            config_entry += f"\\n    IdentityFile ~/.ssh/{key_file}"
            
        config_entry += "\\n    ServerAliveInterval 60\\n    ServerAliveCountMax 3"
        
        return f"📝 Configuração SSH gerada:\\n{config_entry}"
    
    def ssh_security_audit(self):
        """Realiza uma auditoria básica de segurança SSH"""
        audit_results = []
        ssh_dir = Path.home() / ".ssh"
        
        # Verificar se existe diretório .ssh
        if not ssh_dir.exists():
            audit_results.append("❌ Diretório ~/.ssh não existe")
            return "\\n".join(audit_results)
        
        # Verificar permissões do diretório .ssh
        try:
            stat = ssh_dir.stat()
            perms = oct(stat.st_mode)[-3:]
            if perms == "700":
                audit_results.append("✅ Permissões do diretório ~/.ssh estão corretas (700)")
            else:
                audit_results.append(f"⚠️ Permissões do diretório ~/.ssh: {perms} (recomendado: 700)")
        except:
            audit_results.append("❌ Erro ao verificar permissões do diretório ~/.ssh")
        
        # Verificar chaves privadas
        for key_file in ["id_rsa", "id_ed25519", "id_ecdsa"]:
            key_path = ssh_dir / key_file
            if key_path.exists():
                try:
                    stat = key_path.stat()
                    perms = oct(stat.st_mode)[-3:]
                    if perms == "600":
                        audit_results.append(f"✅ Chave {key_file} com permissões corretas (600)")
                    else:
                        audit_results.append(f"⚠️ Chave {key_file} com permissões {perms} (recomendado: 600)")
                except:
                    audit_results.append(f"❌ Erro ao verificar permissões de {key_file}")
        
        # Verificar arquivo config
        config_file = ssh_dir / "config"
        if config_file.exists():
            try:
                stat = config_file.stat()
                perms = oct(stat.st_mode)[-3:]
                if perms in ["600", "644"]:
                    audit_results.append("✅ Arquivo config com permissões adequadas")
                else:
                    audit_results.append(f"⚠️ Arquivo config com permissões {perms}")
            except:
                audit_results.append("❌ Erro ao verificar permissões do arquivo config")
        
        return "🔒 Auditoria de Segurança SSH:\\n" + "\\n".join(audit_results)
    
    def port_scanner(self, host="localhost", start_port=20, end_port=80):
        """Escaneia portas abertas (versão educativa limitada)"""
        if end_port - start_port > 50:
            return "❌ Range de portas muito amplo. Máximo 50 portas por escaneamento."
            
        open_ports = []
        
        for port in range(start_port, end_port + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                continue
        
        if open_ports:
            return f"🔍 Portas abertas em {host}: {', '.join(map(str, open_ports))}"
        else:
            return f"🔍 Nenhuma porta aberta encontrada em {host} (range {start_port}-{end_port})"

def main():
    """Função principal para testes"""
    print("🚀 SSH MCP Server - Modo de Teste")
    print("=" * 50)
    
    server = SSHMCPServer()
    
    # Demonstrar todas as ferramentas
    print("🛠️ Ferramentas disponíveis:")
    for tool_name in server.tools.keys():
        print(f"  - {tool_name}")
    
    print("\\n🧪 Executando testes das ferramentas...")
    
    # Teste 1: Verificar conexão SSH
    print("\\n1. Verificando conexão SSH:")
    result = server.check_ssh_connection()
    print(f"   {result}")
    
    # Teste 2: Listar chaves SSH
    print("\\n2. Listando chaves SSH:")
    result = server.list_ssh_keys()
    print(f"   {result}")
    
    # Teste 3: Gerar configuração SSH
    print("\\n3. Gerando configuração SSH de exemplo:")
    result = server.generate_ssh_config("exemplo", "servidor.com", "usuario")
    print(f"   {result}")
    
    # Teste 4: Auditoria de segurança
    print("\\n4. Auditoria de segurança:")
    result = server.ssh_security_audit()
    print(f"   {result}")
    
    # Teste 5: Port scan limitado
    print("\\n5. Escaneamento de portas:")
    result = server.port_scanner("localhost", 20, 25)
    print(f"   {result}")
    
    print("\\n✨ Todos os testes concluídos!")

if __name__ == "__main__":
    main()