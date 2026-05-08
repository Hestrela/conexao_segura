import streamlit as st

# ==========================================
# 1. BANCO DE DADOS SIMPLES (Lista de Dicionários)
# ==========================================
# Fácil manutenção e expansão. Em um projeto maior, poderia vir de um JSON.
MENSAGENS = [
    {
        "texto": "⚠️ ALERTA INSS: Seu benefício será suspenso hoje. Acesse http://inss-gov-seguro.com para regularizar sua prova de vida.",
        "e_golpe": True,
        "explicacao": "Nenhum órgão do governo envia links pedindo dados com urgência. Repare no link estranho: o site oficial sempre termina com '.gov.br'."
    },
    {
        "texto": "Oi Vó, troquei de número, salva aí! Meu aplicativo travou e preciso pagar uma conta urgente, pode me emprestar R$ 500?",
        "e_golpe": True,
        "explicacao": "Golpe clássico do perfil falso! Os golpistas usam a foto de um familiar e criam uma história de urgência para pedir dinheiro."
    },
    {
        "texto": "Olá! Lembramos que sua consulta com o Dr. Carlos no Posto de Saúde está marcada para amanhã às 14h. Não é necessário responder.",
        "e_golpe": False,
        "explicacao": "Esta é uma mensagem segura. Ela apenas traz uma informação útil, não exige que você clique em links e não pede dinheiro."
    },
    {
        "texto": "Você acumulou 15.000 pontos no seu cartão de crédito! Clique aqui para resgatar sua TV de 50 polegadas antes que expirem: http://premio-facil.net",
        "e_golpe": True,
        "explicacao": "Promessas de prêmios fáceis e urgência ('antes que expirem') são armadilhas para fazer você clicar por impulso."
    }
]

# ==========================================
# 2. CONFIGURAÇÃO DE UI/UX (Frontend e CSS)
# ==========================================
def configurar_interface():
    st.set_page_config(page_title="Treino de Segurança", page_icon="📱", layout="centered")
    
    # CSS focado em ACESSIBILIDADE e compatível com MODO ESCURO/CLARO:
    st.markdown("""
        <style>
            .titulo { 
                font-size: 40px !important; 
                font-weight: 900; 
                /* Usa a cor de texto padrão do Streamlit (Preto no claro, Branco no escuro) */
                color: var(--text-color) !important; 
                text-align: center; 
                margin-bottom: 20px;
                line-height: 1.2;
            }
            .texto-grande { 
                font-size: 26px !important; 
                color: var(--text-color) !important; 
                line-height: 1.6; 
                font-weight: 600; 
            }
            .chat-bubble {
                background-color: #E6F3FF; /* Azul claro fixo */
                border: 4px solid #0056B3; 
                border-radius: 15px;
                padding: 30px;
                margin: 30px 0;
                font-size: 30px; 
                font-weight: 700;
                /* Como o fundo é sempre claro, o texto DEVE ser preto para manter o contraste */
                color: #000000 !important; 
            }
            .feedback-box {
                background-color: #FFFFE0; /* Amarelo claro fixo */
                border-left: 10px solid #D97706; 
                padding: 25px;
                margin-top: 30px;
                font-size: 26px;
                /* Fundo amarelo exige texto escuro */
                color: #000000 !important; 
                font-weight: 700;
            }
            
            /* Customizando os botões para respeitarem o tema */
            div.stButton > button {
                font-size: 26px !important;
                font-weight: 900 !important;
                padding: 25px 20px !important;
                height: auto !important;
                /* Borda, cor e fundo se adaptam ao modo do usuário */
                border: 4px solid var(--text-color) !important; 
                border-radius: 12px !important;
                color: var(--text-color) !important; 
                background-color: var(--secondary-background-color) !important; 
                white-space: normal !important; 
                box-shadow: 0px 4px 6px rgba(0,0,0,0.4); 
            }
            
            div.stButton > button:hover {
                background-color: var(--primary-color) !important;
                color: white !important;
                border-color: var(--primary-color) !important;
                transform: scale(1.02); 
            }
            
            /* Separador adaptável */
            hr {
                border-top: 3px solid var(--text-color);
                opacity: 0.2;
            }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE ESTADO (Backend)
# ==========================================
def inicializar_estado():
    """Gerencia a persistência de dados durante a navegação do usuário."""
    if 'etapa' not in st.session_state:
        st.session_state.etapa = 'boas_vindas' # Pode ser: boas_vindas, simulacao, feedback, conclusao
    if 'indice_msg' not in st.session_state:
        st.session_state.indice_msg = 0
    if 'resposta_correta' not in st.session_state:
        st.session_state.resposta_correta = None

def processar_resposta(escolha_usuario):
    """Valida a ação do usuário contra o banco de dados e muda o estado da tela."""
    msg_atual = MENSAGENS[st.session_state.indice_msg]
    # Se o usuário clicou que é golpe e realmente era (ou vice-versa), ele acertou
    acertou = (escolha_usuario == "Golpe") == msg_atual["e_golpe"]
    
    st.session_state.resposta_correta = acertou
    st.session_state.etapa = 'feedback'

def avancar_mensagem():
    """Prepara o sistema para a próxima mensagem ou finaliza o simulador."""
    if st.session_state.indice_msg < len(MENSAGENS) - 1:
        st.session_state.indice_msg += 1
        st.session_state.etapa = 'simulacao'
    else:
        st.session_state.etapa = 'conclusao'

# ==========================================
# 4. RENDERIZAÇÃO DAS TELAS (Controlador)
# ==========================================
def tela_boas_vindas():
    st.markdown('<p class="titulo">Bem-vindo ao Treino de Segurança no Celular! 🛡️</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto-grande">Vamos praticar juntos para você usar a internet com tranquilidade. Vamos ler algumas mensagens e você me diz o que acha delas, combinado?</p>', unsafe_allow_html=True)
    
    if st.button("Começar o Treino", use_container_width=True):
        st.session_state.etapa = 'simulacao'
        st.rerun()

def tela_simulacao():
    msg = MENSAGENS[st.session_state.indice_msg]
    st.markdown(f'<p class="texto-grande">Mensagem {st.session_state.indice_msg + 1} de {len(MENSAGENS)}:</p>', unsafe_allow_html=True)
    
    # Exibe a mensagem simulando um balão de chat
    st.markdown(f'<div class="chat-bubble">{msg["texto"]}</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="texto-grande">O que você acha desta mensagem?</p>', unsafe_allow_html=True)
    
    # Botões grandes e contrastantes
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Parece Seguro", use_container_width=True, type="secondary"):
            processar_resposta("Seguro")
            st.rerun()
    with col2:
        if st.button("🚨 É Golpe!", use_container_width=True, type="primary"):
            processar_resposta("Golpe")
            st.rerun()

def tela_feedback():
    msg = MENSAGENS[st.session_state.indice_msg]
    
    if st.session_state.resposta_correta:
        st.success("🎉 Muito bem! Você identificou corretamente.")
    else:
        st.warning("👀 Fique de olho! Vamos entender o que aconteceu aqui.")
        
    # Feedback claro, sem termos técnicos (focando nos gatilhos)
    st.markdown(f'<div class="feedback-box"><strong>Explicação:</strong> {msg["explicacao"]}</div>', unsafe_allow_html=True)
    
    st.write("---")
    if st.button("Ir para a próxima mensagem ➡️", use_container_width=True):
        avancar_mensagem()
        st.rerun()

def tela_conclusao():
    st.markdown('<p class="titulo">Parabéns! Você concluiu o treino! 🏆</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto-grande">Lembre-se: na dúvida, <strong>não clique em links, não mande dinheiro e pergunte a alguém de confiança.</strong> Você está no controle do seu celular!</p>', unsafe_allow_html=True)
    
    if st.button("Treinar Novamente", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 5. EXECUÇÃO PRINCIPAL (Roteador)
# ==========================================
def main():
    configurar_interface()
    inicializar_estado()
    
    # Máquina de estados simples para navegação
    if st.session_state.etapa == 'boas_vindas':
        tela_boas_vindas()
    elif st.session_state.etapa == 'simulacao':
        tela_simulacao()
    elif st.session_state.etapa == 'feedback':
        tela_feedback()
    elif st.session_state.etapa == 'conclusao':
        tela_conclusao()

if __name__ == "__main__":
    main()