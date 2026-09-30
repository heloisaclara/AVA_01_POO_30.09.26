from __future__ import annotations
from datetime import date

# Implemente sua classe Medicamento aqui
if __name__ == "__main__":
    m1 = Medicamento("Dipirona 500mg", "L2026A", date(2026, 12, 31), 100, 12.50)
    m2 = Medicamento.de_registro("Amoxicilina 500mg;L2026B;2026-10-15;40;18.90")

    print(f"Dados de m1: {m1}") # ex.: Dipirona 500mg (L2026A) - 100 un. - val. 31/12/2026
    print(f"Dados de m2: {m2}") # ex.: Amoxicilina 500mg (L2026B) - 40 un. - val. 15/10/2026
    print(f"Dias para vencer de m2: {Medicamento.dias_para_vencer(m2.validade)}")
    print("Dispensando 20 medicamentos de m1")

    m1.dispensar(20)
    print(f"Quantidade de m1: {m1.quantidade}")

    try:
        m2.dispensar(999)
    except QuantidadeInvalidaError as erro:
        print(f"Erro esperado: {erro}")

    vencido = Medicamento("Soro Fisiológico", "L2025X", date(2025, 1, 10), 10, 5.0)
    try:
        vencido.dispensar(1)
    except MedicamentoVencidoError as erro:
        print(f"Erro esperado: {erro}")

    outro = Medicamento("Dipirona 500mg", "L2026A", date(2026, 1, 1), 0, 1.0)
    print(f"m1 é igual a outro? {m1 == outro}")

    estoque = [m1, m2, vencido, outro]
    print("Exibindo lista ordenada por data (mais antigos primeiro): ")
    for lote in sorted(estoque):
        print(lote)

    try:
        m1.quantidade = -5
    except ValueError as erro:
        print(f"Erro esperado: {erro}")

    @classmethod
    def de_registro(cls, dados: str) -> Medicamento:
        nome, lote, validade_str, qtd_str, valor_str = dados.split(";")
        return cls(
            nome.strip(),
            lote.strip(),
            date.fromisoformat(validade_str.strip()),
            int(qtd_str.strip()),
            float(valor_str.strip())
        )

    @staticmethod
    def dias_para_vencer(validade: date) -> int:
        return (validade - date.today()).days

    def __str__(self) -> str:
        data_fmt = self.validade.strftime("%d/%m/%Y")
        return f"{self.nome} ({self.lote}) {self.quantidade} un. val. {data_fmt}"

    def __repr__(self) -> str:
        return f"Medicamento(nome={self.nome!r}, lote={self.lote!r}, validade={self.validade!r}, quantidade={self.quantidade}, valor={self.valor})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Medicamento):
            return NotImplemented
        return self.nome == outro.nome and self.lote == outro.lote

    def __lt__(self, outro: Medicamento) -> bool:
        return self.validade < outro.validade
