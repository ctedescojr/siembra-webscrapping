[English](#english) | [Português](#portugues)

<a name="english"></a>
# Web Scraping - Dimensional and Nortel Stores (English Version)

This project performs web scraping of the [Dimensional](https://www.dimensional.com.br/material-eletrico) and [Nortel](https://www.nortel.com.br) stores, capturing all **product names** and **prices** from the electrical materials section, even with dynamic loading and infinite scrolling.

The result is saved in an Excel file named `dimensional/nortel_YYYY-MM-DD.xlsx`, representing the extraction date.

---

## 🔧 Requirements

*   Python 3.13.2
*   Google Chrome installed
*   ChromeDriver compatible with your Chrome version
*   Virtualenv (optional, but recommended)

---

## 📦 Installation and Execution

### 1. Clone the repository (or copy the files to your machine)

```bash
git clone https://github.com/ctedescojr/siembra-webscrapping.git
cd siembra-webscraping
```

### 2. Create and activate a virtual environment (optional, but recommended)

```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

Install:

```bash
pip install -r requirements.txt
```

### 4. Download ChromeDriver

*   Access: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
*   Check your Chrome version and download the **corresponding ChromeDriver**
*   Extract the file and **copy the full path**
*   Replace in the script:

    ```python
    service = Service('C:/PATH/TO/YOUR/chromedriver.exe')
    ```

### 5. Execute the script

```bash
python dimensional.py
```
Or

```bash
python nortel.py
```

---

## ✅ What the script does

1.  Accesses the initial electrical materials page of the Dimensional store.
2.  Automatically scrolls the page until all visible products are loaded.
3.  Clicks the "Show more" button whenever available.
4.  Extracts the name and price of each product found.
5.  Saves the data to an `.xlsx` file named `dimensional/nortel_YYYY-MM-DD.xlsx`.

---

## 📝 Example Output

| Product                                           | Price     |
| ------------------------------------------------- | --------- |
| Fita Isolante Scotch 33+ 19MMx20M HB004482483 3M  | R\$ 24,99 |
| Disjuntor Mini Bipolar 20A 400VCA C 3KA EZ9F33220 | R\$ 31,99 |

---

## 📌 Notes

*   The script may take a few minutes depending on your connection and the quantity of available products.
*   It is important to keep `ChromeDriver` updated according to your Chrome version.
*   You can schedule daily script execution with **Task Scheduler (Windows)** or **cron (Linux/macOS)**.

---

### 6. Creating an Executable (Windows)

You can package the GUI application into a single executable (`.exe`) file for Windows using PyInstaller.

#### Prerequisites:
*   Ensure you have PyInstaller installed:
    ```bash
    pip install pyinstaller
    ```
*   Have the icon files `exe_icon.ico` and `favicon.ico` in the `resource/img/` folder.

#### Command to create the executable:

Execute the following command in the project's root directory:

```bash
pyinstaller --onefile ^
    --add-data "chromedriver-win64/chromedriver.exe;chromedriver-win64/" ^
    --add-data "resource/img/favicon.ico;resource/img/" ^
    --windowed ^
    --icon="resource/img/exe_icon.ico" ^
    script_runner_gui_refactor.py
```

*   `--onefile`: Packages everything into a single `.exe` file.
*   `--add-data "source;destination"`: Includes additional files.
    *   `chromedriver-win64/chromedriver.exe`: The ChromeDriver executable.
    *   `resource/img/favicon.ico`: The icon for the Tkinter window.
*   `--windowed`: Prevents a black console window from appearing when starting the GUI.
*   `--icon="resource/img/exe_icon.ico"`: Sets the icon of the generated `.exe` file.
*   `script_runner_gui_refactor.py`: The main script of your refactored GUI application.

#### Where to find the executable:

After successful execution, the `.exe` file will be generated in the `dist/` folder. The file name will be `script_runner_gui_refactor.exe` (or similar, depending on PyInstaller's configuration).

## 📄 License

This project is free to use for educational and professional purposes. Please check the store's usage policy before redistributing collected data.

<a name="portugues"></a>
# Web Scraping - Lojas Dimensional e Nortel (Versão Portuguesa)

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
Ou

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

*   `--onefile`: Empacota tudo em um único arquivo `.exe`.
*   `--add-data "source;destination"`: Inclui arquivos adicionais.
    *   `chromedriver-win64/chromedriver.exe`: O executável do ChromeDriver.
    *   `resource/img/favicon.ico`: O ícone para a janela Tkinter.
*   `--windowed`: Impede que uma janela de console preta apareça ao iniciar a GUI.
*   `--icon="resource/img/exe_icon.ico"`: Define o ícone do arquivo `.exe` gerado.
*   `script_runner_gui_refactor.py`: O script principal da sua aplicação GUI refatorada.

#### Onde encontrar o executável:

Após a execução bem-sucedida, o arquivo `.exe` será gerado na pasta `dist/`. O nome do arquivo será `script_runner_gui_refactor.exe` (ou similar, dependendo da configuração do PyInstaller).

## 📄 Licença

Este projeto é de uso livre para fins educacionais e profissionais. Verifique a política de uso da loja antes de redistribuir os dados coletados.
