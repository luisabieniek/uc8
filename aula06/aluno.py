from math import isfinite


class Aluno:
    def __init__(self):
        # TODO: criar nome/turma vazios e uma lista de notas nova por objeto.
        self.nome = None
        self.turma = None
        self.notas = None
        self.media = None

    def atualizar(self, nome, turma, notas_texto):
        # TODO: adaptar sua validação da A05; receber textos, nunca Entry.
        nome = nome.strip()
        turma = turma.strip()

        if not nome or not turma:
            return "Nome e turma não podem estar vazios." 
        
        if len(notas_texto) != 5:
            return "Informe exatamente cinco notas."
        
        novas_notas = []

        for texto in notas_texto:
            try:
                nota = float(texto.strip().replace(",", "."))
            except ValueError:
                return "Todas as notas devem ser números válidos."
            
            if not isfinite(nota):
                return "As notas devem ser números finitos."
            
            if nota < 0 or nota > 10:
                return "As notas devem estar entre 0 e 10."
            
            novas_notas.append(nota)

        media = sum(novas_notas) / len(novas_notas)

        # TODO: confirmar os três atributos apenas depois de validar tudo.
        self.nome = nome
        self.turma = turma
        self.notas = novas_notas
        self.media = media
        
        return "Dados atualizados com sucesso."

    def resumo(self):
        # TODO: somente atributos confirmados; uma casa apenas na apresentação.
        if not self.nome or not self.turma or not self.notas:
            return "Resumo não disponível; dados incompletos."
        
        media = sum(self.notas) / len(self.notas)

        return (
            f"Aluno: {self.nome}\n"
            f"Turma: {self.turma}\n"
            f"Notas: {', '.join(f'{nota:.1f}' for nota in self.notas)}\n"
            f"Média: {self.media:.1f}"
        )