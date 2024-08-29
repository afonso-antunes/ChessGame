import copy

    #TODO extra: fazer um menu e dar a opcao de voltar atras


class Peca:
    def __init__(self, nome, simbolo):
        self.nome = nome
        self.simbolo = simbolo
        self.movido = False
    
    def __repr__(self):
        return self.simbolo


pecas_comidas_brancas = []
pecas_comidas_pretas = []


pecas = {
    'rei_preto': Peca('rei_preto', '\u2654'),
    'rainha_preto': Peca('rainha_preto', '\u2655'),
    'torre_preto': Peca('torre_preto', '\u2656'),
    'bispo_preto': Peca('bispo_preto', '\u2657'),
    'cavalo_preto': Peca('cavalo_preto', '\u2658'),
    'peao_preto': Peca('peao_preto', '\u2659'),
    'rei_branco': Peca('rei_branco', '\u265A'),
    'rainha_branco': Peca('rainha_branco', '\u265B'),
    'torre_branco': Peca('torre_branco', '\u265C'),
    'bispo_branco': Peca('bispo_branco', '\u265D'),
    'cavalo_branco': Peca('cavalo_branco', '\u265E'),
    'peao_branco': Peca('peao_branco', '\u265F')
}


pecas_pretas = ('\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659')
pecas_brancas = ('\u265A', '\u265B', '\u265C', '\u265D', '\u265E', '\u265F')

cores = {
    'vermelho': '\033[91m',    # Vermelho brilhante
    'amarelo': '\033[93m',     # Amarelo brilhante
    'verde': '\033[92m',       # Verde brilhante
    'azul': '\033[94m',        # Azul brilhante
    'ciano': '\033[96m',       # Ciano brilhante
    'magenta': '\033[95m',     # Magenta brilhante
    'negrito': '\033[1m',      # Negrito
    'reset': '\033[0m'         # Resetar para a cor padrão
}

eh_roque = False
en_passant_pos = None
en_passant_para = "" # en_passant_para = brancas quer dizer que as brancas podem fazer en_passant

# Mensagem festiva
def mensagem(jogador_atual):
    print(cores['negrito'] + cores['amarelo'] + "🎉🎉 Xeque-mate! Jogador das peças " +
            cores['ciano'] + jogador_atual + cores['amarelo'] +
            " ganhou! 🎉🎉" + cores['reset'])

# Criando uma instância separada para cada peão
tabuleiro = [
    [pecas['torre_preto'], pecas['cavalo_preto'], pecas['bispo_preto'], pecas['rainha_preto'], pecas['rei_preto'], pecas['bispo_preto'], pecas['cavalo_preto'], pecas['torre_preto']],
    [Peca('peao_preto', '\u2659') for _ in range(8)], 
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [Peca('peao_branco', '\u265F') for _ in range(8)],  
    [pecas['torre_branco'], pecas['cavalo_branco'], pecas['bispo_branco'], pecas['rainha_branco'], pecas['rei_branco'], pecas['bispo_branco'], pecas['cavalo_branco'], pecas['torre_branco']]
]


def ler_input():
    while True:
        try:
            movimento = input("-- Escreva a sua ação: (ex: 'a2 a4'): ")
            origem, destino = movimento.split()
            if len(origem) != 2 or len(destino) != 2:
                raise ValueError("Formato inválido. Tente outra vez.")
            return origem, destino
        except ValueError as e:
            print(cores['vermelho'] + "Erro a passar comando. Tente outra vez no formato ex: a2 a4." + cores['reset'])
            continue





def converter_coordenadas(posicao):
    letras_colunas = ("a", "b", "c", "d", "e", "f", "g", "h")
    letra = posicao[0]
    num = posicao[1]

    if not (letra in letras_colunas and num.isdigit() and 1 <= int(num) <= 8):
        return None

    linha = 8 - int(num)  
    coluna = letras_colunas.index(letra)
    return linha, coluna



def imprimir_tabuleiro(tabuleiro):
    letras_colunas = "  a b c d e f g h"
    print()
    print(letras_colunas)
    
    for i, linha in enumerate(tabuleiro):
        numero_linha = f"{8 - i}"
        print(f"{numero_linha} ", end='')  
        
        for celula in linha:
            if celula is None:
                print("- ", end='')
            else:
                print(celula.simbolo + " ", end='')
        
        # Mostrar peças capturadas na linha correspondente ao meio do tabuleiro
        if i == 1:
            print(f" {numero_linha}\t\t{' '.join(pecas_comidas_brancas)}")
        elif i == 6:
            print(f" {numero_linha}\t\t{' '.join(pecas_comidas_pretas)}")
        else:
            print(f" {numero_linha}")
    
    print(letras_colunas)
    print()


def eh_mov_horizontal(coords_origem, coords_fim):
    return coords_origem[0] == coords_fim[0] and coords_origem[1] != coords_fim[1]

def eh_mov_vertical(coords_origem, coords_fim):
    return coords_origem[0] != coords_fim[0] and coords_origem[1] == coords_fim[1]

def eh_mov_diagonal(coords_origem, coords_fim):
    return abs(coords_origem[0] - coords_fim[0]) == abs(coords_origem[1] - coords_fim[1])

def eh_movimento_em_L(coords_origem, coords_fim):
    delta_linha = abs(coords_origem[0] - coords_fim[0])
    delta_coluna = abs(coords_origem[1] - coords_fim[1])
    
    return (delta_linha == 2 and delta_coluna == 1) or (delta_linha == 1 and delta_coluna == 2)




def peca_no_caminho(coords_origem, coords_fim, tabuleiro):
    linha_origem, coluna_origem = coords_origem
    linha_fim, coluna_fim = coords_fim
    
    # Movimento horizontal
    if eh_mov_horizontal(coords_origem, coords_fim):
        passo = 1 if coluna_fim > coluna_origem else -1
        for coluna in range(coluna_origem + passo, coluna_fim + passo, passo):  # Incluindo a última coluna
            if tabuleiro[linha_origem][coluna] is not None:
                return (linha_origem, coluna, "horizontal")
    
    # Movimento vertical
    elif eh_mov_vertical(coords_origem, coords_fim):
        passo = 1 if linha_fim > linha_origem else -1
        for linha in range(linha_origem + passo, linha_fim + passo, passo):  # Incluindo a última linha
            if tabuleiro[linha][coluna_origem] is not None:
                return (linha, coluna_origem, "vertical")
    
    # Movimento diagonal
    elif eh_mov_diagonal(coords_origem, coords_fim):
        passo_linha = 1 if linha_fim > linha_origem else -1
        passo_coluna = 1 if coluna_fim > coluna_origem else -1
        for i in range(1, abs(linha_fim - linha_origem) + 1):  # Incluindo a última casa diagonal
            linha_atual = linha_origem + i * passo_linha
            coluna_atual = coluna_origem + i * passo_coluna
            if tabuleiro[linha_atual][coluna_atual] is not None:
                return (linha_atual, coluna_atual, "diagonal")
    
    return None


def kill_zone(coords, tabuleiro):
    direcoes = []
    peca = tabuleiro[coords[0]][coords[1]]

    # Definir as direções de ataque para cada peça
    if peca.simbolo in ["\u2654", "\u265A"]:  # Rei
        direcoes = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    elif peca.simbolo in ["\u2655", "\u265B"]:  # Rainha
        direcoes = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    elif peca.simbolo in ["\u2656", "\u265C"]:  # Torre
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    elif peca.simbolo in ["\u2657", "\u265D"]:  # Bispo
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    elif peca.simbolo in ["\u2658", "\u265E"]:  # Cavalo
        direcoes = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    elif peca.simbolo in ["\u2659", "\u265F"]:  # Peão
        if peca.simbolo == "\u2659":  
            direcoes = [(1, -1), (1, 1)]  
        elif peca.simbolo == "\u265F":  
            direcoes = [(-1, -1), (-1, 1)]  

    kill_zone = []

    # Verificar todas as direções possíveis
    if peca.simbolo in ["\u2659", "\u265F"]:  # Apenas para peões
        for direcao in direcoes:
            linha, coluna = coords
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]
         
            # Verificar se a nova posição está dentro do tabuleiro
            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                destino = tabuleiro[nova_linha][nova_coluna]
                
                if destino is not None and verificar_cor_peca((nova_linha, nova_coluna), tabuleiro) != verificar_cor_peca(coords, tabuleiro):
                    kill_zone.append((nova_linha, nova_coluna))
                # Não adicionar casas vazias para peões além da casa inicial
                if destino is None:
                    kill_zone.append((nova_linha, nova_coluna))

    elif peca.simbolo in ["\u2658", "\u265E"]:  # Apenas para cavalos
        for direcao in direcoes:
            linha, coluna = coords
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            # Verificar se a nova posição está dentro do tabuleiro
            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                destino = tabuleiro[nova_linha][nova_coluna]
                if destino is not None and verificar_cor_peca((nova_linha, nova_coluna), tabuleiro) != verificar_cor_peca(coords, tabuleiro):
                    kill_zone.append((nova_linha, nova_coluna))
                elif destino is None:
                    kill_zone.append((nova_linha, nova_coluna))

    elif peca.simbolo in ["\u2654", "\u265A"]:  # Apenas para o rei
        for direcao in direcoes:
            linha, coluna = coords
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            # Verificar se a nova posição está dentro do tabuleiro
            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                destino = tabuleiro[nova_linha][nova_coluna]
                if destino is not None and verificar_cor_peca((nova_linha, nova_coluna), tabuleiro) != verificar_cor_peca(coords, tabuleiro):
                    kill_zone.append((nova_linha, nova_coluna))
                elif destino is None:
                    kill_zone.append((nova_linha, nova_coluna))
    else:
        # Para outras peças, o loop é necessário para verificar todas as casas em cada direção
        for direcao in direcoes:
            linha, coluna = coords
            while True:
                linha += direcao[0]
                coluna += direcao[1]

                if 0 <= linha < 8 and 0 <= coluna < 8:  # Dentro do tabuleiro
                    destino = tabuleiro[linha][coluna]
                    if destino is not None:
                        if verificar_cor_peca((linha, coluna), tabuleiro) != verificar_cor_peca(coords, tabuleiro):
                            kill_zone.append((linha, coluna))  # Adiciona a casa de captura
                        break  # Para de verificar nesta direção se encontrar uma peça
                    else:
                        kill_zone.append((linha, coluna))  # Adiciona casa vazia
                else:
                    break  # Sai do loop se sair do tabuleiro

    return kill_zone



def verificar_cor_peca(coords, tabuleiro):
    
    linha, coluna = coords
    peca = tabuleiro[linha][coluna]
   
    if peca.simbolo in pecas_brancas:
        return "brancas"
    elif peca.simbolo in pecas_pretas:
        return "pretas"
    


def coordenadas_pecas_pretas(tabuleiro):
    coordenadas_pretas = []
    
    for linha in range(8):
        for coluna in range(8):
            peca = tabuleiro[linha][coluna]
            if peca is not None and peca.simbolo in pecas_pretas:
                coordenadas_pretas.append((linha, coluna))
    
    return coordenadas_pretas


def coordenadas_pecas_brancas(tabuleiro):
    coordenadas_brancas = []
    
    for linha in range(8):
        for coluna in range(8):
            peca = tabuleiro[linha][coluna]
            if peca is not None and peca.simbolo in pecas_brancas:
                coordenadas_brancas.append((linha, coluna))
    
    return coordenadas_brancas



def num_casas_percorridas(coords_ini, coords_fim):
    linha_ini, coluna_ini = coords_ini
    linha_fim, coluna_fim = coords_fim

    diff_linha = abs(linha_fim - linha_ini)
    diff_coluna = abs(coluna_fim - coluna_ini)

    if linha_ini == linha_fim:
        return diff_coluna
    elif coluna_ini == coluna_fim:
        return diff_linha
    
    elif diff_linha == diff_coluna:
        return diff_linha 
    
    else:
        return 10  # valor para explodir


def marcar_en_passant(coords_ini, coords_fim, peca):
    global en_passant_pos
    linha_ini, col_ini = coords_ini
    linha_fim, col_fim = coords_fim

    if peca.simbolo == "\u2659" and linha_ini == linha_fim - 2:  # Peão branco avança duas casas
        en_passant_pos = (linha_ini + 1, col_ini)
    elif peca.simbolo == "\u265F" and linha_ini == linha_fim + 2:  # Peão preto avança duas casas
        en_passant_pos = (linha_ini - 1, col_ini)
    else:
        en_passant_pos = None


def pode_fazer_roque(coords_ini, coords_fim, tabuleiro):
    global eh_roque
    linha_ini, col_ini = coords_ini
    linha_fim, col_fim = coords_fim
    rei = tabuleiro[linha_ini][col_ini]

    if rei.movido:
        return False
    
    # Verifica se o movimento é um roque (duas casas para o lado)
    if num_casas_percorridas(coords_ini, coords_fim) == 2:
        if col_fim > col_ini:
            # Roque curto (rei move duas casas para a direita)
            direcao = 1
            torre_col = 7  # Coluna da torre do lado do rei
            nova_pos_torre = 5
        else:
            # Roque longo (rei move duas casas para a esquerda)
            direcao = -1
            torre_col = 0  # Coluna da torre do lado da dama
            nova_pos_torre = 3

        # Verifica se a torre está na posição inicial e não foi movida
        torre = tabuleiro[linha_ini][torre_col]
        if torre is None or torre.simbolo not in ["\u2656", "\u265C"] or torre.movido:
            return False

        # Verifica se as casas entre o rei e a torre estão vazias
        for col in range(col_ini + direcao, torre_col, direcao):
            if tabuleiro[linha_ini][col] is not None:
                return False
        
        eh_roque = True
        return True
    
    return False



def verifica_mov_peca(coords_ini, coords_fim, tabuleiro):
    linha, coluna = coords_ini
    peca = tabuleiro[linha][coluna]
    global en_passant_pos
    peca_simbolo = peca.simbolo
    peca_caminho = peca_no_caminho(coords_ini, coords_fim, tabuleiro)
    # cavalo
    if peca_simbolo in ["\u2658", "\u265E"]:
        if not eh_movimento_em_L(coords_ini, coords_fim):
            return False
        
    # rainha
    elif peca_simbolo in ["\u2655", "\u265B"]:
        if eh_mov_diagonal(coords_ini, coords_fim):
            return True
        if eh_mov_horizontal(coords_ini, coords_fim):
            return True
        if eh_mov_vertical(coords_ini, coords_fim):
            return True
        else: return False
    
    # torre
    elif peca_simbolo in ["\u2656", "\u265C"]:
        if eh_mov_vertical(coords_ini, coords_fim):
            return True 
        if eh_mov_horizontal(coords_ini, coords_fim):
            return True
        else: return False
    
    # bispo
    elif peca_simbolo in ["\u2657", "\u265D"]:
        if not eh_mov_diagonal(coords_ini, coords_fim):
            return False
    
    # peao
    elif peca_simbolo in ["\u2659", "\u265F"]:
        global en_passant_para
        direcao = -1 if peca_simbolo == "\u2659" else 1  # Brancas sobem, pretas descem
        quem_pode_fzr_passant = "pretas" if peca_simbolo == "\u265F" else "brancas"   # propositadamente invertido para o en_passant_para
    
        if peca_simbolo == "\u2659":
            if coords_fim[0] < coords_ini[0]:  # Movimento para trás
                return False
        elif peca_simbolo == "\u265F":
            if coords_fim[0] > coords_ini[0]:  # Movimento para trás
                return False
        if eh_mov_vertical(coords_ini, coords_fim):
            if peca_caminho and peca_caminho[2] == "vertical": # nao saltar pecas
                return False
            if peca.movido == False and num_casas_percorridas(coords_ini, coords_fim) == 2: # caso inicial em que anda 2 casas
                marcar_en_passant(coords_ini, coords_fim, peca)
                en_passant_para = quem_pode_fzr_passant
                return True
            if num_casas_percorridas(coords_ini, coords_fim) == 1: 
                return True
            else: return False
        elif abs(coords_fim[1] - coords_ini[1]) == 1 and (coords_ini[0] - coords_fim[0]) == direcao: # captura diagonal
            if peca_caminho and peca_caminho[2] == "diagonal" and num_casas_percorridas(coords_ini, coords_fim) == 1:
                return True
            elif en_passant_pos and (coords_fim[0], coords_fim[1]) == en_passant_pos:
                return True
            
            else: return False
            
        else: return False

    # rei
    elif peca_simbolo in ["\u2654", "\u265A"]:
        if num_casas_percorridas(coords_ini, coords_fim) == 1:
            return True
        elif pode_fazer_roque(coords_ini, coords_fim, tabuleiro):
            return True
        else: return False
    
    return True

def mudanca_de_peca(jogador_atual):
    nova_peca = input(cores['negrito'] + cores['ciano'] + "-- Escreva o número da peça que deseja:\n1. Rainha\n2. Torre\n3. Bispo\n4. Cavalo\n" +
            cores['reset'])
    while True:
        if jogador_atual == "brancas":
            if nova_peca == "1":
                return "\u265B"
            elif nova_peca == "2":
                return "\u265C"
            elif nova_peca == "3":
                return "\u265D"
            elif nova_peca == "4":
                return "\u265E"
            else:
                print(cores['vermelho'] + "Digite um número entre 1 e 4." + cores['reset'])
        else:
            if nova_peca == "1":
                return "\u2655"
            elif nova_peca == "2":
                return "\u2656"
            elif nova_peca == "3":
                return "\u2657"
            elif nova_peca == "4":
                return "\u2658"
            else:
                print(cores['vermelho'] + "Digite um número entre 1 e 4." + cores['reset'])


def encontrar_rei(jogador_atual, tabuleiro):
    
    simbolo_rei = "\u2654" if jogador_atual == "pretas" else "\u265A"
    for linha in range(8):
        for coluna in range(8):
            peca = tabuleiro[linha][coluna]
            if peca and peca.simbolo == simbolo_rei:
                return linha, coluna
    return None


# ex: se o jogador atual for branco, vai encontrar a posicao do rei branco e vai ver se alguma peca preta pode comer
def eh_xeque(jogador_atual, tabuleiro):
    
    posicao_rei = encontrar_rei(jogador_atual, tabuleiro)
    if posicao_rei is None:
        return True
    linha_rei, coluna_rei = posicao_rei

    if jogador_atual == "brancas":
        coordenadas_pretas = coordenadas_pecas_pretas(tabuleiro)
        for coordenada in coordenadas_pretas:
            lista_coordenadas = kill_zone(coordenada, tabuleiro)
            if (linha_rei, coluna_rei) in lista_coordenadas:
                return True
            
    elif jogador_atual == "pretas":
        coordenadas_brancas = coordenadas_pecas_brancas(tabuleiro)
        for coordenada in coordenadas_brancas:
            lista_coordenadas = kill_zone(coordenada, tabuleiro)
            if (linha_rei, coluna_rei) in lista_coordenadas:
                return True
            
    return False


def eh_xeque_mate(jogador_atual, tabuleiro):

    if not eh_xeque(jogador_atual, tabuleiro):
        return False  
    
    if jogador_atual == "brancas":
        coordenadas_pecas = coordenadas_pecas_brancas(tabuleiro)
    else:
        coordenadas_pecas = coordenadas_pecas_pretas(tabuleiro)
    
    for coords in coordenadas_pecas:
        
        # Verificar todos os movimentos possíveis dessa peça
        for linha in range(8):
            for coluna in range(8):
                destino = (linha, coluna)
                
                if verifica_mov_peca(coords, destino, tabuleiro):
                    if not movimento_resulta_em_xeque(coords, destino, jogador_atual, tabuleiro):
                        print(coords, destino)
                        return False  # Se encontrar um movimento que não deixa o rei em xeque, não é xeque-mate
    
    # Se nenhum movimento legal puder tirar o rei do xeque, é xeque-mate
    return True


def executa_roque(coords_ini, coords_fim, tabuleiro):
    # Move o rei para a posição final
    tabuleiro[coords_fim[0]][coords_fim[1]] = tabuleiro[coords_ini[0]][coords_ini[1]]
    tabuleiro[coords_ini[0]][coords_ini[1]] = None

    # Verifica se o roque é curto ou longo
    if coords_fim[1] > coords_ini[1]:
        # Roque curto
        tabuleiro[coords_ini[0]][5] = tabuleiro[coords_ini[0]][7]
        tabuleiro[coords_ini[0]][7] = None
    else:
        # Roque longo
        tabuleiro[coords_ini[0]][3] = tabuleiro[coords_ini[0]][0]
        tabuleiro[coords_ini[0]][0] = None


def movimento_resulta_em_xeque(coords_ini, coords_final, jogador_atual, tabuleiro):
    global eh_roque
    # Salva o estado original do tabuleiro
    tabuleiro_temp = [linha.copy() for linha in tabuleiro]  # Copia o tabuleiro
    peca = tabuleiro_temp[coords_ini[0]][coords_ini[1]]
    destino_original = tabuleiro_temp[coords_final[0]][coords_final[1]]  # Salva a peça original

    peca_caminho = peca_no_caminho(coords_ini, coords_final, tabuleiro_temp)
    if peca_caminho is None:
        # se tivermos a lidar com roque
        if eh_roque:
            executa_roque(coords_ini, coords_final, tabuleiro_temp)
        else:
            # Mover a peça
            tabuleiro_temp[coords_final[0]][coords_final[1]] = peca
            tabuleiro_temp[coords_ini[0]][coords_ini[1]] = None
    else: 
        cor_peca_caminho = verificar_cor_peca((peca_caminho[0], peca_caminho[1]), tabuleiro_temp)
        if cor_peca_caminho == jogador_atual:
            return True
        else:                                                               # MUDANCA AQUI
            tabuleiro_temp[coords_final[0]][coords_final[1]] = peca
            tabuleiro_temp[coords_ini[0]][coords_ini[1]] = None

    # Verifica se o movimento coloca o jogador em xeque
    xeque = eh_xeque(jogador_atual, tabuleiro_temp)

    # Restaura o tabuleiro ao estado original
    tabuleiro = [linha.copy() for linha in tabuleiro_temp]
    tabuleiro[coords_final[0]][coords_final[1]] = destino_original  # Restaura a peça original

    return xeque



def eh_empate(jogador_atual, tabuleiro):
    
    if eh_xeque(jogador_atual, tabuleiro):
        return False

    if jogador_atual == "brancas":
        coordenadas_pecas = coordenadas_pecas_brancas(tabuleiro)
    else:
        coordenadas_pecas = coordenadas_pecas_pretas(tabuleiro)

    # Verifique se há algum movimento legal
    for coords in coordenadas_pecas:
        for linha in range(8):
            for coluna in range(8):
                destino = (linha, coluna)
                if verifica_mov_peca(coords, destino, tabuleiro):
                    if not movimento_resulta_em_xeque(coords, destino, jogador_atual, tabuleiro):
                        return False  # Há um movimento legal disponível
    
    
    return True

def verificar_material_insuficiente(tabuleiro):
    pecas = []
    for linha in tabuleiro:
        for peca in linha:
            if peca and peca.simbolo not in ["\u2654", "\u265A"]:  # ignorae os reis
                pecas.append(peca.simbolo)

    if len(pecas) == 0:
        return True  # Rei contra rei
    if len(pecas) == 1 and pecas[0] in ["\u2657", "\u265D", "\u2658", "\u265E"]:
        return True  # Rei e bispo/cavalo contra rei

    return False


def movimentar_pecas(coords_ini, coords_final, jogador_atual, tabuleiro):
    global en_passant_pos
    global en_passant_para
    global eh_roque

    if coords_ini is None or coords_final is None:
        print(cores['vermelho'] + "Coordenadas inválidas." + cores['reset'])
        return False
    
    if tabuleiro[coords_ini[0]][coords_ini[1]] is None:
        print(cores['vermelho'] + "Não há peça na coordenada de origem." + cores['reset'])
        return False
    
    if not (0 <= coords_ini[0] < 8 and 0 <= coords_ini[1] < 8 and 0 <= coords_final[0] < 8 and 0 <= coords_final[1] < 8):
        print(cores['vermelho'] + "Movimento fora dos limites do tabuleiro." + cores['reset'])
        return False
        
    cor_peca_jogada = verificar_cor_peca(coords_ini, tabuleiro)
    if cor_peca_jogada != jogador_atual: 
        print(cores['vermelho'] + "Não pode jogar a peça do adversário..." + cores['reset'])
        return False
    
    if not verifica_mov_peca(coords_ini, coords_final, tabuleiro):
        print(cores['vermelho'] + "Ação impossível." + cores['reset'])
        return False
    
    if movimento_resulta_em_xeque(coords_ini, coords_final, jogador_atual, tabuleiro):
        print(cores['vermelho'] + "Xeque!" + cores['reset'])
        print(cores['vermelho'] + "Ação inválida!." + cores['reset'])
        return False
    
    peca = tabuleiro[coords_ini[0]][coords_ini[1]]
    peca_caminho = peca_no_caminho(coords_ini, coords_final, tabuleiro)
    # Se não existir peça no caminho, mover para as coordenadas pedidas
    if peca_caminho is None:
        if eh_roque:
            executa_roque(coords_ini, coords_final, tabuleiro)
            eh_roque = False
            return True
        # Se o movimento é uma captura en passant, remove o peão capturado
        elif en_passant_pos and (coords_final[0], coords_final[1]) == en_passant_pos:
            if peca.simbolo == "\u2659":  # Peão preto
                pecas_comidas_pretas.append(tabuleiro[coords_final[0] - 1][coords_final[1]].simbolo)
                tabuleiro[coords_final[0] - 1][coords_final[1]] = None
            elif peca.simbolo == "\u265F":  # Peão branco
                pecas_comidas_brancas.append(tabuleiro[coords_final[0] + 1][coords_final[1]].simbolo)
                tabuleiro[coords_final[0] + 1][coords_final[1]] = None
        
        tabuleiro[coords_final[0]][coords_final[1]] = tabuleiro[coords_ini[0]][coords_ini[1]]
        if tabuleiro[coords_final[0]][coords_final[1]] is not None:
            tabuleiro[coords_final[0]][coords_final[1]].movido = True

        if en_passant_pos and not (coords_final[0], coords_final[1]) == en_passant_pos and en_passant_para == jogador_atual:
            en_passant_pos = None
        
        # Se peao chegar a ultima linha
        elif (tabuleiro[coords_ini[0]][coords_ini[1]].simbolo == "\u2659" and coords_final[0] == 7) or \
            (tabuleiro[coords_ini[0]][coords_ini[1]].simbolo == "\u265F" and coords_final[0] == 0):             # VERIFICAR ISTO CASO MUDANCA NAO FUNCIONE
            tabuleiro[coords_final[0]][coords_final[1]].simbolo = mudanca_de_peca(jogador_atual)

    # Se tiver uma peça no caminho, mover para as coordenadas da peça (exceto se a peça for da mesma cor)
    else:
        cor_peca_caminho = verificar_cor_peca((peca_caminho[0], peca_caminho[1]), tabuleiro)
        if cor_peca_caminho == cor_peca_jogada:
            print(cores['vermelho'] + "Ação impossível." + cores['reset'])
            return False
        
        if jogador_atual == "brancas":
            pecas_comidas_brancas.append(tabuleiro[peca_caminho[0]][peca_caminho[1]].simbolo) 
        else:
            pecas_comidas_pretas.append(tabuleiro[peca_caminho[0]][peca_caminho[1]].simbolo)
        tabuleiro[peca_caminho[0]][peca_caminho[1]] = tabuleiro[coords_ini[0]][coords_ini[1]]

        if tabuleiro[peca_caminho[0]][peca_caminho[1]] is not None:
            tabuleiro[peca_caminho[0]][peca_caminho[1]].movido = True

        if en_passant_pos and en_passant_para == jogador_atual:
            en_passant_pos = None
        
        # Se peao chegar a ultima linha
        if (tabuleiro[coords_ini[0]][coords_ini[1]].simbolo == "\u2659" and peca_caminho[0] == 7) or \
            (tabuleiro[coords_ini[0]][coords_ini[1]].simbolo == "\u265F" and peca_caminho[0] == 0):
            tabuleiro[peca_caminho[0]][peca_caminho[1]].simbolo = mudanca_de_peca(jogador_atual)
        
    # Limpar a peça do sítio original
    tabuleiro[coords_ini[0]][coords_ini[1]] = None
    eh_roque = False
    return True


def jogo_xadrez():
    
    jogador_atual = "brancas"

    while True:
        imprimir_tabuleiro(tabuleiro)
        cor = cores['azul']  
        estilo = cores['negrito']  

        print(f"{estilo}{cor}-- Vez das peças {jogador_atual}{cores['reset']}")

        origem, destino = ler_input()
        coords_origem = converter_coordenadas(origem)
        coords_final = converter_coordenadas(destino)
        
        if coords_origem and coords_final:
            sucesso = movimentar_pecas(coords_origem, coords_final, jogador_atual, tabuleiro)
            if sucesso:
                jogador_atual = "pretas" if jogador_atual == "brancas" else "brancas"
                if eh_xeque_mate(jogador_atual, tabuleiro):
                    jogador_atual = "pretas" if jogador_atual == "brancas" else "brancas"
                    imprimir_tabuleiro(tabuleiro)
                    mensagem(jogador_atual)
                    return
            empate_stalemate = eh_empate(jogador_atual, tabuleiro)
            if empate_stalemate:
                print(f"{estilo}{cores['amarelo']}-- Empate por stalemate!{cores['reset']}")
                return
            empate_material_ins = verificar_material_insuficiente(tabuleiro)
            if empate_material_ins:
                print(f"{estilo}{cores['amarelo']}-- Empate por insuficiência de peças!{cores['reset']}")
                return
        else:
            print(cores['vermelho'] + "Coordenadas inválidas. Tente novamente." + cores['reset'])

        

jogo_xadrez()


