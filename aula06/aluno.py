from math import isfinite


class Aluno:
    def __init__(self):
        # TODO: criar nome/turma vazios e uma lista de notas nova por objeto.
        self.nome = ""
        self.turma = ""
        self.notas = []
        self.registros = []
        # self.media = ""

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

        # media = sum(novas_notas) / len(novas_notas)

        # TODO: confirmar os três atributos apenas depois de validar tudo.
        self.nome = nome
        self.turma = turma
        self.notas = novas_notas.copy()
        # self.media = media

        registro = {
            "nome": nome,
            "turma": turma,
            "notas": novas_notas.copy(),
        }

        self.registros.append(registro)
        
        return "Aluno atualizado com sucesso."
    
    def calcular_media(self):
        if len(self.notas) == 0:
            return None

        return round(sum(self.notas) / len(self.notas), 1)
    

    def resumo(self):

        if len(self.registros) == 0:
            return "Nenhum registro confirmado nesta sessão."

        texto = ""

        for numero, registro in enumerate(self.registros, start=1):
            media = round(sum(registro['notas']) / len(registro['notas']), 1)

            texto += (
                f"REGISTRO {numero}\n"
                f"Aluno: {registro['nome']}\n"
                f"Turma: {registro['turma']}\n"
                f"Notas: {', '.join(f'{nota:.1f}' for nota in registro['notas'])}\n"
                f"Média: {media:.1f}\n"
                f"{'-' * 35}\n\n"
            )

        return texto