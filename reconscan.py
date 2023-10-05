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

    # Instale as ferramentas que não estão instaladas ou que estão desatualizadas
    for tool_info in tools_to_install:
        install_tool(tool_info)

    # Solicite o nome do domínio ao usuário
    global domain
    domain = input("Digite o nome do domínio: ")
  
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
