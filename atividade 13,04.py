STATUS_ACTIVE = "active"
STATUS_CANCELED = "canceled"
STATUS_FINISHED = "finished"

class Reserva:
    def __init__(
        self,
        id: int,
        usuario_id: int,
        sala_id: int,
        data: str,
        hora_inicio: str,
        hora_fim: str,
        status: str = STATUS_ACTIVE
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status

    def cancelar(self):

        if self.status == STATUS_ACTIVE:
        self.status = STATUS_CANCELED

    def finalizar(self, hora_atual: str):

        if self.status != STATUS_ACTIVE:
        raise Exception("Apenas reservas ativas podem ser finalizadas.")

    if hora_atual < self.hora_fim:
        raise Exception("A reserva só pode ser finalizada após o horário de término.")

    self.status = STATUS_FINISHED

    def duracao_em_horas(self) -> float:
       inicio = int(self.hora_inicio[:2]) + int(self.hora_inicio[3:]) / 60
        fim = int(self.hora_fim[:2]) + int(self.hora_fim[3:]) / 60

        return fim - inicio

    def conflita_com(self, outra_reserva) -> bool:
          if self.sala_id != outra_reserva.sala_id or self.data != outra_reserva.data:
        return False

        return not (self.hora_fim <= outra_reserva.hora_inicio or
                outra_reserva.hora_fim <= self.hora_inicio)