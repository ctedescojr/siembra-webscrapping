# Web Scraping - Loja Dimensional

Este projeto realiza um web scraping da loja [Dimensional](https://www.dimensional.com.br/material-eletrico), capturando todos os **nomes de produtos** e **preços** da seção de materiais elétricos, mesmo com carregamento dinâmico e rolagem infinita.

O resultado é salvo em um arquivo Excel com o nome `dimensional_YYYY-MM-DD.xlsx`, representando a data da extração.

---

## 🔧 Requisitos

* Python 3.8+
* Google Chrome instalado
* ChromeDriver compatível com a versão do Chrome
* Virtualenv (opcional, mas recomendado)

---

## 📦 Instalação e Execução

### 1. Clone o repositório (ou copie os arquivos para sua máquina)

```bash
git clone https://github.com/seu-usuario/webscraping-dimensional.git
cd webscraping-dimensional
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

---

## ✅ O que o script faz

1. Acessa a página inicial de materiais elétricos da loja Dimensional.
2. Rola a página automaticamente até carregar todos os produtos visíveis.
3. Clica no botão "Mostrar mais" sempre que estiver disponível.
4. Extrai o nome e o preço de cada produto encontrado.
5. Salva os dados em um arquivo `.xlsx` com o nome `dimensional_YYYY-MM-DD.xlsx`.

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

## 📄 Licença

Este projeto é de uso livre para fins educacionais e profissionais. Verifique a política de uso da loja antes de redistribuir os dados coletados.
