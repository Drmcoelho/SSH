# MCQs para MVP 1 - Fundamentos do SSH

## Questões de Múltipla Escolha para o Primeiro Módulo

### Pergunta 1: Conceito Básico do SSH

O que significa a sigla SSH e qual é seu principal objetivo?

a) Secure Shell - protocolo para transferência segura de arquivos  
b) Secure Shell - protocolo para comunicação segura e criptografada entre computadores  
c) System Shell - protocolo para acesso local ao sistema operacional  
d) Super Shell - protocolo para execução de comandos com privilégios elevados  

**Resposta Correta: b)**  
**Justificativa:** SSH significa Secure Shell e é um protocolo de rede criptográfico que permite comunicação segura entre dois computadores, substituindo protocolos inseguros como Telnet e rlogin.

---

### Pergunta 2: Conexão Básica

Qual comando é usado para iniciar uma conexão SSH com um servidor remoto no endereço `servidor.com` utilizando o nome de usuário `admin`?

a) `ssh admin@servidor.com`  
b) `connect admin@servidor.com`  
c) `ssh servidor.com -u admin`  
d) `telnet admin@servidor.com`  

**Resposta Correta: a)**  
**Justificativa:** O formato padrão do comando SSH é `ssh usuario@host`. As outras opções usam sintaxes incorretas ou comandos diferentes (como telnet, que não é seguro).

---

### Pergunta 3: Porta Padrão do SSH

Por padrão, o serviço SSH escuta em qual porta?

a) 21  
b) 22  
c) 23  
d) 80  

**Resposta Correta: b)**  
**Justificativa:** A porta padrão do SSH é 22. A porta 21 é do FTP, 23 é do Telnet e 80 é do HTTP.

---

### Pergunta 4: Primeira Conexão

Quando você se conecta a um servidor SSH pela primeira vez, o que acontece?

a) A conexão é automaticamente aceita sem verificação  
b) Você recebe um aviso sobre a autenticidade do host e deve confirmar  
c) O servidor rejeita automaticamente a primeira conexão  
d) É necessário reiniciar o cliente SSH  

**Resposta Correta: b)**  
**Justificativa:** Na primeira conexão, o SSH exibe a fingerprint da chave do servidor e pergunta se você deseja continuar conectando, adicionando a chave ao arquivo `known_hosts`.

---

### Pergunta 5: Geração de Chaves SSH

Para gerar um novo par de chaves SSH (pública e privada) utilizando o algoritmo moderno e seguro Ed25519, qual comando você executaria?

a) `ssh-keygen -t rsa -b 4096`  
b) `ssh-keygen -t ed25519`  
c) `ssh-add -t ed25519`  
d) `ssh-copy-id -t ed25519`  

**Resposta Correta: b)**  
**Justificativa:** O comando `ssh-keygen` é a ferramenta para criar chaves, e a flag `-t` especifica o tipo (algoritmo) da chave. Ed25519 é uma escolha excelente por sua segurança e performance.

---

### Pergunta 6: Localização das Chaves SSH

Por padrão, onde ficam armazenadas as chaves SSH do usuário em sistemas Unix/Linux?

a) `/etc/ssh/`  
b) `~/.ssh/`  
c) `/var/ssh/`  
d) `/usr/local/ssh/`  

**Resposta Correta: b)**  
**Justificativa:** As chaves SSH do usuário ficam no diretório `.ssh` dentro do diretório home do usuário (`~/.ssh/`). O diretório `/etc/ssh/` contém configurações do sistema.

---

### Pergunta 7: Arquivo de Configuração do Cliente

Em qual arquivo você pode configurar aliases e opções padrão para conexões SSH?

a) `/etc/ssh/sshd_config`  
b) `~/.ssh/authorized_keys`  
c) `~/.ssh/config`  
d) `~/.ssh/known_hosts`  

**Resposta Correta: c)**  
**Justificativa:** O arquivo `~/.ssh/config` é usado para configurações do cliente SSH por usuário, incluindo aliases, porta padrão, usuário, arquivo de chave, etc.

---

### Pergunta 8: Verificação de Conexão

Qual comando você usaria para testar se consegue se conectar a um servidor SSH sem executar comandos remotos?

a) `ssh -t usuario@servidor`  
b) `ssh -N usuario@servidor`  
c) `ssh -T usuario@servidor`  
d) `ssh -v usuario@servidor`  

**Resposta Correta: c)**  
**Justificativa:** A flag `-T` desabilita a alocação de pseudo-terminal, sendo útil para testes. A flag `-N` é para não executar comandos remotos (útil para port forwarding), e `-v` é para modo verbose.

---

### Pergunta 9: Transferência de Arquivos

Qual comando SSH você usaria para copiar um arquivo local chamado `documento.txt` para o diretório home de um servidor remoto?

a) `scp documento.txt usuario@servidor:/home/usuario/`  
b) `ssh cp documento.txt usuario@servidor:/home/usuario/`  
c) `sftp documento.txt usuario@servidor:/home/usuario/`  
d) `rsync documento.txt usuario@servidor:/home/usuario/`  

**Resposta Correta: a)**  
**Justificativa:** O comando `scp` (Secure Copy) é usado para transferir arquivos via SSH. A sintaxe é `scp origem destino`.

---

### Pergunta 10: Desconexão Segura

Qual é a maneira correta de encerrar uma sessão SSH?

a) Fechar a janela do terminal  
b) Pressionar Ctrl+C  
c) Digitar `exit` ou pressionar Ctrl+D  
d) Pressionar Ctrl+Z  

**Resposta Correta: c)**  
**Justificativa:** O comando `exit` ou Ctrl+D encerra a sessão SSH de forma adequada. Ctrl+C interrompe processos, Ctrl+Z suspende, e fechar a janela pode não encerrar a sessão adequadamente.

---

## Gabarito Resumido

1. b) Secure Shell - protocolo para comunicação segura e criptografada
2. a) `ssh admin@servidor.com`
3. b) 22
4. b) Você recebe um aviso sobre a autenticidade do host
5. b) `ssh-keygen -t ed25519`
6. b) `~/.ssh/`
7. c) `~/.ssh/config`
8. c) `ssh -T usuario@servidor`
9. a) `scp documento.txt usuario@servidor:/home/usuario/`
10. c) Digitar `exit` ou pressionar Ctrl+D

---

## Critérios de Avaliação Sugeridos

- **8-10 acertos:** Excelente compreensão dos fundamentos SSH
- **6-7 acertos:** Boa compreensão, revisar alguns conceitos
- **4-5 acertos:** Compreensão básica, necessário estudo adicional
- **0-3 acertos:** Revisão completa do módulo recomendada

## Observações para o Instrutor

Estas questões cobrem os conceitos essenciais do MVP 1:
- Conceitos básicos do SSH
- Comandos fundamentais
- Geração e localização de chaves
- Configuração básica
- Transferência de arquivos
- Boas práticas de conexão

As questões foram elaboradas para:
- Testar conhecimento prático, não apenas teórico
- Incluir pegadinhas comuns que iniciantes encontram
- Preparar para os conceitos mais avançados dos próximos MVPs