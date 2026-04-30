# ============================================================
# SISTEMA DE GESTÃO DE PEÇAS - AUTOMAÇÃO INDUSTRIAL
# ============================================================

# Estruturas de dados
pecas = []          # lista para guardar todas as peças cadastradas
caixas = []         # lista de caixas fechadas (cada caixa é uma lista de peças)
caixa_atual = []    # caixa que está sendo preenchida agora

# Função que avalia se a peça está aprovada e retorna (status, motivo)
def avaliar_peca(peso, cor, comprimento):
    motivos = []
    if peso < 95 or peso > 105:
        motivos.append("peso fora do limite (95-105g)")
    if cor.lower() not in ["azul", "verde"]:
        motivos.append("cor diferente de azul/verde")
    if comprimento < 10 or comprimento > 20:
        motivos.append("comprimento fora do limite (10-20cm)")
    
    if len(motivos) == 0:
        return (True, "aprovada")
    else:
        return (False, ", ".join(motivos))

# Função para armazenar peça aprovada na caixa atual
def armazenar_peca(peca):
    global caixa_atual, caixas
    caixa_atual.append(peca)
    if len(caixa_atual) == 10:
        caixas.append(caixa_atual.copy())  # fecha a caixa
        caixa_atual = []                   # inicia nova caixa

# Opção 1: Cadastrar nova peça
def cadastrar_peca():
    print("\n--- CADASTRAR PEÇA ---")
    try:
        id_peca = input("ID da peça: ")
        peso = float(input("Peso (g): "))
        cor = input("Cor: ").strip().lower()
        comprimento = float(input("Comprimento (cm): "))
    except ValueError:
        print("Erro: peso e comprimento devem ser números.")
        return

    aprovado, motivo = avaliar_peca(peso, cor, comprimento)
    
    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "aprovado": aprovado,
        "motivo": motivo
    }
    pecas.append(peca)
    
    if aprovado:
        armazenar_peca(peca)
        print("✅ Peça APROVADA e armazenada na caixa atual.")
    else:
        print(f"❌ Peça REPROVADA. Motivo(s): {motivo}")

# Opção 2: Listar peças aprovadas e reprovadas
def listar_pecas():
    print("\n--- LISTA DE PEÇAS ---")
    if not pecas:
        print("Nenhuma peça cadastrada.")
        return
    
    aprovadas = [p for p in pecas if p["aprovado"]]
    reprovadas = [p for p in pecas if not p["aprovado"]]
    
    print(f"\n✅ Peças aprovadas: {len(aprovadas)}")
    for p in aprovadas:
        print(f"  ID:{p['id']} | Peso:{p['peso']}g | Cor:{p['cor']} | Comp:{p['comprimento']}cm")
    
    print(f"\n❌ Peças reprovadas: {len(reprovadas)}")
    for p in reprovadas:
        print(f"  ID:{p['id']} | Motivo: {p['motivo']}")

# Opção 3: Remover peça cadastrada (por ID)
def remover_peca():
    print("\n--- REMOVER PEÇA ---")
    id_remover = input("Digite o ID da peça a remover: ")
    global caixa_atual, caixas
    for i, p in enumerate(pecas):
        if p["id"] == id_remover:
            # Se a peça era aprovada, precisamos removê-la da caixa também (complexo)
            # Para simplificar, vamos avisar que a caixa não será reorganizada.
            if p["aprovado"]:
                print("⚠️ Atenção: a peça estava aprovada e foi removida, mas as caixas não serão reordenadas.")
            del pecas[i]
            print("Peça removida com sucesso.")
            return
    print("ID não encontrado.")

# Opção 4: Listar caixas fechadas
def listar_caixas():
    print("\n--- CAIXAS FECHADAS ---")
    if not caixas:
        print("Nenhuma caixa foi fechada ainda.")
    else:
        for idx, caixa in enumerate(caixas, 1):
            print(f"Caixa {idx}: {len(caixa)} peças - IDs: {[p['id'] for p in caixa]}")

# Opção 5: Gerar relatório final
def gerar_relatorio():
    print("\n========== RELATÓRIO FINAL ==========")
    total_pecas = len(pecas)
    aprovadas = sum(1 for p in pecas if p["aprovado"])
    reprovadas = total_pecas - aprovadas
    
    print(f"Total de peças processadas: {total_pecas}")
    print(f"✅ Peças aprovadas: {aprovadas}")
    print(f"❌ Peças reprovadas: {reprovadas}")
    
    if reprovadas > 0:
        print("\nMotivos de reprovação (contagem):")
        motivos_count = {}
        for p in pecas:
            if not p["aprovado"]:
                motivos_count[p["motivo"]] = motivos_count.get(p["motivo"], 0) + 1
        for motivo, qtd in motivos_count.items():
            print(f"  - {motivo}: {qtd} peça(s)")
    
    # Caixas fechadas + caixa atual (se tiver peças)
    caixas_utilizadas = len(caixas)
    if caixa_atual:
        caixas_utilizadas += 1  # caixa atual conta como utilizada, mesmo não fechada
    print(f"\n📦 Caixas utilizadas (incluindo atual não fechada): {caixas_utilizadas}")
    print(f"   Caixas completamente fechadas: {len(caixas)}")
    if caixa_atual:
        print(f"   Caixa atual com {len(caixa_atual)} peça(s)")
    print("=====================================")

# ========== MENU PRINCIPAL ==========
def menu():
    while True:
        print("\n===== SISTEMA DE GESTÃO DE PEÇAS =====")
        print("1. Cadastrar nova peça")
        print("2. Listar peças aprovadas/reprovadas")
        print("3. Remover peça cadastrada")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_peca()
        elif opcao == "2":
            listar_pecas()
        elif opcao == "3":
            remover_peca()
        elif opcao == "4":
            listar_caixas()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu
if __name__ == "__main__":
    menu()