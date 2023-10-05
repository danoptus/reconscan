print("""

█▄▄▄▄ ▄███▄   ▄█▄    ████▄    ▄      ▄▄▄▄▄   ▄█▄    ██      ▄   
█  ▄▀ █▀   ▀  █▀ ▀▄  █   █     █    █     ▀▄ █▀ ▀▄  █ █      █  
█▀▀▌  ██▄▄    █   ▀  █   █ ██   █ ▄  ▀▀▀▀▄   █   ▀  █▄▄█ ██   █ 
█  █  █▄   ▄▀ █▄  ▄▀ ▀████ █ █  █  ▀▄▄▄▄▀    █▄  ▄▀ █  █ █ █  █ 
  █   ▀███▀   ▀███▀        █  █ █            ▀███▀     █ █  █ █ 
 ▀                         █   ██                     █  █   ██ 
                                                     ▀

                                            By D4n0PtU5
""")


import os
import subprocess

# Solicite o nome do domínio ao usuário
domain = input("Digite o nome do domínio: ")

# Lista de ferramentas a serem instaladas e seus comandos de verificação de versão
tools_to_install = [
    {"name": "subfinder", "command": "subfinder -version"},
    {"name": "assetfinder", "command": "assetfinder --version"},
    {"name": "paramspider", "command": "paramspider --version"},
    {"name": "httpx", "command": "httpx --version"},
    {"name": "nuclei", "command": "nuclei -version"},
]

def is_tool_installed(tool_info):
    try:
        subprocess.run([tool_info["command"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def is_tool_up_to_date(tool_info):
    try:
        installed_version = subprocess.check_output([tool_info["command"]], stderr=subprocess.STDOUT, shell=True).decode().strip()
        print(f"Versão instalada de {tool_info['name']}: {installed_version}")
        # Adicione uma lógica aqui para verificar se a versão está desatualizada
        # Você pode comparar installed_version com a versão desejada e decidir se precisa atualizar
        # Por exemplo, você pode verificar uma fonte de versão online
        return True  # Altere para False se a ferramenta estiver desatualizada
    except subprocess.CalledProcessError:
        return False

def install_tool(tool_info):
    tool_name = tool_info["name"]
    if is_tool_installed(tool_info):
        if not is_tool_up_to_date(tool_info):
            try:
                print(f"Atualizando {tool_name}...")
                subprocess.run(["go", "get", f"github.com/projectdiscovery/{tool_name}"])
                print(f"{tool_name} atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao atualizar {tool_name}: {str(e)}")
        else:
            print(f"{tool_name} já está instalado e atualizado.")
    else:
        try:
            print(f"Instalando {tool_name}...")
            subprocess.run(["go", "get", f"github.com/projectdiscovery/{tool_name}"])
            print(f"{tool_name} instalado com sucesso!")
        except Exception as e:
            print(f"Erro ao instalar {tool_name}: {str(e)}")

def main():
    # Solicite o nome do domínio ao usuário
    global domain
    domain = input("Digite o nome do domínio: ")

    # Instale as ferramentas que não estão instaladas ou que estão desatualizadas
    for tool_info in tools_to_install:
        install_tool(tool_info)

    # Execute o comando desejado com o nome do domínio fornecido pelo usuário
    try:
        subprocess.run(
            f'echo {domain} | subfinder -silent | assetfinder -subs-only | tee sub.txt; paramspider -l sub.txt; xargs -a sub.txt -I@ sh -c "paramspider -d @"; cat *.txt | tr -d "FUZZ" | anew | httpx -silent -timeout 60 | nuclei -t ~/nuclei-templates/ -severity low,medium,high,critical | notify',
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {str(e)}")

if __name__ == "__main__":
    main()
