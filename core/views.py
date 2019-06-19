from django.shortcuts import render
import collections
import itertools

# Função que fará o processamento do texto.
def results(request):
    # Se o verbo da requisição for POST
    # Iremos processar os dados contidos.
    if request.method == 'POST':

        # Recebendo o input com o texto sem processamento
        texto_para_processamento = request.POST.get('texto_para_processamento')
        texto_sem_espaços_em_branco_duplicados = texto_para_processamento.split()
        # Põe os caracteres em uma lista pra segmentar a análise
        texto_pre_processado = list(texto_para_processamento)
        # A quantida de palavras é definida pela quantidade
        # de espaços na lista texto_sem_espaços_em_branco_duplicados
        quantidade_de_palavras = len(texto_sem_espaços_em_branco_duplicados)
        # Para evitar que esses caracteres sejam processados como 2 cada
        precessar_como_um_caracter = ('\n', '\r')
        # A quantidade de caracteres é o 
        # tamanho da lista texto_pre_processado
        quantidade_de_caracteres = 0
        for palavra in texto_pre_processado:
            if palavra not in precessar_como_um_caracter:
                quantidade_de_caracteres += 1
        
        quantidade_de_caracteres_sem_espaco = 0
        for palavra in texto_sem_espaços_em_branco_duplicados:
            quantidade_de_caracteres_sem_espaco += len(palavra)

        # Uma frase/período é definido pela quantidade de '.' no 
        # texto. Logo se não houverem '.' porem houverem palavras
        # a qnt de períodos vai ser 1.
        quantidade_de_frases = 0
        if quantidade_de_palavras > 0:
            quantidade_de_frases = 0
            # Um paragrafo é representado por /n
            quantidade_de_paragrafos = 1


        if quantidade_de_palavras > 1:
            for caracter in texto_pre_processado:
                # Conta as frases
                if caracter == '.':
                    quantidade_de_frases += 1
                elif caracter == '\n':
                    # Conta os paragrafos
                    quantidade_de_paragrafos += 2
        
        def contar_frequencia(texto):
            contagem_final = {} 
            conjuncoes_e_pronomes_populares = ('de', 'a', 'os', 'o', 'um', 'ou', 'e', 'que', 'Com', 'com', 'você')
            for palavra in texto:
                if not palavra in conjuncoes_e_pronomes_populares:
                    if palavra in contagem_final.keys():
                        contagem_final[palavra] += 1
                    else:
                        contagem_final[palavra] = 1

            return contagem_final

        def ordernar_dicionario(dicio):
            sorted_d = sorted(dicio.items(), key=lambda kv: kv[1], reverse=True)
            dicio_ordenado = collections.OrderedDict(sorted_d)
            dicio_limpo = {}
            # Retira caracteres especiais das palavras
            pontuacoes = ('.', ',', "...", "'")
            for chave, valor in dicio_ordenado.items():
                possivel_pontuacao = chave[-1:]
                # Verifica se há pontuação junto a palavra
                if possivel_pontuacao in pontuacoes:
                    # Retira a pontuação
                    chave_limpa = chave.strip(possivel_pontuacao)
                    # Se a chave não existir no dicio limpo a adiciona
                    if not chave_limpa in dicio_limpo.keys():
                        dicio_limpo[chave_limpa] = valor
                    # Se ela existir soma 1 ao resultado
                    else:
                        dicio_limpo[chave_limpa] += 1 
                # Mesma lógica acima porém quando a palavra não tem pontuação
                else:
                    if not chave in dicio_limpo.keys():
                        dicio_limpo[chave] = valor
                    else: 
                        dicio_limpo[chave] += valor

            return dicio_limpo

        def contar_palavras_unicas(dicio:dict):
            unicas = 0
            for palavra, frequencia in dicio.items():
                if frequencia == 1:
                    unicas += 1
            
            return unicas

        frequencia_ordenada = ordernar_dicionario(contar_frequencia(texto_sem_espaços_em_branco_duplicados))

        return render(
            request,
            template_name='core/results.html', # Caminho relativo
            context={
                'texto_recebido':texto_para_processamento,
                'quantidade_de_palavras':quantidade_de_palavras,
                'quantidade_de_caracteres':quantidade_de_caracteres,
                'caracteres_sem_espaco':quantidade_de_caracteres_sem_espaco,
                'quantidade_de_frases':quantidade_de_frases,
                'quantidade_de_paragrafos':quantidade_de_paragrafos,
                'frequencia_ordenada':frequencia_ordenada,
                'palavras_unicas': contar_palavras_unicas(frequencia_ordenada)
            }
        ) 


def index(request):
    if request.method == 'GET':
        return render(
            request,
            template_name='core/index.html', # Caminho relativo
        ) 