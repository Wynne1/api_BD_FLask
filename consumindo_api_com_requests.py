# fazer as solicitações da api:
from requests.auth import HTTPBasicAuth
import requests

# Para obter o token: (PARA FUNCIONAR A APLICAÇÃO API_BANCO_DE_DADOS PRECISA ESTAR RODANDO TAMBÉM)
resultado = requests.get('http://localhost:5000/login', auth=('Douglas','123456')) 
print(resultado.json())

# Para usar o token dentro das requisições:
resultado_autores = requests.get('http://localhost:5000/autores', headers={'x-access-token': resultado.json()['token']}) # o headers inclui um dicionário com todas as propriedades que devem ser definidas. Igual como é feito no postman, passando o x-access-token, e o token.
print(resultado_autores.json())