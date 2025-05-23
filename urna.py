import tkinter as tk
from tkinter import messagebox, filedialog, font
from fpdf import FPDF
from PIL import Image, ImageTk
import json
from datetime import datetime
import webbrowser

# Criação da janela pelo tkinter
janela = tk.Tk()
janela.title("Urna eletrônica") # Titulo da window aberta pelo Sistema Operacional

janela_largura = 800 # largura da window que se abre na tela
janela_altura = 600 # altura da window que se abre na tela

# Criação das váriaveis para centralizar a janela
largura_tela = janela.winfo_screenwidth() # largura da tela do usuário
altura_tela = janela.winfo_screenheight() # altura da tela do usuário

posx = (largura_tela - janela_largura) // 2 # Posição x da janela (ponto mais a esquerda da window)
posy = (altura_tela - janela_altura) // 2 # Posição y da janela (ponto mais alto da window)

# Criação da base do arquivo PDF que vai conter os resultados da votação
saida_pdf = FPDF() # Inicializa o arquivo onde será atribuid
saida_pdf.add_page() # Adciona uma página ao PDF

# Váriaveis para funcionalidade do código
with open("candidatos.json", "r", encoding="utf-8") as arquivo:
    candidatos = json.load(arquivo)
votacao_ativa = False

# Definição das fontes
fonte_titulo = font.Font(family="Helvetica", size=40, weight="bold")
fonte_media = font.Font(family="Helvetica", size=19, weight="bold")
fonte_pequena = font.Font(family="Helvetica", size=13)

# Mostra a tela inicial
def mostra_menu():
    # Definições básicas da janela atual
    janela.configure(bg="#f0f0f0", padx=20, pady=60) # Adiciona fundo cinza claro e margem grande
    janela.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # Define a proporção e posição (centralizada) da janela 

    label_menu = tk.Label(janela, text="Escolha uma opção:", bg="#f0f0f0", font=fonte_titulo) # "Caixa" p/ exibir texto ou imagem
    label_menu.pack(pady=10) # Espaçamento entre o rótulo e os botões

    botao1 = tk.Button(janela, text="Cadastro de Candidato", command=cadastra_candidato) # Botão que chama função determinada ao clicar
    botao1.pack(pady=50) # Espaçamento vertical até o próximo widget na janela

    botao2 = tk.Button(janela, text="Iniciar Votação", command=iniciar_votacao) # Linha 45
    botao2.pack(pady=5) # Linha 46

    botao3 = tk.Button(janela, text="Encerrar Votação", command=encerrar_votacao) # Linha 45
    botao3.pack(pady=5) # Linha 46

    janela.mainloop() # Mantém a janela rodando (sem isso ela abriria e fecharia logo em seguida, sem se quer ser visivel)

# Exibe uma imagem em uma das janelas
def exibir_imagens(tela, imagem_tk):
    label_imagem = tk.Label(tela, image=imagem_tk) # Linha 42
    label_imagem.image = imagem_tk # Garante que a imagem não se perde no parâmetro do Label

    label_imagem.pack(pady=5) # Linha 46

# Carrega/Renderiza as imagens a partir do caminho delas
def carregar_imagem(caminho):
    imagem = Image.open(caminho) # Recebe um caminho de arquivo e o renderiza como iamgem

    imagem_redimensionada = imagem.resize((200, 200)) # Redimensiona, para tornar padrão
    
    return ImageTk.PhotoImage(imagem_redimensionada) # Retorna a imagem totalmente tratada

# Mostra a tela de cadastro de candidatos
def cadastra_candidato():
    janela.withdraw() # Esconde a janela inicial
    janela_cadastro = tk.Toplevel() # Cria um "filho" da var janela para ser exibido
    janela_cadastro.protocol("WM_DELETE_WINDOW", janela.destroy) # Caso o usuário feche a janela filha, o programa para

    # Definições básicas da janela atual
    janela_cadastro.title("Cadastro de Candidato") # Linha 9
    janela_cadastro.configure(bg='#f0f0f0') # Linha 39
    janela_cadastro.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40

    # Conteúdo da janela atual
    tk.Label(janela_cadastro, text="Número do Candidato:").pack(pady=5) # Linha 42
    entrada_numero = tk.Entry(janela_cadastro) # Input que recebe "Número do Candidato"
    entrada_numero.pack(pady=5) # Linha 46

    tk.Label(janela_cadastro, text="Nome do Candidato:").pack(pady=5) # Linha 42
    entrada_nome = tk.Entry(janela_cadastro) # Input que recebe "Nome do Candidato"
    entrada_nome.pack(pady=5) # Linha 46

    tk.Label(janela_cadastro, text="Partido do Candidato:").pack(pady=5) # Linha 42
    entrada_partido = tk.Entry(janela_cadastro) # Input que recebe "Partido do Candidato"
    entrada_partido.pack(pady=5) # Linha 46
    
    # Dicionário para guardar as informações ultima imagem escolhida
    candidato_imgs = {
        "imagem_path": None,
        "imagem_tk": None
    }

    # Abre o gerenciador de arquivos para a escolha da imagem
    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem", # Titulo da janela do gerenciador de arquivos
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")] # Legenda (à direita da barra de pequisa) e extensões escolhiveis
        )
        if caminho:
            imagem_tk = carregar_imagem(caminho) # Linha 86

            candidato_imgs["imagem_path"] = caminho # Guarda o caminho do arquivo da imagem atual
            candidato_imgs["imagem_tk"] = imagem_tk # Guarda a imagem renderizada atual

            exibir_imagens(janela_cadastro, imagem_tk) # Mostra a ultima imagem escolhida pelo usuário

    # Conteúdo da janela - Continuação
    tk.Button(janela_cadastro, text="Escolher imagem:", command=escolher_imagem).pack(pady=5) # Linha 45; Linha 46

    tk.Button(janela_cadastro, text="Voltar",
        command=lambda: (janela_cadastro.destroy(), janela.deiconify())).pack(pady=5) # Linha 45; Destrói janela atual e desesconde janela principal; Linha 46

    # Salva as informações atuais na lista candidato como um candidato novo
    def salvar_candidato():
        # Pega os valores dos inputs
        numero = entrada_numero.get() # Recebe a string guardada em entada_numero
        nome = entrada_nome.get() # Recebe a string guardada em entada_nome
        partido = entrada_partido.get() # Recebe a string guardada em entada_partido

        # Verifica se algum input ficou vazio
        if numero.strip() == '' or nome.strip() == '' or partido.strip() == '':
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return

        # Verifica se número ou partido do candidato é repetido
        for c in candidatos:
            if c['numero'] == numero or c['partido'] == partido:
                if c['numero'] == numero and c['partido'] == partido:
                    menssagem = "Número e Partido do candidato já cadastrados."
                elif c['numero'] == partido:
                    menssagem = "Número do candidato já cadastrado."
                else:
                    menssagem = "Partido do candidato já cadastrado."

                messagebox.showwarning("Erro", f"{menssagem}")
                return
        
        # Adciona os dados validados do candidato a lista dos candidatos 
        candidatos.append({"numero": numero,
                            "nome": nome,
                            "partido": partido,
                            "foto": candidato_imgs["imagem_path"] if candidato_imgs["imagem_path"] else None,
                            "votos": 0})

        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!") # Retorna menssagem em pop-up

        # Reseta a tela
        janela_cadastro.destroy()
        cadastra_candidato()

        # Por ultimo, reescreve o conteúdo do JSON
        with open("candidatos.json", "w", encoding="utf-8", ) as arquivo:
            json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

    tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato).pack(pady=5) # Linha 45; Linha 46

# Inicia a votação e a formatação do PDF
def iniciar_votacao():
    # Váriavel que permite a execução de registrar voto e impede encerrar votação sem iniciar antes
    global votacao_ativa
    votacao_ativa = True

    # Informações de tempo
    agora = datetime.now() # Tempo atual do mundo, mês, dia, ano, hora, minuto, segundo, milisegundos
    data_votacao = agora.date() # Apenas a data do tempo atual do mundo
    inicio_votacao = agora.strftime("%H:%M:%S") # Apenas as horas, minutos e segundos do tempo atual do mundo

    # Formatações do PDF
    saida_pdf.set_font('Arial', size=12) # Define a fonte a paritr desse ponto do PDF
    saida_pdf.cell(95, 10, txt=f"Data: {data_votacao}", ln=False, align="L") # Data no topo a esquerda
    saida_pdf.cell(95, 10, txt=f"Inicio da votação: {inicio_votacao}", ln=True, align="R") # Hora no topo a direita
    saida_pdf.set_font('Arial', 'B', size=30) # Define a fonte a paritr desse ponto do PDF
    saida_pdf.cell(190, 40, txt="Resultados da votação:", ln=True, align="C") # Titulo centralizado abaixo das informações de tempo

    registrar_voto()

# Mostra os candidatos disponíveis e registra os votos do usuário 
def registrar_voto():
    if votacao_ativa:
        janela.withdraw() # Linha 65
        janela_votacao = tk.Toplevel() # Linha 66
        janela_votacao.protocol("WM_DELETE_WINDOW", janela.destroy) # Linha 67

        # Definições básicas da janela atual
        janela_votacao.title("Votação") # Linha 9
        janela_votacao.configure(bg="#f0f0f0") # Linha 39
        janela_votacao.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40

        # Conteúdo da janela atual
        # Frame que envolve toda a janela
        frame_principal = tk.Frame(janela_votacao)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Lado esquerdo
        frame_esquerda = tk.Frame(frame_principal)
        frame_esquerda.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        tk.Button(frame_esquerda, text="Voltar", command=lambda: (janela_votacao.destroy(), janela.deiconify())).pack(padx=10, pady=(20,5), anchor="w") # Linha
        tk.Label(frame_esquerda, text="Digite sua matrícula:", font=fonte_pequena).pack(padx=10, pady=5, anchor="w") # Linha 42
        entrada_matricula = tk.Entry(frame_esquerda)
        entrada_matricula.pack(padx=10, pady=5, anchor="w")
        tk.Label(frame_esquerda, text="Digite o número do candidato:", font=fonte_pequena).pack(padx=10, pady=5, anchor="w") # Linha 42
        entrada_voto = tk.Entry(frame_esquerda)
        entrada_voto.pack(padx=10, pady=5, anchor="w")

    # Valida as informações e altera o JSON
    def confirmar_voto():
        matricula = entrada_matricula.get() # Linha
        voto = entrada_voto.get() # Linha
        if not matricula:
            messagebox.showwarning("Erro", "Matrícula não pode ser vazia.") # Linha
            return # Linha
        c_e = next((c for c in candidatos if c["numero"] == voto), None) # c_e = candidato de número igual ao voto
        if not c_e:
            messagebox.showwarning("Erro", "Número de candidato inválido.") # Linha
            return # Linha
        if c_e:
            confirmar = messagebox.askyesno("Confirmação",
                f"Confirmar voto para {c_e['nome']} ({c_e['partido']})?") # pop-up de confirmação (sim/não)

            # Finaliza operação de voto
            if confirmar:
                c_e["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!") # Linha
            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")  # Linha
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")  # Linha

            # Linha
            janela_votacao.destroy()
            registrar_voto()

            # Linha 161
            with open("candidatos.json", "w", encoding="utf-8") as arquivo:
                json.dump(candidatos, arquivo, indent=4, ensure_ascii=False)

    # Centro
    frame_central = tk.Frame(frame_principal)
    frame_central.grid(row=0, column=1, sticky="n", padx=10, pady=10)

    # Linha
    botao_votar = tk.Button(frame_central, text="Votar", command=confirmar_voto, bg="green") # Linha 45
    botao_votar.pack(side="bottom", pady=10) # Linha

    # Lado direito
    frame_direita = tk.Frame(frame_principal)
    frame_direita.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    tk.Label(frame_direita, text="Candidatos disponiveis", font=fonte_pequena).pack(pady=5) # Linha 42

    # Frame com barra de rolagem para os candidatos
    frame_scroll = tk.Frame(frame_direita) # Cria um frame na janela
    frame_scroll.pack(fill="both", expand=True) # Definições de proporção do frame

    canvas = tk.Canvas(frame_scroll, bg="#f0f0f0") # Cria um canvas dentro do frame criado
    scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview) # Cria uma scrollbar vertical que muda o y visivel
    canvas.configure(yscrollcommand=scrollbar.set) # Relaciona o canvas (conteúddo visivel) com o estado da scrollbar

    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0") # Mais um frame (onde o conteúdo será inserido)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    ) # Define toda a área do canvas como scrollavel

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Exibir os candidatos com imagem + texto
    for c in candidatos:
        frame_candidato = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid", padx=5, pady=5)
        frame_candidato.pack(pady=5, fill="x", expand=True)

        if c["foto"]:
            imagem_tk = carregar_imagem(c["foto"])
            exibir_imagens(frame_candidato, imagem_tk)

        info = f"Número: {c['numero']}\nNome: {c['nome']}\nPartido: {c['partido']}"
        label_info = tk.Label(frame_candidato, text=info, bg="white", justify="center") # Linha 42
        label_info.pack()

    frame_principal.grid_columnconfigure(0, weight=0)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(2, weight=2)

def imprime_relatorio():
    if not votacao_ativa:
        messagebox.showinfo("Erro", "Votação não pode ser encerrada antes de ser iniciada.")
        return
    janela.withdraw() # Linha 65
    janela_relatorio = tk.Toplevel() # Linha 66
    janela_relatorio.protocol("WM_DELETE_WINDOW", janela.destroy) # Linha 67

    # Definições básicas da janela atual
    janela_relatorio.title("Resultados") # Linha 9
    janela_relatorio.configure(bg='#f0f0f0') # linha 39
    janela_relatorio.geometry(f"{janela_largura}x{janela_altura}+{posx}+{posy}") # linha 40
    
    # Conteúdo da janela atual
    total_votos = sum(c["votos"] for c in candidatos)
    botao = tk.Button(janela_relatorio, text="Voltar", command=lambda: (janela.deiconify(), janela_relatorio.destroy())) # Linha 45; Linha 117
    botao.pack(pady=5)

    # Preenche a página e o PDF com conteúdo
    if total_votos > 0:
        mais_votos = 0
        for candidato in candidatos:
            mais_votos = candidato["votos"] if candidato["votos"] > mais_votos else mais_votos
            print(mais_votos)
            saida_pdf.set_font("Arial", size=12)
            saida_pdf.cell(190, 0, txt=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos", ln=True, align='C')
            if candidato["foto"]:
                saida_pdf.image(candidato['foto'], 80, saida_pdf.get_y(), 50, 50)
    else:
        saida_pdf.set_font("Arial", size=20)
        saida_pdf.cell(190, 50, txt="Não houve votos válidos.", ln=True, align='C')
        saida_pdf.image("logo-je.png", 55, saida_pdf.get_y(), 100)

    def gerar_pdf():
        saida_pdf.output('Resultados_Votação.pdf')
        webbrowser.open('Resultados_Votação.pdf')

    tk.Button(janela_relatorio, text="Gerar PDF", command=gerar_pdf).pack() # Linha 45

def encerrar_votacao():
    global votacao_ativa
    imprime_relatorio()

mostra_menu()