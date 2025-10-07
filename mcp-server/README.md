# SSH MCP Server

## 🚀 Servidor Model Context Protocol para Demonstração SSH

Este servidor MCP foi criado como parte do **MVP 6 - MVPs Surpreendentes** do curso de SSH, demonstrando como conectar ferramentas modernas de IA (como Claude) com conceitos e ferramentas SSH.

## 📋 O que é este servidor?

O **Model Context Protocol (MCP)** é um protocolo desenvolvido pela Anthropic que permite que Large Language Models (LLMs) se conectem de forma segura a ferramentas e fontes de dados externas. Este servidor específico oferece:

### 🛠️ Ferramentas Disponíveis

1. **check_ssh_connection** - Verifica se uma conexão SSH está funcionando
2. **generate_ssh_config** - Gera configurações SSH automaticamente
3. **list_ssh_keys** - Lista chaves SSH do sistema
4. **ssh_security_audit** - Realiza auditoria de segurança SSH
5. **port_scanner** - Escaneia portas abertas (versão educativa)

### 📚 Recursos Informativos

- **ssh_best_practices** - Melhores práticas de segurança SSH
- **ssh_troubleshooting** - Guia de solução de problemas
- **ssh_algorithms** - Informações sobre algoritmos de criptografia

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip

### Passo a Passo

1. **Clone/Navegue para o diretório:**
   ```bash
   cd /workspaces/SSH/mcp-server
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o servidor:**
   ```bash
   python server.py
   ```

4. **Para modo debug:**
   ```bash
   python server.py --debug
   ```

## 🔌 Como Conectar ao Claude

Para usar este servidor MCP com Claude Desktop, adicione a seguinte configuração ao seu arquivo de configuração:

### macOS
Arquivo: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Arquivo: `%APPDATA%\Claude\claude_desktop_config.json`

### Linux
Arquivo: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ssh-tools": {
      "command": "python",
      "args": ["/caminho/para/workspaces/SSH/mcp-server/server.py"],
      "env": {}
    }
  }
}
```

## 💡 Exemplos de Uso

Depois de conectado, você pode usar comandos como:

- "Verifique se posso me conectar ao servidor example.com"
- "Gere uma configuração SSH para meu servidor de produção"
- "Liste minhas chaves SSH disponíveis"
- "Faça uma auditoria de segurança das minhas configurações SSH"
- "Escaneie as portas abertas no localhost"

## 🎯 Propósito Educativo

Este servidor foi criado especificamente para demonstrar:

1. **Integração Moderna**: Como ferramentas clássicas (SSH) se integram com IA moderna
2. **Automação**: Como automatizar tarefas SSH através de IA
3. **Segurança**: Boas práticas de segurança em ambientes automatizados
4. **Prototipagem**: Como criar ferramentas MCP personalizadas

## ⚠️ Avisos de Segurança

- Este servidor é **apenas para fins educativos**
- Não execute em ambientes de produção sem revisão de segurança
- Algumas ferramentas podem expor informações do sistema
- Use apenas em ambientes controlados e seguros

## 🧪 Teste das Funcionalidades

Você pode testar cada ferramenta individualmente:

```bash
# Teste de conexão
python -c "from server import check_ssh_connection; print(check_ssh_connection('localhost', 22, 'seu_usuario'))"

# Listar chaves SSH
python -c "from server import list_ssh_keys; print(list_ssh_keys())"
```

## 📖 Estrutura do Projeto

```
mcp-server/
├── server.py              # Servidor MCP principal
├── requirements.txt       # Dependências Python
├── package.json          # Configuração do projeto
├── README.md             # Este arquivo
└── examples/             # Exemplos de uso
    └── test_connection.py
```

## 🤝 Contribuição

Este é um projeto educativo! Sinta-se à vontade para:

- Adicionar novas ferramentas SSH
- Melhorar a documentação
- Reportar bugs ou problemas
- Sugerir melhorias de segurança

## 📚 Links Úteis

- [Documentação oficial do MCP](https://modelcontextprotocol.io/)
- [Repositório MCP no GitHub](https://github.com/modelcontextprotocol)
- [Manual SSH](https://man.openbsd.org/ssh.1)

---

**Criado com 💻 para o Curso SSH - MVP 6: MVPs Surpreendentes**