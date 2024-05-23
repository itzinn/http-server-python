import socket
import threading

"""
Diretrizes para escrever docstrings
Descrição Breve: Comece com uma breve descrição da função.
Argumentos (Args/Parameters): Liste e descreva todos os parâmetros da função.
Retorno (Returns): Descreva o que a função retorna.
Exceções (Raises): Opcionalmente, descreva quaisquer exceções que a função possa levantar.
"""

HTTP_VERSION = 'HTTP/1.1'
CRLF = '\r\n'
ALLOWED_METHODS = ["GET", "POST"]

def verified_method(method):
    if method not in ALLOWED_METHODS:
        return False
    return True
    

def create_response(method, resource, http_version, headers):
    """
    analisa os elementos da requisição e cria uma resposta baseada neles

    args:
        method: método da requisição
        resource: recurso especificado pela requisição
        http_version: versão do protocolo da requisição
        headers: headers da requisição

    returns:
        response(bytes)

    """

    headers=''
    message_body = ""

    if not verified_method(method):
       status_code = 405
       reason_phrase = "Method Not Allowed"
    else:
        status_code = 200
        reason_phrase = "OK"
        message_body = "segredo"

    status_line = "{} {} {}".format(HTTP_VERSION, status_code, reason_phrase)     

    response = status_line+CRLF+headers+CRLF+CRLF+message_body

    return response
    


def handle_client(client_socket):
    """
    lida com a conexão de um cliente ao socket da aplicação.
    
    args:
        client_socket(object): objeto socket que representa a conexao do cliente

    """
    request = client_socket.recv(4096).decode('utf-8')

    method, resource, http_version, headers = parse_http_request(request)

    #create response
    response = create_response(method, resource, http_version, headers);

    print("Received request:")
    print(f"Method: {method}")
    print(f"Resource: {resource}")
    print(f"HTTP Version: {http_version}")
    print("Headers:")

    for key, value in headers.items():
        print(f"{key}: {value}")

    client_socket.send(response.encode('utf-8'))

    client_socket.close()

def start_server(host, port):
    """
    inicia o socket principal da aplicação que receberá requisições

    args:
        host(string): localhost
        port(int): xxxx

    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()

        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))

        client_handler.start()

def parse_http_request(request):
    """
    recebe mensagem de request e obtém todos seus componentes relevantes

    args:
        request(bytes): a requisição

    returns:
        method: método da requisição
        resource: recurso para o qual a requisição foi feita
        http_version: a versão do protocolo http da requisição
        headers: cabeçalhos da requsição

    """

    lines = request.split('\r\n')

    method, resource, http_version = lines[0].split()
    
    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        
        if line.strip():
            key, value = line.split(': ', 1)
            headers[key] = value
    
    return method, resource, http_version, headers

host = 'localhost'
port = 8181

start_server(host, port)