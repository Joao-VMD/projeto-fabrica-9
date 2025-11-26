import streamlit as st
import pandas as pd

# ==========================
# Inicialização do estado
# ==========================
if "items" not in st.session_state:
    st.session_state.items = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# ==========================
# Funções CRUD
# ==========================
def add_item(nome, quantidade, categoria, prioridade, comprado):
    st.session_state.items.append({
        "id": st.session_state.next_id,
        "nome": nome,
        "quantidade": quantidade,
        "categoria": categoria,
        "prioridade": prioridade,
        "comprado": comprado
    })
    st.session_state.next_id += 1


def update_item(item_id, **kwargs):
    for item in st.session_state.items:
        if item["id"] == item_id:
            item.update({k: v for k, v in kwargs.items() if v is not None})
            return True
    return False


def delete_item(item_id):
    st.session_state.items = [i for i in st.session_state.items if i["id"] != item_id]


# ==========================
# Layout
# ==========================
st.title("🛒 Lista de Compras")

tabs = st.tabs(["➕ Adicionar", "📋 Lista de Itens"])
# ==========================


# ==========================
# Aba: Adicionar
# ==========================
with tabs[0]:
    st.header("Adicionar Item")

    with st.form("add_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            nome = st.text_input("Nome do item")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=1, step=1, value=1)

        categorias_default = ["Outros", "Alimentos", "Limpeza", "Higiene"]
        categoria = st.selectbox("Categoria", categorias_default)

        prioridade = st.radio("Prioridade", ["baixa", "media", "alta"], horizontal=True)
        comprado = st.checkbox("Já comprado?")

        submit_add = st.form_submit_button("Cadastrar")

        if submit_add:
            if nome.strip():
                add_item(nome, quantidade, categoria, prioridade, comprado)
                st.success(f"Item **{nome}** adicionado!")
                st.experimental_rerun()
            else:
                st.error("❌ O nome do item é obrigatório")


# ==========================
# Aba: Listagem e Ações
# ==========================
with tabs[1]:
    st.header("Itens cadastrados")

    if not st.session_state.items:
        st.info("Nenhum item cadastrado ainda.")
    else:
        # Ordenar itens por prioridade (alta → baixa)
        prioridade_ordem = {"alta": 1, "media": 2, "baixa": 3}
        lista_ordenada = sorted(st.session_state.items, key=lambda x: prioridade_ordem[x["prioridade"]])

        df = pd.DataFrame(lista_ordenada)
        df_display = df.copy()

        # Badge visual
        df_display["status"] = df_display["comprado"].apply(lambda x: "🟢 Sim" if x else "🔴 Não")
        st.dataframe(df_display[["id", "nome", "quantidade", "categoria", "prioridade", "status"]])

        st.markdown("### ✏️ Editar / Remover")

        selected_id = st.selectbox("Escolha o item:", df["id"])
        item = next(i for i in st.session_state.items if i["id"] == selected_id)

        with st.form("edit_form"):
            novo_nome = st.text_input("Nome", value=item["nome"])
            nova_qtd = st.number_input("Qtd", min_value=1, step=1, value=item["quantidade"])
            nova_categoria = st.selectbox("Categoria", ["Outros", "Alimentos", "Limpeza", "Higiene"], index=0)
            nova_prioridade = st.radio("Prioridade", ["baixa","media","alta"], horizontal=True, index=["baixa","media","alta"].index(item["prioridade"]))
            novo_comprado = st.checkbox("Comprado", value=item["comprado"])

            atualizar = st.form_submit_button("Salvar alterações")
            deletar = st.form_submit_button("🗑️ Deletar")

            if atualizar:
                update_item(selected_id,
                            nome=novo_nome,
                            quantidade=nova_qtd,
                            categoria=nova_categoria,
                            prioridade=nova_prioridade,
                            comprado=novo_comprado)
                st.success("Atualizado com sucesso!")
                st.experimental_rerun()

            if deletar:
                delete_item(selected_id)
                st.warning("Item removido!")
                st.experimental_rerun()
