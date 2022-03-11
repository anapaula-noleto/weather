## 🌦️ Weather web app

### Descrição
Um aplicativo web feito com Flask e Bootstrap que consome o [Open Weather Map API](https://openweathermap.org/current) para mostrar como está o tempo
na cidade escolhida pelo usuário de forma dinâmica e fácil de usar.

Fiz esse projeto para treinar o uso de Flask e uso de banco de dados. Futuramente vou colocar checkbox para permitir o usuário acompanhar mais variáveis
como umidade e velocidade do vento.

<img src="weather1.gif">

### Requesitos
Todas as bibliotecas utilizadas estão no arquivo requirements.txt

### Tratamento de erros
A aplicação explica para o usuário caso a cidade que ele digitou não exista, caso a cidade já esteja presente no banco de dados (o app não permite a repetição)
ou caso o usuário não tenha digitado nada.

### Setup
1. Faça download ou clone este repositório
2. <code>pip install -r requirements.txt</code>
3. <code>python app.py</code>
4. Vá para <code>http://127.0.0.1:5000</code>
