# Web Scraping - Loja Dimensional e Nortel

Este projeto realiza um web scraping da loja [Dimensional](https://www.dimensional.com.br/material-eletrico) e [Nortel] (https://www.nortel.com.br) capturando todos os **nomes de produtos** e **preços** da seção de materiais elétricos, mesmo com carregamento dinâmico e rolagem infinita.

O resultado é salvo em um arquivo Excel com o nome `dimensional/nortel_YYYY-MM-DD.xlsx`, representando a data da extração.

---

## 🔧 Requisitos

* Python 3.13.2
* Google Chrome instalado
* ChromeDriver compatível com a versão do Chrome
* Virtualenv (opcional, mas recomendado)

---

## 📦 Instalação e Execução

### 1. Clone o repositório (ou copie os arquivos para sua máquina)

```bash
git clone https://github.com/ctedescojr/siembra-webscrapping.git
cd siembra-webscraping
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Instale as dependências

Instale:

```bash
pip install -r requirements.txt
```

### 4. Baixe o ChromeDriver

* Acesse: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
* Verifique a versão do seu Chrome e baixe o **ChromeDriver correspondente**
* Extraia o arquivo e **copie o caminho completo**
* Substitua no script:

  ```python
  service = Service('C:/CAMINHO/DO/SEU/chromedriver.exe')
  ```

### 5. Execute o script

```bash
python dimensional.py
```
# Ou

```bash
python nortel.py
```

---

## ✅ O que o script faz

1. Acessa a página inicial de materiais elétricos da loja Dimensional.
2. Rola a página automaticamente até carregar todos os produtos visíveis.
3. Clica no botão "Mostrar mais" sempre que estiver disponível.
4. Extrai o nome e o preço de cada produto encontrado.
5. Salva os dados em um arquivo `.xlsx` com o nome `dimensional/nortel_YYYY-MM-DD.xlsx`.

---

## 📝 Exemplo de saída

| Produto                                           | Preço     |
| ------------------------------------------------- | --------- |
| Fita Isolante Scotch 33+ 19MMx20M HB004482483 3M  | R\$ 24,99 |
| Disjuntor Mini Bipolar 20A 400VCA C 3KA EZ9F33220 | R\$ 31,99 |

---

## 📌 Observações

* O script pode levar alguns minutos dependendo da sua conexão e da quantidade de produtos disponíveis.
* É importante manter o `ChromeDriver` sempre atualizado conforme sua versão do Chrome.
* Você pode agendar a execução diária do script com o **Task Scheduler (Windows)** ou **cron (Linux/macOS)**.

---

### 6. Criando um Executável (Windows)

Você pode empacotar a aplicação GUI em um único arquivo executável (`.exe`) para Windows usando PyInstaller.

#### Pré-requisitos:
*   Certifique-se de ter o PyInstaller instalado:
    ```bash
    pip install pyinstaller
    ```
*   Tenha os arquivos de ícone `exe_icon.ico` e `favicon.ico` na pasta `resource/img/`.

#### Comando para criar o executável:

Execute o seguinte comando no diretório raiz do projeto:

```bash
pyinstaller --onefile ^
    --add-data "chromedriver-win64/chromedriver.exe;chromedriver-win64/" ^
    --add-data "resource/img/favicon.ico;resource/img/" ^
    --windowed ^
    --icon="resource/img/exe_icon.ico" ^
    script_runner_gui_refactor.py
```

- `--onefile`: Empacota tudo em um único arquivo `.exe`.

- `--add-data "source;destination"`: Inclui arquivos adicionais.

  - `chromedriver-win64/chromedriver.exe`: O executável do ChromeDriver.
  - `resource/img/favicon.ico`: O ícone para a janela Tkinter.

- `--windowed`: Impede que uma janela de console preta apareça ao iniciar a GUI.

- `--icon="resource/img/exe_icon.ico"`: Define o ícone do arquivo `.exe` gerado.

- `script_runner_gui_refactor.py`: O script principal da sua aplicação GUI refatorada.

#### Onde encontrar o executável:

Após a execução bem-sucedida, o arquivo `.exe` será gerado na pasta `dist/`. O nome do arquivo será `script_runner_gui_refactor.exe` (ou similar, dependendo da configuração do PyInstaller).

## 📄 Licença

Este projeto é de uso livre para fins educacionais e profissionais. Verifique a política de uso da loja antes de redistribuir os dados coletados.
