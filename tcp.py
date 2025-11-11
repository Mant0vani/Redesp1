# JAMAIS MODIFIQUE O CONTEÚDO DESTE ARQUIVO

import socket
import asyncio

class Servidor:
    def __init__(self, porta):
        s = self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', porta))
        s.listen(5)

    def registrar_monitor_de_conexoes_aceitas(self, callback):
        asyncio.get_event_loop().add_reader(self.s, lambda: callback(Conexao(self.s.accept())))


class Conexao:
    def __init__(self, accept_tuple):
        self.s, _ = accept_tuple

    def registrar_recebedor(self, callback):
        asyncio.get_event_loop().add_reader(self.s, lambda: callback(self, self.s.recv(8192)))

    def enviar(self, dados):
        try:
            self.s.sendall(dados)
        except (OSError, ConnectionAbortedError, ConnectionResetError):
        # Conexão já encerrada pelo cliente
            pass

    def fechar(self):
        asyncio.get_event_loop().remove_reader(self.s)
        self.s.close()
