import os 
from random import randint
""" inspirei-me no site https://stackoverflow.com/questions/33594958/is-it-possible-to-align-a-print-statement-to-the-center-in-python 
para conseguir centrar qualquer string na consola.
A variável width_console armazena o valor de os.get_terminal_size().columns, propriedade esta que devolve o número total de colunas que dividem a consola. width_console
é usada como parãmetro de .center(). Este método é chamado dentro da função desenharTabulero() para fazer com que as strings, que desenham o tabuleiro, fiquem centradas na consola."""
def desenharTabuleiro(tabuleiro,width_consola): # Inspirei-me no código do video https://www.youtube.com/watch?v=RvqmZLuCQrw&t=508s para conseguir desenhar o tabuleiro
    print(str("_"*19).center(width_consola))
    print("|     |     |     |".center(width_consola))
    string_linha = ["|","|","|"]
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            string_linha[i] += "  " + tabuleiro[i][j] + "  |"
        print(string_linha[i].center(width_consola))
        print("|     |     |     |".center(width_consola))
        if i == 2:
            print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾".center(width_consola))
            break
        print("|‾‾‾‾‾|‾‾‾‾‾|‾‾‾‾‾|".center(width_consola))


#Para desenhar o X no tabuleiro
def desenharX(tabuleiro,linha,coluna,quem_joga,tente_novamente):
    if linha > 3 or coluna > 3 or linha < 0 or coluna < 0: #Se o utilizador escrever coordenadas inválidas
        quem_joga = 1
        tente_novamente = True
        return [quem_joga,tente_novamente] 
    linha -= 1  #Se o utilizador indicar a linha 1, significa que a linha escolhida é a que pertence ao index 0 (1-1 = 0)
    coluna -= 1
    for i in range(len(tabuleiro)):
        if i == linha:      #Se a linha escolhida corresponder à linha iterada
            for j in range(len(tabuleiro[i])):
                if j == coluna : #Se a coluna escolhida corresponder à coluna iterada
                    if tabuleiro[i][j] == ' ': #Se o elemento estiver vazio
                        tabuleiro[i][j] = 'X'
                        quem_joga = 2
                        return [quem_joga, False]
                    else: #Senão vai alertar que o utilizador escreveu coordenadas inválidas.
                        quem_joga = 1
                        tente_novamente = True
                        return [quem_joga,tente_novamente]


#Para desenhar o O no tabuleiro
def desenharO(tabuleiro,linha,coluna,quem_joga,tente_novamente):
    if linha > 3 or coluna > 3 or linha < 0 or coluna < 0:
        quem_joga = 2
        tente_novamente = True
        return [quem_joga,tente_novamente] 
    linha -= 1
    coluna -= 1
    for i in range(len(tabuleiro)):
        if i == linha:
            for j in range(len(tabuleiro[i])):
                if j == coluna:
                    if tabuleiro[i][j] == ' ':
                        tabuleiro[i][j] = 'O'
                        quem_joga = 1
                        return [quem_joga, False]
                    else:
                        quem_joga = 2
                        tente_novamente = True
                        return [quem_joga,tente_novamente]


def analisarAMelhorJogada(tabuleiro,nr_da_jogada,estrategia,estrategia_posiçoes):
    linha = -1
    coluna = -1
    #Segundo o site https://blog.ostermiller.org/tic-tac-toe-strategy/ , a melhor estratégia para a  
    # pessoa que vai jogar primeiro é começar por ocupar um dos cantos (opção para quem quer ganhar) ou o meioo (opção para quem quer empatar). Se na primeira jogada ocupou-se um dos cantos, 
    #na segunda jogada, deve-se ocupar o meio. Se na primeira jogada ocupou-se o meio,
    #na segunda, deve-se ocupar um dos cantos. Com este conhecimento, consigo fazer com que o computador faça isso nas primeiras jogadas.
    #Portanto, a primeira coisa em que devo me focalizar é relativamente à primeira e segunda jogada que o robo deve fazer mecanica 
    # e automaticamente.
    novaPosiçao = [] #Armazena o index da nova linha, da nova coluna e o tipo de estrategia que ela usará na prox. jogada
    if nr_da_jogada == 0: #Se a máquina é a primeira a jogar
        #deve escolher aleatóriamente um dos quatro cantos ou o meio para ocupar.
        escolha_aleatoria = randint(1,5)
        if escolha_aleatoria == 1: #canto superior esquerdo
            linha = 0
            coluna = 0
        elif escolha_aleatoria == 2: #canto superior direito
            linha = 0
            coluna = 2
        elif escolha_aleatoria == 3: #canto inferior esquerdo
            linha = 2
            coluna = 0
        elif escolha_aleatoria == 4: #canto inferior direito
            linha = 2
            coluna = 2
        else:   #meio. ATUALIZAÇÃO: não tenciono fazer com que a minha máquina nunca perca. Quero que os utilizadores tenham, às vezes, hipóteses de ganhar. 
            linha = 1
            coluna = 1
    elif nr_da_jogada == 1: #Se a máquina é a segunda a jogar
        #deve verificar se o meio está livre.
        if tabuleiro[1][1] == " ":
            linha = 1
            coluna = 1
        else: #se não estiver livre, então deve ocupar um dos cantos, isto é, se também estiver livre.
            #Desta vez, o programa vai escolher um número random entre 0 e 3 e o número gerado será o index da variável 'cantos_posiçoes'
            escolha_aleatoria = randint(0,3)
            cantos_posiçoes = [[0,0],[0,2],[2,0],[2,0]]
            canto_preenchido = True
            while canto_preenchido:
                linha = cantos_posiçoes[escolha_aleatoria][0] #index da linha
                coluna = cantos_posiçoes[escolha_aleatoria][1] #index da coluna
                if tabuleiro[linha][coluna] == ' ':
                    canto_preenchido = False
    else: #em qualquer restante jogada que não seja a primeira nem a segunda
        #Depois de feitas as duas primeiras jogadas, as próximas jogadas têm que ser pensadas.
        #Considero que a máquina devia, em primeiro lugar, verificar se existe algum espaço
        # que possa ocupar para ganhar. Caso contrário, verifica se existe algum espaço que tem obrigatoriamente de ser ocupado para não permitir 
        # que o utilizador ganhe. Por exemplo, o utilizador já ocupou os dois espaços de uma fila e falta-lhe 
        # ocupar mais um para ganhar. O computador tem que colocar imediatamente um O nesse lugar que falta.
        #A soma das coordenadas de cada posição : 0 | 1 | 2    (0,0 ==> 0+0 = 0 ou 2,2 ==> 2+2=4)
        #                                         1 | 2 | 3
        #                                         2 | 3 | 4
        #Para que cada posição seja única, marquei cada uma com ids diferentes, entre 0 a 8:
        #  0 | 1 | 2
        #  3 | 4 | 5
        #  6 | 7 | 8
        # Sequência das posições que garantem a vitória: 0,1,2; 0,3,6; 0,4,8; 1,4,7; 2,5,8; 3,4,5; 6,7,8 e 2,4,6
        posiçoes = [[0,0,0],[0,1,1],[0,2,2],[1,0,3],[1,1,4],[1,2,5],[2,0,6],[2,1,7],[2,2,8]] #O último index de cada sub-lista representa o id de cada posição
        id_posiçao = -1 # id da posição do espaço que a máquina tem que ocupar para impedir que o utilizador ganhe. -1 não representa nenhum id.
        #verificar se esta jogada garante-lhe a vitória.
        id_posiçao = vencerOJogo(id_posiçao, tabuleiro,posiçoes)
        if id_posiçao == -1: #Significa que a máquina não se encontra em nenhuma situação preocupante, podendo então, optar por uma jogada ofensiva.
            #verificar se a máquina precisa de ocupar um espaço para evitar a vitória do adversário.
            id_posiçao = impedirDerrota(id_posiçao, tabuleiro,posiçoes)
            if id_posiçao == -1: #Se a máquina não consegue ganhar ainda nesta jogada
                #Depois de vários jogos feitos contra o computador do site https://www.hypatiamat.com/jogos/jogoDoGalo/jogoDoGalo_Vhtml.html,
                # descobri duas estratégias para ganharmos garantidamente um jogo, isto é, se formos os primeiros a jogar e
                # na segunda jogada o espaço do meio não for ocupado. Todas as respostas que a máquina deve dar, dado a primeira
                #jogada do utilizador, estão mais detalhados no ficheiro drawio anexado.
                if tabuleiro[1][1] == ' ': #Se o meio ainda não foi ocupado
                    novaPosiçao = usarEstrategia(tabuleiro,nr_da_jogada,estrategia,estrategia_posiçoes,linha,coluna)
                else: #Se o meio já foi ocupado, a probabilidade de alguêm ganhar é quase nula, por isso o programa vai apenas ocupar espaços aleatorios, se não estiver
                    #numa situação de perigo
                    novaPosiçao = posicionarAleatoriamente(tabuleiro)
                linha = novaPosiçao[0]
                coluna = novaPosiçao[1]
                try: estrategia_posiçoes = novaPosiçao[2]
                except: pass
                else:print(estrategia_posiçoes, 'estrategia_posiçoes go')
        if id_posiçao != -1:
            for i in range(len(posiçoes)):
                if id_posiçao == posiçoes[i][2]:
                    linha = posiçoes[i][0]
                    coluna = posiçoes[i][1]
    #Desenha o O
    tabuleiro[linha][coluna] = 'O'
    return [1, False, tabuleiro, estrategia_posiçoes]        #quem_joga = 1, tente_novamente = False e tabuleiro = [...]


#Função que verifica se precisa de impedir que o utilizador ganhe
def impedirDerrota(id_posiçao, tabuleiro,posiçoes):
    #listar todas as coordenadas do tabuleiro com os seus respetivos ids:
    sequencias = [[0,1,2],[0,3,6],[0,4,8],[1,4,7],[2,5,8],[3,4,5],[6,7,8],[2,4,6]] 
    posiçoesAtuaisX = [] #lista com todas as coordenadas dos X existentes no tabuleiro
    #Estrutura de repetição que vai listar todas as coordenadas dentro da lista da variável posiçoesAtuaisX
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j] == 'X':
                posiçoesAtuaisX.append([i,j])
    #Exemplo de uma lista que posiçoesAtuaisX pode armazenar = [[0,0], [0,2], [1,2], [2,2]]
    #Estrutura de repetição que vai marcar os ids respetivos de todas as coordenadas dentro da lista da variável posiçoesAtuaisX
    for i in range(len(posiçoesAtuaisX)):      #Por exemplo, se 0 ->[1,0]
        for ii in range(len(posiçoes)):      #0 -> [0,0,0], 1 -> [0,1,1] ... 3 -> [1,0,3]
            if posiçoesAtuaisX[i][0] == posiçoes[ii][0] and posiçoesAtuaisX[i][1] == posiçoes[ii][1]:
                posiçoesAtuaisX[i].append(posiçoes[ii][2])      #[1,0].append(3) = [1,0,3]
    #A nesma lista atualizada = [[0,0,0], [0,2,2], [1,2,5], [2,2,8]]
    for i in range(len(posiçoesAtuaisX)):      #Por exemplo, se 0 ->[1,0,3]
        for ii in range(len(sequencias)):      #0 -> [0,1,2], 1 -> [0,3,6]
            for j in range(len(sequencias[ii])):        #0 -> 0, 1-> 3
                if posiçoesAtuaisX[i][2] == sequencias[ii][j]:      #3 == 3
                    del sequencias[ii][j]       #[[0,1,2],[0,6],[0,4,8],[1,4,7],[2,5,8],[4,5],[6,7,8],[2,4,6]] 
                    if len(sequencias[ii]) == 1:
                        linha = posiçoes[sequencias[ii][0]][0]
                        coluna = posiçoes[sequencias[ii][0]][1]
                        if tabuleiro[linha][coluna] != 'O': #Se a máquina ainda não ocupou esse espaço. Esta condição é importante ser verificada, porque se a máquina já ocupou esse espaço
                        #o programa tem que, então, ignorar este espaço, senão o programa irá lembrar-se sempre que esse espaço é para ser ocupado.
                            id_posiçao = sequencias[ii][0]
                    break
    return id_posiçao


def vencerOJogo(id_posiçao, tabuleiro,posiçoes):
    #listar todas as coordenadas do tabuleiro com os seus respetivos ids:
    sequencias = [[0,1,2],[0,3,6],[0,4,8],[1,4,7],[2,5,8],[3,4,5],[6,7,8],[2,4,6]] 
    posiçoesAtuaisO = [] #lista com todas as coordenadas dos O existentes no tabuleiro
    #Estrutura de repetição que vai listar todas as coordenadas dentro da lista da variável posiçoesAtuaisO
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j] == 'O':
                posiçoesAtuaisO.append([i,j])
    #Exemplo de uma lista que posiçoesAtuaisO pode armazenar = [[0,0], [0,2], [1,2], [2,2]]
    #Estrutura de repetição que vai marcar os ids respetivos de todas as coordenadas dentro da lista da variável posiçoesAtuaisO
    for i in range(len(posiçoesAtuaisO)):      #Por exemplo, se 0 ->[1,0]
        for ii in range(len(posiçoes)):      #0 -> [0,0,0], 1 -> [0,1,1] ... 3 -> [1,0,3]
            if posiçoesAtuaisO[i][0] == posiçoes[ii][0] and posiçoesAtuaisO[i][1] == posiçoes[ii][1]:
                posiçoesAtuaisO[i].append(posiçoes[ii][2])      #[1,0].append(3) = [1,0,3]
    #A nesma lista atualizada = [[0,0,0], [0,2,2], [1,2,5], [2,2,8]]
    for i in range(len(posiçoesAtuaisO)):      #Por exemplo, se 0 ->[1,0,3]
        for ii in range(len(sequencias)):      #0 -> [0,1,2], 1 -> [0,3,6]
            for j in range(len(sequencias[ii])):        #0 -> 0, 1-> 3
                if posiçoesAtuaisO[i][2] == sequencias[ii][j]:      #3 == 3
                    del sequencias[ii][j]       #[[0,1,2],[0,6],[0,4,8],[1,4,7],[2,5,8],[4,5],[6,7,8],[2,4,6]] 
                    if len(sequencias[ii]) == 1:
                        linha = posiçoes[sequencias[ii][0]][0]
                        coluna = posiçoes[sequencias[ii][0]][1]
                        if tabuleiro[linha][coluna] != 'X': #Se o utilizador ainda não ocupou esse espaço. Esta condição é importante ser verificada, porque se o utilizador já ocupou esse espaço
                        #o programa tem que, então, ignorar este espaço, senão o programa irá lembrar-se sempre que esse espaço é para ser ocupado.
                            id_posiçao = sequencias[ii][0]
                    break
    return id_posiçao


#Para o computador saber qual é o espaço que tem que ocupar, com base na primeira jogada do utilizador 
def usarEstrategia(tabuleiro,nr_da_jogada,estrategia,estrategia_posiçoes,linha,coluna):
    if nr_da_jogada == 2: #Se a segunda jogada da máquina for a terceira do jogo. Por outras palavras, a máquina jogou (nr_da_jogada=0), depois jogou o tuilizador (nr_da_jogada=1) jogou e agora é a vez da máquina a jogar (nr_da_jogada=3) 
        #Para verificar se a primeira condição é verdadeira (ver documento drawio)
        if tabuleiro[0][2] == 'O' and tabuleiro[1][0] == 'X':
            estrategia_posiçoes = [[0,0],[2,2]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0]
        elif tabuleiro[0][2] == 'O' and tabuleiro[2][1] == 'X':
            estrategia_posiçoes = [[2,2],[0,0]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[2][2] == 'O' and tabuleiro[1][0] == 'X':      
            estrategia_posiçoes = [[2,0],[0,2]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[2][2] == 'O' and tabuleiro[0][1] == 'X':
            estrategia_posiçoes = [[0,2],[2,0]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[2][0] == 'O' and tabuleiro[1][2] == 'X':      
            estrategia_posiçoes = [[0,0],[2,2]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[2][0] == 'O' and tabuleiro[0][1] == 'X':
            estrategia_posiçoes = [[2,2],[0,0]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[0][0] == 'O' and tabuleiro[2][1] == 'X':      
            estrategia_posiçoes = [[2,0],[0,2]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        elif tabuleiro[0][0] == 'O' and tabuleiro[1][2] == 'X':
            estrategia_posiçoes = [[0,2],[2,0]]
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
            del estrategia_posiçoes[0] 
        if linha != -1:  # Se a primeira condição for verdadeira
            estrategia = 2
        else: # Se a primeira condição não for verdadeira
            #Para verificar se a segunda condição é verdadeira (ver documento drawio)
            if estrategia == 1: #Para estratégia 1
                numero_random = randint(0,1)
                if tabuleiro[0][2] == 'O' and tabuleiro[2][0] == 'X':
                    estrategia_posiçoes = [[2,2],[0,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[0][2] == 'O' and tabuleiro[2][2] == 'X':
                    estrategia_posiçoes = [[2,0],[0,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[0][2] == 'O' and tabuleiro[0][0] == 'X':
                    estrategia_posiçoes = [[2,2],[2,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][2] == 'O' and tabuleiro[0][0] == 'X':      
                    estrategia_posiçoes = [[2,0],[0,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][2] == 'O' and tabuleiro[0][2] == 'X':      
                    estrategia_posiçoes = [[2,0],[0,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][2] == 'O' and tabuleiro[2][0] == 'X' :      
                    estrategia_posiçoes = [[0,0],[0,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][0] == 'O' and tabuleiro[0][0] == 'X' :      
                    estrategia_posiçoes = [[0,2],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][0] == 'O' and tabuleiro[0][2] == 'X':      
                    estrategia_posiçoes = [[0,0],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[2][0] == 'O' and tabuleiro[2][2] == 'X':      
                    estrategia_posiçoes = [[0,0],[0,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[0][0] == 'O' and tabuleiro[2][0] == 'X':      
                    estrategia_posiçoes = [[0,2],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[0][0] == 'O' and tabuleiro[2][2] == 'X':      
                    estrategia_posiçoes = [[0,2],[2,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
                elif tabuleiro[0][0] == 'O' and tabuleiro[0][2] == 'X':      
                    estrategia_posiçoes = [[2,0],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random] 
            else: #Para estratégia 2
                numero_random = randint(0,1)
                if tabuleiro[0][2] == 'O' and tabuleiro[0][1] == 'X':
                    estrategia_posiçoes = [[2,0],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[0][2] == 'O' and tabuleiro[1][2] == 'X':
                    estrategia_posiçoes = [[0,0],[2,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[2][2] == 'O' and tabuleiro[2][1] == 'X':      
                    estrategia_posiçoes = [[0,0],[0,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[2][2] == 'O' and tabuleiro[1][2] == 'X' :      
                    estrategia_posiçoes = [[0,2],[2,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[2][0] == 'O' and tabuleiro[2][1] == 'X':      
                    estrategia_posiçoes = [[0,2],[0,0]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[2][0] == 'O' and tabuleiro[1][0] == 'X':      
                    estrategia_posiçoes = [[0,2],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[0][0] == 'O' and tabuleiro[0][1] == 'X':      
                    estrategia_posiçoes = [[2,0],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                elif tabuleiro[0][0] == 'O' and tabuleiro[1][0] == 'X':      
                    estrategia_posiçoes = [[0,2],[2,2]]
                    linha = estrategia_posiçoes[numero_random][0]
                    coluna = estrategia_posiçoes[numero_random][1]
                    del estrategia_posiçoes[numero_random]
                if linha == -1: # Se a segunda condição não for verdadeira
                    #Para verificar se a terceira condição é verdadeira (ver documento drawio)
                    if estrategia == 1: #Para a estratégia 1
                        if tabuleiro[0][2] == 'O' and tabuleiro[0][1] == 'X':
                            linha = 1
                            coluna = 2
                        elif tabuleiro[0][2] == 'O' and tabuleiro[1][2] == 'X':
                            linha = 0
                            coluna = 1
                        elif tabuleiro[2][2] == 'O' and tabuleiro[2][1] == 'X':      
                            linha = 1
                            coluna = 2
                        elif tabuleiro[2][2] == 'O' and tabuleiro[1][2] == 'X' :      
                            linha = 2
                            coluna = 1
                        elif tabuleiro[2][0] == 'O' and tabuleiro[2][1] == 'X':      
                            linha = 1
                            coluna = 0
                        elif tabuleiro[2][0] == 'O' and tabuleiro[1][0] == 'X':      
                            linha = 2
                            coluna = 1
                        elif tabuleiro[0][0] == 'O' and tabuleiro[0][1] == 'X':      
                            linha = 1
                            coluna = 0
                        elif tabuleiro[0][0] == 'O' and tabuleiro[1][0] == 'X':      
                            linha = 0
                            coluna = 1
                    else: #Para estratégia 2
                        numero_random = randint(0,1)
                        if tabuleiro[0][2] == 'O' and tabuleiro[0][0] == 'X':
                            estrategia_posiçoes = [[2,0],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[0][2] == 'O' and tabuleiro[2][2] == 'X':
                            estrategia_posiçoes = [[0,0],[2,0]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[0][2] == 'O' and tabuleiro[2][0] == 'X':
                            estrategia_posiçoes = [[0,0],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][2] == 'O' and tabuleiro[2][0] == 'X':      
                            estrategia_posiçoes = [[0,0],[0,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][2] == 'O' and tabuleiro[0][2] == 'X' :      
                            estrategia_posiçoes = [[0,0],[2,0]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][2] == 'O' and tabuleiro[0][0] == 'X' :      
                            estrategia_posiçoes = [[0,2],[2,0]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][0] == 'O' and tabuleiro[2][2] == 'X':      
                            estrategia_posiçoes = [[0,2],[0,0]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][0] == 'O' and tabuleiro[0][0] == 'X':      
                            estrategia_posiçoes = [[0,2],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[2][0] == 'O' and tabuleiro[0][2] == 'X':      
                            estrategia_posiçoes = [[0,0],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[0][0] == 'O' and tabuleiro[0][2] == 'X':      
                            estrategia_posiçoes = [[2,0],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[0][0] == 'O' and tabuleiro[2][0] == 'X':      
                            estrategia_posiçoes = [[0,2],[2,2]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
                        elif tabuleiro[0][0] == 'O' and tabuleiro[2][2] == 'X':      
                            estrategia_posiçoes = [[0,2],[2,0]]
                            linha = estrategia_posiçoes[numero_random][0]
                            coluna = estrategia_posiçoes[numero_random][1]
                            del estrategia_posiçoes[numero_random]
    if nr_da_jogada == 4: #Nesta jogada, o computador vai fazer "check mate" ao utilizador
        if estrategia_posiçoes == []: #Significa que a máquina está a usar a estratégia 1
            linha = 1
            coluna = 1
        else: #Se o programa estiver a usar a estratégia 2
            linha = estrategia_posiçoes[0][0]
            coluna = estrategia_posiçoes[0][1]
        estrategia_posiçoes = []
    return [linha,coluna,estrategia_posiçoes]


#Função que vai ocupar um espaço aleatoriamente, uma vez que o espaço do meio já foi ocupado e não há hipóteses de ganhar.
def posicionarAleatoriamente(tabuleiro):
    numero_random = randint(0,2)
    repetir= True
    while repetir:
        if tabuleiro[numero_random].count(' ') > 0:
            numero_random1 = randint(0,2)
            if tabuleiro[numero_random][numero_random1] == ' ':
                tabuleiro[numero_random][numero_random1] == 'O'
                return [numero_random, numero_random1]
            

# Para verificar se o jogo já terminou
def analisarTabuleiro(tabuleiro): 
    #Não usei estruturas de repetição for/while para descobrir quem foi o vencedor ou se foi empate, porque a lista tem apenas três listas
    #Se uma das filas forem ocupadas por três símbolos iguais: 
    if tabuleiro[0] == ['X','X','X'] or tabuleiro[1] == ['X','X','X'] or tabuleiro[2] == ['X','X','X']:
        return 2
    elif tabuleiro[0] == ['O','O','O'] or tabuleiro[1] == ['O','O','O'] or tabuleiro[2] == ['O','O','O']:
        return 2
    #Se três símbolos iguais ocuparem uma das duas diagonais: 
    if ((tabuleiro[0][0] == 'X' and tabuleiro[1][1] == 'X' and tabuleiro[2][2] == 'X') or 
    (tabuleiro[2][0] == 'X' and tabuleiro[1][1] == 'X' and tabuleiro[0][2] == 'X')):
        return 2
    elif ((tabuleiro[0][0] == 'O' and tabuleiro[1][1] == 'O' and tabuleiro[2][2] == 'O') or 
    (tabuleiro[2][0] == 'O' and tabuleiro[1][1] == 'O' and tabuleiro[0][2] == 'O')):
        return 2
    #Se uma das colunas forem ocupadas por três símbolos iguais: 
    if ((tabuleiro[0][0] == 'X' and tabuleiro[1][0] == 'X' and tabuleiro[2][0] == 'X') or 
    (tabuleiro[0][1] == 'X' and tabuleiro[1][1] == 'X' and tabuleiro[2][1] == 'X') or
    (tabuleiro[0][2] == 'X' and tabuleiro[1][2] == 'X' and tabuleiro[2][2] == 'X')):
        return 2
    elif ((tabuleiro[0][0] == 'O' and tabuleiro[1][0] == 'O' and tabuleiro[2][0] == 'O') or 
    (tabuleiro[0][1] == 'O' and tabuleiro[1][1] == 'O' and tabuleiro[2][1] == 'O') or
    (tabuleiro[0][2] == 'O' and tabuleiro[1][2] == 'O' and tabuleiro[2][2] == 'O')):
        return 2
    #se todos os espaços vazios do tabuleiro foram ocupados, significa que é empate
    if tabuleiro[0].count(' ') + tabuleiro[1].count(' ') + tabuleiro[2].count(' ') == 0:
        return 3
    #caso contrário, o jogo continuará.
    return False
    

#Contra um amigo
def vsAmigo(player1,player2,jogar_novamente):
    linha,coluna = 0,0
    resultados = []
    width_consola = os.get_terminal_size().columns  
    tabuleiro = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    tente_novamente = False
    quem_joga = randint(1,2)
    fim_do_jogo = False
    for i in range(10):    #É de 0 a 10, porque se formos os primeiros a jogar, a primeira iteração não conta. A primeira iteração serve para mostrar apenas o tabuleiro vazio
        print('\n'*10)     # substitui os.system('cls') por este print, uma vez que se eu fizesse scroll para cima na consola, 
        #algumas partes dos tabuleiros antigos apareciam e sujavam a consola. Este problema de os.system('cls') não conseguir
        #apagar totalmente a consola deve-se secalhar ao facto de ser chamada muitas vezes
        if quem_joga == 1:
            desenharTabuleiro(tabuleiro,width_consola)
            if fim_do_jogo:
                if fim_do_jogo == 3:
                    print('\t\t\tEmpate!' ,end="")
                else: print('\t\t\tParabéns {0} Foste o Vencedor!' .format(player2) , end="")
                jogar_novamente = input('\t Jogar novamente? (S/N): ')
                if jogar_novamente.upper() == 'S':
                    os.system('cls')
                    return 'S'
                else:
                    return 'N'
            if tente_novamente:
                print('\t\t\tCoordenadas Inválidas! {0} Tente Novamente!' .format(player1),end="")
                tente_novamente = False
            else:
                print('\t\t\tÉ a Vez de {0} Jogar!' .format(player1),end="\t")
            linha_valida = True
            coluna_valida = True
            while linha_valida:
                try: linha = int(input('\t\t\tLinha: '))
                except: print('\t\t\tNúmero válido por favor')
                else: linha_valida = False
            while coluna_valida:
                try: coluna = int(input('\t\t\tColuna: '))
                except: print('\t\t\tNúmero válido por favor')
                else: coluna_valida = False
            resultados = desenharX(tabuleiro,linha,coluna,quem_joga,tente_novamente)
            quem_joga,tente_novamente = resultados[0], resultados[1]
            fim_do_jogo = analisarTabuleiro(tabuleiro)
        else:
            desenharTabuleiro(tabuleiro,width_consola)
            if fim_do_jogo:
                if fim_do_jogo == 3:
                    print('\t\t\tEmpate!' ,end="")
                else: print('\t\t\tParabéns {0} Foste o Vencedor!' .format(player1) , end="")
                jogar_novamente = input('\t Jogar novamente? (S/N): ')
                if jogar_novamente.upper() == 'S':
                    os.system('cls')
                    return 'S'
                else:
                    return 'N'
            if tente_novamente:
                print('\t\t\tCoordenadas Inválidas! {0} Tente Novamente!' .format(player2),end="")
                tente_novamente = False
            else:
                print('\t\t\tÉ a Vez de {0} jogar!' .format(player2),end="\t")
            linha_valida = True
            coluna_valida = True
            while linha_valida:
                try: linha = int(input('\t\t\tLinha: '))
                except: print('\t\t\tNúmero válido por favor')
                else: linha_valida = False
            while coluna_valida:
                try: coluna = int(input('\t\t\tColuna: '))
                except: print('\t\t\tNúmero válido por favor')
                else: coluna_valida = False
            resultados = desenharO(tabuleiro,linha,coluna,quem_joga,tente_novamente)
            quem_joga,tente_novamente = resultados[0], resultados[1]
            fim_do_jogo = analisarTabuleiro(tabuleiro)


#Contra o computador
def vsMaquina(jogar_novamente,estrategia,quem_joga):
    resultados = []
    width_consola = os.get_terminal_size().columns  #Ler o primeiro comentário para perceber esta variável
    tabuleiro = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    tente_novamente = False
    fim_do_jogo = False
    estrategia_posiçoes = []
    for nr_da_jogada in range(10): #É de 0 a 10, porque se formos os primeiros a jogar, a primeira iteração não conta. A primeira iteração serve para mostrar apenas o tabuleiro vazio
        print('\n'*10)  
        print(nr_da_jogada, "nr_da_jogada")
        if quem_joga == 1: #Se é a vez do utilizador a jogar
            desenharTabuleiro(tabuleiro,width_consola)
            if fim_do_jogo:
                if fim_do_jogo == 3:
                    print('\t\t\tEmpate!' ,end="")
                else: print('\t\t\tA Máquina Foi a Vencedora!', end="")
                jogar_novamente = input('\t Jogar novamente? (S/N): ')
                if jogar_novamente.upper() == 'S':
                    os.system('cls')
                    return 'S'
                else:
                    return 'N'
            if tente_novamente:
                print('\t\t\tCoordenadas Inválidas! Tente Novamente!',end="")
                tente_novamente = False
            else:
                print('\t\t\tÉ a Tua Vez de Jogar!' ,end="\t")
            linha_valida = True
            coluna_valida = True
            while linha_valida:
                try: linha = int(input('\t\t\tLinha: '))
                except: print('\t\t\tNúmero válido por favor')
                else: linha_valida = False
            while coluna_valida:
                try: coluna = int(input('\t\t\tColuna: '))
                except: print('\t\t\tNúmero válido por favor')
                else: coluna_valida = False
            resultados = desenharX(tabuleiro,linha,coluna,quem_joga,tente_novamente)
            quem_joga,tente_novamente = resultados[0], resultados[1]
            fim_do_jogo = analisarTabuleiro(tabuleiro)
        else:   #Se é vez da máquina a jogar
            desenharTabuleiro(tabuleiro,width_consola)
            if fim_do_jogo:
                if fim_do_jogo == 3:
                    print('\t\t\tEmpate!' ,end="")
                else: print('\t\t\tParabéns Foste o Vencedor!' , end="")
                jogar_novamente = input('\t Jogar novamente? (S/N): ')
                if jogar_novamente.upper() == 'S':
                    os.system('cls')
                    return 'S'
                else:
                    return 'N'
            resultados = analisarAMelhorJogada(tabuleiro,nr_da_jogada,estrategia,estrategia_posiçoes)
            quem_joga,tente_novamente,tabuleiro,estrategia_posiçoes = resultados[0], resultados[1], resultados[2], resultados[3]
            fim_do_jogo = analisarTabuleiro(tabuleiro)


def menuJogarPrimeiro():
        opçao1 = input('\n\n\n\t\t\tQUEM COMEÇA PRIMEIRO?\n\t\t\t1-Eu\n\t\t\t2-Computador\n\t\t\t3-Aleatorio\n\t\t\t0-Retroceder\n\t\t\tEscolha uma opção: ')
        estrategia = randint(1,2) #O computador vai escolher aleatoriamente uma das estratégias.
        if opçao1 == '1':
            quem_joga = 1
        elif opçao1 == '2':
            quem_joga = 2
        elif opçao1 == '3':
            quem_joga = randint(1,2)
        elif opçao1 == '0':
            os.system('cls')
            quem_joga = -1
        else:
            print('\n'*20)
            print('\t\t\tEscolha uma das opções, por favor.')
            return menuJogarPrimeiro()
        return [estrategia,quem_joga,opçao1]


jogar_novamente = "S"
while jogar_novamente.upper() == 'S':
    opçao = input('\n\n\n\t\t\tMENU\n\t\t\t1-Jogar com um amigo\n\t\t\t2-Jogar contra o computador\n\t\t\t0-Sair\n\t\t\tEscolha uma opção: ')
    if opçao == '1':
        os.system('cls')
        player1 = input('\n\n\n\t\t\tNome do Player 1: ')
        os.system('cls')
        nomes_iguais = True
        while nomes_iguais:
            player2 = input('\n\n\n\t\t\tNome do Player 2: ')
            os.system('cls')
            if player2 != player1:
                nomes_iguais = False
            else:
                print('\n\n\n\t\t\tPlayer 2 Não Pode Ter o Mesmo Nome Que o Player 1, Insira Outro Nome Por Favor.')
        jogar_novamente = vsAmigo(player1,player2,jogar_novamente)
    elif opçao == '2':
        print('\n'*10)
        escolha = menuJogarPrimeiro()
        estrategia = escolha[0]
        quem_joga = escolha[1]
        opçao1 = escolha[2]
        if opçao1 != '0':
            jogar_novamente = vsMaquina(jogar_novamente,estrategia,quem_joga) 
        
    elif opçao == '0':
        jogar_novamente = 'N'
    else:
        print('\n'*20)
        print('\t\t\tEscolha uma das opções, por favor.')

