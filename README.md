# 📈 Módulo de Estudo de Correlação

Bem-vindo ao repositório de estudo de correlação do projeto PRECORSIA. Neste módulo você encontrará Jupyter Notebooks contendo scripts para analisar a correlação entre as variáveis do sistema e outros estudos para testes e validações de hipóteses.

## 📚 Notebooks Disponíveis

1. [Análise de correlação entre Temperatura e Cobertura Vegetal](https://github.com/PRECORSIA/precorsia-computedocs/blob/main/temperature-vegetation.ipynb)

## 💡 Como Utilizar

1. Clone este repositório para a sua máquina local.
2. Abra o Jupyter Notebook.
3. Escolha o notebook relevante para a análise que deseja realizar.
4. Faça uma cópia deste notebook para o seu ambiente de desenvolvimento.
5. Certifique-se de que você tem todas as dependências necessárias instaladas. Você pode fazê-lo executando o seguinte comando em seu ambiente:
        `pip install numpy matplotlib seaborn earthengine-api geemap Pillow --upgrade`
6. Execute cada célula do notebook sequencialmente para realizar a análise. Certifique-se de ler e entender cada passo, e ajuste o código, conforme necessário, para atender aos seus requisitos específicos.
7. Se você desejar contribuir com melhorias ou adicionar novas análises, siga as diretrizes no README do sub-módulo para contribuições.  
Você pode criar um novo notebook ou fazer modificações neste, se necessário.

## 🗺️ Autorização para utilizar os serviços Google Earth Engine

Sempre que inicializar a aplicação, será solicitado acesso ao serviço GEE através da sua conta google pessoal.  
Para prover acesso e utilizar a API, relize a autorização executando o código abaixo:
```python
import ee
ee.Authenticate()
ee.Initialize()
```
Você será direcionado(a) à uma página WEB, onde será requisitado permissões de acesso.  

> Granting permission. This creates a web application definition controlled by your project provided above. After you click Generate Token, Google will ask for your permission to grant the application access to your data. See details in the step-by-step guide.

> Expiry period. The granted permissions will expire in a week, after which you'll need to call ee.Authenticate() again.

> Revoking permissions. You can view all applications connected to your account, and revoke permissions if needed, on https://myaccount.google.com/permissions. Search for "Earth Engine Notebook Client" to find the application defined by this page.

> Technical details. The web application is defined by a development-mode "OAuth2 Client" on your specified project, which you can manage on the Google Cloud Console.

## 🌟 Contribuições

Gostaríamos de incentivar a contribuição para este módulo de estudo de correlação. Se você deseja adicionar novas análises de correlação ou melhorar as existentes, siga os passos abaixo:

1. Faça um fork deste repositório.
2. Crie uma nova branch (`git checkout -b nova-analise-correlacao`).
3. Implemente as mudanças necessárias no notebook.
4. Faça um commit das alterações (`git commit -am 'Nova análise de correlação'`).
5. Envie a branch (`git push origin nova-analise-correlacao`).
6. Crie um Pull Request.

## 🚀 Tecnologias Utilizadas

- [Jupyter Notebook](https://jupyter.org) - A aplicação web para criação e compartilhamento de documentos computacionais.

## 👥 Equipe

<a href="https://github.com/DIEGOVZK">
  <img src="https://avatars.githubusercontent.com/u/45247817?v=4" alt="Diego Anestor Coutinho" width="150" height="auto">
  <p> Diego Anestor Coutinho </p>
</a>

Fique à vontade para explorar, contribuir e aprimorar nossos estudos de correlação neste módulo!