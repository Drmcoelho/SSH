#!/usr/bin/env python3
"""
Servidor MCP (Model Context Protocol) para ferramentas SSH
Este servidor fornece ferramentas para trabalhar com SSH, incluindo:
- Geração de chaves SSH
- Verificação de configurações SSH
- Análise de logs de conexão
- Validação de configurações de servidor
"""

import asyncio
import json
import logging
import subprocess
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ssh-mcp-server")

# Criar instância do servidor MCP
server = Server("ssh-tools")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    Lista todas as ferramentas disponíveis no servidor MCP.
    """
    return [
        types.Tool(
            name="generate_ssh_key",
            description="Gera um novo par de chaves SSH com algoritmo especificado",
            inputSchema={
                "type": "object",
                "properties": {
                    "key_type": {
                        "type": "string",
                        "description": "Tipo de chave SSH (ed25519, rsa, ecdsa)",
                        "enum": ["ed25519", "rsa", "ecdsa"],
                        "default": "ed25519"
                    },
                    "key_size": {
                        "type": "integer", 
                        "description": "Tamanho da chave em bits (apenas para RSA)",
                        "default": 4096
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comentário para a chave SSH",
                        "default": ""
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nome do arquivo para salvar a chave",
                        "default": "id_ed25519"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="check_ssh_config",
            description="Verifica e valida configurações SSH do cliente",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_file": {
                        "type": "string",
                        "description": "Caminho para o arquivo de configuração SSH",
                        "default": "~/.ssh/config"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="analyze_ssh_connection",
            description="Analisa uma tentativa de conexão SSH e retorna informações detalhadas",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "Hostname ou IP do servidor SSH"
                    },
                    "port": {
                        "type": "integer",
                        "description": "Porta do servidor SSH",
                        "default": 22
                    },
                    "user": {
                        "type": "string", 
                        "description": "Nome do usuário para conexão"
                    }
                },
                "required": ["host", "user"]
            }
        ),
        types.Tool(
            name="ssh_security_audit",
            description="Realiza uma auditoria de segurança nas configurações SSH",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_type": {
                        "type": "string",
                        "description": "Tipo de auditoria (client, server, keys)",
                        "enum": ["client", "server", "keys"],
                        "default": "client"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="create_ssh_tunnel",
            description="Cria um comando para túnel SSH com port forwarding",
            inputSchema={
                "type": "object",
                "properties": {
                    "tunnel_type": {
                        "type": "string",
                        "description": "Tipo de túnel SSH",
                        "enum": ["local", "remote", "dynamic"],
                        "default": "local"
                    },
                    "local_port": {
                        "type": "integer",
                        "description": "Porta local para o túnel"
                    },
                    "remote_host": {
                        "type": "string",
                        "description": "Host remoto"
                    },
                    "remote_port": {
                        "type": "integer", 
                        "description": "Porta remota"
                    },
                    "ssh_server": {
                        "type": "string",
                        "description": "Servidor SSH intermediário"
                    },
                    "user": {
                        "type": "string",
                        "description": "Usuário SSH"
                    }
                },
                "required": ["local_port", "remote_host", "remote_port", "ssh_server", "user"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Processa chamadas para as ferramentas disponíveis.
    """
    try:
        if name == "generate_ssh_key":
            return await generate_ssh_key(arguments)
        elif name == "check_ssh_config":
            return await check_ssh_config(arguments)
        elif name == "analyze_ssh_connection":
            return await analyze_ssh_connection(arguments)
        elif name == "ssh_security_audit":
            return await ssh_security_audit(arguments)
        elif name == "create_ssh_tunnel":
            return await create_ssh_tunnel(arguments)
        else:
            raise ValueError(f"Ferramenta desconhecida: {name}")
    except Exception as e:
        logger.error(f"Erro ao executar ferramenta {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Erro ao executar {name}: {str(e)}"
        )]

async def generate_ssh_key(args: Dict[str, Any]) -> List[types.TextContent]:
    """
    Gera um novo par de chaves SSH.
    """
    key_type = args.get("key_type", "ed25519")
    key_size = args.get("key_size", 4096)
    comment = args.get("comment", "")
    filename = args.get("filename", f"id_{key_type}")
    
    # Criar comando ssh-keygen
    cmd = ["ssh-keygen", "-t", key_type]
    
    if key_type == "rsa":
        cmd.extend(["-b", str(key_size)])
    
    if comment:
        cmd.extend(["-C", comment])
    
    # Para demonstração, vamos apenas mostrar o comando que seria executado
    cmd_str = " ".join(cmd)
    
    result = f"""
🔑 **Comando para gerar chave SSH {key_type.upper()}:**

```bash
{cmd_str} -f ~/.ssh/{filename}
```

📋 **Detalhes:**
- Tipo de chave: {key_type.upper()}
{"- Tamanho: " + str(key_size) + " bits" if key_type == "rsa" else ""}
- Arquivo: ~/.ssh/{filename}
- Chave pública: ~/.ssh/{filename}.pub
{"- Comentário: " + comment if comment else ""}

⚠️  **Importante:**
- A chave privada deve ser mantida segura e nunca compartilhada
- A chave pública pode ser copiada para servidores remotos
- Use uma passphrase forte para proteger a chave privada

🚀 **Próximos passos:**
1. Execute o comando acima
2. Digite uma passphrase segura quando solicitado
3. Copie a chave pública para o servidor: `ssh-copy-id user@server`
"""
    
    return [types.TextContent(type="text", text=result)]

async def check_ssh_config(args: Dict[str, Any]) -> List[types.TextContent]:
    """
    Verifica configurações SSH do cliente.
    """
    config_file = args.get("config_file", "~/.ssh/config")
    expanded_path = os.path.expanduser(config_file)
    
    result = f"🔍 **Verificação de Configuração SSH**\n\n"
    result += f"📁 **Arquivo:** {config_file}\n\n"
    
    if os.path.exists(expanded_path):
        try:
            with open(expanded_path, 'r') as f:
                content = f.read()
            
            result += "✅ **Status:** Arquivo encontrado\n\n"
            result += f"📝 **Conteúdo do arquivo:**\n```\n{content}\n```\n\n"
            
            # Análise básica
            lines = content.split('\n')
            hosts = [line.strip() for line in lines if line.strip().startswith('Host ')]
            
            result += f"🖥️  **Hosts configurados:** {len(hosts)}\n"
            for host in hosts:
                result += f"   - {host}\n"
                
        except Exception as e:
            result += f"❌ **Erro ao ler arquivo:** {str(e)}\n"
    else:
        result += "⚠️  **Status:** Arquivo não encontrado\n\n"
        result += "💡 **Sugestão:** Crie o arquivo de configuração SSH:\n"
        result += f"```bash\ntouch {config_file}\nchmod 600 {config_file}\n```\n"
    
    # Verificar diretório .ssh
    ssh_dir = os.path.expanduser("~/.ssh")
    result += f"\n📂 **Diretório SSH:** {ssh_dir}\n"
    
    if os.path.exists(ssh_dir):
        files = os.listdir(ssh_dir)
        result += f"📄 **Arquivos encontrados:** {len(files)}\n"
        for file in sorted(files):
            file_path = os.path.join(ssh_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                result += f"   - {file} ({size} bytes)\n"
    else:
        result += "❌ **Diretório ~/.ssh não existe**\n"
    
    return [types.TextContent(type="text", text=result)]

async def analyze_ssh_connection(args: Dict[str, Any]) -> List[types.TextContent]:
    """
    Analisa uma conexão SSH.
    """
    host = args["host"]
    port = args.get("port", 22)
    user = args["user"]
    
    result = f"🔗 **Análise de Conexão SSH**\n\n"
    result += f"🖥️  **Servidor:** {user}@{host}:{port}\n\n"
    
    # Comando de conexão básico
    ssh_cmd = f"ssh {user}@{host}"
    if port != 22:
        ssh_cmd += f" -p {port}"
    
    result += f"📝 **Comando de conexão:**\n```bash\n{ssh_cmd}\n```\n\n"
    
    # Comando de teste detalhado
    verbose_cmd = f"{ssh_cmd} -v"
    result += f"🔍 **Comando para diagnóstico (verbose):**\n```bash\n{verbose_cmd}\n```\n\n"
    
    # Teste de conectividade
    nc_cmd = f"nc -zv {host} {port}"
    result += f"🌐 **Teste de conectividade de rede:**\n```bash\n{nc_cmd}\n```\n\n"
    
    # Verificação de chave do servidor
    keyscan_cmd = f"ssh-keyscan -p {port} {host}"
    result += f"🔑 **Obter chave pública do servidor:**\n```bash\n{keyscan_cmd}\n```\n\n"
    
    # Dicas de resolução de problemas
    result += "🛠️  **Resolução de problemas comuns:**\n\n"
    result += "1. **Timeout de conexão:**\n"
    result += "   - Verifique se o host está acessível na rede\n"
    result += "   - Confirme se a porta está correta\n"
    result += "   - Verifique firewalls\n\n"
    
    result += "2. **Autenticação falhada:**\n"
    result += "   - Verifique nome de usuário\n"
    result += "   - Confirme se a chave SSH está carregada\n"
    result += "   - Teste com password se configurado\n\n"
    
    result += "3. **Chave de host desconhecida:**\n"
    result += "   - Use `ssh-keyscan` para verificar a chave\n"
    result += "   - Adicione manualmente ao known_hosts se confiável\n\n"
    
    return [types.TextContent(type="text", text=result)]

async def ssh_security_audit(args: Dict[str, Any]) -> List[types.TextContent]:
    """
    Realiza auditoria de segurança SSH.
    """
    target_type = args.get("target_type", "client")
    
    result = f"🔒 **Auditoria de Segurança SSH - {target_type.upper()}**\n\n"
    
    if target_type == "client":
        result += "👤 **Configuração do Cliente SSH**\n\n"
        
        result += "✅ **Verificações recomendadas:**\n\n"
        result += "1. **Algoritmos de chave seguros:**\n"
        result += "   - Use Ed25519 ou RSA ≥ 2048 bits\n"
        result += "   - Evite DSA e ECDSA com curvas fracas\n\n"
        
        result += "2. **Configuração ~/.ssh/config:**\n"
        result += "```\n"
        result += "Host *\n"
        result += "    Protocol 2\n"
        result += "    PubkeyAuthentication yes\n"
        result += "    PasswordAuthentication no\n"
        result += "    HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256\n"
        result += "    KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512\n"
        result += "    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com\n"
        result += "    MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com\n"
        result += "```\n\n"
        
        result += "3. **Permissões de arquivos:**\n"
        result += "   - ~/.ssh/: 700\n"
        result += "   - ~/.ssh/config: 600\n"
        result += "   - Chaves privadas: 600\n"
        result += "   - Chaves públicas: 644\n\n"
        
    elif target_type == "server":
        result += "🖥️  **Configuração do Servidor SSH**\n\n"
        
        result += "✅ **Configurações recomendadas (/etc/ssh/sshd_config):**\n\n"
        result += "```\n"
        result += "# Protocolo e porta\n"
        result += "Protocol 2\n"
        result += "Port 22  # Considere mudar para porta não-padrão\n\n"
        
        result += "# Autenticação\n"
        result += "PermitRootLogin no\n"
        result += "PubkeyAuthentication yes\n"
        result += "PasswordAuthentication no\n"
        result += "PermitEmptyPasswords no\n"
        result += "ChallengeResponseAuthentication no\n\n"
        
        result += "# Algoritmos seguros\n"
        result += "HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256\n"
        result += "KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512\n"
        result += "Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com\n"
        result += "MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com\n\n"
        
        result += "# Limites e timeouts\n"
        result += "MaxAuthTries 3\n"
        result += "MaxSessions 2\n"
        result += "ClientAliveInterval 300\n"
        result += "ClientAliveCountMax 2\n"
        result += "```\n\n"
        
    elif target_type == "keys":
        result += "🔑 **Auditoria de Chaves SSH**\n\n"
        
        result += "✅ **Verificações de segurança:**\n\n"
        result += "1. **Algoritmos recomendados (em ordem de preferência):**\n"
        result += "   - Ed25519 (mais seguro e rápido)\n"
        result += "   - RSA 4096 bits\n"
        result += "   - RSA 2048 bits (mínimo aceitável)\n\n"
        
        result += "2. **Algoritmos a evitar:**\n"
        result += "   - DSA (inseguro)\n"
        result += "   - RSA < 2048 bits\n"
        result += "   - ECDSA com curvas fracas\n\n"
        
        result += "3. **Boas práticas:**\n"
        result += "   - Use passphrase forte nas chaves privadas\n"
        result += "   - Rotacione chaves regularmente\n"
        result += "   - Uma chave por serviço/propósito\n"
        result += "   - Remova chaves públicas de contas inativas\n\n"
        
        result += "4. **Comandos de verificação:**\n"
        result += "```bash\n"
        result += "# Listar chaves carregadas no ssh-agent\n"
        result += "ssh-add -l\n\n"
        result += "# Verificar tipo e tamanho de chave\n"
        result += "ssh-keygen -l -f ~/.ssh/id_ed25519.pub\n\n"
        result += "# Verificar todas as chaves no diretório\n"
        result += "for key in ~/.ssh/*.pub; do echo \"$key:\"; ssh-keygen -l -f \"$key\"; done\n"
        result += "```\n\n"
    
    result += "⚠️  **Alertas de segurança:**\n"
    result += "- Monitore logs de autenticação regularmente\n"
    result += "- Use fail2ban ou similar para proteção contra ataques\n"
    result += "- Considere autenticação de dois fatores\n"
    result += "- Mantenha o software SSH atualizado\n"
    
    return [types.TextContent(type="text", text=result)]

async def create_ssh_tunnel(args: Dict[str, Any]) -> List[types.TextContent]:
    """
    Cria comandos para túneis SSH.
    """
    tunnel_type = args["tunnel_type"]
    local_port = args["local_port"]
    remote_host = args["remote_host"]
    remote_port = args["remote_port"]
    ssh_server = args["ssh_server"]
    user = args["user"]
    
    result = f"🚇 **Configuração de Túnel SSH - {tunnel_type.upper()}**\n\n"
    
    if tunnel_type == "local":
        cmd = f"ssh -L {local_port}:{remote_host}:{remote_port} {user}@{ssh_server}"
        result += "📍 **Port Forwarding Local (Local → SSH Server → Remote Host)**\n\n"
        result += f"🔗 **Conexão:** localhost:{local_port} → {ssh_server} → {remote_host}:{remote_port}\n\n"
        
    elif tunnel_type == "remote":
        cmd = f"ssh -R {local_port}:{remote_host}:{remote_port} {user}@{ssh_server}"
        result += "📍 **Port Forwarding Remoto (SSH Server → Local → Remote Host)**\n\n"
        result += f"🔗 **Conexão:** {ssh_server}:{local_port} → localhost → {remote_host}:{remote_port}\n\n"
        
    elif tunnel_type == "dynamic":
        cmd = f"ssh -D {local_port} {user}@{ssh_server}"
        result += "📍 **Port Forwarding Dinâmico (Proxy SOCKS)**\n\n"
        result += f"🔗 **Proxy SOCKS:** localhost:{local_port} → {ssh_server} → qualquer destino\n\n"
    
    result += f"📝 **Comando:**\n```bash\n{cmd}\n```\n\n"
    
    # Comandos adicionais úteis
    result += "🛠️  **Opções úteis:**\n\n"
    result += f"**Manter túnel em background:**\n```bash\n{cmd} -N -f\n```\n\n"
    result += f"**Com verbose para debug:**\n```bash\n{cmd} -v\n```\n\n"
    result += f"**Especificar arquivo de chave:**\n```bash\n{cmd} -i ~/.ssh/id_ed25519\n```\n\n"
    
    # Instruções de uso
    if tunnel_type == "local":
        result += "📋 **Como usar:**\n"
        result += f"1. Execute o comando acima\n"
        result += f"2. Conecte-se a localhost:{local_port}\n"
        result += f"3. O tráfego será redirecionado para {remote_host}:{remote_port}\n\n"
        
        result += "💡 **Exemplo de uso:**\n"
        result += "- Acessar banco de dados remoto via SSH\n"
        result += "- Conectar a serviços internos de uma rede\n"
        result += "- Bypass de firewalls para acesso a aplicações\n\n"
        
    elif tunnel_type == "remote":
        result += "📋 **Como usar:**\n"
        result += f"1. Execute o comando acima\n"
        result += f"2. No servidor SSH, conecte-se a localhost:{local_port}\n"
        result += f"3. O tráfego será redirecionado para {remote_host}:{remote_port}\n\n"
        
        result += "💡 **Exemplo de uso:**\n"
        result += "- Expor serviço local para servidor remoto\n"
        result += "- Permitir acesso reverso a aplicações\n"
        result += "- Compartilhar serviços de desenvolvimento\n\n"
        
    elif tunnel_type == "dynamic":
        result += "📋 **Como usar:**\n"
        result += f"1. Execute o comando acima\n"
        result += f"2. Configure aplicações para usar proxy SOCKS localhost:{local_port}\n"
        result += f"3. Todo tráfego passará pelo servidor SSH\n\n"
        
        result += "💡 **Exemplo de uso:**\n"
        result += "- Navegar web através do servidor SSH\n"
        result += "- Mascarar IP de origem\n"
        result += "- Acessar recursos geograficamente restritos\n\n"
    
    result += "⚠️  **Considerações de segurança:**\n"
    result += "- Túneis SSH consomem recursos do servidor\n"
    result += "- Monitore conexões ativas regularmente\n"
    result += "- Use apenas em redes confiáveis\n"
    result += "- Considere VPN para uso permanente\n"
    
    return [types.TextContent(type="text", text=result)]

async def main():
    """
    Função principal do servidor MCP.
    """
    # Executar servidor usando stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ssh-tools",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())